
# Welvox Automated Tests

This directory contains automated tests for Welvox Studio AI.

## Current coverage

- Production-plan validation.
- Required field checks.
- Schema version checks.
- Output setting checks.
- Asset reference checks.
- Scene timing checks.
- Layer timing checks.
- Project inspection.
- Capability detection.
- JSON plan loading.

## Automated execution

GitHub Actions runs the test suite when changes are pushed to the main branch or a pull request targets main.

The workflow is located at:

`.github/workflows/core-tests.yml`

## Local execution

In a compatible Python environment, run:

```bash
python -m unittest discover -s tests -v
```

## Test philosophy

Tests should verify real behavior, not merely confirm that files or functions exist.

Every new engine should include tests for normal operation, invalid inputs, and failure handling.
