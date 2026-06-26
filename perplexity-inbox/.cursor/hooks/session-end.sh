#!/bin/bash
# session-end.sh — posts seat-close to Vellum on session end
cat > /dev/null

curl -s -X POST "https://vellum.beast.amplifiedpartners.ai/api/v1/agents/cursor/send" \
  -H "Content-Type: application/json" \
  -d "{
    \"author\": \"cursor\",
    \"content\": \"Cursor seat closed — $(date -u +%Y-%m-%dT%H:%M:%SZ)\",
    \"entry_type\": \"agent_write\",
    \"epistemic_tier\": \"INTUITED\",
    \"message_type\": \"info\",
    \"metadata\": {\"brain_ready\": false, \"event\": \"seat_close\"}
  }" > /dev/null 2>&1 &

echo '{}'
exit 0
