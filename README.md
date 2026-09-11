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

## 📚 Editions Included

| Edition | Primary Target | Highlights | Directory |
| :--- | :--- | :--- | :--- |
| **V1: AutoExpert Classic** | GPT-3.5, GPT-4 | Canonical spdustin instructions, `autodev.py`, userscripts | [`editions/v1-classic/`](editions/v1-classic/) |
| **V2: Gemini REV1** | Gemini 1.5/2.0 Pro | 1M–2M context optimization, Gems suite, Google grounding | [`editions/v2-gemini-rev1/`](editions/v2-gemini-rev1/) |
| **V3: Universal Edition** | Multi-Model (Claude, GPT-4o, Gemini) | Strategy & Context Table, model-agnostic directives | [`editions/v3-universal/`](editions/v3-universal/) |
| **Agent Skill** | Google Antigravity, Open Interpreter | Autonomous tool use and runbook workflows | [`skills/autoexpert/`](skills/autoexpert/) |

---

## ⚡️ Quick Start

### 1. Universal System Prompt
To use AutoExpert in any AI chat interface (OpenAI, Anthropic Claude, Google Gemini, Cursor, LibreChat), copy the prompt from [`editions/v3-universal/system-prompt.md`](editions/v3-universal/system-prompt.md) into your system instructions.

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
