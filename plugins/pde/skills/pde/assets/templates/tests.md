# [Product Name] — Behavioral Tests (Implementation [NN])

**Date:** YYYY-MM-DD
**Derived from:** `behavior.md`

---

## How to Use This File

Each test maps to a desired behavior from `behavior.md`. Tests are written in given/when/then format to describe expected outcomes without prescribing implementation. Start with manual verification, then automate as the product matures.

---

## Behavioral Tests

### Behavior 1: [Name from behavior.md]

**Test 1.1: [Scenario name]**

```
Given [initial state or precondition]
When [user action or trigger]
Then [expected outcome]
```

**Verification:** [How to manually check this works]

**Test 1.2: [Edge case or variant]**

```
Given [initial state]
When [action]
Then [expected outcome]
```

---

### Behavior 2: [Name from behavior.md]

**Test 2.1: [Scenario name]**

```
Given [initial state]
When [action]
Then [expected outcome]
```

**Verification:** [How to manually check]

**Test 2.2: [Scenario name]**

```
Given [initial state]
When [action]
Then [expected outcome]
```

---

### Behavior 3: [Name from behavior.md]

**Test 3.1: [Scenario name]**

```
Given [initial state]
When [action]
Then [expected outcome]
```

**Verification:** [How to manually check]

---

## Metrics to Instrument

These metrics should be tracked in production to validate behaviors are working as intended.

| Metric | Behavior | What to Measure | Target |
|--------|----------|----------------|--------|
| [Metric 1] | [Behavior #] | [Measurement] | [Threshold] |
| [Metric 2] | [Behavior #] | [Measurement] | [Threshold] |
| [Metric 3] | [Behavior #] | [Measurement] | [Threshold] |

## Acceptance Summary

| Behavior | Tests | Passing | Status |
|----------|-------|---------|--------|
| [Behavior 1] | [Count] | | |
| [Behavior 2] | [Count] | | |
| [Behavior 3] | [Count] | | |
| **Total** | **[Count]** | | |
