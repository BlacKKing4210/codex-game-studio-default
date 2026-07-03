# Workflow Test Spec: <workflow-id>

## Workflow Summary

**Route:**

**Inputs:**

**Outputs:**

**Gates:**

## Static Assertions

- [ ] Workflow has a clear owner route.
- [ ] Workflow has concrete outputs.
- [ ] Workflow includes verification.
- [ ] Workflow avoids overwriting user-edited files without approval.

## Test Cases

### Case 1: Happy Path

**Fixture:**

**Input:**

**Expected:**

**Assertions:**

- [ ] Required context is read.
- [ ] Output follows the workflow contract.
- [ ] Verification is performed or blocker is reported.

### Case 2: Missing Context

**Fixture:**

**Input:**

**Expected:**

**Assertions:**

- [ ] Missing information is identified.
- [ ] The workflow asks only necessary questions or makes a safe assumption.

### Case 3: Existing User Work

**Fixture:**

**Input:**

**Expected:**

**Assertions:**

- [ ] Existing work is preserved.
- [ ] Changes are scoped and additive unless explicitly requested.

## Coverage Notes

- Missing cases:
- Follow-up tests:
