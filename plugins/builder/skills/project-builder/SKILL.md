---
name: project-builder
description: "Build .project/ directory structures for any AI coding tool. Guides users through a discovery interview, generates PROJECT.md manifests, instructions, memory, context, resources, agents, and provider adapters. Use when: (1) setting up a new AI project, (2) migrating to the .project standard, (3) scaffolding project config for Claude/Codex/Gemini. Triggers on 'build project', 'create .project', 'project setup', 'scaffold project', 'init project', 'project builder', 'new .project'."
---

# Project Builder

Build vendor-neutral `.project/` directory structures that work across Claude Code, OpenAI Codex, Google Gemini, and any tool supporting the [.project standard](https://protocols.difflab.ai/docs/projects/).


---

## What You Get

**Core (always generated):**
1. **PROJECT.md** — The project manifest (the only required file, written to `.project/`)
2. **Instructions** — Custom instructions teaching the AI about the project's workflow, standards, and quality criteria (written to `.project/instructions/`)
3. **Project files** — Files identified during the interview (created in the project root alongside `.project/`, referenced by the manifest)
4. **Adapter scripts** — Symlink-based provider mappings (Claude, Codex, Gemini)
5. **Setup guidance** — What to do after generation

**Advanced (optional, configured on request):**
6. **Context** — References to local project files and external documents for AI analysis (usually files alongside `.project/`, not inside it)
7. **Resources** — References to external systems and services (dashboards, CI/CD, monitoring)
8. **Memory** — Persistent knowledge, decision records, entity data
9. **Tasks** — Lightweight task tracking with status workflows (usually referencing external trackers)
10. **Agents** — Specialized AI role definitions

---

## Activation

Trigger with phrases like:
- "Build a .project for this repo"
- "Set up project configuration"
- "Create .project structure"
- "Scaffold project for Claude/Codex/Gemini"
- "Initialize AI project config"
- "Migrate to .project standard"

---

## Workflow

### Step 1: Detect Environment and Auto-Discover

Before starting the interview, silently gather what you can from the project tree. Do not ask the user for information that can be determined automatically.

1. **Identify the invoking agent.** Check which AI coding tool is running this skill:
   - **Claude Code** — Will run the Claude adapter script
   - **OpenAI Codex** — Will run the Codex adapter script
   - **Google Gemini** — Will run the Gemini adapter script
   - **Other/Unknown** — Generate `.project/` only, no adapter

2. **Auto-detect project details** from the file system (do not ask the user for these):
   - **Project name** — From the directory name, `package.json`, `Cargo.toml`, `pyproject.toml`, or similar
   - **Repository URL** — From `.git/config` if it exists
   - **Language/framework** — From file extensions, config files, lock files present in the tree
   - **License** — From `LICENSE` or `LICENSE.md` if present
   - **Existing structure** — Scan the project tree to understand what files and directories exist

3. **Record the detected agent** for use in Step 6.

### Step 2: Discovery Interview

Conduct a structured interview following the five areas below. Adapt based on what the user has already told you and what was auto-detected in Step 1. Skip questions whose answers are already known.

#### 1. Workflow Discovery
- What task or workflow will this project support?
- How often do you do this task?
- What makes it challenging or time-consuming?

#### 2. Context Needs
- What information do you reference while doing this work?
- Where does it live? (local files, cloud docs, APIs, dashboards)
- How often does it change?

#### 3. Output Requirements
- What should the AI produce when working on this project?
- What format should it use?
- Who is the audience?

#### 4. Quality Criteria
- What distinguishes good output from bad?
- Can you give examples of excellent work?
- What mistakes should be avoided?

#### 5. Personal Context
- What is your role and expertise level?
- Any domain-specific terminology the AI should know?
- Preferred tone or style?

After the interview, **summarize your understanding** back to the user and confirm before proceeding. Include the auto-detected details (project name, repo, language, etc.) so the user can correct anything.

### Step 3: Determine Output Location

Ask the user where to write the `.project/` structure:

1. **Ask:** "Where should I write the `.project/` directory? (default: current working directory)"
2. **Check for conflicts at the target location:**
   - If a `.project/` **directory** already exists: warn that files may be overwritten and confirm
   - If a `.project` **file** exists (common with Eclipse IDE): ask the user whether to:
     - **Overwrite** the file and create a `.project/` directory in its place
     - **Use `.aiproject/`** as the alternative directory name instead
   - If neither exists: proceed with `.project/`
3. **Record the chosen directory name** (`.project` or `.aiproject`) for all subsequent writes.

### Step 4: Generate Core Files

Generate the core `.project/` files using the templates in `assets/templates/`. Use the `.project/` standard's markdown-with-YAML-frontmatter format.

**Files inside `.project/` (always generate):**
- `PROJECT.md` — The project manifest. Lists all project files, describes the project, and references any files identified during the interview.

**Files inside `.project/` (based on interview):**
- `instructions/index.md` — Base instructions covering the project's primary workflow, quality criteria, and conventions
- `instructions/<topic>.md` — Topic-specific instructions (one per major area identified in the interview)

**Files alongside `.project/` in the project root (based on interview):**
- Any files identified during the interview that should exist in the project — config files, schemas, documentation, CI configs, etc. These are referenced by the manifest but live in the normal project file structure, not inside `.project/`.

**File format for `.project/` files:**
```markdown
---
name: identifier
description: Brief explanation (1-3 sentences)
[additional fields per spec]
---

# Heading

Body content in markdown.
```

### Step 5: Confirm and Write

Before writing any files:

1. **Present the file list** — Show the user every file that will be created, grouped by location:
   - **Inside `.project/`**: `PROJECT.md`, `instructions/index.md`, etc.
   - **In project root**: any additional files identified during the interview
2. **Flag overwrites** — For any file that already exists at the target location, explicitly note it and ask for confirmation.
3. **Ask about advanced areas** — Before writing, ask: "Would you like to configure any advanced areas before I write the files?"
   - **Context** — References to local project files (alongside `.project/`) and external documents that the AI should analyze. Context entries typically point to files in the project tree or remote URLs, not files inside `.project/`.
   - **Resources** — References to external systems and services (dashboards, CI/CD, monitoring, documentation sites). Resources are for awareness only and are never fetched automatically.
   - **Memory** — Persistent knowledge like architectural decisions, discovered patterns, and entity data.
   - **Tasks** — Task tracking, usually referencing an external tracker or backlog.
   - **Agents** — Specialized AI role definitions (e.g., reviewer, architect, tester).

   If the user wants to configure any of these, gather the relevant information and add the corresponding files to the generation list (these go inside `.project/`).
4. **Write files** — After confirmation, write all files to their target locations.
5. **Report results** — List all files written with their paths.

### Step 6: Run Provider Adapter Script (automatic)

Based on the agent detected in Step 1, run the appropriate adapter script from `scripts/`. These scripts create symlinks mapping `.project/` files to the provider's expected locations.

The scripts are bundled with this skill at `scripts/adapt-{provider}.sh` (Unix/macOS/WSL) and `scripts/adapt-{provider}.ps1` (Windows PowerShell).

#### If Claude Code

Run the Claude adapter script, passing the project root as an argument:

```bash
# Unix/macOS/WSL
bash <skill-path>/scripts/adapt-claude.sh <project-root>

# Windows PowerShell
.\<skill-path>\scripts\adapt-claude.ps1 -ProjectRoot <project-root>
```

This creates symlinks:
- `instructions/index.md` -> `CLAUDE.md`
- `instructions/<topic>.md` -> `.claude/rules/<topic>.md`
- `agents/<agent>.md` -> `.claude/agents/<agent>.md`
- `skills/<name>/index.md` -> `.claude/skills/<name>/SKILL.md`

#### If OpenAI Codex

Run the Codex adapter script:

```bash
# Unix/macOS/WSL
bash <skill-path>/scripts/adapt-codex.sh <project-root>

# Windows PowerShell
.\<skill-path>\scripts\adapt-codex.ps1 -ProjectRoot <project-root>
```

This creates symlinks:
- `instructions/index.md` -> `AGENTS.md`
- `skills/<name>/index.md` -> `.agents/skills/<name>/SKILL.md`

#### If Google Gemini

Run the Gemini adapter script:

```bash
# Unix/macOS/WSL
bash <skill-path>/scripts/adapt-gemini.sh <project-root>

# Windows PowerShell
.\<skill-path>\scripts\adapt-gemini.ps1 -ProjectRoot <project-root>
```

This creates symlinks:
- `instructions/index.md` -> `GEMINI.md`
- `skills/<name>/index.md` -> `.gemini/skills/<name>/SKILL.md`

#### If Other/Unknown

Do not run any adapter script. Inform the user they can manually run an adapter later:

```bash
bash <skill-path>/scripts/adapt-claude.sh <project-root>   # for Claude
bash <skill-path>/scripts/adapt-codex.sh <project-root>    # for Codex
bash <skill-path>/scripts/adapt-gemini.sh <project-root>   # for Gemini
```

#### Cleaning Up Adapter Symlinks

All adapter scripts support a `--clean` flag (or `-Clean` on PowerShell) to remove previously created symlinks:

```bash
bash <skill-path>/scripts/adapt-claude.sh --clean <project-root>
```

### Step 7: Housekeeping and Next Steps

After writing all files, handle safe housekeeping automatically and provide guidance for the rest.

**Do automatically (no confirmation needed):**

1. **Update .gitignore** — If a `.gitignore` exists, append the required `.project/` patterns if they are not already present. If no `.gitignore` exists, create one with these patterns:
   ```
   .project/local.md
   .project/**/local.md
   .project/**/*.local.md
   .project/**/*.secret.*
   .project/users/*.local.md
   ```
   If `.aiproject/` was used instead, substitute `.aiproject/` in the patterns.

**Explain to the user:**

2. **Personal overrides** — They can create `local.md` files for personal preferences (these are gitignored)
3. **Progressive expansion** — They can add more `.project/` directories and files as needed
4. **Adapter sync** — If an adapter script was run, re-running it will update symlinks. The `--clean` flag removes them.

---

## Design Principles

- **Spec compliance** — All generated files conform to `.project` standard v1
- **Progressive disclosure** — Start minimal, expand as needed
- **Markdown-first** — Every file is human-readable markdown with structured YAML frontmatter
- **Vendor-neutral** — Core structure works with any AI coding tool
- **Convention over configuration** — Sensible defaults, explicit overrides only when needed
- **Confirm before overwrite** — Never silently replace existing files

---

## Templates

Templates are located in `assets/templates/` and follow the `.project` standard format. Each template contains placeholder markers in `[brackets]` that are replaced during generation.

**Core templates (always available):**
- `PROJECT.md` — Project manifest
- `instructions-index.md` — Base instructions catalog
- `instruction-topic.md` — Domain-specific instruction

**Advanced templates (used when user opts into advanced areas):**
- `context-index.md` — Context file catalog
- `resources-index.md` — Resource reference catalog
- `memory-index.md` — Memory/knowledge catalog
- `tasks-index.md` — Task board overview
- `agents-index.md` — Agent catalog
- `agent-definition.md` — Individual agent definition

---

## References

- [.project Standard Specification v1](https://github.com/difflabai/protocols/blob/main/project-standard/spec/v1/specification.md)
- [Original ProjectBuilder Skill](https://github.com/leegonzales/AISkills/tree/main/ProjectBuilder/project-builder)
