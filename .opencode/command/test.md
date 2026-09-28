---
description: Run the backend tests and report failures with the failing assertion and a one-line cause
agent: build
---
Run `make test`. If everything passes, reply with the summary line only.
If tests fail, list each failure as `test name — failing assertion — most likely cause` and fix the code
(not the tests) unless the test is demonstrably wrong; explain when it is.
Extra focus: $ARGUMENTS
