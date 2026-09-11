# AutoExpert 🚀

> **The Unified Framework for Adaptive AI Persona Induction, Attention Steering, and Pair-Programming State Continuity.**

Originally created by **Dustin Miller ([@spdustin](https://github.com/spdustin))** and evolved through real-world software engineering by **Sean Tyler ([@seanbuilds](https://github.com/seanbuilds))**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Creative Commons: CC BY-NC-SA 4.0](https://img.shields.io/badge/Prompts-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Tests](https://github.com/seanbuilds/autoexpert/actions/workflows/validate.yml/badge.svg)](https://github.com/seanbuilds/autoexpert/actions)

---

## 🌟 What is AutoExpert?

Base Large Language Models default to cautious, generic conversational behavior. **AutoExpert** is an architecture designed to bypass generic assistant weights by priming the model's emergent attention mechanisms toward deep, domain-specific authority roles.

### The 5 Architectural Pillars

1. **Dynamic Expert Persona Induction**: Self-selects the exact authority role required for the task (e.g., `Python > Distributed Systems Architect`) instead of static personas.
2. **Attention Steering Preambles**: Pre-calibrates reasoning before emitting generation tokens with formal keywords, role specifications, and execution roadmaps.
3. **Dual Verbosity Dialing**: V=1–5 for knowledge/research depth AND V=0–3 for code engineering density — in one unified scale.
4. **Standardized Slash Commands**: 20+ intuitive commands (`/help`, `/v`, `/review`, `/plan`, `/refactor`, `/as`, `/code`, `/eli5`, `/memory`, and more).
5. **Session Continuity & Source Tree Epilogues**: Turn-by-turn state tracking with standardized emoji status trees (`💾`, `⚠️`, `👻`, `📦`, `✅`, `⭕`, `🔴`) to preserve context across long-horizon sessions.

---

## 📚 How to Use

### The Core Prompt

Copy the system instruction from [`core/SYSTEM_PROMPT.md`](core/SYSTEM_PROMPT.md) into any AI chat interface — OpenAI, Anthropic Claude, Google Gemini, Cursor, Windsurf, or any local model.

This single prompt handles **everything**: general questions, research, coding, data analysis, multimodal transcription, and technical architecture.

### @Work Add-On Modules (Optional)

Append one or both to the core prompt for workplace contexts:

| Module | Use For | File |
| :--- | :--- | :--- |
| **@work** | Brand voice, word choice, email standards, PR guidelines, signature blocks | [`core/work/WORK_MODULE.md`](core/work/WORK_MODULE.md) |
| **@work.benefits** | Benefits administration — COBRA, HSA/FSA, FMLA, open enrollment, compliance | [`core/work/WORK_BENEFITS_MODULE.md`](core/work/WORK_BENEFITS_MODULE.md) |

> All legacy editions (V1 Classic, V2 Gemini REV1, specialized variants) are preserved in [`docs/legacy-editions-archive.zip`](docs/legacy-editions-archive.zip).

---

## 📁 Repository Structure

```text
.
|-- core
|   |-- SYSTEM_PROMPT.md           # ← The unified AutoExpert prompt (use this)
|   `-- work
|       |-- WORK_MODULE.md         # ← @work: brand voice, comms, PR
|       `-- WORK_BENEFITS_MODULE.md # ← @work.benefits: HR & benefits admin
|-- formats
|   |-- agent_skills               # Skill files for Antigravity, Claude Code, Open Interpreter
|   `-- system_prompts             # Portable copy of core prompt
|-- skills
|   `-- autoexpert                 # Antigravity agent skill definition
|-- docs                           # Master compendium, omnibus reference, legacy archive
|-- tests
`-- tools
    |-- autodev                    # CLI: stash, recall, preamble, lint
    |-- mcp_server                 # FastMCP server
    `-- prompt_compiler            # Multi-model prompt generator
```

---

## ⚡️ Quick Start

### 1. Verbosity Dialing Cheat Sheet

**Knowledge & Research** — prefix with `V=[1-5]`:

| Level | Mode | Depth |
| :---: | :--- | :--- |
| V=1 | Micro / Terse | Key bullet points only |
| V=2 | Concise | Executive summary |
| V=3 | Standard (default) | Balanced with trade-offs |
| V=4 | Technical Deep Dive | Edge cases, failure modes |
| V=5 | Exhaustive Academic | Multi-turn, benchmarks, proofs |

**Code & Engineering** — prefix with `V=[0-3]`:

| Level | Mode | Output |
| :---: | :--- | :--- |
| V=0 | Code Golf | Raw code, zero commentary |
| V=1 | Concise | Minimal implementation notes |
| V=2 | Simple (default) | Professional with documentation |
| V=3 | Verbose DRY | Modular, docstrings, error boundaries |

### 2. Key Engineering Mandates
- **File Path Headers**: Every code block starts with `// path/to/file.ext` or `# path/to/file.py`.
- **No-Elision Mandate**: Never `// ... rest unchanged ...`. Always complete, runnable code.
- **ISO Standards**: Dates as `YYYY-MM-DD`, currencies as ISO 4217 (`USD`), measurements in SI units.

### 3. Slash Commands at a Glance
`/help` · `/v [0-5]` · `/as [Role]` · `/review` · `/plan` · `/summary` · `/refactor` · `/q` · `/more` · `/links` · `/alt` · `/arg` · `/redo` · `/steps` · `/table` · `/code [lang]` · `/eli5` · `/memory` · `/stash` · `/recall`

---

## 🛠 Tools & Automation

### AutoDev CLI
```bash
python tools/autodev/cli.py stash auth_decision "Use JWT with RS256 rotation"
python tools/autodev/cli.py recall auth_decision
python tools/autodev/cli.py lint path/to/file.py
python tools/autodev/cli.py preamble --lang TypeScript --role "Principal Systems Architect" -v V=4
```

### Prompt Compiler
```bash
python tools/prompt_compiler/compiler.py --target claude -v 4 --specialist "Distributed Systems Architect"
```

---

## 🙏 Credits & Acknowledgments

- **Dustin Miller ([@spdustin](https://github.com/spdustin))**: Creator of the original AutoExpert framework, `autodev.py`, and the revolutionary prompt engineering methodologies that made this project possible.
- **Sean Tyler ([@seanbuilds](https://github.com/seanbuilds))**: Modernization, universal unification, and agentic skill integration.

Read the full history and attribution in [CREDITS.md](CREDITS.md).

---

## 📄 Licensing
- Prompts, documentation, and compendiums are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
- Code utilities and CLI tools are licensed under the [MIT License](LICENSE).
