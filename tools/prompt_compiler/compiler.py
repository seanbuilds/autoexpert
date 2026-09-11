#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoExpert Prompt Compiler.
Generates tailored system instructions for ChatGPT, Gemini, Claude, and local models
with exact verbosity targets and domain specializations.
"""

import argparse
import sys

def generate_system_instruction(target: str, verbosity: int, specialist: str) -> str:
    target = target.lower()
    v_str = f"V={verbosity}"

    if target in ["gemini", "gemini-rev1"]:
        return f"""# Gemini AutoExpert System Directive
Role Authority: {specialist}
Verbosity Target: {v_str}

## Principles
1. Dynamic Role Selection: Internalize the mental models and rigor of a {specialist}.
2. Silent Refinement: Sharpen user inquiries before responding.
3. Grounding & Search: Use live search where facts or recency are relevant.
4. Epilogue State Tracking: For code or long projects, append source tree status.
"""
    elif target in ["claude", "anthropic"]:
        return f"""<autoexpert_instructions>
<role_specialist>{specialist}</role_specialist>
<verbosity>{v_str}</verbosity>
<directives>
1. Always output complete, runnable code with zero placeholder elisions.
2. Structure responses with explicit architectural reasoning.
3. Prepend responses with the Strategy & Context Table.
</directives>
</autoexpert_instructions>"""
    else:  # universal / chatgpt default
        return f"""# AutoExpert Operating Directive
Specialist Persona: {specialist}
Active Verbosity: {v_str}

Follow the AutoExpert 5-Step Execution Lifecycle:
1. Strategy & Context Table
2. Silent Question Refinement
3. Authoritative Answer Delivery with No-Elision
4. Interactive Slash Commands support (/help, /v, /review, /plan, /summary)
5. Project Epilogue with Source Tree Status
"""

def main():
    parser = argparse.ArgumentParser(description="Compile AutoExpert prompts")
    parser.add_argument("--target", choices=["universal", "gemini", "claude", "chatgpt"], default="universal", help="Target LLM architecture")
    parser.add_argument("-v", "--verbosity", type=int, choices=range(0, 6), default=3, help="Verbosity level (0-5)")
    parser.add_argument("--specialist", default="Principal Software Engineer", help="Expert domain role")

    args = parser.parse_args()
    prompt = generate_system_instruction(args.target, args.verbosity, args.specialist)
    print(prompt)

if __name__ == "__main__":
    main()
