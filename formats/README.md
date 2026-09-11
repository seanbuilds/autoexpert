# AutoExpert Instruction Formats Directory

This directory organizes AutoExpert by deployment format and target runtime interface:

```
formats/
├── custom_instructions/        # Web UI settings (OpenAI Custom Instructions, Gemini Instructions)
│   ├── gemini/                 # Pure raw text and formatted breakdown
│   ├── openai/                 # About Me & How to Respond pairs (Standard & Developer)
│   └── claude/                 # Claude Project system prompts
├── system_prompts/             # Raw & Markdown system prompts for APIs, Cursor, and frontends
│   ├── standard/               # General knowledge and reasoning engine
│   ├── developer/              # Software architecture & pair-programming engine
│   ├── research/               # Academic synthesis & evidence matrix
│   ├── enterprise/             # Enterprise dual-role governance & code
│   ├── multimodal/             # Audio/video transcription & ISO/SI standards
│   └── data_analysis/          # Statistical computation & reproducible pipelines
├── agent_skills/               # Portable agent runbooks & skill definitions
│   ├── antigravity/            # Google Antigravity SKILL.md
│   ├── claude_code/            # Claude Code / CLI integration
│   └── open_interpreter/       # Open Interpreter skill definitions
├── gems_and_projects/          # Configured profiles for Gemini Gems and Custom AI Assistants
│   ├── standard_gem/           # Daily research & knowledge work
│   ├── developer_gem/          # Whole-repo architecture & coding
│   └── research_gem/           # Systematic reviews & citations
├── userscripts_and_browser/    # Tampermonkey / Violentmonkey browser extensions
│   ├── autoexpert_userscript.js
│   └── autoExpertClassicDebugHelper.user.js
└── api_and_runtime/            # Machine-readable schemas, MCP server configs, and JSON specs
    ├── plugin_spec.json
    └── mcp_config.json
```
