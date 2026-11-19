# Demo: overdue tasks filter

A worked run of the flow against [project-manager](https://github.com/mchlwall/project-manager), branch `mwall/product-brief` (`6a57359..05f35c5`).

| File | What it is | Produced by |
|---|---|---|
| [01-brief.md](01-brief.md) | Product brief: overdue tasks filter | Written by hand |
| [02-plan.md](02-plan.md) | Manual test plan, results blank | test-plan-generator |
| [03-regression-analysis.md](03-regression-analysis.md) | Manual cases and suites for the branch diff | regression-analyzer |
| [04-automation.md](04-automation.md) | Suites to run, coverage gaps, draft tickets | suite-and-ticket-recommender |
| [05-plan-completed.md](05-plan-completed.md) | The plan with **sample** results | Written for the demo |
| [06-report.md](06-report.md) | Test report from the completed plan | test-report-generator |
| [06-report.html](06-report.html) | The same report as a one-page HTML view (`--html`) | test-report-generator |

## About the sample results

`05-plan-completed.md` is illustrative. Its results were not all produced by running the tests, and
the failure in row #6 (and the row #9 it blocks) is invented so the report has something to show.

## What was actually run

The feature was checked for real, separately from the sample plan:

- **API:** a live app with six tasks covering each overdue boundary. `overdue=true`, `false`, no
  parameter, an invalid value, combinations with `status` and `priority`, and an unknown project
  all behaved as the brief says.
- **Browser:** the existing e2e suite (9 tests) passed against the feature build, and 7 temporary
  Playwright checks for the **Overdue only** checkbox passed (visible and labelled, filters and
  restores, combines with status and priority, marking a task `DONE` removes it, empty state,
  keyboard, narrow window). The temporary checks were deleted afterwards, so the branch has no
  tests for the new filter. That is the gap `04-automation.md` reports.

## Rows the brief leaves open

Plan rows #21 (`overdue=`), #22 (`overdue=TRUE`) and #26 (keyboard use) say "Not stated: confirm with
owner". The flow leaves them unrun instead of guessing.
