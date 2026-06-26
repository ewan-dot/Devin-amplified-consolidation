#!/usr/bin/env bash
# beforeSubmitPrompt — cheap secret-pattern check (no LLM)
set -euo pipefail
INPUT=$(cat)

PROMPT=""
if command -v jq >/dev/null 2>&1; then
  PROMPT=$(echo "$INPUT" | jq -r '.prompt // .text // empty' 2>/dev/null || true)
else
  PROMPT="$INPUT"
fi

if [[ -z "$PROMPT" ]]; then
  echo '{}'
  exit 0
fi

# Obvious secret shapes — deny before they enter context
if echo "$PROMPT" | grep -qE 'sk-[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[0-9A-Za-z-]{10,}|-----BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY-----'; then
  echo '{"user_message":"Possible secret in prompt — remove before submitting.","agent_message":"beforeSubmitPrompt: secret pattern detected."}'
  exit 2
fi

# Soft nudge for token-heavy narrative (policy in token-efficiency rule)
if [[ ${#PROMPT} -gt 1200 ]] && ! echo "$PROMPT" | grep -q $'\n'; then
  echo '{"additional_context":"[prompt-lint] Long single-line prompt — consider structured fields (File:/Bug:/Action:) per token-efficiency rule."}'
  exit 0
fi

echo '{}'
exit 0
