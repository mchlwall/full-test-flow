# Regression analysis (Draft)

- **Range:** `6a57359..05f35c5` (main to mwall/product-brief)
- **Files:** 4 changed: 4 analysed, 0 ignored
- **Areas:** Tasks (Medium), Web UI (Medium)
- **Highest risk:** Medium
- **Suite source:** `suite-mapping.md`

## 1. Manual test cases

| # | Test case | Expected behaviour | Risk | Source | Status |
|---|---|---|---|---|---|
| 1 | Request a project's tasks with `?overdue=true` when it has tasks due yesterday (`TODO`), yesterday (`DONE`), today, tomorrow and with no due date | Only the task due yesterday that is `TODO` is returned | Medium: the date and status comparison decides which tasks users see | `src/main/java/com/example/projectmanager/task/TaskRepository.java:74` | Draft |
| 2 | Request tasks with `?overdue=maybe` | `400` with `{"error": "overdue must be true or false"}` | Medium: new request validation | `src/main/java/com/example/projectmanager/task/TaskController.java:71` | Draft |
| 3 | Request tasks with `?overdue=false`, then with no `overdue` parameter | Both return every task in the project, as before the change | Medium: the existing list endpoint changed shape | `src/main/java/com/example/projectmanager/task/TaskController.java:65` | Draft |
| 4 | Request tasks with `?overdue=true&status=TODO`, then `?overdue=true&priority=HIGH` | Each returns only overdue tasks that also match the status or priority | Medium: new condition added to an existing filtered query | `src/main/java/com/example/projectmanager/task/TaskRepository.java:74` | Draft |
| 5 | Request tasks with only `?status=DONE`, then only `?priority=HIGH` | Results are filtered exactly as before the change | Medium: the repository and service method signatures changed | `src/main/java/com/example/projectmanager/task/TaskService.java:53` | Draft |
| 6 | Open a project in the browser and tick **Overdue only** with overdue and non-overdue tasks present | Only the overdue tasks are listed | Medium: new UI control that changes the request | `src/main/resources/static/index.html:195` | Draft |
| 7 | Untick **Overdue only** | The full task list returns | Medium: the list must restore after filtering | `src/main/resources/static/index.html:195` | Draft |
| 8 | Tick **Overdue only** and choose a status in the status filter | Only tasks that are overdue and match that status are listed | Medium: three controls now build one request | `src/main/resources/static/index.html:195` | Draft |
| 9 | Open a project and use the status and priority dropdowns without ticking the box | Both dropdowns filter the list as before | Medium: the filter bar markup and request building changed | `src/main/resources/static/index.html:44` | Draft |

## 2. Suite recommendations

| Suite | Why (tied to the diff) | Narrow to | Runs in PR CI | Run command |
|---|---|---|---|---|
| `app-unit` | `TaskService.java` and `TaskRepository.java` method signatures changed | Full suite | Yes (CI / Build and run tests) | `./mvnw test` |
| `e2e-tasks` | `index.html` filter bar and task loading changed; the suite covers the task list and status filter | Full suite | Yes (CI / Run E2E tests against the running app) | `cd e2e && npx playwright test tasks.spec.ts` |
