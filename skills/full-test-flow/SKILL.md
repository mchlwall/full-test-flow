---
name: full-test-flow
description: >-
  Runs a QA flow from a product brief to a test report in two commands. `plan` turns a brief into
  a manual test plan, a regression analysis of the implementing branch, and an automation
  recommendation with draft tickets. `report` turns the completed plan into a test report. Use when
  the user gives a product brief and asks for the full QA flow, "plan the testing for this brief",
  "what should we test and automate for this feature", or returns a completed test plan and asks
  for the report.
---

# Full Test Flow

This skill only sequences other skills and holds the gates between them. It judges nothing itself.
Each step's output is saved as written by its skill, and each skill's rules still apply.

| Step | Skill | Output file |
|---|---|---|
| 1 | test-plan-generator | `02-plan.md` |
| 2 | regression-analyzer | `03-regression-analysis.md` |
| 3 | suite-and-ticket-recommender | `04-automation.md` |
| (you) | run the suites, fill in the result columns | e.g. `05-plan-completed.md` |
| 4 | test-report-generator | `06-report.md` |

Files are written next to the brief (`01-brief.md` in the demo). Existing files with those names
are not overwritten without asking.

## Command: plan

### Inputs

| Input | Required | Default |
|---|---|---|
| Brief | yes | a Markdown file |
| Target repository | yes | none: ask |
| Head ref | no | the working tree, when it has uncommitted changes; otherwise `HEAD` |
| Base ref | no | `git merge-base origin/main HEAD`, else `main` |
| Ticket repository | no | none: ask once, as `owner/name` |

If any required input is missing, ask for all of them in one message before starting.

### Procedure

1. **Check the brief.** It must have a title and numbered acceptance criteria. If not, say what is
   missing and stop.
2. **Plan.** Run test-plan-generator in `new-feature` mode: feature name from the brief's title,
   the brief as the source, environments from the surfaces the brief names (for example `API,
   Browser`). Write `02-plan.md`. If the generator returns "Input incomplete", show it and stop.
3. **Regression analysis.** Run regression-analyzer on the target repository for the base and
   head refs. Write `03-regression-analysis.md`. If it returns the "not run" variant, show it and
   stop; the recommender can't run without a usable analysis.
4. **Automation.** Run suite-and-ticket-recommender with the brief, `02-plan.md`,
   `03-regression-analysis.md`, the target repository and the ticket repository. Write
   `04-automation.md`.
5. **Hand over.** Reply with: the three file paths; the plan's row count and any rows marked
   "Not stated: confirm with owner"; the suites to run with their commands; and the suggested
   ticket titles. Don't repeat the tables.
6. **Tickets.** Ask whether to create the suggested issues. Create them only after an explicit yes,
   following the recommender's step 9. Otherwise leave the dry-run commands in `04-automation.md`.
7. Tell the user the next move: run the suites, record results in the plan's result columns
   (`Pass`, `Fail`, `Blocked`, `N/A`), save it, and run `report`.

## Command: report

### Inputs

| Input | Required | Notes |
|---|---|---|
| Completed plan | yes | The Markdown plan with result columns filled in |
| Context | no | One line: build, environment or dates tested |

### Procedure

1. Run test-report-generator on the completed plan. Write `06-report.md` next to it.
2. Follow that skill's procedure for an unparseable plan or an unexecuted one (ask before sharing
   a report where nothing was run).
3. Reply with the verdict, the one-line summary and each non-empty failures, blocked or
   unrecognised list by row number.
4. Add one line saying the report reflects the manual plan only. Automated suite results count
   only where the tester copied them into the plan's Notes.

## Rules

1. Never fill in, edit or "tidy" a plan's result cells. Only the tester records results.
2. Never run the target repository's tests or start its app. This flow plans and reports; it
   doesn't execute.
3. Never create, edit or close issues without the user's explicit confirmation.
4. Stop at the first gate that fails and show the failing skill's own message. Don't continue with
   partial inputs.
5. Don't reword or summarise a skill's output inside its file. The chat reply may summarise.
6. Don't invent steps, skills or file names beyond those in the table above.

## Limitations

- The report reads Markdown results only. It doesn't read JUnit, Playwright or Allure output.
- One feature, one brief and one branch per run.
- Regression analysis is limited by regression-analyzer: more than 30 changed files, more than
  3 unrelated areas or more than 6 suites stops the flow at step 3.
- Briefs must be Markdown files for now. Pasted text can be saved to a file first.
