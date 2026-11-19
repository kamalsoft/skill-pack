# Skill grades

Every skill in the package, graded from A+ to D on how well it serves a project. The top criterion is how strongly the skill supports the project and the request; usage, presence, importance and severity complete the grade. This page states the scope, the criteria and their weights, what each grade means, and the reasoning for every skill, so each grade can be checked and challenged.

Graded on 2026-11-19 against the skills as committed in `2407d3e`. Re-grade at every grooming review (MAINTAINERS.md in the source repository).

## Scope

- **What is graded:** the 33 skills in `skills/registry.json`. The grade decides the tier (see "Tier rule" below); the tier never affects the grade.
- **Reference project:** a team that builds and runs a commercial web application or service, with a front end, APIs, a database, third-party dependencies and a CI pipeline. Usage and presence are judged for this project. A team with a different product (for example a browser extension, or a decentralized identity system) should raise the presence and usage of the skills that match it; the reasoning column says where this applies.
- **Evidence:** a design review of each `SKILL.md`: its method, verification steps, evidence rules, output format, not-checked list and helpers. No skill has yet been run against a model with measured results (backlog B-1, B-9, B-23 to B-25, B-29, B-34). These are therefore **design grades**. When a skill is validated, its support-strength score is replaced by the measured result and the skill is re-graded.
- **Not graded:** the quality of a particular model's output, and the commercial value of a tier.

## Criteria and weights

Each skill gets a score from 1 to 5 on five criteria. The weighted sum gives a score out of 5.

| Criterion | Weight | Question | 5 means | 3 means | 1 means |
| --- | --- | --- | --- | --- | --- |
| **Support strength** (S) | 35% | How strongly does the skill drive the agent to a correct, complete and checkable result? | Scoped inventory, explicit checks, verification against the source, cited evidence, a verdict or structured output, a not-checked list, guardrails, and a helper or tool for scale | A sound method with one or two of these missing | General advice with no method |
| **Importance** (I) | 20% | How much does the outcome matter to the project's success? | A quality gate for releases, security or revenue | Useful for quality or speed | Nice to have |
| **Severity** (V) | 20% | How bad is what the skill catches or prevents? | Breach, data loss, outage or legal exposure | Degraded experience, performance or maintainability | Cosmetic |
| **Usage** (U) | 15% | How often does the reference project need it? | Every change or every day | Each month or project phase | Rarely, or once |
| **Presence** (P) | 10% | How many projects contain what the skill reviews? | Virtually all | Many | Few |

**Why these weights.** Support strength carries the most weight because a skill that is important but weakly specified gives unreliable output, and unreliable output costs more than no output. Importance and severity together carry 40%, because the purpose of the package is to prevent costly failures. Usage and presence carry 25%: they decide how often the value is realised, but a rarely used skill that prevents a breach is still worth having, so they must not dominate.

Score = 0.35 S + 0.20 I + 0.20 V + 0.15 U + 0.10 P

## Grade bands and what each means

| Grade | Score | Meaning | Action |
| --- | --- | --- | --- |
| **A+** | 4.60 to 5.00 | Essential. Strongly specified and needed by almost every project. | Default on where the tier allows. Validate first. |
| **A** | 4.30 to 4.59 | Core. High value with a strong method. | Recommend in the install picker. |
| **A-** | 4.00 to 4.29 | Strong. High value; one criterion holds it back. | Recommend; fix the named limit. |
| **B+** | 3.70 to 3.99 | Valuable for many projects, or vital for some. | Offer; keep improving the method. |
| **B** | 3.40 to 3.69 | Solid, in a narrower or lower-severity area. | Offer for matching projects. |
| **B-** | 3.10 to 3.39 | Useful, with a clear weakness. | Improve before promoting. |
| **C+** | 2.80 to 3.09 | Situational or lightly specified. | Keep off by default; strengthen the method. |
| **C** | 2.50 to 2.79 | Narrow benefit or early technology. | Keep off by default; re-grade when the area matures. |
| **D** | below 2.50 | Little value to the reference project. | Merge or remove at the next grooming review. |

Distribution: A+ 3, A 5, A- 3, B+ 7, B 8, B- 0, C+ 5, C 2, D 0.

## Tier rule

The grade decides the subscription tier. The best-supported, highest-value skills are premium. Essentials is the entry tier: it installs without a key.

| Grades | Tier | Skills now |
| --- | --- | --- |
| A+, A, A- | **premium** | 11 |
| B+, B, B- | **pro** | 15 |
| C+, C, D | **essentials** | 7 |

The rule is enforced: `skills/registry.json` holds each skill's grade and tier, `scripts/new-skill.mjs` derives the tier from `--grade`, and `npm test` fails if a tier does not follow its grade, or if the grade or tier in this page, docs/SKILLS.md or the consumer guide differs from the registry. A re-grade that crosses a band boundary changes the skill's tier: update the registry, the `<!-- tier: -->` line in its `SKILL.md`, and every document, then run `npm test`.

## Grades

| Rank | Skill | Category | Tier | S | I | V | U | P | Score | Grade |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `code-review` | Engineering review | premium | 5 | 5 | 5 | 5 | 5 | 5.00 | **A+** |
| 2 | `rlm-security-audit` | Analysis (chunked) | premium | 5 | 5 | 5 | 3 | 5 | 4.70 | **A+** |
| 3 | `web-client-security` | Web platform | premium | 5 | 5 | 5 | 3 | 4 | 4.60 | **A+** |
| 4 | `rlm-llm-app-review` | Security and risk | premium | 5 | 5 | 5 | 3 | 3 | 4.50 | **A** |
| 5 | `rlm-test-gap-analysis` | Analysis (chunked) | premium | 5 | 4 | 4 | 4 | 5 | 4.45 | **A** |
| 6 | `rlm-accessibility-audit` | Web platform | premium | 5 | 4 | 5 | 3 | 4 | 4.40 | **A** |
| 7 | `web-forms-autofill` | Web platform | premium | 5 | 4 | 4 | 4 | 4 | 4.35 | **A** |
| 8 | `dependency-audit` | Engineering review | premium | 4 | 4 | 5 | 4 | 5 | 4.30 | **A** |
| 9 | `db-migration-safety` | Engineering review | premium | 4 | 5 | 5 | 3 | 4 | 4.25 | **A-** |
| 10 | `threat-model` | Security and risk | premium | 4 | 5 | 5 | 3 | 4 | 4.25 | **A-** |
| 11 | `rlm-refactor-planner` | Analysis (chunked) | premium | 5 | 4 | 3 | 3 | 5 | 4.10 | **A-** |
| 12 | `browser-extension-review` | Web platform | pro | 5 | 4 | 5 | 2 | 1 | 3.95 | **B+** |
| 13 | `rlm-performance-review` | Analysis (chunked) | pro | 4 | 4 | 4 | 3 | 5 | 3.95 | **B+** |
| 14 | `cicd-pipeline-review` | Domain review | pro | 4 | 4 | 5 | 2 | 4 | 3.90 | **B+** |
| 15 | `rlm-privacy-review` | Analysis (chunked) | pro | 4 | 4 | 5 | 2 | 4 | 3.90 | **B+** |
| 16 | `api-contract-review` | Engineering review | pro | 4 | 4 | 4 | 3 | 3 | 3.75 | **B+** |
| 17 | `rlm-log-triage` | Analysis (chunked) | pro | 4 | 4 | 4 | 2 | 4 | 3.70 | **B+** |
| 18 | `rlm-migration-planner` | Analysis (chunked) | pro | 4 | 4 | 4 | 2 | 4 | 3.70 | **B+** |
| 19 | `stack-auditor` | Domain review | pro | 4 | 3 | 4 | 3 | 4 | 3.65 | **B** |
| 20 | `web-performance` | Web platform | pro | 4 | 4 | 3 | 3 | 4 | 3.65 | **B** |
| 21 | `web-css-layout` | Web platform | pro | 4 | 3 | 3 | 4 | 4 | 3.60 | **B** |
| 22 | `web-ui-components` | Web platform | pro | 4 | 3 | 3 | 4 | 4 | 3.60 | **B** |
| 23 | `license-attribution` | Compliance | pro | 4 | 3 | 4 | 2 | 4 | 3.50 | **B** |
| 24 | `memory-manager` | Memory | pro | 4 | 3 | 2 | 4 | 5 | 3.50 | **B** |
| 25 | `trust-layer-validator` | Domain review | pro | 4 | 4 | 5 | 1 | 1 | 3.45 | **B** |
| 26 | `web-app-platform` | Web platform | pro | 4 | 3 | 4 | 2 | 3 | 3.40 | **B** |
| 27 | `rlm-doc-generator` | Analysis (chunked) | essentials | 3 | 3 | 2 | 3 | 5 | 3.00 | **C+** |
| 28 | `audit-evidence-collector` | Compliance | essentials | 4 | 3 | 3 | 1 | 2 | 2.95 | **C+** |
| 29 | `token-saver` | Efficiency | essentials | 3 | 2 | 1 | 5 | 5 | 2.90 | **C+** |
| 30 | `incident-postmortem` | Operations | essentials | 3 | 3 | 3 | 2 | 3 | 2.85 | **C+** |
| 31 | `compliance-control-check` | Compliance | essentials | 3 | 3 | 4 | 1 | 2 | 2.80 | **C+** |
| 32 | `release-notes` | Engineering review | essentials | 3 | 2 | 2 | 3 | 4 | 2.70 | **C** |
| 33 | `web-built-in-ai` | Web platform | essentials | 4 | 2 | 3 | 1 | 1 | 2.65 | **C** |

## Reasoning per skill

Each entry gives the reason for the scores and what would raise the grade.

### A+

**`code-review`** (5.00). Applies to every change in every project, and catches correctness, security and data-safety defects before merge. The method reads callers as well as the diff, demands the triggering input for each finding, and ends with a verdict and the tests to run.

*To raise the grade:* Already at the top. Keep it there by validating it against a model (B-1).

**`rlm-security-audit`** (4.70). Vulnerabilities and leaked secrets are the most severe class of defect. The chunk helper covers a whole repository, every high-severity item is confirmed reachable, secrets are redacted, and dismissed findings are listed. A full audit runs per release, not per change, which is the only point lost.

*To raise the grade:* Run it in CI on changed folders to raise usage; validate recall on planted issues (B-1).

**`web-client-security`** (4.60). Sign-in, injected HTML and third-party scripts are where web apps are breached. The skill checks passkeys end to end, a strict CSP rolled out through report-only, Trusted Types and sanitizing, cross-origin messaging and browser cryptography, and traces each injection from source to sink.

*To raise the grade:* Validate on a sample app with planted issues (B-34).

### A

**`rlm-llm-app-review`** (4.50). Prompt injection and unsafe use of model output are severe and growing as more applications call models. The skill limits scope to the model surface, maps each finding to the OWASP Top 10 for LLM Applications, and traces input to sink before reporting. Presence is still limited to projects that call models.

*To raise the grade:* Presence rises as more projects add model features; validate on a planted app (B-23).

**`rlm-test-gap-analysis`** (4.45). Every project has untested risk. The skill uses real coverage data first, confirms each gap by searching the tests, and gives the test to add, so the output is directly actionable.

*To raise the grade:* Validate the ranking against a coverage report on a real project (B-1).

**`rlm-accessibility-audit`** (4.40). Accessibility failures exclude users and carry legal exposure in many markets. The chunked method covers a whole front end, ties every finding to a WCAG 2.2 success criterion, and merges findings from shared components. A code review cannot replace assistive-technology testing, which the skill states.

*To raise the grade:* Validate on a sample UI with planted failures (B-29).

**`web-forms-autofill`** (4.35). Forms are where users sign in, sign up and pay, so failures cost revenue directly. The skill carries a complete autocomplete-token table and specific checks for errors, one-time codes and input methods, and gives corrected markup.

*To raise the grade:* Validate on a sample checkout and sign-in flow (B-34).

**`dependency-audit`** (4.30). Nearly every project has third-party packages, and a known-vulnerable dependency is a common breach path. The skill runs the installed audit tools, confirms each finding in the lock file, and plans upgrades by risk. It cites advisory IDs but has no file-level evidence rule for where a vulnerable package is used.

*To raise the grade:* Require the call site of each vulnerable package before rating it high; run end to end (B-12).

### A-

**`db-migration-safety`** (4.25). A migration that locks a large table or drops data a running release still reads causes outages and data loss. The skill checks each statement for locks, rewrites, data loss, deploy order and reversibility, and gives the safe migration sequence. The engine-specific lock rules still need a practitioner check.

*To raise the grade:* Have a PostgreSQL and MySQL practitioner confirm the rules (B-25).

**`threat-model`** (4.25). Finding a design flaw before code is written is the cheapest fix there is. STRIDE per element, every control backed by a code reference, and a verification pass make it rigorous. Quality depends on the architecture documents available, which caps support strength.

*To raise the grade:* Add a worked example data-flow diagram; validate on a sample system (B-9).

**`rlm-refactor-planner`** (4.10). The import-graph helper gives evidence that no prompt-only approach has: real cycles and the most-imported modules. Findings are verified before a change is recommended. Refactoring is planned work, not a daily need, and its defects are maintainability rather than outage risks.

*To raise the grade:* Add language coverage to the graph (B-6).

### B+

**`browser-extension-review`** (3.95). For projects that ship an extension, the risks are severe: a web page driving the extension, over-broad permissions, store rejection. The method covers the worker lifecycle, sender checks, permissions and store readiness, with a verdict. Few projects ship an extension, so presence and usage are low.

*To raise the grade:* Grade rises for teams whose product is an extension; validate on a sample extension (B-34).

**`rlm-performance-review`** (3.95). Queries in loops and unbounded reads cause most slow-downs as data grows. The skill ranks findings by how hot the path is and puts a real profile ahead of inference. Without a profile the ranking is an estimate, which caps support strength.

*To raise the grade:* Validate the hot-path ranking on a planted repository (B-24).

**`cicd-pipeline-review`** (3.90). A pipeline holds deployment credentials, so a leaked secret or an over-permitted token is a supply-chain risk. The checks are specific, and findings cite lines. Pipelines change less often than code.

*To raise the grade:* Settle the overlap with stack-auditor (B-10).

**`rlm-privacy-review`** (3.90). Mishandled personal data has legal and trust consequences. The skill maps collection, storage, logging, sharing and retention without reproducing personal values. It finds personal data by field name, so unusual names are missed.

*To raise the grade:* Accept an organisation-specific list of personal field names (B-11).

**`api-contract-review`** (3.75). A breaking API change silently breaks every client. The skill classifies each change against explicit rules, checks the schema against the handlers, and runs compatibility checkers where installed. It has no explicit verification pass, and applies only to projects with published contracts.

*To raise the grade:* Add a verification step that re-reads each drift item in the handler.

**`rlm-log-triage`** (3.70). During an incident, turning thousands of log lines into ranked causes shortens the outage. Clustering is done by the model per chunk, so counts are approximate, and log citations are not required at line level.

*To raise the grade:* Require a log file and line for each cluster's first occurrence.

**`rlm-migration-planner`** (3.70). Framework and runtime migrations are high-risk projects; the skill orders work by the import graph and requires a rollback path. Migrations are occasional.

*To raise the grade:* Add a verification pass on each compatibility risk before it enters the plan.

### B

**`stack-auditor`** (3.65). Configuration mistakes and secrets in container files cause outages and leaks. The method runs format validators and gives a verdict. Its scope overlaps cicd-pipeline-review.

*To raise the grade:* Settle the overlap with cicd-pipeline-review (B-10).

**`web-performance`** (3.65). Core Web Vitals affect conversion and search ranking. The skill groups findings by metric and asks for field data first. Without field data the ranking is an estimate, and most findings degrade experience rather than break it.

*To raise the grade:* Validate against field data on a real site (B-34).

**`web-css-layout`** (3.60). Every front end has stylesheets, and layout bugs, contrast failures and overflow are common. The support rule checks each newer feature against the project's targets with a fallback. Most defects are visual rather than severe.

*To raise the grade:* Validate on a sample front end (B-34).

**`web-ui-components`** (3.60). Interactive components are built in most front ends, and their keyboard, focus and motion defects affect real users. The coverage is broad, but many recommended features are recent, so much of the advice depends on a support check.

*To raise the grade:* Validate component by component on a sample UI (B-34).

**`license-attribution`** (3.50). Shipping copyleft or unknown licences can force disclosure or a recall. The skill checks against a policy and drafts the attribution. It is needed at distribution time, not daily.

*To raise the grade:* Validate with licence tools installed.

**`memory-manager`** (3.50). Recalling earlier answers saves time and tokens on repeat requests, and staleness flags stop an outdated answer being reused silently. It improves efficiency rather than preventing defects, and it has no not-checked list.

*To raise the grade:* Add a not-checked list (what recall cannot see); set a store size policy (B-16).

**`trust-layer-validator`** (3.45). A forged credential or replayed message is severe, and the checks are specific (pinned contexts, proof allow-lists, replay protection, key handling). Very few projects implement decentralized identity, so presence and usage are minimal.

*To raise the grade:* Grade rises sharply for identity projects; keep it off by default.

**`web-app-platform`** (3.40). Date and time-zone bugs and caches that leak personal data are real failures, and an origin move breaks storage and passkeys without a plan. Installable and offline apps, and origin moves, are not common needs.

*To raise the grade:* Validate the date checks with failing-input fixtures (B-34).

### C+

**`rlm-doc-generator`** (3.00). Every project needs documentation, and the import graph gives the overview structure. Documentation errors are low severity, and the skill has no not-checked list: it does not say which modules were left undocumented.

*To raise the grade:* Add a not-checked list and require each documented signature to cite its file and line.

**`audit-evidence-collector`** (2.95). During an audit, an indexed evidence set with a hash per item saves days. Audits are periodic and only regulated organisations run them.

*To raise the grade:* Confirm the collection steps with the organisation's auditor (B-18).

**`token-saver`** (2.90). It applies to every reply and cuts cost and reading time, but it prevents no defects. Its rules are clear and it defers to other skills' required sections, but it has nothing to verify.

*To raise the grade:* Measure the token reduction end to end (B-17).

**`incident-postmortem`** (2.85). A sourced timeline and owned actions stop incidents repeating. The method has no verification pass on timeline sources, and it is used only after incidents.

*To raise the grade:* Require a source (log line, message, commit) for every timeline entry and a check that each one exists.

**`compliance-control-check`** (2.80). Missing control evidence fails an audit. The reference table was checked against secondary sources only, which caps support strength, and only regulated organisations need it.

*To raise the grade:* Practitioner review of the reference table and more frameworks (B-18, B-30).

### C

**`release-notes`** (2.70). Useful at each release, and notes trace to commits. A wrong note misleads users but rarely causes harm, and there is little to verify beyond the history.

*To raise the grade:* Group by user impact using labels from merged pull requests, and flag commits with no description.

**`web-built-in-ai`** (2.65). The safety guidance is solid: fallbacks when the model is missing, untrusted input and output, confirmation before agent actions. The APIs and the agent-tools draft are still changing, and few projects use them yet.

*To raise the grade:* Re-grade as the APIs stabilise and adoption grows; validate (B-34).

## What the grades show

- **Security and correctness skills lead.** `code-review`, `rlm-security-audit` and `web-client-security` score A+: they prevent the most severe failures and have the strongest methods.
- **The tier follows the grade.** 11 skills graded A- or better are premium, 15 graded B+ to B- are pro, and 7 graded C+ or lower are essentials. Without a key, only the essentials skills install.
- **Specific weaknesses lower some grades,** and each has a named fix: `rlm-doc-generator` and `memory-manager` have no not-checked list; `api-contract-review`, `rlm-migration-planner` and `incident-postmortem` lack an explicit verification pass; `compliance-control-check` rests on a reference table that a practitioner has not checked.
- **No skill is graded D.** The lowest grades (`release-notes`, `web-built-in-ai`) reflect narrow benefit or early technology, not a broken method.

## How to re-grade

1. Re-read each changed `SKILL.md` and re-score support strength against the anchors above.
2. Re-score usage and presence only if the reference project changes; say so in the scope.
3. When a skill has been run against a model (B-1), set support strength from the measured result: 5 for high recall with few false findings, 3 for useful but noisy output, 1 for unreliable output.
4. Recompute the score with the formula, update this page, and add a line to the review log in MAINTAINERS.md.
