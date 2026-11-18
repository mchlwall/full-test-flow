# Automation recommendation (Draft): Overdue tasks filter

- **Brief:** `demo/01-brief.md`
- **Branch range:** `6a57359..05f35c5`
- **Ticket repository:** `mchlwall/full-test-flow`

## 1. Suites to run

| Suite | Why | Narrow to | Runs in PR CI | Run command |
|---|---|---|---|---|
| `app-unit` | `TaskService.java` and `TaskRepository.java` method signatures changed | Full suite | Yes (CI / Build and run tests) | `./mvnw test` |
| `e2e-tasks` | `index.html` filter bar and task loading changed; the suite covers the task list and status filter | Full suite | Yes (CI / Run E2E tests against the running app) | `cd e2e && npx playwright test tasks.spec.ts` |

## 2. Automated coverage of the brief

| Criterion | Coverage | Evidence | Gap | Layer |
|---|---|---|---|---|
| AC-1: `overdue=true` returns only tasks due before today that are not `DONE` | None | none found | No test requests the task list with `overdue` | api |
| AC-2: due today, future, no due date or `DONE` are never returned by `overdue=true` | None | none found | None of the boundary cases (today, `DONE`, no due date, future) is checked | api |
| AC-3: `overdue=false` or no parameter returns tasks as before | None | none found | No test lists tasks through the API | api |
| AC-4: any other `overdue` value returns `400` with the error message | None | none found | The error response is not checked | api |
| AC-5: `overdue` combines with `status` and `priority` | None | none found | No combined filter request or combined UI filter is checked | api, e2e |
| AC-6: **Overdue only** checkbox filters when ticked and restores when unticked | None | none found | The checkbox does not exist in any browser test | e2e |
| AC-7: existing status and priority filtering is unchanged | Partial | `e2e/tests/tasks.spec.ts:52` status filter shows only matching tasks | Priority filtering and the API's `status` and `priority` parameters have no test | api, e2e |

## 3. Suggested tickets

### T1: API tests for the task list `overdue` filter (Medium)

- **Layer:** api (existing layer, no task tests yet; needs a new suite name, which isn't in the current suite list)
- **Closes gaps in:** AC-1, AC-2, AC-3, AC-4, AC-5, AC-7 (plan rows #1, #4, #10, #11, #12, #13, #14, #15, #16, #17, #18, #19, #20, #23, #24)
- **Scope:** Add API tests that list a project's tasks with and without `overdue`, covering the overdue definition and its boundaries, combinations with `status` and `priority`, the error response and the unknown-project response.
- **Acceptance:**
  - `overdue=true` returns only tasks due before today that are not `DONE`.
  - Tasks due today, due in the future, with no due date, or `DONE` are not returned.
  - `overdue=false` and no `overdue` parameter return all tasks.
  - `overdue=maybe` returns `400` with `{"error": "overdue must be true or false"}`.
  - `overdue=true` combines with `status` and `priority`; `status` and `priority` alone behave as before.
  - `overdue=true` for an unknown project returns `404`.
- **Not in scope:** empty (`overdue=`) and upper-case (`overdue=TRUE`) values, until the owner confirms the expected result (plan rows #21, #22).

### T2: Browser tests for the **Overdue only** filter (Medium)

- **Layer:** e2e (existing layer)
- **Closes gaps in:** AC-5, AC-6, AC-7 (plan rows #2, #3, #5, #6, #7, #8, #9, #15)
- **Scope:** Add Playwright tests to the tasks suite for the new checkbox: filtering, restoring the full list, combining with the status filter, and the priority filter on its own.
- **Acceptance:**
  - Ticking **Overdue only** lists only overdue tasks; unticking restores the full list.
  - Ticked together with a status filter, only tasks matching both are listed.
  - Marking an overdue task `DONE` while the box is ticked removes it from the list.
  - The priority filter alone shows only matching tasks.
- **Not in scope:** whether the box stays ticked after switching projects or reloading, and rapid ticking and unticking (the brief doesn't say).

## 4. Ticket commands (dry run, nothing created)

```bash
gh label create test-automation --repo mchlwall/full-test-flow --color 0E8A16 \
  --description "Add or extend automated tests" 2>/dev/null || true

gh issue create --repo mchlwall/full-test-flow --label test-automation \
  --title "API tests for the task list overdue filter" \
  --body "Layer: api (no task tests yet; needs a new suite name)
Closes gaps in: AC-1, AC-2, AC-3, AC-4, AC-5, AC-7 (plan rows #1, #4, #10-#20, #23, #24)

Scope: List a project's tasks with and without overdue; cover the overdue definition and its boundaries, combinations with status and priority, the error response and the unknown-project response.

Acceptance:
- overdue=true returns only tasks due before today that are not DONE
- tasks due today, in the future, with no due date, or DONE are not returned
- overdue=false and no overdue parameter return all tasks
- overdue=maybe returns 400 with {\"error\": \"overdue must be true or false\"}
- overdue=true combines with status and priority; status and priority alone behave as before
- overdue=true for an unknown project returns 404

Not in scope: overdue= (empty) and overdue=TRUE until the owner confirms the expected result."

gh issue create --repo mchlwall/full-test-flow --label test-automation \
  --title "Browser tests for the Overdue only filter" \
  --body "Layer: e2e (tasks suite)
Closes gaps in: AC-5, AC-6, AC-7 (plan rows #2, #3, #5-#9, #15)

Scope: Playwright tests for the Overdue only checkbox: filtering, restoring the full list, combining with the status filter, and the priority filter on its own.

Acceptance:
- ticking Overdue only lists only overdue tasks; unticking restores the full list
- ticked with a status filter, only tasks matching both are listed
- marking an overdue task DONE while the box is ticked removes it from the list
- the priority filter alone shows only matching tasks

Not in scope: whether the box stays ticked after switching projects or reloading; rapid toggling."
```
