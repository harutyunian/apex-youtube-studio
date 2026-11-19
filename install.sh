#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<EOF
Apex YouTube Studio Installer

Usage:
  ./install.sh --opencode               Install agents & skills globally to ~/.config/opencode/
  ./install.sh --claude                 Install agents & skills globally to ~/.claude/
  ./install.sh --all                    Install globally to BOTH OpenCode and Claude Code
  ./install.sh --project /path/to/dir   Install project-local .opencode/, .claude/, and channel templates
EOF
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

install_opencode_global() {
  local dest="$HOME/.config/opencode"
  mkdir -p "$dest/agents" "$dest/skills"
  cp -f "$REPO_DIR/agents/"*.md "$dest/agents/"
  for d in "$REPO_DIR/skills/"*; do
    local name
    name="$(basename "$d")"
    rm -rf "$dest/skills/$name"
    cp -R "$d" "$dest/skills/$name"
  done
  find "$dest/skills" -name "*.py" -exec chmod +x {} +
  echo "[OK] Installed $(ls "$REPO_DIR/agents" | wc -l | tr -d ' ') agents and $(ls "$REPO_DIR/skills" | wc -l | tr -d ' ') skills to $dest"
}

install_claude_global() {
  local dest="$HOME/.claude"
  mkdir -p "$dest/agents" "$dest/skills"
  cp -f "$REPO_DIR/agents/"*.md "$dest/agents/"
  for d in "$REPO_DIR/skills/"*; do
    local name
    name="$(basename "$d")"
    rm -rf "$dest/skills/$name"
    cp -R "$d" "$dest/skills/$name"
  done
  find "$dest/skills" -name "*.py" -exec chmod +x {} +
  echo "[OK] Installed agents and skills to $dest"
}

install_project() {
  local proj="$1"
  mkdir -p "$proj/.opencode/agents" "$proj/.opencode/skills" "$proj/.claude/agents" "$proj/.claude/skills"
  cp -f "$REPO_DIR/agents/"*.md "$proj/.opencode/agents/"
  cp -f "$REPO_DIR/agents/"*.md "$proj/.claude/agents/"
  for d in "$REPO_DIR/skills/"*; do
    local name
    name="$(basename "$d")"
    rm -rf "$proj/.opencode/skills/$name" "$proj/.claude/skills/$name"
    cp -R "$d" "$proj/.opencode/skills/$name"
    cp -R "$d" "$proj/.claude/skills/$name"
  done
  find "$proj/.opencode/skills" "$proj/.claude/skills" -name "*.py" -exec chmod +x {} +
  [[ ! -f "$proj/CHANNEL_PROFILE.md" ]] && cp "$REPO_DIR/templates/CHANNEL_PROFILE.template.md" "$proj/CHANNEL_PROFILE.md"
  [[ ! -f "$proj/AGENTS.md" ]] && cp "$REPO_DIR/templates/AGENTS.template.md" "$proj/AGENTS.md"
  [[ ! -f "$proj/CLAUDE.md" ]] && cp "$REPO_DIR/templates/CLAUDE.template.md" "$proj/CLAUDE.md"
  [[ ! -f "$proj/opencode.jsonc" ]] && cp "$REPO_DIR/templates/opencode.jsonc.template" "$proj/opencode.jsonc"
  echo "[OK] Bootstrapped project at $proj (agents, skills, CHANNEL_PROFILE.md, AGENTS.md, CLAUDE.md, opencode.jsonc)"
}

case "${1:-}" in
  --opencode)
    install_opencode_global
    ;;
  --claude)
    install_claude_global
    ;;
  --all)
    install_opencode_global
    install_claude_global
    ;;
  --project)
    if [[ -z "${2:-}" ]]; then
      echo "Error: pass target directory after --project"
      exit 1
    fi
    install_project "$2"
    ;;
  *)
    usage
    exit 1
    ;;
esac
