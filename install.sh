#!/usr/bin/env bash
# agentfiles installer: wires this repo (and the private companion, if present) into the AI tools on this machine.
# Idempotent: safe to re-run after every pull.
#
#   ./install.sh            install or update
#   ./install.sh --dry-run  show what would change, change nothing
#   ./install.sh --check    verify only; exits 1 if something is off
#
# Claude skills are NOT linked here: they reach chat, Cowork and Claude Code through the plugin
# marketplace (see README). This script handles what plugins can't carry: global instructions,
# Claude settings and status line, the Codex config, and skills for every other agent.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PRIVATE="${AGENTFILES_PRIVATE:-$(dirname "$ROOT")/agentfiles-private}"
[[ -d "$PRIVATE" ]] || PRIVATE=""
MODE=install
case "${1:-}" in
  --dry-run) MODE=dry-run ;;
  --check) MODE=check ;;
  "") ;;
  *) echo "usage: $0 [--dry-run|--check]" >&2; exit 2 ;;
esac

problems=0
info()   { printf "\033[1;34m==>\033[0m \033[1m%s\033[0m\n" "$*"; }
ok()     { printf "\033[1;32m ✓\033[0m %s\n" "$*"; }
change() { printf "\033[1;36m →\033[0m %s\n" "$*"; }
warn()   { printf "\033[1;33m !\033[0m %s\n" "$*"; problems=$((problems + 1)); }
short()  { printf "%s" "${1/#$HOME/~}"; }
backup() { mv "$1" "$1.backup.$(date +%Y%m%d%H%M%S)"; change "backed up $(short "$1")"; }

# link <source> <target>: make target a symlink to source, backing up whatever was there
link() {
  local src=$1 dst=$2
  if [[ -L "$dst" && "$(readlink "$dst")" == "$src" ]]; then ok "$(short "$dst")"; return; fi
  case $MODE in
    check)   warn "$(short "$dst") is not linked to $(short "$src")" ;;
    dry-run) change "would link $(short "$dst") → $(short "$src")" ;;
    install)
      mkdir -p "$(dirname "$dst")"
      if [[ -e "$dst" || -L "$dst" ]]; then backup "$dst"; fi
      ln -s "$src" "$dst"; change "linked $(short "$dst") → $(short "$src")" ;;
  esac
}

# write_file <target> <content>: write a generated file when its content differs
write_file() {
  local dst=$1 content=$2
  if [[ -f "$dst" && ! -L "$dst" && "$(cat "$dst")" == "$content" ]]; then ok "$(short "$dst")"; return; fi
  case $MODE in
    check)   warn "$(short "$dst") is out of date" ;;
    dry-run) change "would write $(short "$dst")" ;;
    install)
      mkdir -p "$(dirname "$dst")"
      if [[ -e "$dst" || -L "$dst" ]]; then backup "$dst"; fi
      printf "%s\n" "$content" > "$dst"; change "wrote $(short "$dst")" ;;
  esac
}

# real_dir <dir>: tools write into these folders, so they must be real folders, not links into a repo
real_dir() {
  local dir=$1
  if [[ -d "$dir" && ! -L "$dir" ]]; then ok "$(short "$dir")/"; return; fi
  case $MODE in
    check)   warn "$(short "$dir") should be a real folder" ;;
    dry-run) change "would make $(short "$dir") a real folder" ;;
    install)
      if [[ -L "$dir" ]]; then
        local from; from="$(readlink "$dir")"; rm "$dir"; mkdir -p "$dir"
        if [[ -d "$from" ]]; then cp -R "$from/." "$dir/" 2>/dev/null || true; fi; rm -f "$dir/.gitkeep"
        change "$(short "$dir") is now a real folder (copied from $(short "$from"))"
      else
        mkdir -p "$dir"; change "created $(short "$dir")"
      fi ;;
  esac
}

# merge_settings: repo settings win for the keys they define, lists are unioned, and keys that only
# exist locally (plugin installs, Herdr hooks, /model) are kept. ~/.claude/settings.json stays a real
# file so Claude Code's own writes never land in a repo.
merge_settings() {
  local dst=~/.claude/settings.json existing='{}' merged
  [[ -e "$dst" ]] && existing="$(cat "$dst")"
  local layers=("$ROOT/global/claude/settings.json")
  [[ -n "$PRIVATE" && -f "$PRIVATE/global/claude/settings.json" ]] && layers+=("$PRIVATE/global/claude/settings.json")
  merged="$(printf "%s" "$existing" | jq -s -f "$ROOT/scripts/merge-settings.jq" - "${layers[@]}")"
  if [[ -f "$dst" && ! -L "$dst" ]] && [[ "$(jq -S . "$dst")" == "$(printf "%s" "$merged" | jq -S .)" ]]; then
    ok "$(short "$dst")"; return
  fi
  case $MODE in
    check)   warn "$(short "$dst") is out of date or still a symlink" ;;
    dry-run) change "would merge repo settings into $(short "$dst")" ;;
    install)
      mkdir -p ~/.claude
      if [[ -e "$dst" || -L "$dst" ]]; then backup "$dst"; fi
      printf "%s\n" "$merged" > "$dst"; change "merged repo settings into $(short "$dst")" ;;
  esac
}

# seed <source> <target>: copy once; the tool owns the file afterwards
seed() {
  local src=$1 dst=$2
  if [[ -f "$dst" ]]; then ok "$(short "$dst") (exists; edits stay local)"; return; fi
  case $MODE in
    check)   warn "$(short "$dst") is missing" ;;
    dry-run) change "would copy $(short "$src") to $(short "$dst")" ;;
    install) mkdir -p "$(dirname "$dst")"; cp "$src" "$dst"; change "copied $(short "$src") to $(short "$dst")" ;;
  esac
}

# Every skill in this repo and the private companion
skills() {
  local repo
  for repo in "$ROOT" ${PRIVATE:+"$PRIVATE"}; do
    find "$repo/plugins" -mindepth 3 -maxdepth 3 -type d -path '*/skills/*' 2>/dev/null
  done | sort
}

# Tools that read one global instruction file: "name|target". Only tools that are installed get a link.
instruction_targets() {
  has() { command -v "$1" >/dev/null 2>&1; }
  { has codex || [[ -d ~/.codex ]]; }                          && echo "Codex|$HOME/.codex/AGENTS.md"
  { [[ -d /Applications/Zed.app ]] || [[ -d ~/.config/zed ]]; } && echo "Zed|$HOME/.config/zed/AGENTS.md"
  has opencode                                                 && echo "OpenCode|$HOME/.config/opencode/AGENTS.md"
  has amp                                                      && echo "Amp|$HOME/.config/amp/AGENTS.md"
  has goose                                                    && echo "Goose|$HOME/.config/goose/AGENTS.md"
  has copilot                                                  && echo "Copilot|$HOME/.copilot/copilot-instructions.md"
  { has gemini || has agy; }                                   && echo "Gemini|$HOME/.gemini/GEMINI.md"
  return 0
}

command -v jq >/dev/null || { echo "jq is required (brew install jq)" >&2; exit 1; }
info "agentfiles · $MODE · $(short "$ROOT")${PRIVATE:+ + $(short "$PRIVATE")}"

info "Claude Code"
# Inlined, not imported or symlinked: Cowork skips a symlinked ~/.claude/CLAUDE.md and @imports that point
# outside the session's folder. After editing global/AGENTS.md, re-run ./install.sh (--check flags drift).
claude_md="<!-- Generated by agentfiles/install.sh from global/AGENTS.md. Edit that file and re-run the installer. -->
$(cat "$ROOT/global/AGENTS.md")"
private_md=false
[[ -n "$PRIVATE" && -f "$PRIVATE/global/AGENTS.md" ]] && private_md=true
$private_md && claude_md+="

$(cat "$PRIVATE/global/AGENTS.md")"
write_file ~/.claude/CLAUDE.md "$claude_md"
merge_settings
link "$ROOT/global/claude/statusline.sh" ~/.claude/statusline.sh
for d in skills agents commands hooks; do real_dir ~/.claude/$d; done

info "Global instructions for other agents"
# A link keeps them current, but can't include the private companion's lines; with those, they get Claude's copy.
while IFS='|' read -r tool target; do
  [[ -z "$tool" ]] && continue
  if $private_md; then write_file "$target" "$claude_md"; else link "$ROOT/global/AGENTS.md" "$target"; fi
done < <(instruction_targets)

info "Codex"
seed "$ROOT/global/codex/config.toml" ~/.codex/config.toml

info "Skills for every agent except Claude (~/.agents/skills)"
while read -r dir; do
  [[ -n "$dir" ]] && link "$dir" "$HOME/.agents/skills/$(basename "$dir")"
done < <(skills)
# Remove links to skills that were renamed or deleted in the repos
for l in ~/.agents/skills/*; do
  [[ -L "$l" && ! -e "$l" ]] || continue
  case "$(readlink "$l")" in "$ROOT"/*|"${PRIVATE:-/nonexistent}"/*) ;; *) continue ;; esac
  case $MODE in
    install) rm "$l"; change "removed stale $(short "$l")" ;;
    *) warn "stale link $(short "$l")" ;;
  esac
done

echo
if [[ $MODE == check ]]; then
  if ((problems == 0)); then
    ok "agentfiles is fully installed"
  else
    warn "run ./install.sh to fix the $problems item(s) above"; exit 1
  fi
else
  cat <<EOF
Claude skills come from the plugin marketplaces. Add them once in claude.ai, and they sync to chat,
Cowork and Claude Code on every machine you sign in to:
  claude.ai › Customize › Plugins › Add marketplace › reijerteunis/agentfiles
EOF
  [[ -n "$PRIVATE" ]] && echo "  …and the private one: reijerteunis/agentfiles-private (needs the Claude GitHub App to have access)"
fi
