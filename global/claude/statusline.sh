#!/usr/bin/env bash
# Claude Code status line:  Opus 5.5 · dotfiles (main) · ctx 34% · 5h 61% · 7d 22%
# Reads the session JSON on stdin — field reference: https://code.claude.com/docs/en/statusline
IFS=$'\t' read -r model dir ctx five week <<<"$(jq -r '[
  .model.display_name // "?",
  (.workspace.current_dir // .cwd // ""),
  ((.context_window.used_percentage // -1) | floor),
  ((.rate_limits.five_hour.used_percentage // -1) | floor),
  ((.rate_limits.seven_day.used_percentage // -1) | floor)
] | @tsv')"

branch=$(git --no-optional-locks -C "$dir" branch --show-current 2>/dev/null)

pct() {  # pct <label> <value>: green < 50% < yellow < 80% < red; skipped when unknown
  local label=$1 v=$2 c=32
  ((v < 0)) && return
  ((v >= 50)) && c=33
  ((v >= 80)) && c=31
  printf ' · %s \033[%sm%s%%\033[0m' "$label" "$c" "$v"
}

printf '\033[1m%s\033[0m · %s' "$model" "${dir##*/}"
[[ -n $branch ]] && printf ' \033[36m(%s)\033[0m' "$branch"
pct ctx "$ctx"
pct 5h "$five"
pct 7d "$week"
