# Skills reference

The package has thirty-three skills. This page explains what each one is for, how to ask for it, and its pros and cons. For installing them, see [DOCUMENTATION.md](DOCUMENTATION.md).

Every skill has a grade from A+ to D, and the grade sets its tier: A+ to A- are **premium** (11 skills), B+ to B- are **pro** (15) and C+ to D are **essentials** (7). Essentials skills install without a key; pro and premium skills need a licence key. The criteria and the reasoning for each grade are in [skill-grade.md](skill-grade.md).

## Choosing a skill

Start from the question you want answered:

- **"Is this safe?" or "Is this change correct?"** Use a security, review or threat-model skill.
- **"Is this too big to read in one go?"** Use one of the chunked analysis skills (`rlm-*`). They split the input into pieces and review each piece.
- **"What did we decide before?"** Use `memory-manager`.
- **"Is this about one technology we use?"** Use a domain skill (`stack-auditor`, `trust-layer-validator`, `cicd-pipeline-review`).
- **"Do we meet a control or licence policy?"** Use a compliance skill.
- **"Is this front end secure, fast, accessible and easy to use?"** Use a web platform skill (`web-*`, `rlm-accessibility-audit`, `browser-extension-review`).

Keep the default selection unless you have a reason to change it. Each selected skill adds instructions to the agent's context, so remove the ones you never use.

Skills marked **Off** are not selected in the install picker. Select them there when you need them.

| Skill | Use it for | Default | Tier | Grade | Point it at |
| --- | --- | --- | --- | --- | --- |
| `rlm-security-audit` | Vulnerabilities, leaked secrets, injection | On | premium | A+ | A repository or folder |
| `rlm-refactor-planner` | Import cycles, coupling, a phased refactor plan | On | premium | A- | A repository or module |
| `rlm-doc-generator` | Module and public API documentation | On | essentials | C+ | A package or folder |
| `rlm-test-gap-analysis` | Untested behaviour and weak assertions | On | premium | A | Source and test folders |
| `rlm-migration-planner` | Framework, runtime or major-version migration | On | pro | B+ | Source and target versions |
| `rlm-log-triage` | Errors and likely causes in incident logs | On | pro | B+ | A folder of log files |
| `rlm-privacy-review` | Where personal data is collected, stored and shared | On | pro | B+ | A repository or folder |
| `code-review` | A branch, pull request or diff before merge | On | premium | A+ | A branch or diff |
| `dependency-audit` | Vulnerable, outdated or duplicated dependencies | On | premium | A | Manifests and lock files |
| `release-notes` | Release notes from commits and merged pull requests | Off | essentials | C | Git history |
| `api-contract-review` | Breaking changes in OpenAPI, protobuf or GraphQL | On | pro | B+ | Schema and route changes |
| `threat-model` | Threats to a system or change, using STRIDE | On | premium | A- | A system or design |
| `cicd-pipeline-review` | Pipeline secrets, permissions and deployments | On | pro | B+ | Pipeline files |
| `stack-auditor` | Configuration, Docker and environment variables | Off | pro | B | Configuration and Docker files |
| `trust-layer-validator` | Decentralized identity and credential code | Off | pro | B | Identity and credential files |
| `incident-postmortem` | A blameless postmortem after an incident | Off | essentials | C+ | Timeline, alerts and notes |
| `compliance-control-check` | Which controls have evidence in the repository | Off | essentials | C+ | A control list you supply |
| `audit-evidence-collector` | Change, review and pipeline evidence for an audit period | Off | essentials | C+ | An audit period |
| `license-attribution` | Dependency licences against a policy, and NOTICE text | Off | pro | B | Manifests and a licence policy |
| `memory-manager` | Recording and recalling past requests and answers | On | pro | B | Nothing; it works from your requests |
| `token-saver` | Shorter answers: no filler, diff-only edits | On | essentials | C+ | Nothing; it changes how answers are written |
| `rlm-llm-app-review` | Prompt injection and unsafe model output in apps that call a model | Off | premium | A | A repository with model calls |
| `rlm-performance-review` | N+1 queries, blocking calls and code that will not scale | Off | pro | B+ | A repository, plus a profile if available |
| `db-migration-safety` | Locks, data loss and deploy-order breakage in migrations | Off | premium | A- | A branch with migrations |
| `web-client-security` | Passkeys, CSP, Trusted Types and cross-origin messaging | Off | premium | A+ | Sign-in code, HTML sinks, headers |
| `web-forms-autofill` | Forms that browsers and password managers can fill | Off | premium | A | Form markup and handlers |
| `rlm-accessibility-audit` | Accessibility failures, each tied to WCAG 2.2 | Off | premium | A | Front-end templates, components and styles |
| `browser-extension-review` | Manifest V3 permissions, messaging and store readiness | Off | pro | B+ | Extension manifest and source |
| `web-performance` | Core Web Vitals: LCP, INP and CLS | Off | pro | B | Pages, plus field data if available |
| `web-css-layout` | Modern CSS layout, theming and typography | Off | pro | B | Stylesheets and browser targets |
| `web-ui-components` | Dialogs, menus and other components, keyboard-ready | Off | pro | B | Component source |
| `web-app-platform` | Installable and offline apps, origin moves, dates and locales | Off | pro | B | Manifest, service worker, date code |
| `web-built-in-ai` | On-device browser AI and tools for browser agents | Off | essentials | C | Browser AI calls and agent tools |

## How the chunked skills work

The nine `rlm-*` skills use the same method. The helper does the file handling. The agent does the judgement.

1. **Scan** the input to count files and see what will be skipped.
2. **Split** it into pieces of at most 800 lines or 100,000 characters.
3. **Review** each piece. The agent reads one piece at a time, or in separate sub-tasks where the agent supports them.
4. **Merge** the results and drop duplicates. A piece that fails is reported, never counted as "no findings".
5. **Report.** The agent checks the serious findings against the source and writes the report.

Narrow any run with a folder or pattern in your request, such as "only `src/`".

---

## Analysis (chunked)

### rlm-security-audit

**Tier:** premium · **Grade:** A+

**Use it for:** a security review of code that is too large to read in one pass.

> Use the rlm-security-audit skill to audit this repository. Scope it to `src/` first.

The agent checks each piece for hardcoded secrets, injection, unsafe deserialization, disabled TLS checks, weak cryptography, missing authorization and sensitive data in logs. Each finding gives `path:line`, a severity and a fix. Secret values are shown as `<redacted>`.

- **Pros:** covers every file in scope, not only the files the agent happened to open. Serious findings are checked against the source before they are reported.
- **Cons:** the findings depend on the model's judgement, so expect some false positives and some misses. It is not a static analyser.

### rlm-refactor-planner

**Tier:** premium · **Grade:** A-

**Use it for:** planning a refactor: which modules depend on which, where the cycles are, and the order of the work.

> Use the rlm-refactor-planner skill to plan splitting the billing module. Start from the import graph.

The agent starts from the import graph, which lists the cycles and the most-imported files, then writes a phased plan. Each phase is small and says what must stay stable.

- **Pros:** the plan starts from measured structure. The import graph is the same on every run.
- **Cons:** the graph misses dynamic imports, reflection, dependency-injection containers and generated code. A plan is not a change; each phase still needs testing.

### rlm-doc-generator

**Tier:** essentials · **Grade:** C+

**Use it for:** documentation for the modules and public API of a large codebase, with an overview of how they connect.

> Use the rlm-doc-generator skill to document the `packages/core` folder. One page per package.

The agent collects each module's purpose and public signatures, then writes one page per module. Undocumented items are listed rather than guessed at, and quoted signatures are checked against the source.

- **Pros:** consistent module pages. The overview uses the import graph.
- **Cons:** the prose is a draft to read and edit. Code examples are not compiled or run. Behaviour that is not in the code, such as what another service does, cannot be documented from the repository.

### rlm-test-gap-analysis

**Tier:** premium · **Grade:** A

**Use it for:** finding risky code that has no test, and tests that pass without checking anything.

> Use the rlm-test-gap-analysis skill on `src/` against `tests/`. Use the coverage report if one exists.

The agent uses the project's coverage report when there is one, reviews the source against the tests, and ranks the gaps by risk. Each gap comes with an example test you can add.

- **Pros:** points at risky paths such as validation, authorization, money and error handling. Each gap has a concrete test.
- **Cons:** without a coverage report, gaps are inferred from names and can be wrong. The quality of fixtures and mocks is not judged.

### rlm-migration-planner

**Tier:** pro · **Grade:** B+

**Use it for:** moving from one framework, runtime or major version to another, such as "Python 3.9 to 3.12" or "React 17 to 18".

> Use the rlm-migration-planner skill to plan React 17 to 18 for the `web/` folder.

Name the source and the target. The skill asks if either is missing. The agent lists every use of the old version, matches each one to its equivalent in the new version, and writes phases with a rollback step for each.

- **Pros:** you know how big the migration is before you start. Each phase can ship and be reverted on its own.
- **Cons:** the model may suggest an equivalent that does not exist, so check each one against the new version's documentation. Changes that do not show in the code, such as new default timeouts, are not found.

### rlm-log-triage

**Tier:** pro · **Grade:** B+

**Use it for:** an incident with many log lines, where you need to know what failed first and why.

Decompress the time window you need into a folder first. Then:

> Use the rlm-log-triage skill on `incident-2026-11-18/`. The outage started around 14:05 UTC.

The agent groups the errors by signature, counts each group with its first and last timestamps, traces the first error in each chain, and ranks the likely causes. Each cause cites the log lines that support it. Personal data and secrets are redacted.

- **Pros:** thousands of lines become a few groups with counts and time ranges. Each cause can be checked against the lines given.
- **Cons:** compressed `.gz` files are not read. The time window is applied by hand. Counts are approximate, because the grouping is done by the model.

### rlm-privacy-review

**Tier:** pro · **Grade:** B+

**Use it for:** a data-protection review of a large codebase: where personal data is collected, stored, logged, shared with third parties and deleted.

> Use the rlm-privacy-review skill on `services/` for a data-protection assessment.

The agent builds a data inventory, follows the flows between components, and lists retention gaps. It reports field names and locations only, never personal values.

- **Pros:** the inventory is built from the code. Logging of personal data and transfers to third parties are reported explicitly.
- **Cons:** fields are found by name and context, so an unusually named field can be missed. Databases, backups and third-party consoles are not in the repository. Whether a practice meets a legal requirement is for your privacy team to decide.

### rlm-performance-review (Off)

**Tier:** pro · **Grade:** B+

**Use it for:** a slow service, a planned load increase, or the question of where the code will not scale.

> Use the rlm-performance-review skill on `api/`. Here is last week's slow-query log.

The agent chunks the code and looks in each chunk for queries in loops, blocking calls on async paths, unbounded reads, quadratic work, repeated set-up and calls with no timeout. It then finds what calls each high-severity item and ranks it by how often that path runs. A profile or trace from the user outranks anything inferred from the code.

- **Pros:** ranks by how hot the path is, not by the pattern alone, so start-up code does not crowd out request handlers. Skips micro-optimisations unless the path is shown to be hot.
- **Cons:** reads code; does not measure. Without a profile, the ranking is an estimate. Query plans, index statistics and production data volumes are not visible.

---

## Engineering review

### code-review

**Tier:** premium · **Grade:** A+

**Use it for:** reviewing a branch, pull request or diff before merge.

> Use the code-review skill on the changes between `origin/main` and this branch.

The agent reads the diff file by file, checks the code around each changed function, and writes a verdict. Findings are ranked as blocker, major, minor or nit, and the report lists the tests to run.

- **Pros:** a consistent checklist: correctness, security, data safety, compatibility, performance, tests and operations. It needs only git.
- **Cons:** it reads the code; it does not run the code, the tests or a static analyser. Design and product decisions are for the reviewer.

### dependency-audit

**Tier:** premium · **Grade:** A

**Use it for:** supply-chain risk before a release: known vulnerabilities, unmaintained packages, licences and duplicate versions.

> Use the dependency-audit skill before the next release.

The agent finds the manifests and lock files, runs the audit tools that are installed, and writes a prioritised upgrade plan. It changes nothing.

- **Pros:** findings match the versions you actually have, including indirect dependencies. It never runs fix commands without your approval.
- **Cons:** coverage depends on which audit tools are installed. Without them, findings come from the lock file alone. Vulnerability lookups need network access.

### release-notes (Off)

**Tier:** essentials · **Grade:** C

**Use it for:** release notes and changelog entries from commits and merged pull requests since the last tag.

> Use the release-notes skill for everything since tag v2.0.0.

The agent groups the changes by impact and writes upgrade steps for each breaking change. Every note traces to a commit or a pull request.

- **Pros:** reads the substance of each change, not only its title.
- **Cons:** needs tags and reasonable commit messages. The impact grouping is the model's judgement, so read it before you publish.

### api-contract-review

**Tier:** pro · **Grade:** B+

**Use it for:** a change to an OpenAPI, protobuf or GraphQL contract, or to the routes behind it, before a release.

> Use the api-contract-review skill on the changes to `api/openapi.yaml` since `main`.

The agent compares the contract with the previous version, marks each change as breaking or not, using written rules, and checks that the handlers match the schema.

- **Pros:** breaking changes are found by named rules, not by memory. Schema drift between contract and code is reported.
- **Cons:** consumers outside the repository are not visible, so a "non-breaking" verdict depends on that assumption. Without a compatibility tool, the result is a reading of the schema, not a machine check.

### db-migration-safety (Off)

**Tier:** premium · **Grade:** A-

**Use it for:** a branch or pull request that adds or changes a database migration.

> Use the db-migration-safety skill on this branch. PostgreSQL 16; `orders` has about 40 million rows; migrations run before the new code in a rolling deploy.

The agent lists the migration files in the change, reads the SQL (printing it from the ORM tool where it can), and checks each statement for blocking locks and table rewrites, missing lock timeouts, data loss, deploy-order breakage, unsafe backfills, statements that cannot run in a transaction, and reversibility. It gives a verdict and the safe sequence of migrations when a change needs expand and contract.

- **Pros:** never connects to a database. It reads files and printed SQL only. Rules that depend on engine version or table size are reported as conditional, with what would decide them.
- **Cons:** lock behaviour differs by engine and version. The checks name PostgreSQL and MySQL examples; other engines rely on their documentation. Real table sizes, traffic and long-running transactions are unknown unless the user gives them.

---

## Security and risk

### threat-model

**Tier:** premium · **Grade:** A-

**Use it for:** a threat model of a system or change, before a security review, when you add an external interface, or when you design something new.

> Use the threat-model skill on the new payments webhook. Assets are card tokens and order status.

The agent lists the routes, handlers and configuration, draws a data-flow diagram with trust boundaries (in Mermaid), applies STRIDE to each part, and looks for each control in the code. A control that the documents claim but the code does not show is recorded as a gap.

- **Pros:** gives reviewers the architecture and threat context a diff review does not. Every control has a `file:line` reference, or is listed as a gap.
- **Cons:** the quality depends on the architecture documents and code it can read. STRIDE is a checklist, not a proof. Controls outside the repository, such as cloud IAM rules, are not visible.

### rlm-llm-app-review (Off)

**Tier:** premium · **Grade:** A

**Use it for:** an application that calls a language model or runs an agent with tools, before release or after adding a model feature.

> Use the rlm-llm-app-review skill on `services/assistant/`. The agent can send email and create tickets.

The agent first finds the model surface (clients, prompt builders, tool definitions, retrieval code) and limits the scope to it, then chunks that code and checks each chunk for prompt injection paths, unsafe use of model output, over-privileged tools, data sent to the model, and missing limits. Each finding carries its OWASP Top 10 for LLM Applications identifier. High-severity items are traced from the untrusted input to the sink before they are reported.

- **Pros:** does not accept a prompt instruction or a model-based filter as a control on its own; it asks for a deterministic one. Never reproduces a whole system prompt in the report.
- **Cons:** a code review, not a red-team test. It does not show how the model actually behaves. Prompts stored outside the repository (a database, a prompt service, the provider console) are not seen.

---

## Web platform

These skills review front-end work on the modern web platform. All are off by default; select the ones your front end needs.

### web-client-security (Off)

**Tier:** premium · **Grade:** A+

**Use it for:** adding sign-in or passkeys, rendering untrusted HTML, embedding third-party scripts, or reviewing front-end security.

> Use the web-client-security skill on the sign-in flow and the comment rendering.

The agent lists sign-in flows, HTML sinks, message channels, third-party origins, security headers and client-side cryptography. It checks passkeys and other sign-in, what code the page runs (CSP, Trusted Types, sanitizing, integrity), whom the page talks to, browser cryptography and privacy, and gives a header table.

- **Pros:** traces each injection from source to sink before reporting it. Names maintained libraries; never suggests custom cryptography or WebAuthn verification.
- **Cons:** headers set by infrastructure outside the repository are not seen. Third-party script contents are not reviewed.

### web-forms-autofill (Off)

**Tier:** premium · **Grade:** A

**Use it for:** building or reviewing sign-in, sign-up, checkout, address or any data-entry form.

> Use the web-forms-autofill skill on the checkout and sign-up forms.

The agent lists every field with its type, name, label, autocomplete token and validation, and checks structure, autofill, keyboards, validation and errors, one-time codes, input-method handling and custom controls. Fixes are given as corrected markup.

- **Pros:** a complete autocomplete-token table for identity, address and payment fields. Never suggests blocking paste or client-only validation.
- **Cons:** behaviour differs between password managers; the skill does not test them. Server-side validation outside the scope is not read.

### rlm-accessibility-audit (Off)

**Tier:** premium · **Grade:** A

**Use it for:** an accessibility review of a whole front end, before release, or after a report from an assistive-technology user.

> Use the rlm-accessibility-audit skill on `web/`. Our target is WCAG 2.2 AA.

The agent limits the scope to templates, components and styles, runs any checker the project already has, then chunks the front end and checks each chunk for text alternatives, structure, names and roles, keyboard and focus, announcements, visual and motion issues, pointer targets, and forms. Each finding names its WCAG 2.2 success criterion. Findings from a shared component are reported once, at the component.

- **Pros:** prefers native HTML fixes over ARIA. Never claims conformance; reports failures and what was not checked.
- **Cons:** a code review cannot replace testing with assistive technology or with disabled users. Contrast is computed only where colour values are known; others are marked likely.

### browser-extension-review (Off)

**Tier:** pro · **Grade:** B+

**Use it for:** writing, reviewing or preparing to publish a Manifest V3 browser extension.

> Use the browser-extension-review skill on this extension before we submit it to the store.

The agent reads the manifest first, then the service worker, content scripts and extension pages. It checks the worker lifecycle, permissions, messaging and sender checks, content-script safety, network and identity, code security, the UI surfaces and store readiness, and gives a verdict with a permission table.

- **Pros:** each permission is tied to the code that uses it, or marked for removal. Says where a rule is specific to Chrome.
- **Cons:** store policies change; the skill tells the agent to check the current text. Server components the extension talks to are not reviewed.

### web-performance (Off)

**Tier:** pro · **Grade:** B

**Use it for:** a page that is slow to load or respond, failing Core Web Vitals, or a heavy front-end change before release.

> Use the web-performance skill on the product page. Field data from our RUM is attached; INP is failing.

The agent asks for field data, finds the largest-content element, scripts, fonts and images for each page, and checks loading, layout stability, responsiveness, navigation, analytics and background work. Findings are grouped by the metric they affect.

- **Pros:** field data outranks lab results, and the report says which was used. Never claims a speed-up it has not measured.
- **Cons:** without field data the ranking is an estimate. Server response time and CDN set-up are outside the scope; use rlm-performance-review for back-end code.

### web-css-layout (Off)

**Tier:** pro · **Grade:** B

**Use it for:** writing or reviewing stylesheets, fixing layout bugs, or replacing JavaScript layout code with CSS.

> Use the web-css-layout skill on `src/components/`. Targets are in `.browserslistrc`.

The agent reads the browser targets, lists the stylesheets and the JavaScript that does layout work, and checks layout, selectors and the cascade, tokens and theming, typography, visual effects and motion. Each newer feature it recommends comes with a `@supports` fallback for targets that lack it.

- **Pros:** every newer feature is checked against the project's own browser targets, with a fallback. Does not change the visual design beyond what a finding needs.
- **Cons:** reads source, not the rendered page: visual results are not seen. Browser support changes over time; the skill tells the agent to check it, so results depend on that check.

### web-ui-components (Off)

**Tier:** pro · **Grade:** B

**Use it for:** building or reviewing UI components, overlays, animations or scroll effects.

> Use the web-ui-components skill on our dialog, menu and carousel components.

The agent lists each interactive component and how it is built, then checks overlays, each component against its pattern, motion and scroll effects, interruptions and input variety, and walks each component's keyboard path. It names custom code that a platform feature can replace.

- **Pros:** every recent feature comes with feature detection and a fallback. Covers the common component set, from dialogs to drill-down panels.
- **Cons:** behaviour in real assistive technology is not tested. Third-party component internals are not reviewed.

### web-app-platform (Off)

**Tier:** pro · **Grade:** B

**Use it for:** making a site installable or offline-capable, moving it to a new origin, or fixing date, time or locale bugs.

> Use the web-app-platform skill. We move from app.example.com to example.app next quarter, and users report wrong meeting times.

The agent lists the manifest, service worker and caches, install UI, and every place dates, numbers and currencies are handled. It checks installability, caching and updates, an origin move (including storage and passkeys), and date, time and locale handling, with a failing input for each date finding.

- **Pros:** an ordered origin-move plan that covers what does not move by itself. Every date finding comes with a concrete failing case.
- **Cons:** install flows differ by platform and are not tested. Server-side date handling outside the scope is not read.

### web-built-in-ai (Off)

**Tier:** essentials · **Grade:** C

**Use it for:** a feature that uses the browser's on-device AI, or a site being made usable by AI agents.

> Use the web-built-in-ai skill on the new summarize button and the agent tools on the booking page.

The agent lists each AI call or agent tool, then checks availability and model download, sessions and cost, input and output safety, and, for agent tools, descriptions, schemas, authorization and confirmation steps. It produces an availability matrix dated when checked.

- **Pros:** treats page content and model output as untrusted. Never states API names or availability from memory as settled.
- **Cons:** these APIs and the agent-tools draft change often; results are only as current as the date checked. Model output quality is not judged.

---

## Domain review

These skills check one technology. Use them only for projects that use it.

### stack-auditor (Off)

**Tier:** pro · **Grade:** B

**Use it for:** configuration files, Docker files and compose files.

> Use the stack-auditor skill on the `docker/` folder and the compose files.

The agent checks the files for syntax errors, leaked secrets, port and environment-variable problems, and mixing of service boundaries.

- **Pros:** small and specific. Catches configuration mistakes before deployment.
- **Cons:** the checks are generic. They do not run a linter such as hadolint or a schema validator.

### trust-layer-validator (Off)

**Tier:** pro · **Grade:** B

**Use it for:** decentralized identity code: credential schemas, JSON-LD contexts, agent-to-agent messages and protocol handlers.

> Use the trust-layer-validator skill on the credential schema changes in this branch.

The agent checks JSON-LD context references and schema structure, the shape of agent messages, and flags hardcoded keys and insecure transport.

- **Pros:** covers failure modes of credential code that a general review can miss.
- **Cons:** very narrow, so most projects should leave it off. Schema validity is checked by reading, not by a validator.

### cicd-pipeline-review

**Tier:** pro · **Grade:** B+

**Use it for:** pipeline files for GitHub Actions, GitLab CI, Jenkins, Azure Pipelines or CircleCI, before a pipeline or runner is enabled, or when one changes.

> Use the cicd-pipeline-review skill on `.github/workflows/`.

The agent checks permissions, secret exposure, untrusted input in scripts, pinning of third-party actions, deployment protection and build provenance. Each finding names the trigger that makes it exploitable. It runs `actionlint` or `zizmor` if they are installed.

- **Pros:** finds the mistakes that give an attacker a path to secrets or to production. Read-only.
- **Cons:** repository and organization settings, such as branch protection and environment reviewers, are not in the files and are not checked.

---

## Operations

### incident-postmortem (Off)

**Tier:** essentials · **Grade:** C+

**Use it for:** a blameless postmortem, written after an incident is contained.

Run `rlm-log-triage` on the incident window first, then:

> Use the incident-postmortem skill. Inputs are the log triage report, the alert export and the incident channel notes.

The agent builds a timeline in which every entry has a source. It separates the trigger from the root cause and the contributing factors, and writes action items with an owner role, a date and a type (prevent, detect or mitigate). Anything the evidence does not show is marked as unknown or as a hypothesis.

- **Pros:** blameless by rule: roles and decisions are described, not individuals. Gaps stay visible.
- **Cons:** only as complete as the inputs. The root cause can only be as firm as the evidence the team has.

---

## Compliance

These skills report whether evidence is present or missing. They do not certify compliance. Only your auditor or assessor can do that.

### compliance-control-check (Off)

**Tier:** essentials · **Grade:** C+

**Use it for:** a readiness review against a control set your organization supplies.

Give the skill your control list. Without one, it reports only general areas and says so.

> Use the compliance-control-check skill with our internal policy file `docs/controls.md`.

The agent maps each control to the evidence it needs, searches the repository, and reports each control as present, partial, absent, outside the repository, or not applicable. Each item cites `file:line`.

- **Pros:** shows which evidence exists before an audit, and which gaps need an owner. The control list is yours, not invented.
- **Cons:** code being present does not prove a control works. Operation needs testing or sampling outside the repository.

### audit-evidence-collector (Off)

**Tier:** essentials · **Grade:** C+

**Use it for:** collecting change, review, pipeline and scan evidence for a fixed audit period.

> Use the audit-evidence-collector skill for the period 2026-07-01 to 2026-09-30 on this repository.

The agent lists merges, pipeline runs and configuration history for the period, saves what it finds, and writes an index with a SHA-256 hash for each item.

- **Pros:** read-only. Each item has a source and a hash, so the collection can be checked again.
- **Cons:** review approvals need the hosting CLI and access. Without them, approvals are marked as not collected. Evidence is a snapshot.

### license-attribution (Off)

**Tier:** pro · **Grade:** B

**Use it for:** checking dependency licences against a policy before you ship, and drafting the NOTICE file.

> Use the license-attribution skill before we ship the desktop build. Policy: permissive only, plus LGPL with dynamic linking.

The agent lists direct and indirect dependencies, classifies each licence, flags violations and unknown licences, and drafts the attribution text.

- **Pros:** finds copyleft and unknown licences from the lock file, including indirect dependencies.
- **Cons:** this is not legal advice. Exceptions belong to your legal team. Without the licence tools installed, the review relies on the lock file alone.

---

## Memory

### memory-manager

**Tier:** pro · **Grade:** B

**Use it for:** remembering what was asked and answered in a project, so follow-up questions start from earlier conclusions.

Nothing special is needed. Ask as normal. The skill tells the agent to recall related earlier answers before it answers, and to record the new one afterwards. You can look at the store yourself:

```bash
python3 .github/skills/memory-manager/scripts/memory_graph.py stats
python3 .github/skills/memory-manager/scripts/memory_graph.py recall "billing invoice"
```

Each recalled entry has a `stale` list. If the list is not empty, a file that the earlier answer depends on has changed, been deleted or appeared since it was written, so check the answer again before you reuse it.

- **Pros:** follow-up questions are answered from recorded conclusions. Answers that depend on changed code are flagged rather than reused silently. Secret-looking values are removed before anything is stored.
- **Cons:** this is not a code index; it has no call graph and no symbol search beyond the entries. It is only as good as what the agent records. The store grows until you prune it (`prune --keep N`). It is designed for one machine at a time.

---

## Efficiency

### token-saver

**Tier:** essentials · **Grade:** C+

**Use it for:** shorter answers with no filler, no repeated code, and edits shown only as changed lines.

Once installed, it applies to the agent's replies and code edits. It does not shorten what other skills must include, such as verdicts, findings, lists of what was not checked and tests to run.

- **Pros:** less to read and less output to generate. No setup and nothing stored.
- **Cons:** brevity can drop context you need, such as the reason for a decision. The savings have not been measured, so treat them as expected rather than proven.
