from hitchstory import StoryCollection, BaseEngine, no_stacktrace_for, validate, HitchStoryException
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from hitchrun import expected
from commandlib import Command
from strictyaml import Str, Map, MapPattern, Int, Bool, Optional, load
from pathquery import pathquery
from commandlib import python
from hitchrun import DIR
from hitchrun.decorators import ignore_ctrlc
from hitchrunpy import ExamplePythonCode, HitchRunPyException
from templex import Templex
import hitchpylibrarytoolkit
import dirtemplate


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

    def __init__(self, keypath, rewrite=False):
        self.path = keypath
        self._rewrite = rewrite
        self._cprofile = False

    def set_up(self):
        """Set up your applications and the test environment."""
        self.path.state = self.path.gen.joinpath("state")
        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()

        for script in self.given.get("scripts", []):
            script_path = self.path.state.joinpath(script)

            if not script_path.dirname().exists():
                script_path.dirname().makedirs()

            script_path.write_text(self.given['scripts'][script])
            script_path.chmod("u+x")

        for filename, contents in self.given.get("files", {}).items():
            self.path.state.joinpath(filename).write_text(contents)

        self.python = hitchpylibrarytoolkit.project_build(
            "commandlib",
            self.path,
            self.given["python version"],
        ).bin.python

        self.example_py_code = ExamplePythonCode(self.python, self.path.state)\
            .with_code(self.given.get('code', ''))\
            .with_setup_code(self.given.get('setup', ''))

    def _story_friendly_output(self, text):
        return text.replace(self.path.state, "/path/to")

    @no_stacktrace_for(AssertionError)
    @no_stacktrace_for(HitchRunPyException)
    @validate(
        code=Str(),
        will_output=Str(),
        raises=Map({
            Optional("type"): Map({"in python 2": Str(), "in python 3": Str()}) | Str(),
            Optional("message"): Map({"in python 2": Str(), "in python 3": Str()}) | Str(),
        })
    )
    def run(self, code, will_output=None, raises=None):
        to_run = self.example_py_code.with_code(code)

        if self._cprofile:
            to_run = to_run.with_cprofile(
                self.path.profile.joinpath("{0}.dat".format(self.story.slug))
            )

        result = to_run.expect_exceptions().run() if raises is not None else to_run.run()

        if will_output is not None:
            actual_output = '\n'.join([line.rstrip() for line in result.output.split("\n")])
            try:
                Templex(will_output).assert_match(actual_output)
            except AssertionError:
                if self._rewrite:
                    self.current_step.update(**{"will output": actual_output})
                else:
                    raise

        if raises is not None:
            differential = False  # Difference between python 2 and python 3 output?
            exception_type = raises.get('type')
            message = raises.get('message')

            if exception_type is not None:
                if not isinstance(exception_type, str):
                    differential = True
                    exception_type = exception_type['in python 2']\
                        if self.given['python version'].startswith("2")\
                        else exception_type['in python 3']

            if message is not None:
                if not isinstance(message, str):
                    differential = True
                    message = message['in python 2']\
                        if self.given['python version'].startswith("2")\
                        else message['in python 3']

            try:
                result = self.example_py_code.expect_exceptions().run()
                result.exception_was_raised(exception_type)
                exception_message = self._story_friendly_output(result.exception.message)
                Templex(exception_message).assert_match(message)
            except AssertionError:
                if self._rewrite and not differential:
                    new_raises = raises.copy()
                    new_raises['message'] = self._story_friendly_output(result.exception.message)
                    self.current_step.update(raises=new_raises)
                else:
                    raise

    def file_contents_will_be(self, filename, contents):
        file_contents = '\n'.join([
            line.rstrip() for line in
            self.path.state.joinpath(filename).bytes().decode('utf8').strip().split('\n')
        ])
        try:
            # Templex(file_contents).assert_match(contents.strip())
            assert file_contents == contents.strip(), \
                "{0} not {1}".format(file_contents, contents.strip())
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
                self.path.profile.joinpath("{0}.dat".format(self.story.slug))
            ).run()


def _storybook(**kwargs):
    return StoryCollection(pathquery(DIR.key).ext("story"), Engine(DIR, **kwargs))


def _personal_settings():
    settings_file = DIR.key.joinpath("personalsettings.yml")

    if not settings_file.exists():
        settings_file.write_text((
            "engine:\n"
            "  rewrite: no\n"
            "  cprofile: no\n"
            "params:\n"
            "  python version: 3.7.0n"
        ))
    return load(
        settings_file.bytes().decode('utf8'),
        Map({
            "engine": Map({
                "rewrite": Bool(),
                "cprofile": Bool(),
            }),
            "params": Map({
                "python version": Str(),
            }),
        })
    )


@expected(HitchStoryException)
def bdd(*keywords):
    """
    Run tests matching keywords.
    """
    settings = _personal_settings().data
    _storybook()\
        .with_params(**{"python version": settings['params']['python version']})\
        .only_uninherited()\
        .shortcut(*keywords).play()


@expected(HitchStoryException)
def rbdd(*keywords):
    """
    Run tests matching keywords and rewrite test if output changed.
    """
    settings = _personal_settings().data
    _storybook(rewrite=True)\
        .with_params(**{"python version": settings['params']['python version']})\
        .only_uninherited()\
        .shortcut(*keywords).play()


@expected(HitchStoryException)
def regressfile(filename):
    """
    Run all stories in filename 'filename' in python 2 and 3.

    Rewrite stories if appropriate.
    """
    _storybook().in_filename(filename)\
                .with_params(**{"python version": "2.7.14"})\
                .ordered_by_name().play()
    _storybook().with_params(**{"python version": "3.7.0"})\
                .in_filename(filename).ordered_by_name().play()


@expected(HitchStoryException)
def regression():
    """
    Run regression testing - lint and then run all tests.
    """
    storybook = _storybook().only_uninherited()
    storybook.with_params(**{"python version": "2.7.14"})\
             .filter(lambda story: not story.info.get('fails on python 2', False))\
             .ordered_by_name().play().report()
    storybook.with_params(**{"python version": "3.7.0"}).ordered_by_name().play().report()
    lint()


def lint():
    """
    Lint all code.
    """
    python("-m", "flake8")(
        DIR.project.joinpath("commandlib"),
        "--max-line-length=100",
        "--exclude=__init__.py",
    ).run()
    python("-m", "flake8")(
        DIR.key.joinpath("key.py"),
        "--max-line-length=100",
        "--exclude=__init__.py",
    ).run()
    print("Lint success!")


def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    hitchpylibrarytoolkit.deploy(DIR.project, "commandlib", version)


@expected(dirtemplate.exceptions.DirTemplateException)
def docgen():
    """
    Build documentation.
    """
    hitchpylibrarytoolkit.docgen(_storybook(), DIR.project, DIR.key, DIR.gen)


@expected(dirtemplate.exceptions.DirTemplateException)
def readmegen():
    """
    Build documentation.
    """
    hitchpylibrarytoolkit.readmegen(_storybook(), DIR.project, DIR.key, DIR.gen, "commandlib")


@ignore_ctrlc
def ipy():
    """
    Run IPython in environment."
    """
    Command(DIR.gen.joinpath("py3.5.0", "bin", "ipython")).run()


def hvenvup(package, directory):
    """
    Install a new version of a package in the hitch venv.
    """
    pip = Command(DIR.gen.joinpath("hvenv", "bin", "pip"))
    pip("uninstall", package, "-y").run()
    pip("install", DIR.project.joinpath(directory).abspath()).run()


def rerun(version="3.5.0"):
    """
    Rerun last example code block with specified version of python.
    """
    Command(DIR.gen.joinpath("py{0}".format(version), "bin", "python"))(
        DIR.gen.joinpath("state", "examplepythoncode.py")
    ).in_dir(DIR.gen.joinpath("state")).run()
