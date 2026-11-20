# RLM Agent Skills: installation and troubleshooting

This guide covers installing the extension and the skills, choosing how the helper scripts run, and fixing common problems. For what each skill does, see [SKILLS.md](SKILLS.md).

## 1. What the extension does

RLM Agent Skills writes agent skills into your project. A skill is a folder with a `SKILL.md` file (instructions for the agent) and, for some skills, a `scripts/` folder with a helper. GitHub Copilot, Claude Code and other agents read these skills and follow them.

The extension:

- makes **no** model calls and needs **no** API key,
- does **not** analyse your code itself,
- only writes files into your project, when you run its command.

The analysis happens in your agent's chat, under your own agent subscription. The agent sends the code it reads to its model provider, as it does for any other task.

## 2. What you need

- **VS Code 1.146 or newer.**
- **An AI agent that reads skills:** GitHub Copilot (primary), Claude Code, OpenAI Codex, Cursor, Gemini CLI or Windsurf.
- **Optionally, a helper runtime:** Python 3 (recommended), Node.js, or neither (see section 5).

## 3. Install the extension

The extension is not on the VS Code Marketplace yet. Download [`skill-pack-2.1.0.vsix`](https://github.com/kamalsoft/skill-pack/raw/main/binary/skill-pack-2.1.0.vsix) from the `binary/` folder of the repository, then install it.

From a terminal:

```bash
code --install-extension skill-pack-2.1.0.vsix
```

From VS Code:

1. Open the Extensions view (`⇧⌘X` on macOS, `Ctrl+Shift+X` on Windows).
2. Click the `…` menu at the top of the view.
3. Choose **Install from VSIX…** and select the file.
4. Reload VS Code if asked.

To check the install, search the Extensions view for `RLM Agent Skills`. The command **RLM: Install Agent Skills** should appear in the Command Palette.

The terminal install can print a `url.parse()` deprecation warning. It comes from VS Code's own command line, not from the extension, and you can ignore it.

## 4. Install the skills into a project

1. Open the project as a **folder** (**File > Open Folder**). A single file will not work.
2. Open the Command Palette (`⇧⌘P` on macOS, `Ctrl+Shift+P` on Windows) and run **RLM: Install Agent Skills**.
3. Answer the questions in order:

   **a. How should the helper scripts run?** Option 1 is selected by default. See section 5.

   **b. Where should the skills go?** Choose one or more agents. **GitHub Copilot** is selected by default. Each agent gets its own folder:

   | Agent | Folder in your project |
   | --- | --- |
   | GitHub Copilot | `.github/skills/` |
   | Claude Code | `.claude/skills/` |
   | OpenAI Codex | `.agents/skills/` |
   | Cursor | `.cursor/skills/` |
   | Gemini CLI | `.gemini/skills/` |
   | Windsurf | `.windsurf/skills/` |

   **c. Which skills should be installed?** Fourteen skills are selected by default. Four are off: `release-notes`, `stack-auditor`, `trust-layer-validator` and `incident-postmortem`. The three compliance skills are also off. Select any of them you need. [SKILLS.md](SKILLS.md) describes each one.

4. When the install finishes, a message reads **RLM: wrote N file(s).** If it also says some files were left unchanged, those were files you had edited. See section 6.

## 5. Choose how the helper scripts run

Some skills use a small helper script to split files into chunks, build an import graph or store memory. The install asks how these should run.

| Option | What runs | What it needs | Choose it when |
| --- | --- | --- | --- |
| 1. Python (recommended) | `rlm_corpus.py`, `memory_graph.py` | Python 3 (`python3`, or `py -3` on Windows) | Python 3 is installed and allowed |
| 2. Node.js | `rlm_corpus.js`, `memory_graph.js` | Node.js. Uses only built-in modules | Node.js is installed but Python is not |
| 3. Portable Python | A Python interpreter inside the skills folder | Windows only, and a build that includes the runtime | Python cannot be installed, but scripts may run |
| 4. Instructions only | Nothing. The agent follows written steps itself | Nothing | Programs may not run on your machine |

Notes:

- Options 1 and 2 give the same results.
- **Option 3 needs a build that includes the portable runtime.** The standard build does not include it. If you choose option 3 without it, the install stops with a message saying so. Choose option 1, 2 or 4 instead.
- **Option 4** works for smaller projects. It uses more of the agent's context, is slower and less consistent. Memory is turned off in this mode.
- The choice only affects skills that use a helper. Other skills install the same way in every mode.

## 6. Your files and your edits

- Every file the extension writes starts with the marker line `managed-by: vscode-rlm-agent`.
- **Update:** run **RLM: Install Agent Skills** again. Files with the marker are replaced with the new version.
- **Keep your changes:** if you edit a skill file and remove the marker line, the installer leaves that file alone from then on.
- **Remove:** delete the skill folders from the agent's folder (for example `.github/skills/`). The extension never deletes anything.
- **Memory:** the memory skill stores its records in `.agent-memory/graph.json` in your project. If the project uses git, add `.agent-memory/` to `.gitignore`. The extension does not change `.gitignore` for you.

## 7. Use the skills

Ask your agent in plain words, and name the skill:

> Use the rlm-security-audit skill on `src/`. Report findings with file and line.

Check that the agent can see the skills:

- **GitHub Copilot:** open Copilot Chat and type `/skills`. The `rlm-*` skills should be listed.
- **Claude Code:** the skills are in `.claude/skills/`. Name a skill in your request.

The helper scripts run from inside the skill folder. You do not normally run them yourself, but you can check what they report. For example, from your project root:

```bash
python3 .github/skills/rlm-security-audit/scripts/rlm_corpus.py scan .
```

| Command | What it reports |
| --- | --- |
| `scan` | How many files there are, their size, and what was skipped |
| `chunk` | The files split into pieces for the agent to read one at a time |
| `graph` | Which files import which, and any import cycles |
| `pending` | Which pieces still need a review |
| `merge` | The results from all pieces, with duplicates removed |

Use `--include 'src/*'` to limit a command to part of the project. Use `--max-bytes` to change the size above which files are skipped.

## 8. Privacy and safety

- The extension sends nothing anywhere, and its files stay in your project folder.
- The agent sends the code it reads to its model provider. Do not run the skills on code you are not allowed to send there.
- The helpers remove secrets and personal data from their output where they can, and the skills tell the agent not to copy them. This is a safeguard, not a guarantee. Check reports before you share them.
- Logs, configuration files and pipeline files are treated as data, not instructions.

## 9. Troubleshooting

| What you see | What to do |
| --- | --- |
| **RLM: Install Agent Skills** is missing from the Command Palette | Run **Developer: Reload Window**. Check that **RLM Agent Skills** is installed and enabled in the Extensions view. |
| "open a folder first" | Open a project folder, not a single file. |
| The skills do not appear in `/skills` (Copilot) | Run **Developer: Reload Window**. Check that the skill folders exist in the agent's folder. |
| The install wrote 0 files, and all were skipped | The files already exist and lack the marker line, so the installer treats them as yours. Delete the skill folder to let the installer rewrite it, or put the marker line back. |
| The install wrote fewer files than expected | Some files were kept because you edited them. The message after the install gives the count. |
| Option 1 fails with "python3 not found" | Install Python 3 (on Windows, `py -3` must work). Or re-run the install and choose option 2 or 4. |
| "The portable Python runtime is not bundled in this build" | Choose option 1, 2 or 4. |
| The agent does not use the skill | Name the skill in your request, for example "use the rlm-security-audit skill". |
| A helper command fails, or `scan` reports 0 files | Run the command by hand from the project root and read its output. Check that the path is correct and that `.gitignore` is not excluding everything. |
| `merge` reports a failed output | A piece of the review did not produce a valid result. Run the agent again on the pieces the report names. |
| The agent reads far more of the project than you expected | Narrow the request, for example "only `src/`". Instructions-only mode uses more context by design. |

## 10. Known limits

- **Results depend on the agent and its model.** The skills are written as instructions and have not been tuned against each model. Check every finding against the source before you act on it.
- **Chunks** are at most 800 lines or 100,000 characters. The helper cuts at a function, a method, a blank line or a closing brace where it can. A block with no such cut point, such as a minified file, is cut in the middle and marked as continued.
- **Large or binary files** are skipped. The default limit is 20 MB; `--max-bytes` changes it. `scan` lists what was skipped, and the skill report says so too.
- **Compressed logs** (`.gz`) are not read. Decompress the time window you need into a folder first.
- **Import graph:** Python, JavaScript and TypeScript (including `tsconfig.json` and `jsconfig.json` path aliases), Java, Kotlin, Scala, C#, PHP, Go, Rust, Ruby and C/C++ includes are covered. C# and PHP are matched by path, since their namespaces do not always follow folders. Other languages are not parsed.
- **Secret detection** is pattern-based. It catches common key formats, not every secret.
- **Memory** records conversations, not a full code index. It is stored in one file and is intended for one machine at a time.
- **Cursor** also reads `.agents/skills/`. If you install for both Codex and Cursor, Cursor may list a skill twice.
- **Portable Python** has not been tested on Windows.
- **Compliance skills** report evidence. They do not certify compliance.

## 11. Update and uninstall

**Update.** Download the newer `.vsix` from the [`binary/` folder](https://github.com/kamalsoft/skill-pack/tree/main/binary) and install it over the old one, then run **RLM: Install Agent Skills** again in each project:

```bash
code --install-extension skill-pack-2.1.0.vsix --force
```

**Uninstall.**

1. If you entered a licence key, run **RLM: Remove Licence Key** first, so it does not stay in VS Code's secret storage.
2. Uninstall the extension, from a terminal or from the Extensions view (gear on **RLM Agent Skills** > **Uninstall**):
   ```bash
   code --uninstall-extension kamalsoft.skill-pack
   ```
3. Quit VS Code completely (`⌘Q` on macOS) and start it again. VS Code removes uninstalled extensions only on a full restart.
4. Check: `code --list-extensions --show-versions | grep kamalsoft` should print nothing.
5. Uninstalling does not change your projects. To remove the skills as well, delete the skill folders the extension wrote in each agent folder (`.github/skills/`, `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.gemini/skills/`, `.windsurf/skills/`) and the memory store `.agent-memory/`.

Earlier builds were published as `kamalsoft.rlm-agent-skills` and `kamalsoft.vscode-rlm-agent`. If the skill picker shows an old list, uninstall those copies the same way and restart VS Code.

## 12. Command reference

**Command Palette** (`⇧⌘P` on macOS, `Ctrl+Shift+P` on Windows):

| Command | What it does |
| --- | --- |
| **RLM: Install Agent Skills** | Installs or updates the skills in the open project. Asks how helpers run, which agents and which skills. |
| **RLM: Enter Licence Key** | Checks a key offline and stores it in VS Code's secret storage on this machine. Unlocks pro or premium skills in every project. |
| **RLM: Remove Licence Key** | Deletes the stored key. Essentials skills keep working. |

**Terminal:**

| To | Run |
| --- | --- |
| Install | `code --install-extension skill-pack-2.1.0.vsix` |
| Update over an older copy | `code --install-extension skill-pack-2.1.0.vsix --force` |
| See the installed version | `code --list-extensions --show-versions \| grep kamalsoft` |
| Uninstall | `code --uninstall-extension kamalsoft.skill-pack` |

**Helper scripts.** The chunked skills include `scripts/rlm_corpus.py` (or `rlm_corpus.js`, run with `node`, if you chose Node.js). The agent runs them; run them yourself from the project root to see what a skill will read:

| Command | Output |
| --- | --- |
| `rlm_corpus.py scan ROOT` | Files, lines and characters in scope, per top-level folder, and what was skipped |
| `rlm_corpus.py chunk ROOT OUT_DIR [--max-lines N] [--max-chars N]` | Chunk files of at most 800 lines and 100,000 characters, and `manifest.json` |
| `rlm_corpus.py graph ROOT` | The local import graph, its cycles and the most-imported files |
| `rlm_corpus.py pending CHUNKS_DIR OUT_DIR` | Which chunks have no usable review yet |
| `rlm_corpus.py merge OUT_DIR [--out FILE]` | Chunk results merged, duplicates removed, failed outputs listed (exit code 1 if any failed) |

Every helper command accepts `--include GLOB` (repeatable, for example `--include 'src/*'`) and `--max-bytes N` (default 20 MB).

```bash
python3 .github/skills/rlm-security-audit/scripts/rlm_corpus.py scan .
python3 .github/skills/rlm-security-audit/scripts/rlm_corpus.py chunk . /tmp/rlm-chunks --include 'src/*'
```

