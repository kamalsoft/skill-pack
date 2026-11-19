# Skills reference

The package has twenty-one skills. This page explains what each one is for, how to ask for it, and its pros and cons. For installing them, see [DOCUMENTATION.md](DOCUMENTATION.md).

## Choosing a skill

Start from the question you want answered:

- **"Is this safe?" or "Is this change correct?"** Use a security, review or threat-model skill.
- **"Is this too big to read in one go?"** Use one of the chunked analysis skills (`rlm-*`). They split the input into pieces and review each piece.
- **"What did we decide before?"** Use `memory-manager`.
- **"Is this about one technology we use?"** Use a domain skill (`stack-auditor`, `trust-layer-validator`, `cicd-pipeline-review`).
- **"Do we meet a control or licence policy?"** Use a compliance skill.

Keep the default selection unless you have a reason to change it. Each selected skill adds instructions to the agent's context, so remove the ones you never use.

Skills marked **Off** are not selected in the install picker. Select them there when you need them.

| Skill | Use it for | Default | Point it at |
| --- | --- | --- | --- |
| `rlm-security-audit` | Vulnerabilities, leaked secrets, injection | On | A repository or folder |
| `rlm-refactor-planner` | Import cycles, coupling, a phased refactor plan | On | A repository or module |
| `rlm-doc-generator` | Module and public API documentation | On | A package or folder |
| `rlm-test-gap-analysis` | Untested behaviour and weak assertions | On | Source and test folders |
| `rlm-migration-planner` | Framework, runtime or major-version migration | On | Source and target versions |
| `rlm-log-triage` | Errors and likely causes in incident logs | On | A folder of log files |
| `rlm-privacy-review` | Where personal data is collected, stored and shared | On | A repository or folder |
| `code-review` | A branch, pull request or diff before merge | On | A branch or diff |
| `dependency-audit` | Vulnerable, outdated or duplicated dependencies | On | Manifests and lock files |
| `release-notes` | Release notes from commits and merged pull requests | Off | Git history |
| `api-contract-review` | Breaking changes in OpenAPI, protobuf or GraphQL | On | Schema and route changes |
| `threat-model` | Threats to a system or change, using STRIDE | On | A system or design |
| `cicd-pipeline-review` | Pipeline secrets, permissions and deployments | On | Pipeline files |
| `stack-auditor` | Configuration, Docker and environment variables | Off | Configuration and Docker files |
| `trust-layer-validator` | Decentralized identity and credential code | Off | Identity and credential files |
| `incident-postmortem` | A blameless postmortem after an incident | Off | Timeline, alerts and notes |
| `compliance-control-check` | Which controls have evidence in the repository | Off | A control list you supply |
| `audit-evidence-collector` | Change, review and pipeline evidence for an audit period | Off | An audit period |
| `license-attribution` | Dependency licences against a policy, and NOTICE text | Off | Manifests and a licence policy |
| `memory-manager` | Recording and recalling past requests and answers | On | Nothing; it works from your requests |
| `token-saver` | Shorter answers: no filler, diff-only edits | On | Nothing; it changes how answers are written |

## How the chunked skills work

The seven `rlm-*` skills use the same method. The helper does the file handling. The agent does the judgement.

1. **Scan** the input to count files and see what will be skipped.
2. **Split** it into pieces of at most 800 lines or 100,000 characters.
3. **Review** each piece. The agent reads one piece at a time, or in separate sub-tasks where the agent supports them.
4. **Merge** the results and drop duplicates. A piece that fails is reported, never counted as "no findings".
5. **Report.** The agent checks the serious findings against the source and writes the report.

Narrow any run with a folder or pattern in your request, such as "only `src/`".

---

## Analysis (chunked)

### rlm-security-audit

**Use it for:** a security review of code that is too large to read in one pass.

> Use the rlm-security-audit skill to audit this repository. Scope it to `src/` first.

The agent checks each piece for hardcoded secrets, injection, unsafe deserialization, disabled TLS checks, weak cryptography, missing authorization and sensitive data in logs. Each finding gives `path:line`, a severity and a fix. Secret values are shown as `<redacted>`.

- **Pros:** covers every file in scope, not only the files the agent happened to open. Serious findings are checked against the source before they are reported.
- **Cons:** the findings depend on the model's judgement, so expect some false positives and some misses. It is not a static analyser.

### rlm-refactor-planner

**Use it for:** planning a refactor: which modules depend on which, where the cycles are, and the order of the work.

> Use the rlm-refactor-planner skill to plan splitting the billing module. Start from the import graph.

The agent starts from the import graph, which lists the cycles and the most-imported files, then writes a phased plan. Each phase is small and says what must stay stable.

- **Pros:** the plan starts from measured structure. The import graph is the same on every run.
- **Cons:** the graph misses dynamic imports, reflection, dependency-injection containers and generated code. A plan is not a change; each phase still needs testing.

### rlm-doc-generator

**Use it for:** documentation for the modules and public API of a large codebase, with an overview of how they connect.

> Use the rlm-doc-generator skill to document the `packages/core` folder. One page per package.

The agent collects each module's purpose and public signatures, then writes one page per module. Undocumented items are listed rather than guessed at, and quoted signatures are checked against the source.

- **Pros:** consistent module pages. The overview uses the import graph.
- **Cons:** the prose is a draft to read and edit. Code examples are not compiled or run. Behaviour that is not in the code, such as what another service does, cannot be documented from the repository.

### rlm-test-gap-analysis

**Use it for:** finding risky code that has no test, and tests that pass without checking anything.

> Use the rlm-test-gap-analysis skill on `src/` against `tests/`. Use the coverage report if one exists.

The agent uses the project's coverage report when there is one, reviews the source against the tests, and ranks the gaps by risk. Each gap comes with an example test you can add.

- **Pros:** points at risky paths such as validation, authorization, money and error handling. Each gap has a concrete test.
- **Cons:** without a coverage report, gaps are inferred from names and can be wrong. The quality of fixtures and mocks is not judged.

### rlm-migration-planner

**Use it for:** moving from one framework, runtime or major version to another, such as "Python 3.9 to 3.12" or "React 17 to 18".

> Use the rlm-migration-planner skill to plan React 17 to 18 for the `web/` folder.

Name the source and the target. The skill asks if either is missing. The agent lists every use of the old version, matches each one to its equivalent in the new version, and writes phases with a rollback step for each.

- **Pros:** you know how big the migration is before you start. Each phase can ship and be reverted on its own.
- **Cons:** the model may suggest an equivalent that does not exist, so check each one against the new version's documentation. Changes that do not show in the code, such as new default timeouts, are not found.

### rlm-log-triage

**Use it for:** an incident with many log lines, where you need to know what failed first and why.

Decompress the time window you need into a folder first. Then:

> Use the rlm-log-triage skill on `incident-2026-11-18/`. The outage started around 14:05 UTC.

The agent groups the errors by signature, counts each group with its first and last timestamps, traces the first error in each chain, and ranks the likely causes. Each cause cites the log lines that support it. Personal data and secrets are redacted.

- **Pros:** thousands of lines become a few groups with counts and time ranges. Each cause can be checked against the lines given.
- **Cons:** compressed `.gz` files are not read. The time window is applied by hand. Counts are approximate, because the grouping is done by the model.

### rlm-privacy-review

**Use it for:** a data-protection review of a large codebase: where personal data is collected, stored, logged, shared with third parties and deleted.

> Use the rlm-privacy-review skill on `services/` for a data-protection assessment.

The agent builds a data inventory, follows the flows between components, and lists retention gaps. It reports field names and locations only, never personal values.

- **Pros:** the inventory is built from the code. Logging of personal data and transfers to third parties are reported explicitly.
- **Cons:** fields are found by name and context, so an unusually named field can be missed. Databases, backups and third-party consoles are not in the repository. Whether a practice meets a legal requirement is for your privacy team to decide.

---

## Engineering review

### code-review

**Use it for:** reviewing a branch, pull request or diff before merge.

> Use the code-review skill on the changes between `origin/main` and this branch.

The agent reads the diff file by file, checks the code around each changed function, and writes a verdict. Findings are ranked as blocker, major, minor or nit, and the report lists the tests to run.

- **Pros:** a consistent checklist: correctness, security, data safety, compatibility, performance, tests and operations. It needs only git.
- **Cons:** it reads the code; it does not run the code, the tests or a static analyser. Design and product decisions are for the reviewer.

### dependency-audit

**Use it for:** supply-chain risk before a release: known vulnerabilities, unmaintained packages, licences and duplicate versions.

> Use the dependency-audit skill before the next release.

The agent finds the manifests and lock files, runs the audit tools that are installed, and writes a prioritised upgrade plan. It changes nothing.

- **Pros:** findings match the versions you actually have, including indirect dependencies. It never runs fix commands without your approval.
- **Cons:** coverage depends on which audit tools are installed. Without them, findings come from the lock file alone. Vulnerability lookups need network access.

### release-notes (Off)

**Use it for:** release notes and changelog entries from commits and merged pull requests since the last tag.

> Use the release-notes skill for everything since tag v2.0.0.

The agent groups the changes by impact and writes upgrade steps for each breaking change. Every note traces to a commit or a pull request.

- **Pros:** reads the substance of each change, not only its title.
- **Cons:** needs tags and reasonable commit messages. The impact grouping is the model's judgement, so read it before you publish.

### api-contract-review

**Use it for:** a change to an OpenAPI, protobuf or GraphQL contract, or to the routes behind it, before a release.

> Use the api-contract-review skill on the changes to `api/openapi.yaml` since `main`.

The agent compares the contract with the previous version, marks each change as breaking or not, using written rules, and checks that the handlers match the schema.

- **Pros:** breaking changes are found by named rules, not by memory. Schema drift between contract and code is reported.
- **Cons:** consumers outside the repository are not visible, so a "non-breaking" verdict depends on that assumption. Without a compatibility tool, the result is a reading of the schema, not a machine check.

---

## Security and risk

### threat-model

**Use it for:** a threat model of a system or change, before a security review, when you add an external interface, or when you design something new.

> Use the threat-model skill on the new payments webhook. Assets are card tokens and order status.

The agent lists the routes, handlers and configuration, draws a data-flow diagram with trust boundaries (in Mermaid), applies STRIDE to each part, and looks for each control in the code. A control that the documents claim but the code does not show is recorded as a gap.

- **Pros:** gives reviewers the architecture and threat context a diff review does not. Every control has a `file:line` reference, or is listed as a gap.
- **Cons:** the quality depends on the architecture documents and code it can read. STRIDE is a checklist, not a proof. Controls outside the repository, such as cloud IAM rules, are not visible.

---

## Domain review

These skills check one technology. Use them only for projects that use it.

### stack-auditor (Off)

**Use it for:** configuration files, Docker files and compose files.

> Use the stack-auditor skill on the `docker/` folder and the compose files.

The agent checks the files for syntax errors, leaked secrets, port and environment-variable problems, and mixing of service boundaries.

- **Pros:** small and specific. Catches configuration mistakes before deployment.
- **Cons:** the checks are generic. They do not run a linter such as hadolint or a schema validator.

### trust-layer-validator (Off)

**Use it for:** decentralized identity code: credential schemas, JSON-LD contexts, agent-to-agent messages and protocol handlers.

> Use the trust-layer-validator skill on the credential schema changes in this branch.

The agent checks JSON-LD context references and schema structure, the shape of agent messages, and flags hardcoded keys and insecure transport.

- **Pros:** covers failure modes of credential code that a general review can miss.
- **Cons:** very narrow, so most projects should leave it off. Schema validity is checked by reading, not by a validator.

### cicd-pipeline-review

**Use it for:** pipeline files for GitHub Actions, GitLab CI, Jenkins, Azure Pipelines or CircleCI, before a pipeline or runner is enabled, or when one changes.

> Use the cicd-pipeline-review skill on `.github/workflows/`.

The agent checks permissions, secret exposure, untrusted input in scripts, pinning of third-party actions, deployment protection and build provenance. Each finding names the trigger that makes it exploitable. It runs `actionlint` or `zizmor` if they are installed.

- **Pros:** finds the mistakes that give an attacker a path to secrets or to production. Read-only.
- **Cons:** repository and organization settings, such as branch protection and environment reviewers, are not in the files and are not checked.

---

## Operations

### incident-postmortem (Off)

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

**Use it for:** a readiness review against a control set your organization supplies.

Give the skill your control list. Without one, it reports only general areas and says so.

> Use the compliance-control-check skill with our internal policy file `docs/controls.md`.

The agent maps each control to the evidence it needs, searches the repository, and reports each control as present, partial, absent, outside the repository, or not applicable. Each item cites `file:line`.

- **Pros:** shows which evidence exists before an audit, and which gaps need an owner. The control list is yours, not invented.
- **Cons:** code being present does not prove a control works. Operation needs testing or sampling outside the repository.

### audit-evidence-collector (Off)

**Use it for:** collecting change, review, pipeline and scan evidence for a fixed audit period.

> Use the audit-evidence-collector skill for the period 2026-07-01 to 2026-09-30 on this repository.

The agent lists merges, pipeline runs and configuration history for the period, saves what it finds, and writes an index with a SHA-256 hash for each item.

- **Pros:** read-only. Each item has a source and a hash, so the collection can be checked again.
- **Cons:** review approvals need the hosting CLI and access. Without them, approvals are marked as not collected. Evidence is a snapshot.

### license-attribution (Off)

**Use it for:** checking dependency licences against a policy before you ship, and drafting the NOTICE file.

> Use the license-attribution skill before we ship the desktop build. Policy: permissive only, plus LGPL with dynamic linking.

The agent lists direct and indirect dependencies, classifies each licence, flags violations and unknown licences, and drafts the attribution text.

- **Pros:** finds copyleft and unknown licences from the lock file, including indirect dependencies.
- **Cons:** this is not legal advice. Exceptions belong to your legal team. Without the licence tools installed, the review relies on the lock file alone.

---

## Memory

### memory-manager

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

**Use it for:** shorter answers with no filler, no repeated code, and edits shown only as changed lines.

Once installed, it applies to the agent's replies and code edits. It does not shorten what other skills must include, such as verdicts, findings, lists of what was not checked and tests to run.

- **Pros:** less to read and less output to generate. No setup and nothing stored.
- **Cons:** brevity can drop context you need, such as the reason for a decision. The savings have not been measured, so treat them as expected rather than proven.
