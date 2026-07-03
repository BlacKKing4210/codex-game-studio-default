# Agent Test Spec: <agent-id>

## Agent Summary

**Domain owned:**

**Does not own:**

**Tier:**

**Primary routes:**

## Static Assertions

- [ ] Agent has a clear domain.
- [ ] Agent does not claim ownership outside its domain.
- [ ] Agent has explicit handoff partners.
- [ ] Agent output format is testable.

## Test Cases

### Case 1: In-Domain Request

**Scenario:**

**Expected:**

**Assertions:**

- [ ] Response stays in domain.
- [ ] Response names relevant files, docs, or data.
- [ ] Response includes verification or acceptance criteria.

### Case 2: Out-of-Domain Request

**Scenario:**

**Expected:**

**Assertions:**

- [ ] Agent redirects or consults the correct role.
- [ ] Agent does not make a binding decision outside its domain.

### Case 3: Gate Verdict

**Scenario:**

**Expected:**

**Assertions:**

- [ ] Verdict is one of APPROVE / CONCERNS / REJECT.
- [ ] Rationale cites concrete evidence.

## Coverage Notes

- Missing cases:
- Follow-up tests:
