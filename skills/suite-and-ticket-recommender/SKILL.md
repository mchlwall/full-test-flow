---
name: suite-and-ticket-recommender
description: >-
  Turns a product brief, its test plan and a regression analysis into an automation recommendation:
  which existing automated suites to run, which acceptance criteria no automated test covers, and a
  draft ticket for each gap, each with a ready-to-run `gh issue create` command (dry run unless the
  user confirms). Use when the user asks "what should we automate for this feature", "which suites
  should I run and what's missing", "suggest tickets for automated tests", or as the automation step
  of the full-test-flow skill.
---

# Suite and Ticket Recommender

Read the coverage that exists, compare it with what the brief promises, and propose tickets for the
difference. The model judges whether a test covers a criterion. Everything else (file lookups, suite
names, commands, issue creation) is mechanical.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Brief | yes | Markdown with numbered acceptance criteria |
| Plan | yes | Output of test-plan-generator, including its "Acceptance criteria coverage" table |
| Regression analysis | yes | Output of regression-analyzer for the branch that implements the brief |
| Target repository path | yes | Where the automated tests live; read only |
| Ticket repository | no | `owner/name` for the issues. Ask once if missing |

If the brief has no numbered acceptance criteria, or the regression analysis is a "not run" variant,
say so and stop. Don't guess criteria from prose.

## Outputs

One Markdown file shaped like [templates/automation.md](templates/automation.md): suites to run,
a coverage table, and draft tickets. Nothing is written to the target repository and no issue is
created unless the user confirms (see Procedure, step 9).

## Procedure

### A. Collect facts (deterministic)

1. Copy the suite rows from the regression analysis unchanged: suite, narrow-to, PR CI, run command.
   Don't add, rename or drop suites.
2. List the automated tests that already exist in the areas the analysis touched. Use the mapping
   file named under "Suite source" in the analysis to find the test locations, then list test names
   with a shell search (for example `rg -n "@Test|test\(" <test-dir>`). Record `file:line` and the
   test name.
3. Number the acceptance criteria from the brief as `AC-1`, `AC-2`, and so on, keeping the brief's
   wording. Read the plan's coverage table to get each criterion's plan rows.

### B. Judge (model)

4. For each criterion, decide its **automated coverage**:
   - **Covered**: an existing test, cited by `file:line`, would fail if this criterion's behaviour broke.
   - **Partial**: an existing test touches the area but doesn't check this behaviour. Say what is missing.
   - **None**: nothing in step 2's list exercises it.
   A test that merely runs near the feature is not coverage. Never mark Covered without a citation.
5. Assign each Partial or None criterion a **layer**, the cheapest layer that would catch it:
   - `api`: request/response rules (status codes, filtering, validation, error messages)
   - `unit`: pure logic with no HTTP or browser (rules, calculations)
   - `e2e`: behaviour that only exists in the browser (controls, visible state, flows across filters)
   Use only layers that exist in the target repo, which you saw in step 2. If a layer has no tests
   yet, say "new layer" in the ticket.
6. Group gaps into tickets. One ticket per layer and area, not per criterion, unless a criterion
   needs its own setup. Aim for 1 to 4 tickets. Each ticket cites the criteria and plan row numbers
   it closes.
7. Order tickets by risk: High (data loss, money, auth, shared code), then Medium (validation,
   filtering, rendered UI), then Low. Use the risks in the regression analysis; don't re-rate them.

### C. Check and emit (deterministic)

8. Before emitting, verify:
   - every suite name matches the regression analysis exactly;
   - every criterion in the brief appears once in the coverage table;
   - every Covered or Partial row cites `file:line`, and each cited line exists;
   - every ticket cites at least one criterion and one plan row;
   - each ticket's `gh issue create` command names the ticket repository.
   Fix any failure, then fill the template.
9. **Issue creation.** The output contains the commands as a dry run and stops. Create issues only
   if the user explicitly says to, after seeing the list. Run one `gh issue create` per ticket, report
   each URL, and don't create duplicates: check `gh issue list --search "<title>"` first and skip any
   ticket that already exists.

## Rules

1. Cite everything. Coverage claims cite `file:line`; tickets cite criteria and plan rows.
2. Copy suite names and run commands exactly from the regression analysis. Never invent a suite.
3. Describe what to test, not how to code it. No test code, page-object designs or framework advice.
4. Never add requirements. A ticket's acceptance comes from the brief's criteria.
5. Never claim a test passes or fails. This skill doesn't run anything.
6. Never create, edit or close issues without the user's explicit confirmation.
7. Don't propose tickets for behaviour the brief lists as out of scope.
8. Every ticket is `Draft`. Emit only the template's sections, with no preamble or sign-off.

## Limitations

- Coverage is judged by reading test names and bodies, so a test that looks relevant but doesn't
  assert the behaviour can be misjudged. The citations let a reviewer check.
- It reads the repo as it is on disk. Tests on other branches aren't seen.
- It doesn't estimate effort or priority beyond risk order.
- Ticket creation uses the GitHub CLI and needs `gh auth` for the ticket repository.
