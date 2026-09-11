# AutoExpert Framework: Master Compendium & Architecture Index


## Executive Summary

The AutoExpert framework represents a sophisticated leap in prompt engineering architecture, designed to maximize the utility and precision of Large Language Models (LLMs). Originally conceived by Dustin Miller (spdustin) as AutoExpert Custom Instructions in both Standard and Developer Editions, the architecture has undergone significant evolution.

Following its initial success, the framework was adapted into a Gemini native port to leverage Google's ecosystem. A pivotal milestone occurred with the May 2026 REV1 restructure, which optimized the system for massive context windows. Further advancements were introduced through Sean Tyler's Universal Edition, alongside various domain-specific hybrid integrations, ensuring the framework remains the gold standard for dynamic, expert-level AI interactions.


## Master Version Directory


| Version Name / Generation | Primary Environment & Models | Core Files & Storage Locations | Key Innovations & Mechanics | Compendium Link |
| --- | --- | --- | --- | --- |
| AutoExpert Standard/Dev | AutoExpert (GPT-3.5, GPT-4) | Drive: 'AutoExpert-AutoExpert' | Original Expert Persona Induction & Verbosity Dialing (V=0-3) | File |
| Gemini Native Port | Gemini 1.5 Pro | Drive: 'gemini-autoexpert-REV1' | Optimization for Gemini's reasoning patterns and native tool use | File |
| REV1 (May 2026) | Gemini 1.5 Pro / 2.0 | Drive: 'gemini-autoexpert-REV1' | Large context window optimization and enhanced state management | File |
| Universal Edition | Multi-model (GPT-4o, Gemini 2.0) | Drive: 'AutoExpert System Prompts Repository' | Cross-platform compatibility and V=1-5 Verbosity scaling | File |
| Hybrid Integrations | Domain-specific variants | Keep Notes / Drive Folders | Tailored expert induction for niche technical domains | File |



## Architectural Pillars of AutoExpert

The efficacy of the AutoExpert system relies on five foundational pillars that govern how the model interprets, processes, and executes user requests.


### Dynamic Expert Persona Induction

The system does not rely on a static personality. Instead, it dynamically self-selects specialized domain authorities based on the user's prompt. By adopting the persona of a highly specific expert, the model aligns its internal weights toward the most relevant knowledge and jargon.


### Attention Steering Preambles

Every interaction is preceded by a structured Markdown preamble. These preambles act as configuration files for the session, defining:

Language Specialist: Identifying the primary linguistic or coding requirements.

Libraries: Loading relevant conceptual or technical frameworks.

Verbosity: Setting the detail level.

Execution Plan: Outlining the immediate steps for task completion.


### Verbosity Dialing

AutoExpert allows users to control the "noise-to-signal" ratio through a numeric dial:

Developer Edition: Utilizes a scale of V=[0-3] for streamlined, technical output.

Standard & Universal Editions: Features an expanded V=[1-5] scale, ranging from terse summaries to exhaustive, multi-perspective analyses.


### Slash Command Framework

The framework introduces a standardized command taxonomy to streamline workflow and minimize repetitive prompting:

/help: Display command guide.

/review: Critically analyze current progress or code.

/summary: Provide a high-level overview of the session.

/q: Quick question mode.

/more: Expand on the previous point.

/links: Surface relevant references or documentation.

/alt: Propose alternative solutions or perspectives.

/redo: Re-execute the last step with adjusted parameters.

/memory: Access and update the session's long-term context.

/stash: Temporarily store data or code snippets.

/recall: Retrieve stashed information.

/plan: Generate a multi-step roadmap for the current task.

/refactor: Optimize existing code or text for clarity and performance.


### Epilogue & Session Continuity

To manage complex, long-running projects, AutoExpert employs an end-of-turn Epilogue. This includes:

State Management: Tracking progress against the execution plan.

Source Tree Visualization: Mapping the directory or conceptual structure.

Class/Symbol Status: Monitoring technical components in development.

Memory Serialization: Formatting session data for easy storage and retrieval in subsequent chats.


## Cross-Version Comparison Matrix


| Feature | AutoExpert Standard/Dev | Gemini REV1 | Universal Edition |
| --- | --- | --- | --- |
| Optimized Models | GPT-3.5, GPT-4 | Gemini 1.5 Pro, 2.0 | GPT-4o, Gemini 2.0, Claude |
| Context Handling | Standard Context | Ultra-Large Context | Hybrid Context Management |
| Memory Architecture | Custom Instructions based | Native File/Thread Memory | Serialized JSON/Markdown Stash |
| Tool Integration | Code Interpreter/Search | Native Google Workspace Tools | Agnostic API/Tool Support |
| Best Use Case | Individual creative/coding tasks | Complex, long-document research | Multi-platform professional workflow |



## Repository & File Index

The following sources contain the core logic, preambles, and configuration files for the various iterations of the framework.

Google Drive: 'AutoExpert-AutoExpert'

Contains the original Standard and Developer Edition .txt and .md instruction files.

Google Drive: 'gemini-autoexpert-REV1'

Hosts the May 2026 restructured instructions optimized for Gemini's architecture.

Google Drive: 'AutoExpert System Prompts Repository'

The central repository for Universal Edition files and multi-model variants.

Google Keep Notes

Source material for quick-access snippets, hybrid domain integrations, and legacy logic drafts.
