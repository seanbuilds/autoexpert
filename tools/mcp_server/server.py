# /// script
# dependencies = [
#   "mcp[cli]>=1.0.0",
# ]
# ///

import os
import re
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    from mcp.server.fastmcp import FastMCP as MCPServer

mcp = MCPServer("autoexpert")

SESSIONS_DIR = Path.home() / ".autoexpert" / "sessions"
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

STATUS_EMOJI_MAP = {
    "saved": "💾",
    "attention": "⚠️",
    "proposed": "👻",
    "built": "📦",
    "verified": "✅",
    "stub": "⭕️",
    "bug": "🔴",
    "error": "🔴",
    "done": "✅",
    "in_progress": "⚠️"
}

STATUS_LABEL_MAP = {
    "saved": "Saved to disk",
    "attention": "Requires attention / refactoring",
    "proposed": "Proposed (not yet created)",
    "built": "Compiled / Built",
    "verified": "Tested and verified",
    "stub": "Placeholder / Stub",
    "bug": "Error / Bug identified"
}

@mcp.tool()
def generate_preamble(
    prompt: str,
    edition: Optional[str] = "developer",
    verbosity: Optional[int] = 3,
    language_specialist: Optional[str] = None,
    frameworks: Optional[List[str]] = None
) -> dict:
    """Generates an AutoExpert attention-steering preamble and strategy context table.

    Args:
        prompt: The user query or task description
        edition: AutoExpert edition: 'developer' (default), 'standard', 'gemini_rev1', 'universal', or 'research'
        verbosity: Verbosity level from 0 to 5 (default: 3)
        language_specialist: Optional language specialist persona (e.g., 'Python > Systems Architect')
        frameworks: List of libraries, frameworks, or conceptual frameworks in scope
    """
    ed = (edition or "developer").lower()
    v = max(0, min(5, verbosity if verbosity is not None else 3))
    fw = frameworks or ["Core Language Standard Library"]

    prompt_low = prompt.lower()
    if not language_specialist:
        if any(k in prompt_low for k in ["python", "django", "fastapi", "flask", "pytorch"]):
            specialist = "Python > Principal Software Architect"
        elif any(k in prompt_low for k in ["typescript", "javascript", "react", "next", "node", "vue"]):
            specialist = "TypeScript / Modern Web > Frontend & Full-App Engineer"
        elif any(k in prompt_low for k in ["swift", "macos", "ios", "appkit", "swiftui"]):
            specialist = "Apple Systems > macOS / iOS Platform Specialist"
        elif any(k in prompt_low for k in ["sql", "postgres", "database", "query"]):
            specialist = "Data Architecture > Database Reliability Engineer"
        elif any(k in prompt_low for k in ["docker", "k8s", "ci", "cd", "bash", "zsh", "linux"]):
            specialist = "DevOps & Infrastructure > Systems Automation Engineer"
        else:
            specialist = "Senior Technical Specialist & Systems Architect"
    else:
        specialist = language_specialist

    words = re.findall(r"\b[A-Za-z0-9_-]{3,}\b", prompt)
    key_terms = list(dict.fromkeys([w for w in words if len(w) > 3]))[:6] or ["implementation", "architecture"]

    plan_steps = [
        f"Deconstruct core objective: {prompt.strip()[:80]}...",
        f"Apply {specialist} domain patterns and strict error handling.",
        "Generate complete, unelided code or authoritative technical analysis.",
        "Validate against architectural boundaries and provide next milestone steps."
    ]

    strategy_table = [
        "| Strategy Dimension | Operational Directive |",
        "| :--- | :--- |",
        f"| **Specialist Persona** | {specialist} |",
        f"| **Frameworks / In Scope** | {', '.join(fw)} |",
        f"| **Verbosity Level** | V={v} |",
        f"| **Core Keywords** | {', '.join(key_terms)} |",
        f"| **Primary Execution Goal** | {prompt.strip()} |"
    ]

    if ed == "developer":
        preamble_lines = [
            "```yaml",
            f"Language > Specialist: {specialist}",
            f"Includes: {json.dumps(fw)}",
            f"Verbosity: V={v}",
            f"Requirements: [Complete implementation, No-Elision mandate, Strict file headers]",
            "Plan:",
        ] + [f"  - {s}" for s in plan_steps] + [
            "```"
        ]
    elif ed == "universal":
        preamble_lines = [
            "| Expert Persona | Verbosity | Context State |",
            "| :--- | :--- | :--- |",
            f"| {specialist} | V={v} | Active |",
            "",
            "\n".join(strategy_table)
        ]
    else:
        preamble_lines = [
            f"### AutoExpert ({ed.title()} Edition) Attention Preamble",
            "",
            "\n".join(strategy_table),
            "",
            "**Execution Roadmap**:",
        ] + [f"{i}. {s}" for i, s in enumerate(plan_steps, 1)]

    preamble_md = "\n".join(preamble_lines)

    return {
        "status": "success",
        "edition": ed,
        "specialist": specialist,
        "verbosity": v,
        "frameworks": fw,
        "keywords": key_terms,
        "plan_steps": plan_steps,
        "formatted_preamble": preamble_md,
        "strategy_table": "\n".join(strategy_table)
    }

@mcp.tool()
def generate_epilogue(
    history_summary: str,
    next_task: str,
    source_tree: Optional[Dict[str, Any]] = None,
    class_symbol_status: Optional[Dict[str, Any]] = None
) -> dict:
    """Generates an AutoExpert session continuity epilogue with source tree status emojis.

    Args:
        history_summary: Summary of actions taken in the current turn
        next_task: Immediate next priority task
        source_tree: Dictionary mapping file paths to statuses ('saved', 'attention', 'proposed', 'built', 'verified', 'stub', 'bug')
        class_symbol_status: Optional dictionary mapping key classes/functions to their completion status
    """
    tree = source_tree or {}
    symbols = class_symbol_status or {}

    tree_lines = []
    for fpath, raw_status in sorted(tree.items()):
        clean_status = str(raw_status).lower().strip()
        emoji = STATUS_EMOJI_MAP.get(clean_status, "💾" if "save" in clean_status else "⚠️")
        label = STATUS_LABEL_MAP.get(clean_status, clean_status.title())
        tree_lines.append(f"{emoji} `{fpath}` — {label}")

    symbol_lines = []
    for sym, raw_status in sorted(symbols.items()):
        clean_status = str(raw_status).lower().strip()
        emoji = STATUS_EMOJI_MAP.get(clean_status, "✅")
        symbol_lines.append(f"{emoji} `{sym}`: {raw_status}")

    epilogue_lines = [
        "---",
        "### AutoExpert Project Epilogue",
        f"**Turn Summary**: {history_summary}",
        ""
    ]

    if tree_lines:
        epilogue_lines.append("**Source Tree Status**:")
        epilogue_lines.extend(tree_lines)
        epilogue_lines.append("")

    if symbol_lines:
        epilogue_lines.append("**Component & Symbol Status**:")
        epilogue_lines.extend(symbol_lines)
        epilogue_lines.append("")

    epilogue_lines.append(f"**Next Milestone Task**: {next_task}")
    epilogue_lines.append("---")

    epilogue_md = "\n".join(epilogue_lines)

    return {
        "status": "success",
        "history_summary": history_summary,
        "next_task": next_task,
        "source_tree_count": len(tree),
        "formatted_epilogue": epilogue_md,
        "serialized_state": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "history": history_summary,
            "next_task": next_task,
            "source_tree": tree,
            "symbols": symbols
        }
    }

@mcp.tool()
def manage_session_state(
    action: str,
    project_name: str,
    state_data: Optional[Dict[str, Any]] = None
) -> dict:
    """Persists, checkpoints, loads, or lists project session state for multi-turn continuity.

    Args:
        action: Action to perform: 'save', 'load', 'list', or 'checkpoint'
        project_name: Identifier or name of the project
        state_data: State payload to store (for save/checkpoint)
    """
    act = action.lower().strip()
    safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", project_name.strip())
    state_file = SESSIONS_DIR / f"{safe_name}.json"

    if act == "list":
        sessions = []
        for p in SESSIONS_DIR.glob("*.json"):
            try:
                data = json.loads(p.read_text())
                sessions.append({
                    "project": p.stem,
                    "last_updated": data.get("last_updated", "unknown"),
                    "turn_count": len(data.get("history", [])),
                    "tracked_files": len(data.get("source_tree", {}))
                })
            except Exception:
                sessions.append({"project": p.stem, "status": "corrupted"})
        return {"status": "success", "sessions": sessions, "sessions_directory": str(SESSIONS_DIR)}

    elif act in ("save", "checkpoint"):
        current = {}
        if state_file.exists():
            try:
                current = json.loads(state_file.read_text())
            except Exception:
                current = {}

        payload = state_data or {}
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")

        history_entry = payload.get("history_summary") or payload.get("history") or "Checkpoint recorded"
        history_list = current.get("history", [])
        history_list.append({"timestamp": now_str, "entry": history_entry})

        tree = current.get("source_tree", {})
        if "source_tree" in payload:
            tree.update(payload["source_tree"])

        updated_state = {
            "project_name": safe_name,
            "last_updated": now_str,
            "active_context": payload.get("active_context", current.get("active_context", {})),
            "source_tree": tree,
            "known_bugs": payload.get("known_bugs", current.get("known_bugs", [])),
            "history": history_list[-20:],
            "next_task": payload.get("next_task", current.get("next_task", "Next task pending"))
        }

        state_file.write_text(json.dumps(updated_state, indent=2))
        return {
            "status": "success",
            "action": act,
            "project": safe_name,
            "file_path": str(state_file),
            "tracked_files": len(tree),
            "total_history_entries": len(history_list)
        }

    elif act == "load":
        if not state_file.exists():
            return {"status": "error", "message": f"No session found for project '{safe_name}'"}
        data = json.loads(state_file.read_text())
        return {"status": "success", "project": safe_name, "state": data}

    else:
        return {"status": "error", "message": f"Invalid action '{action}'. Supported: 'save', 'load', 'list', 'checkpoint'"}

@mcp.tool()
def audit_code_standards(
    code: str,
    file_path: Optional[str] = None,
    enforce_no_elision: Optional[bool] = True
) -> dict:
    """Audits code against AutoExpert Developer Edition rules (file headers, No-Elision mandate, ISO dates).

    Args:
        code: Code snippet or file content to evaluate
        file_path: Expected file path header for the code block
        enforce_no_elision: Strictly check for placeholder comments like 'rest of file remains same' (default: true)
    """
    violations = []
    lines = code.strip().splitlines()

    # 1. File path header audit
    has_header = False
    if lines:
        first_line = lines[0].strip()
        if first_line.startswith(("//", "#", "/*", "--", "<!--")) and any(c in first_line for c in ["/", ".", "\\"]):
            has_header = True
        elif file_path and file_path in first_line:
            has_header = True

    if not has_header:
        violations.append({
            "rule": "File Path Header Mandate",
            "severity": "WARNING",
            "detail": "Code block is missing an explicit file path comment header on line 1 (e.g. '// src/utils.ts' or '# app/main.py')."
        })

    # 2. No-Elision Mandate audit
    elision_patterns = [
        r"(?i)\b(?:rest\s+of\s+code\s+remains|code\s+remains\s+same|existing\s+code\s+here|remains\s+the\s+same)\b",
        r"(?i)\b(?:insert\s+here|code\s+goes\s+here|your\s+code\s+here|rest\s+of\s+file)\b",
        r"(?i)//\s*\.{3,}",
        r"(?i)#\s*\.{3,}",
        r"(?i)/\*\s*\.{3,}\s*\*/"
    ]

    elision_found = []
    if enforce_no_elision:
        for i, line in enumerate(lines, 1):
            for pat in elision_patterns:
                if re.search(pat, line):
                    elision_found.append({"line": i, "content": line.strip()})

    if elision_found:
        violations.append({
            "rule": "No-Elision Mandate",
            "severity": "CRITICAL_FAIL",
            "detail": f"Found {len(elision_found)} placeholder elision comments. Developer Edition forbids skipping code.",
            "instances": elision_found
        })

    # 3. Date format audit
    bad_date_pattern = r"\b(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/([0-9]{4})\b"
    bad_dates = []
    for i, line in enumerate(lines, 1):
        if re.search(bad_date_pattern, line):
            bad_dates.append({"line": i, "snippet": line.strip()})

    if bad_dates:
        violations.append({
            "rule": "ISO 8601 Date Formatting",
            "severity": "NOTICE",
            "detail": "Detected non-ISO date formats (MM/DD/YYYY). AutoExpert mandates YYYY-MM-DD.",
            "instances": bad_dates
        })

    passed = len([v for v in violations if v["severity"] == "CRITICAL_FAIL"]) == 0
    score = 100 - (len([v for v in violations if v["severity"] == "CRITICAL_FAIL"]) * 40 + len([v for v in violations if v["severity"] == "WARNING"]) * 20)
    score = max(0, score)

    return {
        "status": "success",
        "compliant": passed,
        "compliance_score": score,
        "violations_count": len(violations),
        "violations": violations,
        "recommendation": "Ensure 100% full unelided implementation and top file path header." if not passed else "Code adheres to AutoExpert standards."
    }

@mcp.tool()
def execute_slash_command(
    command: str,
    context: Optional[str] = None
) -> dict:
    """Processes AutoExpert slash commands (/v, /help, /review, /plan, /summary, /refactor, /as, /steps, /eli5).

    Args:
        command: The slash command string (e.g., '/v 4', '/review', '/as Distributed Systems Architect')
        context: Code, text, or task context to apply the command to
    """
    cmd_raw = command.strip()
    parts = cmd_raw.split(maxsplit=1)
    base_cmd = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else ""
    ctx = context or ""

    if base_cmd == "/help":
        return {
            "status": "success",
            "command": "/help",
            "output": """AutoExpert Slash Commands:
  • /v [0-5]: Set verbosity (V=0 raw/code golf to V=5 exhaustive analysis)
  • /review or /critique: Perform rigorous architectural and code review
  • /plan: Formulate a multi-step roadmap and architectural breakdown
  • /summary or /tldr: Produce a high-level executive summary of current progress
  • /refactor: Propose clean, DRY, and performance-oriented refactorings
  • /q: Fast question mode, minimizing conversational preamble
  • /as [Role]: Dynamically switch the persona (e.g. /as Database Architect)
  • /steps: Deconstruct process into numbered sequential actions
  • /eli5: Explain complex concepts without jargon
  • /links: Surface primary citations, official documentation, or search queries
  • /alt: Propose an alternative architectural approach or dissenting view"""
        }

    elif base_cmd == "/v":
        try:
            val = int(arg)
            val = max(0, min(5, val))
            desc = {
                0: "Code Golf / Raw Code Only (No explanations)",
                1: "Terse / Concise (Core facts and dense logic)",
                2: "Simple Default (Standard professional delivery)",
                3: "Standard Balanced / Verbose DRY (Explanatory and modular)",
                4: "Detailed & Comprehensive (Examples and edge-case coverage)",
                5: "Exhaustive Deep Dive (Multi-perspective, full documentation)"
            }.get(val, "Custom")
            return {
                "status": "success",
                "command": "/v",
                "verbosity_level": val,
                "description": desc,
                "directive": f"Operating at Verbosity V={val}: {desc}"
            }
        except Exception:
            return {"status": "error", "message": "Usage: /v [0-5]"}

    elif base_cmd in ("/review", "/critique"):
        return {
            "status": "success",
            "command": base_cmd,
            "action_required": "Perform peer-review audit",
            "review_checklist": [
                "1. Architectural Boundary Adherence: Does code cleanly decouple concerns?",
                "2. No-Elision Verification: Are all functions completely implemented without placeholders?",
                "3. Error Handling & Edge Cases: Are nil/empty inputs, network drops, or exceptions caught?",
                "4. Performance & DRY: Are repeated patterns consolidated into reusable modules?",
                "5. Type Safety & Schema: Are parameters and return values strictly typed?"
            ],
            "context_evaluated": bool(ctx)
        }

    elif base_cmd == "/plan":
        return {
            "status": "success",
            "command": "/plan",
            "action_required": "Formulate phased execution roadmap",
            "framework": [
                "Phase 1: Environment & Dependency Discovery",
                "Phase 2: Architectural Specification & Module Interfaces",
                "Phase 3: Core Implementation (Incremental & Unelided)",
                "Phase 4: Unit Verification & Boundary Testing",
                "Phase 5: Epilogue State Capture & Handoff"
            ]
        }

    elif base_cmd in ("/summary", "/tldr"):
        return {
            "status": "success",
            "command": base_cmd,
            "action_required": "Generate executive summary",
            "guideline": "Provide a high-density, 3-5 bullet point overview of accomplishments, state changes, and pending tasks."
        }

    elif base_cmd == "/as":
        if not arg:
            return {"status": "error", "message": "Usage: /as <Expert Role Title>"}
        return {
            "status": "success",
            "command": "/as",
            "adopted_persona": arg,
            "directive": f"Adopt persona: Principal {arg}. Align reasoning, vocabulary, and standards to this authority."
        }

    elif base_cmd == "/eli5":
        return {
            "status": "success",
            "command": "/eli5",
            "guideline": "Explain target concepts using simple analogies, eliminating technical jargon while preserving fundamental conceptual accuracy."
        }

    elif base_cmd == "/steps":
        return {
            "status": "success",
            "command": "/steps",
            "guideline": "Decompose instructions into atomic, sequential, numbered steps that can be verified individually."
        }

    else:
        return {
            "status": "success",
            "command": base_cmd,
            "arg": arg,
            "message": f"Executed AutoExpert command '{cmd_raw}' across context."
        }

@mcp.tool()
def get_framework_reference(topic: Optional[str] = "all") -> dict:
    """Retrieves reference guides, prompt templates, and core mechanics from the AutoExpert compendium.

    Args:
        topic: Topic to retrieve: 'all' (default), 'versions', 'pillars', 'verbosity', 'slash_commands', 'emojis', 'gems'
    """
    t = (topic or "all").lower()
    ref = {
        "origins": "Conceived by Dustin Miller (spdustin) as ChatGPT Custom Instructions (Standard & Developer); evolved into Gemini REV1 (May 2026) for large context windows, and Sean Tyler's Universal Edition.",
        "five_pillars": {
            "1_persona_induction": "Dynamically self-select specialized domain authorities per query.",
            "2_attention_preambles": "Structured Markdown/YAML headers defining language, modules, verbosity, and plan.",
            "3_verbosity_dialing": "Precision scale from V=0 (golf/terse) to V=5 (exhaustive analysis).",
            "4_slash_commands": "Standardized command taxonomy (/v, /help, /review, /plan, /summary, /refactor, /as).",
            "5_epilogue_continuity": "Turn-ending state tracking with source tree status emojis and memory serialization."
        },
        "source_tree_emojis": {
            "💾": "Saved to disk",
            "⚠️": "Requires attention or refactoring",
            "👻": "Proposed (not yet created)",
            "📦": "Compiled / Built",
            "✅": "Tested and verified",
            "⭕️": "Placeholder / Stub",
            "🔴": "Error / Bug identified"
        },
        "verbosity_scales": {
            "developer": {
                "V=0": "Code Golf (Maximum brevity, no commentary)",
                "V=1": "Concise (Minimal comments, dense implementation)",
                "V=2": "Simple Default (Standard professional style)",
                "V=3": "Verbose DRY (Explanatory comments, highly modular, Don't Repeat Yourself)"
            },
            "standard_and_universal": {
                "V=1": "Terse / direct, minimal fluff",
                "V=2": "Concise but complete",
                "V=3": "Standard balanced response",
                "V=4": "Detailed and comprehensive with examples",
                "V=5": "Exhaustive multi-turn deep dive"
            }
        },
        "gemini_gems": {
            "standard_gem": "Daily expert knowledge work with native Google Search grounding.",
            "developer_gem": "Long-horizon whole-repo architecture, strict file headers, No-Elision mandate.",
            "research_gem": "Evidence-first investigations, scholarly synthesis, source evaluation."
        }
    }

    alias_map = {
        "pillars": "five_pillars",
        "five_pillars": "five_pillars",
        "emojis": "source_tree_emojis",
        "source_tree_emojis": "source_tree_emojis",
        "verbosity": "verbosity_scales",
        "verbosity_scales": "verbosity_scales",
        "gems": "gemini_gems",
        "gemini_gems": "gemini_gems",
        "versions": "origins",
        "origins": "origins"
    }

    resolved_key = alias_map.get(t, t)

    if t == "all":
        return {"status": "success", "compendium_reference": ref}
    elif resolved_key in ref:
        return {"status": "success", resolved_key: ref[resolved_key]}
    else:
        return {"status": "success", "topic": t, "available_topics": list(alias_map.keys()) + ["all"]}

if __name__ == "__main__":
    mcp.run()
