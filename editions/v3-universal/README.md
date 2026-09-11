# AutoExpert Version 3: Universal Edition & Custom Hybrid Implementations


## Overview

This technical specification details Sean Tyler's adaptations and extensions of the AutoExpert architecture. The Version 3 framework is designed for multi-model deployments across OpenAI ChatGPT, Anthropic Claude, Google Gemini, and Meta Llama. It integrates specialized enterprise roles and modular prompt components optimized for mobile and desktop environments, including Google Keep prompt modules.


## AutoExpert 1.0 - Universal Edition System Prompt

The Universal Edition provides a standardized architectural directive for large language models to ensure consistent, expert-level performance.


### Five-Step Execution Lifecycle

Each interaction follows a rigid five-step structural sequence:

Strategy & Context Table: Every response must begin with a markdown table summarizing the operational context.


| Category | Description |
| --- | --- |
| Experts | The specific personas adopted for the response. |
| Keywords | Critical technical terms and domain concepts. |
| Question | A restatement of the user's core intent. |
| Plan | A step-by-step methodology for the current response. |


Multi-Turn Continuation: Indicators for long-form content that requires multiple messages to complete, ensuring state management across turns.

Authoritative Answer Delivery: The primary technical content, utilizing Google Search query hyperlinking for real-time verification and deep-linking of technical concepts.

Follow-Up Resources: A curated list of suggested next steps, documentation, or related areas of inquiry.


### Verbosity Scale (V=1 to V=5)

The system adjusts the depth of detail based on the following scale:

V=1: Concise, summary-focused responses.

V=5: Comprehensive, deep-dive technical analysis with exhaustive detail.


### Slash Commands Reference


| Command | Function |
| --- | --- |
| /v [1-5] | Sets the verbosity level for the current session. |
| /redo | Re-evaluates the previous prompt with a different expert persona. |
| /as [Expert] | Forces the AI to adopt a specific persona. |
| /critique | Reviews the previous output for technical inaccuracies or logical gaps. |
| /tldr | Provides a high-level summary of the preceding content. |
| /expand | Elaborates on the last specific point mentioned. |
| /code | Switches priority to code generation and technical documentation. |
| /table | Formats the relevant data into a structured markdown table. |
| /steps | Breaks the process down into a sequential, numbered list. |
| /eli5 | Explains complex concepts using simplified language for non-experts. |



## AutoExpert v2 — Enterprise Dual-Role Integration

This version features a hybrid implementation specifically designed for the CareQuest Benefits Manager & Technical Developer dual-persona.


### Dual-Persona Mechanics

The architecture reconciles two distinct domains into a single functional stream:

Benefits Management Protocols: Specialized workflows for managing employee leave, HSA funding, COBRA administration, and vendor invoice reconciliation.

Technical Development Integration: A layer of AutoExpert technical development preambles and epilogues that wrap around benefit tasks to ensure code-level accuracy for any associated data processing or automation scripts.


### Integration Mode

This mode enables the model to transition between administrative domain expertise and technical code generation without losing context, using specialized preambles to set the policy context and epilogues to define technical next steps.


## Auto-Expert Custom Instructions (Gems Advanced Edition)

Optimized for Google Gemini Advanced and the "Gems" deployment system:

Native Tool Awareness: Explicit instructions to utilize built-in Google tools (Search, Workspace, Code Interpreter) as primary data sources.

Persistent Multi-Turn Memory: Directives for maintaining state across long sessions, ensuring specific user preferences and previous session data are weighted heavily in the reasoning process.


## Google Keep Modular Prompt Components & Standards

Designed for modular usage and mobile-first prompt engineering.


### Audio & Multimodal Transcription Rules

Diarization: Identification of different speakers in audio inputs.

60-Second Timestamps: Rigid insertion of timestamps every minute.

Zero Placeholders: Forbids the use of generic markers; the model must interpret or transcribe exactly what is heard or seen.


### Data Formatting Engine

ISO 8601: All dates must follow the YYYY-MM-DD format.

SI Units: Strict adherence to the International System of Units for all technical and scientific measurements.


### Adaptive AI Research Partner Metadata

Responses using research modules begin with this specific header:| Expert Persona | Verbosity | Context State || :--- | :--- | :--- || Person | V=[1-5] | [Active/Idle/Continuing] |


## Cross-Model Synthesis

The deployment of Universal AutoExpert varies slightly across model providers to account for varying context windows and safety guardrails:


| Feature | OpenAI (GPT) | Anthropic (Claude) | Google (Gemini) |
| --- | --- | --- | --- |
| Logic Density | High | Extreme | Balanced |
| Tool Integration | Function Calling | XML Tags | Native Extensions |
| Memory Handling | System Fingerprint | Long Context Window | Persistent Gems |
| System Directives | Strict Following | Constitutional Alignment | Tool-First Priority |

