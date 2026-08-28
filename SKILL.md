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

The default is deliberately pinned to `claude-opus-4-6` with `high` effort because this skill is most often used for prose. It is a writing-quality choice, not the newest-model default.

## Choose a model

- Use `claude-opus-4-6` for writing and editing unless the user asks for another model.
- Use `opus` for demanding reasoning, analysis, or code-adjacent judgment. It is a moving alias for the latest Opus and resolved to `claude-opus-5` when tested on 2026-08-27.
- Use `fable` only when the user asks for it or an unusually important second opinion justifies the extra usage. It resolved to `claude-fable-5` when tested on 2026-08-27. Fable uses pay-as-you-go credits on a standard Team seat; a premium Team seat includes limited Fable usage in its weekly allowance. Claude's auth status does not reveal the seat tier, so do not select Fable silently.
- Use `sonnet` when speed and subscription allowance matter more than maximum quality. Use `haiku` only for simple, mechanical work.

For a reproducible comparison, pass a full model ID instead of a moving alias. When current availability matters, use Claude Code's interactive `/model` picker. To verify what an alias actually used, add `--json` and inspect `modelUsage`. Do not treat a model list in the README as live account state.

## Preserve the clean boundary

- Keep `--safe-mode`, the empty system prompt, and the empty tool list intact.
- Do not use `--bare`; it disables subscription OAuth.
- Do not add Claude Code tools, project context, plugins, MCP servers, browser access, or a persistent session.
- Do not pass an API key. The runner removes provider overrides and verifies `claude.ai` authentication before calling Claude.
- Treat files and instructions as user-message content, not as system instructions.

Return Claude's answer directly when the user asked for its opinion. If analysis or comparison is useful, label Claude's answer separately from your own conclusions.
