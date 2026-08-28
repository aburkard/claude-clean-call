#!/usr/bin/env python3
"""Make a tool-free Claude call through an existing claude.ai login."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


PROVIDER_OVERRIDES = {
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_USE_ANTHROPIC_AWS",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_FOUNDRY",
    "CLAUDE_CODE_USE_VERTEX",
}


def subscription_environment() -> dict[str, str]:
    env = os.environ.copy()
    for name in PROVIDER_OVERRIDES:
        env.pop(name, None)
    return env


def claude_executable() -> str:
    executable = shutil.which("claude")
    if not executable:
        raise SystemExit("claude is not installed or is not on PATH")
    return executable


def require_subscription_auth(executable: str, env: dict[str, str]) -> None:
    result = subprocess.run(
        [executable, "auth", "status"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        raise SystemExit("Claude authentication is unavailable. Run `claude auth login`.")

    try:
        status = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit("Could not read `claude auth status` output") from error

    if not status.get("loggedIn") or status.get("authMethod") != "claude.ai":
        raise SystemExit(
            "Claude is not using a claude.ai subscription. Run `claude auth login` "
            "and select the intended subscription."
        )


def read_utf8(path: Path, label: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise SystemExit(f"Could not read {label} {path}: {error}") from error


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt and args.prompt_file:
        raise SystemExit("Use either a prompt argument or --prompt-file, not both")

    if args.prompt_file:
        prompt = read_utf8(args.prompt_file, "prompt file")
    elif args.prompt:
        prompt = args.prompt
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read()
    else:
        raise SystemExit("Provide a prompt, --prompt-file, or stdin")

    if not prompt.strip():
        raise SystemExit("Prompt cannot be empty")

    for input_file in args.input_file:
        content = read_utf8(input_file, "input file")
        prompt += (
            f"\n\n<document name={json.dumps(input_file.name)}>\n"
            f"{content}\n"
            "</document>"
        )
    return prompt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Call Claude without the Claude Code system prompt or tools."
    )
    parser.add_argument("prompt", nargs="?", help="The user prompt")
    parser.add_argument("--prompt-file", type=Path, help="Read the prompt from a UTF-8 file")
    parser.add_argument(
        "--input-file",
        action="append",
        default=[],
        type=Path,
        help="Append a UTF-8 document to the user message; repeat as needed",
    )
    parser.add_argument("--model", default="claude-opus-4-6")
    parser.add_argument(
        "--effort",
        choices=("low", "medium", "high", "xhigh", "max"),
        default="high",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Return Claude Code's JSON result envelope",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prompt = read_prompt(args)
    env = subscription_environment()
    executable = claude_executable()
    require_subscription_auth(executable, env)

    command = [
        executable,
        "--print",
        "--model",
        args.model,
        "--effort",
        args.effort,
        "--safe-mode",
        "--system-prompt",
        "",
        "--tools",
        "",
        "--no-chrome",
        "--no-session-persistence",
        "--output-format",
        "json" if args.json else "text",
    ]
    return subprocess.run(command, input=prompt, text=True, env=env, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
