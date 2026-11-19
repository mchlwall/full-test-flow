# Automation template

Fill the `<placeholders>`. Keep the headings and column order exactly as written.

````markdown
# Automation recommendation (Draft): <feature>

- **Brief:** `<path>`
- **Branch range:** `<base-sha-short>..<head-sha-short>`
- **Ticket repository:** `<owner/name>`

## 1. Suites to run

| Suite | Why | Narrow to | Runs in PR CI | Run command |
|---|---|---|---|---|
| `<suite>` | <from the regression analysis> | <selector or "Full suite"> | <Yes (...) or No> | `<command>` |

## 2. Automated coverage of the brief

| Criterion | Coverage | Evidence | Gap | Layer |
|---|---|---|---|---|
| AC-1: <criterion> | <Covered / Partial / None> | `<file>:<line>` <test name>, or "none found" | <what no test checks; blank if Covered> | <api / unit / e2e / n/a> |

## 3. Suggested tickets

### T1: <ticket title> (<High / Medium / Low>)

- **Layer:** <api / unit / e2e> (<existing layer | new layer>)
- **Closes gaps in:** AC-<n>, AC-<n> (plan rows #<n>, #<n>)
- **Scope:** <what to automate, in one or two sentences>
- **Acceptance:** <bulleted, taken from the brief's criteria>
- **Not in scope:** <anything the brief excludes that a reader might assume>

## 4. Ticket commands (dry run, nothing created)

```bash
gh label create test-automation --repo <owner/name> --color 0E8A16 \
  --description "Add or extend automated tests" 2>/dev/null || true

gh issue create --repo <owner/name> --title "<title>" --label "test-automation" --body "<body>"
```
````

Rules for the template:

- If every criterion is Covered, section 3 reads "No tickets suggested: every criterion has automated coverage." and section 4 is left out.
- Section 4 has one command per ticket, in ticket order. Bodies are plain text built from the ticket's fields.
- A ticket's Layer says "new layer" when the target repo has no tests at that layer yet.

## Input stop variant

```markdown
# Automation recommendation (not generated)

- **Reason:** <brief has no numbered acceptance criteria | regression analysis was not run | ...>

<what to supply, then run again>
```
