# pytest-pretty

[![CI](https://github.com/samuelcolvin/pytest-pretty/workflows/CI/badge.svg?event=push)](https://github.com/samuelcolvin/pytest-pretty/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![pypi](https://img.shields.io/pypi/v/pytest-pretty.svg)](https://pypi.python.org/pypi/pytest-pretty)
[![versions](https://img.shields.io/pypi/pyversions/pytest-pretty.svg)](https://github.com/samuelcolvin/pytest-pretty)
[![license](https://img.shields.io/github/license/samuelcolvin/pytest-pretty.svg)](https://github.com/samuelcolvin/pytest-pretty/blob/main/LICENSE)

Opinionated pytest plugin to make output slightly easier to read and errors easy to find and fix.

This plugin is inspired by [pytest-sugar](https://pypi.org/project/pytest-sugar/)

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
