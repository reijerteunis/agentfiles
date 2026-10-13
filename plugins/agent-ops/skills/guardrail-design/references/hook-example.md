# Hook example: block commits that skip checks or signing

A PreToolUse hook for the Bash tool. It blocks `git commit` with `--no-verify`, `--no-gpg-sign` or `-c commit.gpgsign=false`, and allows everything else.

## The script

Copy `assets/block-unsafe-git.sh` from this skill to `~/.claude/hooks/block-unsafe-git.sh` and make it executable. It reads the command from the event JSON and exits 2, which blocks the call, for `git commit` with `--no-verify`, `--no-gpg-sign` or `commit.gpgsign=false`.

## The settings entry

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/block-unsafe-git.sh" }]
      }
    ]
  }
}
```

## The test

```sh
echo '{"tool_input":{"command":"git commit -m x --no-verify"}}' | sh assets/block-unsafe-git.sh; echo "exit $?"   # expect 2
echo '{"tool_input":{"command":"git commit -m x"}}'             | sh assets/block-unsafe-git.sh; echo "exit $?"   # expect 0
```
