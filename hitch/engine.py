from hitchstory import StoryCollection, BaseEngine, validate
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from strictyaml import Str, Map, Optional, Enum, MapPattern, Int, Bool
from hitchstory import no_stacktrace_for
from hitchrunpy import (
    ExamplePythonCode,
    HitchRunPyException,
    ExpectedExceptionMessageWasDifferent,
)
from commandlib import Command
from templex import Templex


class Engine(BaseEngine):
    """Python engine for running tests."""

    given_definition = GivenDefinition(
        scripts=GivenProperty(MapPattern(Str(), Str())),
        python_version=GivenProperty(Str()),
        pexpect_version=GivenProperty(Str()),
        icommandlib_version=GivenProperty(Str()),
        setup=GivenProperty(Str()),
        files=GivenProperty(MapPattern(Str(), Str())),
        code=GivenProperty(Str()),
    )

    info_definition = InfoDefinition(
        importance=InfoProperty(schema=Int()),
        docs=InfoProperty(schema=Str()),
        fails_on_python_2=InfoProperty(schema=Bool()),
    )

    def __init__(self, keypath, python_path=None, rewrite=False):
        self.path = keypath
        self._python_path = python_path
        self._rewrite = rewrite
        self._cprofile = False

    def set_up(self):
        """Set up your applications and the test environment."""
        self.path.state = self.path.gen.joinpath("state")
        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()
        
        self._included_files = []

        for script in self.given.get("scripts", []):
            script_path = self.path.state.joinpath(script)

            if not script_path.dirname().exists():
                script_path.dirname().makedirs()

            script_path.write_text(self.given["scripts"][script])
            script_path.chmod("u+x")
            self._included_files.append(script_path)

        for filename, contents in self.given.get("files", {}).items():
            self.path.state.joinpath(filename).write_text(contents)
            self._included_files.append(self.path.state.joinpath(filename))

        self.python = Command(self._python_path)

        self.example_py_code = (
            ExamplePythonCode(self.python, self.path.state)
            .with_code(self.given.get("code", ""))
            .with_setup_code(self.given.get("setup", ""))
            .in_dir(self.path.state)
        )

    def _story_friendly_output(self, text):
        return text.replace(self.path.state, "/path/to")

    @no_stacktrace_for(AssertionError)
    @no_stacktrace_for(HitchRunPyException)
    @validate(
        code=Str(),
        will_output=Str(),
        raises=Map(
            {
                Optional("type"): Map({"in python 2": Str(), "in python 3": Str()})
                | Str(),
                Optional("message"): Map({"in python 2": Str(), "in python 3": Str()})
                | Str(),
            }
        ),
    )
    def run(self, code, will_output=None, raises=None):
        to_run = self.example_py_code.with_code(code)

        if self._cprofile:
            to_run = to_run.with_cprofile(
                self.path.profile.joinpath("{0}.dat".format(self.story.slug))
            )

        result = (
            to_run.expect_exceptions().run() if raises is not None else to_run.run()
        )

        if will_output is not None:
            actual_output = "\n".join(
                [line.rstrip() for line in result.output.split("\n")]
            )
            try:
                Templex(will_output).assert_match(actual_output)
            except AssertionError:
                if self._rewrite:
                    self.current_step.update(**{"will output": actual_output})
                else:
                    raise

        if raises is not None:
            differential = False  # Difference between python 2 and python 3 output?
            exception_type = raises.get("type")
            message = raises.get("message")

            if exception_type is not None:
                if not isinstance(exception_type, str):
                    differential = True
                    exception_type = (
                        exception_type["in python 2"]
                        if self.given["python version"].startswith("2")
                        else exception_type["in python 3"]
                    )

            if message is not None:
                if not isinstance(message, str):
                    differential = True
                    message = (
                        message["in python 2"]
                        if self.given["python version"].startswith("2")
                        else message["in python 3"]
                    )

            try:
                result = to_run.expect_exceptions().run()
                result.exception_was_raised(exception_type)
                exception_message = self._story_friendly_output(
                    result.exception.message
                )
                Templex(exception_message).assert_match(message)
            except AssertionError:
                if self._rewrite and not differential:
                    new_raises = raises.copy()
                    new_raises["message"] = self._story_friendly_output(
                        result.exception.message
                    )
                    self.current_step.update(raises=new_raises)
                else:
                    raise

    def file_contents_will_be(self, filename, contents):
        file_contents = "\n".join(
            [
                line.rstrip()
                for line in self.path.state.joinpath(filename)
                .bytes()
                .decode("utf8")
                .strip()
                .split("\n")
            ]
        )
        try:
            # Templex(file_contents).assert_match(contents.strip())
            assert file_contents == contents.strip(), "{0} not {1}".format(
                file_contents, contents.strip()
            )
        except AssertionError:
            if self._rewrite:
                self.current_step.update(contents=file_contents)
            else:
                raise

    def pause(self, message="Pause"):
        import IPython

        IPython.embed()

    def on_success(self):
        if self._cprofile:
            self.python(
                self.path.key.joinpath("printstats.py"),
                self.path.profile.joinpath("{0}.dat".format(self.story.slug)),
            ).run()
