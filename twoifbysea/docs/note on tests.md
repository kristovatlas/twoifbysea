## Writing tests

If writing a test that interacts with the message queue, it usually should use
a temporary database for the duration of the test and not the user-configured
database. See other tests for examples that use the `testfile` module.
