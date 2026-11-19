<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="logo-dark.svg">
    <img src="logo.svg" alt="RLM Agent Skills" width="400">
  </picture>
</p>

# Skill Pack: consumer guide

The skill pack is a VS Code extension, **RLM Agent Skills** (package `skill-pack`). It installs agent skills into your project, so that GitHub Copilot or Claude Code can review, analyze and document large codebases in pieces, remember past answers, and keep its replies short.

The extension makes no model calls and needs no API key. It writes skill files into your project folder. The AI agent you already use does the work, under your own subscription.

> **Disclaimer**
>
> - **Not professional advice.** The skills do not give legal, security, privacy, compliance, licensing or audit advice. Their output is a technical aid for a qualified person to review. It does not replace a security audit, a penetration test, a legal review or a formal compliance assessment.
> - **Output can be wrong.** AI agents can miss real problems, report problems that do not exist, and invent details. Verify every finding against the source before you act on it or share it.
> - **Compliance skills are not certification.** They report whether evidence is present or missing. Only the organization's auditor or assessor can state that a control is met.
> - **Your data.** The agent you use sends the code and files it reads to its model provider, under that provider's terms. Do not use the skills on material you are not allowed to send there.
> - **No warranty.** The software is provided "as is", without warranty of any kind, under the MIT licence. The authors are not liable for decisions taken on the basis of its output.
> - **Not affiliated.** GitHub Copilot, Claude Code, OpenAI Codex, Cursor, Gemini CLI, Windsurf, VS Code and the other products named here are trademarks of their owners. This project is not endorsed by them.

Links in this guide point to the documentation in the `docs/` folder:

- Visual guide, with a 3D view of each skill and install steps: [kamalsoft.github.io/skillpack](https://kamalsoft.github.io/skillpack/).
- Skill-by-skill reference, with examples and pros and cons: [docs/SKILLS.md](docs/SKILLS.md)
- Full installation and troubleshooting guide: [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md)
- Package repository: [github.com/kamalsoft/skill-pack](https://github.com/kamalsoft/skill-pack).

Version 1.0.0 · License MIT ([LICENSE.MD](LICENSE.MD))

## What you need

- **VS Code** 1.146 or newer.
- **An AI agent** that reads skills: GitHub Copilot in VS Code (primary), Claude Code, OpenAI Codex, Cursor, Gemini CLI or Windsurf.
- **One of the helper runtimes**, or none:
  - Python 3 (option 1, recommended), or
  - Node.js (option 2), or
  - nothing at all (option 4, instructions only). Option 3 needs a build that includes the portable Python runtime.

## Install

Installing is two steps: install the extension once, then install the skills into each project that uses them.

### Step 1: Install the extension

The extension is not on the VS Code Marketplace yet. Install it from the `skill-pack-1.0.0.vsix` file, either from a terminal:

```bash
code --install-extension skill-pack-1.0.0.vsix
```

or from VS Code: open the Extensions view (`⇧⌘X`), click the `…` menu at the top, choose **Install from VSIX…**, select the file, and reload VS Code if asked.

### Step 2: Install the skills into a project

1. Open the project as a folder (**File > Open Folder**), not a single file.
2. Open the Command Palette (`⇧⌘P` on macOS, `Ctrl+Shift+P` on Windows) and run **RLM: Install Agent Skills**.
3. Answer the three questions:

   | Question | Default | What to choose |
   | --- | --- | --- |
   | How should the helper scripts run? | 1. Python | 1 if Python 3 is installed. 2 if only Node.js is installed. 4 if programs may not run. Option 3 needs a build with the portable runtime. |
   | Which agents should get the skills? | GitHub Copilot | Every agent you use. You can pick more than one. |
   | Which skills? | Fourteen selected | Keep the defaults, or tick the off ones you want (`release-notes`, `stack-auditor`, `trust-layer-validator`, `incident-postmortem`, and the three compliance skills). |

4. Wait for the message **RLM: wrote N file(s).** If it says some files were left unchanged, you had edited them before; see [Your files and your edits](#your-files-and-your-edits).

Each agent reads skills from its own folder in the project:

| Agent | Skills folder |
| --- | --- |
| GitHub Copilot (default) | `.github/skills/` |
| Claude Code | `.claude/skills/` |
| OpenAI Codex | `.agents/skills/` |
| Cursor | `.cursor/skills/` |
| Gemini CLI | `.gemini/skills/` |
| Windsurf | `.windsurf/skills/` |

Each skill is a folder holding a `SKILL.md`. The analysis skills and `memory-manager` also get a `scripts/` folder with their helper.

### Step 3: Check that the agent sees the skills

- **GitHub Copilot:** open Copilot Chat and type `/skills`. The skill names should be listed.
- **Claude Code:** the skills appear under `.claude/skills/`. Start Claude Code in the project and name a skill in your request.

### Update, remove or install without the extension

- **Update:** run **RLM: Install Agent Skills** again. Files you have edited are left alone.
- **Remove:** delete the skill folders from the agent's skills folder. The extension never deletes anything.

## Choose how the helpers run

| Option | What runs | Needs on your machine | Choose it when |
| --- | --- | --- | --- |
| 1. Python (recommended) | `rlm_corpus.py` and `memory_graph.py` | Python 3 (`python3`, or `py -3` on Windows) | Python is installed and allowed |
| 2. Node.js | `rlm_corpus.js` and `memory_graph.js`, built-in modules only | Node.js | Node is installed but Python is not |
| 3. Portable Python | A Python interpreter inside the skills folder | Windows only; needs a build that includes the runtime | Python cannot be installed, but scripts may run |
| 4. Instructions only | Nothing. The agent follows written steps itself | Nothing | Programs may not run on your machine at all |

The helpers do the mechanical work: listing files, splitting a repository into chunks, building an import graph, merging results, and storing memory. In instructions-only mode, the agent does this with its own file tools. That works for smaller projects, but it uses more of the agent's context, is slower, and gives less consistent results. Memory is turned off in that mode.

## Use the skills

Once installed, ask the agent for the task in plain words. Name the skill when you want a specific method.

- **Review a large codebase for security problems:**
  > Use the rlm-security-audit skill on `src/`. Report findings with file and line.
- **Plan a refactor:**
  > Use the rlm-refactor-planner skill. Start from the import graph and tell me the cycles.
- **Write documentation for one package:**
  > Use the rlm-doc-generator skill on `packages/billing`.
- **Review a pull request:**
  > Use the code-review skill on the changes between `main` and this branch.
- **Check dependencies before a release:**
  > Use the dependency-audit skill before the next release.
- **Plan a migration:**
  > Use the rlm-migration-planner skill to plan React 17 to 18 for `web/`.
- **Investigate an incident:**
  > Use the rlm-log-triage skill on `incident-logs/`. The outage started around 14:05 UTC.

To check that Copilot has the skills, open Copilot Chat, type `/skills`, and look for the names. In Claude Code, the skills appear under `.claude/skills/`.

## The skills

Twenty-one skills in eight categories. Each one has a section in the skills reference with how to use it, and its pros and cons.

| Category | Skill | What it is for | On by default |
| --- | --- | --- | --- |
| Analysis (chunked) | `rlm-security-audit` | Vulnerabilities, leaked secrets, injection, unsafe deserialization | Yes |
| Analysis (chunked) | `rlm-refactor-planner` | Dependency health, import cycles, coupling, phased refactor plan | Yes |
| Analysis (chunked) | `rlm-doc-generator` | Module and public API documentation | Yes |
| Analysis (chunked) | `rlm-test-gap-analysis` | Untested behaviour and weak assertions, with a test to add for each gap | Yes |
| Analysis (chunked) | `rlm-migration-planner` | Framework, runtime or major-version migration | Yes |
| Analysis (chunked) | `rlm-log-triage` | Error clusters and likely causes in large log sets | Yes |
| Analysis (chunked) | `rlm-privacy-review` | Where personal data is collected, stored, logged, shared and kept | Yes |
| Engineering review | `code-review` | Branch, pull request or diff review, with a verdict | Yes |
| Engineering review | `dependency-audit` | Vulnerable, outdated, unmaintained or duplicated dependencies | Yes |
| Engineering review | `api-contract-review` | Breaking changes in OpenAPI, protobuf and GraphQL | Yes |
| Engineering review | `release-notes` | Release notes from commits and merged pull requests | No |
| Security and risk | `threat-model` | Threats to a system or change, using STRIDE | Yes |
| Domain review | `cicd-pipeline-review` | CI/CD pipeline definitions: secrets, permissions, deployments | Yes |
| Domain review | `stack-auditor` | Configuration, Docker and service boundaries | No |
| Domain review | `trust-layer-validator` | Decentralized identity, credentials and protocol handlers | No |
| Operations | `incident-postmortem` | A blameless postmortem from the incident's evidence | No |
| Compliance | `compliance-control-check` | Which controls of a framework you supply have evidence in the repository | No |
| Compliance | `audit-evidence-collector` | Change, review, pipeline and scan evidence for an audit period | No |
| Compliance | `license-attribution` | Dependency licences against a policy, and the NOTICE text | No |
| Memory | `memory-manager` | Records requests and answers, and recalls them later | Yes |
| Efficiency | `token-saver` | Short answers: no filler, diff-only edits | Yes |

The compliance skills report evidence that is present or missing. They do not certify compliance. The `rlm-` skills split the work into chunks; the others follow a written method over git history, a diff, or a manifest.

## Your files and your edits

- Every skill file the extension writes starts with a marker line: `managed-by: vscode-rlm-agent`. Re-running the install command updates those files.
- If you edit a skill file and remove the marker line, the install command leaves that file alone from then on.
- To remove the skills, delete the skill folders in the target folder (for example `.github/skills/`). The extension does not delete anything.
- Memory is stored in `.agent-memory/graph.json` in your project. Add `.agent-memory/` to `.gitignore` if the project is under git. The extension does not change `.gitignore`.

## Privacy and safety

- The extension does not call a model, send your files anywhere, or need a key. Everything it writes stays in your project folder.
- The agent you use sends the code it reads to its model provider, as it does for any other task. The skills do not change that.
- The helpers keep secrets and personal data out of their output where they can, and the skills tell the agent not to copy them. This is a safeguard, not a guarantee. Check reports before you share them.
- Logs, configuration and pipeline files are data to the agent. The skills tell it to treat their contents as data, not as instructions.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| The command is missing from the Command Palette | Reload the window (**Developer: Reload Window**). Check that the extension is installed and enabled. |
| "Open a folder first" | Open a project folder, not a single file. |
| The skills do not appear in `/skills` (Copilot) | Reload the window. Check that the skills are in the folder for that agent. |
| Option 1 fails with "python3 not found" | Install Python 3, or on Windows use `py -3`. Or re-run the install and choose option 2 or 4. |
| "The portable Python runtime is not bundled in this build" | Choose option 1, 2 or 4. Option 3 needs a build that includes the runtime. |
| A skill says a helper command failed | Run the command by hand from the project root and read its error. The error names the file and the problem. |
| The install wrote fewer files than expected | Some files were kept because you edited them. The message after the install says how many. |
| The agent reads far more of the project than the skill describes | Narrow the scope in your request, for example "only `src/`". Instructions-only mode uses more context, by design. |

## Known limits

- Results depend on the AI agent and its model. The skills are not tuned against any one model.
- The analysis skills split large projects into chunks of up to 800 lines and 100,000 characters. A single unbroken block of code, such as a minified file, is cut in the middle and marked as continued.
- Files over 20 MB, and binary files, are skipped. The skill report says what was skipped.
- The import graph covers Python, JavaScript and TypeScript (including path aliases), Java, Kotlin, Scala, C#, PHP, Go, Rust, Ruby and C/C++ includes. Other languages are not parsed.
- Secret detection is pattern-based. It catches common key formats, not every secret.
- The memory skill records conversations, not a full code index.
- Compliance skills give evidence, not certification. Use the control text your organization supplies.
- Portable Python has been prepared for Windows but not yet tested there. A PowerShell helper does not exist yet.

## Licence and version

RLM Agent Skills is released under the MIT licence. Copyright (c) 2026 kamalsoft. The full text is in [LICENSE.MD](LICENSE.MD).

Version 1.0.0.
