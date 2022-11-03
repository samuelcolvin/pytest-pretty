# pytest-pretty

Opinionated pytest plugin to make output slightly prettier.

This plugin is inspired by [pytest-sugar](https://pypi.org/project/pytest-sugar/) which is no longer maintained.

pytest-pretty's only dependencies are [rich](https://pypi.org/project/rich/) and pytest itself.

### Realtime error summary

One-line info on which test has failed while tests are running:

![Realtime Error Summary](./screenshots/realtime-error-summary.png)

### Table of failures

A rich table of failures with both test line number and error line number:

![Table of Failures](./screenshots/table-of-failures.png)

This is extremely useful for navigating to failed tests without having to scroll through the entire test output.

### Prettier Summary of a Test Run

Including time taken for the test run:

![Test Run Summary](./screenshots/test-run-summary.png)
