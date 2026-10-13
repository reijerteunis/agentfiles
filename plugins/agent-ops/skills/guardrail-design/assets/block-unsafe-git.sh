#!/bin/sh
# PreToolUse hook for Bash: block commits that skip hooks or signing.
# Reads the event JSON on stdin; exit 2 blocks the call and shows stderr to the agent. Needs jq (macOS ships it).
cmd=$(jq -r '.tool_input.command // ""')
case "$cmd" in
  *"git commit"*--no-verify*|*"git commit"*--no-gpg-sign*|*"commit.gpgsign=false"*)
    echo "Blocked: commits must run hooks and be signed. Fix the failing check or ask the user." >&2
    exit 2 ;;
esac
exit 0
