# Test plan (Sample results): Overdue tasks filter (new-feature)

> **Sample data.** These results were written to illustrate the report step. They were not produced by running the tests, and the failure in #6 is invented.

- **Source:** `demo/01-brief.md` (Definition of overdue, User flows, States, Options, Edge cases, Layout, Acceptance criteria)
- **Environments:** API, Browser

## Smoke checks

| # | Test case | Expected | API | Browser | Notes | Source |
|---|---|---|---|---|---|---|
| 1 | User requests a project's tasks with `overdue=true` | The request succeeds and returns tasks, with no error | Pass | N/A |  | User flows: API call |
| 2 | User opens a project | An **Overdue only** checkbox is in the filter bar next to the status and priority filters, unticked | N/A | Pass |  | Layout; Options |
| 3 | User ticks **Overdue only** | The task list refreshes and no error message is shown | N/A | Pass |  | User flows: main flow step 2 |

## Core behaviour

| # | Test case | Expected | API | Browser | Notes | Source |
|---|---|---|---|---|---|---|
| 4 | User requests `overdue=true` for a project with overdue and non-overdue tasks | Only the overdue tasks are returned | Pass | N/A |  | Acceptance criteria AC-1 |
| 5 | User ticks **Overdue only** on a project with overdue and non-overdue tasks | Only the overdue tasks are listed | N/A | Pass |  | User flows: main flow step 3; AC-6 |
| 6 | User unticks **Overdue only** | The full task list returns | N/A | Fail | SAMPLE-101: full list only returned after unticking twice | User flows: main flow step 4; AC-6 |
| 7 | User ticks **Overdue only** and picks a status filter | Only tasks that are overdue and have that status are listed | N/A | Pass |  | User flows: alternative 1; AC-5 |
| 8 | User ticks **Overdue only** and picks a priority filter | Only tasks that are overdue and have that priority are listed | N/A | Pass |  | User flows: alternative 1; AC-5 |
| 9 | User marks an overdue task `DONE` while **Overdue only** is ticked | The task leaves the list | N/A | Blocked | Blocked by #6 | User flows: alternative 2 |

## Options and settings

| # | Test case | Expected | API | Browser | Notes | Source |
|---|---|---|---|---|---|---|
| 10 | User requests `overdue=true&status=TODO` | Only overdue tasks with status `TODO` are returned | Pass | N/A |  | Edge cases; AC-5 |
| 11 | User requests `overdue=true&priority=HIGH` | Only overdue tasks with priority `HIGH` are returned | Pass | N/A |  | Edge cases; AC-5 |
| 12 | User requests `overdue=false` | All tasks are returned, including overdue ones (it does not mean "not overdue") | Pass | N/A |  | Options; AC-3 |
| 13 | User requests tasks with no `overdue` parameter | All tasks are returned, as before the feature | Pass | N/A |  | Options; AC-3 |
| 14 | User applies only a status filter | Tasks are filtered by status exactly as before | Pass | Pass |  | AC-7 |
| 15 | User applies only a priority filter | Tasks are filtered by priority exactly as before | Pass | Pass |  | AC-7 |

## Edge cases and resilience

| # | Test case | Expected | API | Browser | Notes | Source |
|---|---|---|---|---|---|---|
| 16 | User filters to overdue tasks when a task is due today | The task is not listed | Pass | Pass |  | Edge cases; AC-2 |
| 17 | User filters to overdue tasks when a task is past due and `DONE` | The task is not listed | Pass | Pass |  | Edge cases; AC-2 |
| 18 | User filters to overdue tasks when a task has no due date | The task is not listed | Pass | Pass |  | Edge cases; AC-2 |
| 19 | User filters to overdue tasks when a task is due in the future | The task is not listed | Pass | Pass |  | Definition of overdue; AC-2 |
| 20 | User requests `overdue=maybe` | `400` with `{"error": "overdue must be true or false"}` | Pass | N/A |  | States: Error; AC-4 |
| 21 | User requests `overdue=` (empty value) | Not stated: confirm with owner |  | N/A | Assumption; awaiting owner | AC-4 ("any other value") |
| 22 | User requests `overdue=TRUE` (upper case) | Not stated: confirm with owner |  | N/A | Assumption; awaiting owner | AC-4 ("any other value") |
| 23 | User requests `overdue=true` for an unknown project | `404`, as for the other filters | Pass | N/A |  | Edge cases |
| 24 | User filters to overdue tasks in a project with none overdue | The list is empty and no error is shown | Pass | Pass |  | States: Empty |

## Accessibility and quality

| # | Test case | Expected | API | Browser | Notes | Source |
|---|---|---|---|---|---|---|
| 25 | User looks at the new checkbox | It is labelled "Overdue only" | N/A | Pass |  | Options |
| 26 | User tabs to the checkbox and toggles it with the keyboard | Not stated: confirm with owner | N/A |  | Assumption; awaiting owner | Not stated in the brief |

## Contexts

| # | Test case | Expected | API | Browser | Notes | Source |
|---|---|---|---|---|---|---|
| 27 | User calls the API with an HTTP client |  | Pass | N/A |  | User flows: API call |
| 28 | User uses the web page in a desktop browser |  | N/A | Pass |  | User flows: main flow |
| 29 | User uses the web page in a narrow window |  | N/A | Pass |  | Layout |

## Closure

| # | Test case | Expected | API | Browser | Notes | Source |
|---|---|---|---|---|---|---|
| 30 | Time-boxed exploratory session | | | | | |
| 31 | Element and layout check | | | | | |
| 32 | Accessibility check | | | | | |
| 33 | Localisation check | | | | | |

## Acceptance criteria coverage

| Criterion | Rows | Note |
|---|---|---|
| AC-1: `overdue=true` returns only tasks due before today that are not `DONE` | #1, #4 | |
| AC-2: due today, future, no due date or `DONE` are never returned by `overdue=true` | #16, #17, #18, #19 | |
| AC-3: `overdue=false` or no parameter returns tasks as before | #12, #13 | |
| AC-4: any other `overdue` value returns `400` with the error message | #20, #21, #22 | #21 and #22 expected results are not stated |
| AC-5: `overdue` combines with `status` and `priority` | #7, #8, #10, #11 | |
| AC-6: **Overdue only** checkbox filters when ticked and restores when unticked | #3, #5, #6 | |
| AC-7: existing status and priority filtering is unchanged | #14, #15 | |

## Exploratory testing

- **Filter state across navigation:** tick **Overdue only**, then open a different project or reload the page. The brief doesn't say whether the box stays ticked or resets.
- **Midnight boundary:** "today" is the server's date. Check a task due on the day the server's date changes, and whether the date shown on the page can differ from the server's. The brief doesn't say how this should look to a user.
- **Rapid toggling:** tick and untick the box quickly several times. The brief doesn't say what the list should show while requests overlap.
- **Past due dates entered in the page:** add a task with a past due date through the form while the box is ticked. The brief doesn't say whether the new task should appear straight away.
