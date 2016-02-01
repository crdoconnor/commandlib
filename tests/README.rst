Tests
=====

To run these tests, check out this code and enter this directory and run the following command:

    $ curl -sSL https://hitchtest.com/init.sh > init.sh ; chmod +x init.sh ; ./init.sh

After set up and the first test run is complete, you can run the following to run a test in development mode:

    $ hitch test somefile.test --settings tdd.settings --tags tag1,tag2

Or you can run the full suite of tests from end to end as follows:

    $ hitch test . --settings ci.settings

For more information on hitch, see the documentation at https://hitchtest.readthedocs.org/