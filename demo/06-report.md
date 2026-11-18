# Test plan (Sample results): Overdue tasks filter (new-feature): test report

- **Verdict:** Failures present
- **Context:** Sample results on branch mwall/product-brief (uncommitted)
- **Source:** 29 test rows (4 closure rows excluded)

## Headline

| Metric | Value |
|---|---|
| Pass rate (passed ÷ executed) | 96% |
| Executed (passed + failed) | 25 |
| Passed | 24 |
| Failed | 1 |
| Blocked | 1 |
| Out of scope (all N/A) | 0 |
| Not run | 3 |
| Expected result not confirmed in plan | 3 |

## By area

| Area | Cases | Passed | Failed | Blocked | Out of scope | Not run |
|---|---|---|---|---|---|---|
| Smoke checks | 3 | 3 | 0 | 0 | 0 | 0 |
| Core behaviour | 6 | 4 | 1 | 1 | 0 | 0 |
| Options and settings | 6 | 6 | 0 | 0 | 0 | 0 |
| Edge cases and resilience | 9 | 7 | 0 | 0 | 0 | 2 |
| Accessibility and quality | 2 | 1 | 0 | 0 | 0 | 1 |
| Contexts | 3 | 3 | 0 | 0 | 0 | 0 |

## By environment

| Environment | Pass | Fail | Blocked | N/A | Blank |
|---|---|---|---|---|---|
| api | 16 | 0 | 0 | 11 | 2 |
| browser | 15 | 1 | 1 | 11 | 1 |

## Failures

- #6 User unticks **Overdue only** (Core behaviour): SAMPLE-101: full list only returned after unticking twice

## Blocked

- #9 User marks an overdue task `DONE` while **Overdue only** is ticked (Core behaviour): Blocked by #6

## Out of scope

None.

## Unrecognised result values

None.

## One-line summary

24/25 executed cases passed across 6 areas; 1 failed, 1 blocked, 3 not run. Verdict: Failures present.
