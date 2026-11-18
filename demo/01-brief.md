# Product brief: Overdue tasks filter

## Problem

A project can hold many tasks, and people lose track of the ones that have slipped past their due date. Today the only way to find them is to scan the Due column by eye.

## Goal

Let a user show only the overdue tasks in a project, in the web page and through the API.

## Definition of overdue

A task is **overdue** when both are true:

- it has a due date that is **before today** (a task due today is not overdue), and
- its status is **not `DONE`**.

A task with no due date is never overdue.

## User flows

**Main flow (web page)**
1. The user opens a project
2. The user ticks **Overdue only** in the filter bar
3. The task list shows only the overdue tasks
4. The user unticks the box and the full list returns

**Alternative flows**
- The user combines **Overdue only** with the existing status or priority filters; only tasks
  matching all of them are shown
- The user marks an overdue task `DONE` while the box is ticked; the task leaves the list
- The user calls the API directly: `GET /api/projects/{id}/tasks?overdue=true`

## States

| State | Behaviour |
|---|---|
| Populated | Only overdue tasks are listed |
| Empty | No overdue tasks: the list is empty and the page shows no error |
| Error | An invalid `overdue` value in the API returns `400` with `{"error": "overdue must be true or false"}` |

## Options

| Option | Values | Default |
|---|---|---|
| `overdue` (API query parameter) | `true`, `false` | not set (no overdue filtering) |
| **Overdue only** checkbox (web page) | ticked, unticked | unticked |

`overdue=false` behaves the same as leaving the parameter out. It does not mean "not overdue".

## Edge cases

- Task due yesterday and `TODO`: overdue.
- Task due today: not overdue.
- Task due in the past and `DONE`: not overdue.
- Task with no due date: not overdue.
- `overdue` combined with `status` or `priority`: all conditions apply.
- `overdue` given for an unknown project: `404`, as for the other filters.

## Layout

The checkbox sits in the existing filter bar next to the status and priority filters. It works at
any window width the filter bar already supports; no new layout is needed.

## Acceptance criteria

1. `GET /api/projects/{id}/tasks?overdue=true` returns only tasks with a due date before today that are not `DONE`.
2. Tasks due today, due in the future, without a due date, or `DONE` are never returned by `overdue=true`.
3. `overdue=false` or no `overdue` parameter returns tasks exactly as before.
4. Any other `overdue` value returns `400` with the error message above.
5. `overdue` can be combined with `status` and `priority`; all conditions must match.
6. The web page has an **Overdue only** checkbox that shows only overdue tasks when ticked and restores the full list when unticked.
7. Existing status and priority filtering behaves exactly as before.

## Out of scope

- Highlighting overdue tasks in the list.
- Sorting by due date.
- Notifications or reminders.
- Time zones: "today" is the server's date.
