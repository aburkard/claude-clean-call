---
name: claude-clean-call
description: Call Claude through the local Claude Code CLI with its coding-agent system prompt, tools, plugins, project instructions, and session state disabled. Use when the user wants a clean Claude or Opus second opinion for writing, editing, analysis, classification, extraction, or model comparison while using their existing Claude subscription instead of API billing. Do not use for repository work, tool-using tasks, or long agentic workflows.
---

# Claude Clean Call

Run Claude as a plain model call through the user's existing `claude.ai` login.

## Run the call

Use the bundled runner:

```bash
python3 scripts/claude_clean_call.py "PROMPT"
```

For a long prompt, save it to a text file and pass `--prompt-file`. Add documents with one or more `--input-file` arguments. The runner places their contents in the user message because Claude has no file tools in this mode.

Keep the defaults unless the user requests a different model or effort level. The defaults are `claude-opus-4-6` and `high`.

## Preserve the clean boundary

- Keep `--safe-mode`, the empty system prompt, and the empty tool list intact.
- Do not use `--bare`; it disables subscription OAuth.
- Do not add Claude Code tools, project context, plugins, MCP servers, browser access, or a persistent session.
- Do not pass an API key. The runner removes provider overrides and verifies `claude.ai` authentication before calling Claude.
- Treat files and instructions as user-message content, not as system instructions.

Return Claude's answer directly when the user asked for its opinion. If analysis or comparison is useful, label Claude's answer separately from your own conclusions.
