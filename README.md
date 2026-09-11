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
3. **Verbosity Dialing (V=0 to V=5)**: Explicit control over output density and detail.
4. **Standardized Slash Commands**: Intuitive commands (`/help`, `/v`, `/review`, `/plan`, `/summary`, `/refactor`, `/as`, `/q`, `/steps`, `/eli5`).
5. **Session Continuity & Source Tree Epilogues**: Turn-by-turn state tracking with standardized emoji status trees (`💾`, `⚠️`, `👻`, `✅`, `⭕️`, `🔴`) to preserve context across long-horizon sessions.

---

## 📚 The Two Editions

| Edition | Use For | Highlights | Location |
| :--- | :--- | :--- | :--- |
| **Standard** | General questions, research, analysis, multimodal | Strategy & Context Table, V=1–5 verbosity, research evidence mode, data analysis mode, multimodal transcription mode | [`core/standard/`](core/standard/) |
| **Developer** | Programming, architecture, pair-coding | Pair-Programming Preamble, No-Elision Mandate, V=0–3 code verbosity, Source Tree Epilogue | [`core/developer/`](core/developer/) |

> All legacy editions (V1 Classic, V2 Gemini REV1, specialized variants) have been consolidated into these two prompts. The originals are preserved in [`docs/pre-consolidation-archive.zip`](docs/pre-consolidation-archive.zip).

## 📁 Repository Structure
```text
.
|-- core
|   |-- standard              # ← General use (research, analysis, multimodal, Q&A)
|   `-- developer             # ← Programming (pair-coding, architecture)
|-- formats
|   |-- agent_skills          # Skill files for Antigravity, Claude Code, Open Interpreter
|   `-- system_prompts        # Portable copies of core/ prompts
|-- skills
|   `-- autoexpert            # Antigravity agent skill definition
|-- docs                      # Master compendium, omnibus reference, legacy archive
|-- tests
`-- tools
    |-- autodev               # CLI: stash, recall, preamble, lint
    |-- mcp_server            # FastMCP server
    `-- prompt_compiler       # Multi-model prompt generator
```

---

## ⚡️ Quick Start

### 1. Choose Your Prompt
Copy the system instruction from the edition that fits your use case:
- **General use** → [`core/standard/SYSTEM_PROMPT.md`](core/standard/SYSTEM_PROMPT.md) — research, analysis, writing, multimodal, Q&A
- **Programming** → [`core/developer/SYSTEM_PROMPT.md`](core/developer/SYSTEM_PROMPT.md) — coding, architecture, pair-programming

### 2. Verbosity Dialing Cheat Sheet
Prefix your queries with `V=[0-5]`:
- **V=0 (Code Golf)**: Raw code only, zero commentary or conversational padding.
- **V=1 (Terse)**: High signal-to-noise, minimal implementation notes.
- **V=2 (Concise)**: Direct answers with clean logic explanations.
- **V=3 (Balanced - Default)**: Standard professional depth with clear rationale.
- **V=4 (Comprehensive)**: Detailed technical breakdowns with edge cases.
- **V=5 (Exhaustive)**: Deep dive with multi-perspective breakdown and multi-turn staging.

### 3. Developer Mandates
- **File Path Headers**: Every code block must begin with an explicit file path comment (`# path/to/file.py`).
- **Strict No-Elision Mandate**: Never use placeholder comments like `// ... rest of code unchanged ...`. Always output complete, runnable code.

---

## 🛠 Tools & Automation

### AutoDev CLI
A modernized CLI for stashing snippets, checking standards, and generating preambles:
```bash
# Stash a snippet or decision
python tools/autodev/cli.py stash auth_decision "Use JWT with RS256 rotation"

# Recall stashed items
python tools/autodev/cli.py recall auth_decision

# Check code for No-Elision violations
python tools/autodev/cli.py lint path/to/file.py

# Generate a preamble
python tools/autodev/cli.py preamble --lang TypeScript --role "Principal Systems Architect" -v V=4
```

### Prompt Compiler
Compile tailored AutoExpert prompts for any model:
```bash
python tools/prompt_compiler/compiler.py --target claude -v 4 --specialist "Distributed Systems Architect"
```

---

## 🙏 Credits & Acknowledgments

- **Dustin Miller ([@spdustin](https://github.com/spdustin))**: Creator of the original AutoExpert framework, `autodev.py`, and the revolutionary prompt engineering methodologies that made this project possible.
- **Sean Tyler ([@seanbuilds](https://github.com/seanbuilds))**: Modernization, Gemini REV1 adaptations, Universal Edition, and Agentic skill integration.

Read the full history and attribution in [CREDITS.md](CREDITS.md).

---

## 📄 Licensing
- Prompts, documentation, and compendiums are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
- Code utilities and CLI tools are licensed under the [MIT License](LICENSE).
