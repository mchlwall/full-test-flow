# full-test-flow

Full E2E test flow from product brief to test report.

## The flow

```
01-brief.md ──plan──▶ 02-plan.md
                      03-regression-analysis.md
                      04-automation.md   (suites to run + draft tickets)

        run the suites, fill in the plan's result columns

05-plan-completed.md ──report──▶ 06-report.md
```

Two commands, from the `full-test-flow` skill:

- **plan**: a product brief becomes a manual test plan, a regression analysis of the branch that implements it, and an automation recommendation (existing suites to run, plus suggested tickets for gaps).
- **report**: the completed plan becomes a test report with a verdict, pass rate and lists of failures and blocked rows.

## Skills

| Skill | Role |
|---|---|
| [full-test-flow](skills/full-test-flow) | Orchestrates the steps below |
| [test-plan-generator](skills/test-plan-generator) | Brief to manual test plan |
| [regression-analyzer](skills/regression-analyzer) | Branch diff to risk-weighted cases and suites |
| [suite-and-ticket-recommender](skills/suite-and-ticket-recommender) | Suites to run, coverage gaps, draft tickets |
| [test-report-generator](skills/test-report-generator) | Completed plan to report |

## Demo

[`demo/`](demo) holds a worked example against [project-manager](https://github.com/mchlwall/project-manager): an "overdue tasks filter" brief and the output of each step.
