# claude-clean-call

A small Codex skill for asking Claude a question without bringing Claude Code's coding prompt, tools, plugins, or project context along for the ride.

It uses the local Claude CLI and your existing `claude.ai` login. It does not use an Anthropic API key. The default is deliberately pinned to `claude-opus-4-6` because this tool is most often used for writing.

This is useful for a second opinion on writing, analysis, extraction, or any other task where you want Claude the model rather than Claude Code the agent.

## Models

The useful choices are:

- `claude-opus-4-6`: the writing default
- `opus`: the latest Opus for reasoning and general judgment; verified as Opus 5 on 2026-08-27
- `fable`: the latest Fable for an occasional high-stakes second opinion; verified as Fable 5 on 2026-08-27
- `sonnet`: a faster, lighter general-purpose choice
- `haiku`: simple mechanical work

Choose a model with `--model`. Use a full model ID when a comparison needs to be reproducible. Use Claude Code's `/model` picker for the current catalog; this list is guidance, not account discovery. Fable can consume usage credits on standard Team seats.

## Install

```bash
git clone https://github.com/aburkard/claude-clean-call.git ~/.codex/skills/claude-clean-call
```

Restart Codex after installing so it discovers the skill.

## Use it directly

```bash
python3 scripts/claude_clean_call.py "Rewrite this sentence without making it sound corporate."
```

To include a document without giving Claude file tools:

```bash
python3 scripts/claude_clean_call.py \
  "Give me specific editorial feedback on this draft." \
  --input-file draft.md
```

The runner disables the normal Claude Code system prompt, all tools, project instructions, plugins, browser integration, and session persistence. It also removes API and cloud-provider overrides before verifying that Claude is authenticated through `claude.ai`.

This is the cleanest call available through a Claude subscription, but it is still transported by Claude Code. It is not the raw Anthropic Messages API.
