#!/bin/bash
set -e
DEST="$HOME/amplified-corpus-clean"
SRC="/Users/ewansair/ingestion-to-research-pipe/_dedup-apply-quarantine"
mkdir -p "$DEST"
mkdir -p "$DEST/01-doctrine"
mkdir -p "$DEST/02-methodology"
mkdir -p "$DEST/04-product"
mkdir -p "$DEST/05-engineering-infra"
mkdir -p "$DEST/06-agents-orchestration"
mkdir -p "$DEST/07-research"
mkdir -p "$DEST/08-content-marketing"
mkdir -p "$DEST/09-transcripts-voice"
mkdir -p "$DEST/99-unsorted"
mkdir -p "$DEST/_archive/agents-orchestration"
mkdir -p "$DEST/_archive/content-marketing"
mkdir -p "$DEST/_archive/doctrine"
mkdir -p "$DEST/_archive/engineering-infra"
mkdir -p "$DEST/_archive/math-logic"
mkdir -p "$DEST/_archive/methodology"
mkdir -p "$DEST/_archive/ops-sessions"
mkdir -p "$DEST/_archive/research"
cat > "$DEST/README.md" <<'EOF'
# Amplified Partners — Clean Corpus

Sorted by department. CURRENT work is visible in numbered folders; superseded versions and operational churn are in `_archive/` so agents are not distracted by stale data.

Naming: canonical files keep their descriptive name; where a file was renamed, the prior name is preserved in (brackets) so search still finds it.

Departments: 01-doctrine, 02-methodology, 03-math-logic, 04-product, 05-engineering-infra, 06-agents-orchestration, 07-research, 08-content-marketing, 09-transcripts-voice. Bloat: _archive/.
EOF
cat > "$DEST/01-doctrine/README.md" <<'EOF'
# 01-doctrine

The law of Amplified Partners: the 5 rods, commitments, Ulysses clause, manifestos, constitution. Identity/dignity/legal-status material lives here and is NOT settled — treat as for-now doctrine.
EOF
cat > "$DEST/02-methodology/README.md" <<'EOF'
# 02-methodology

How we work: Pudding technique, ABC bridge (Swanson 1986), min-rule epistemics, validation methodology, the canonical phrase index, the taxonomy & nomenclature standard.
EOF
cat > "$DEST/04-product/README.md" <<'EOF'
# 04-product

What we sell: Covered AI (tradespeople + HGV), Dave's voice-booking workflow, pricing, go-to-market. Dave = first real customer (Jesmond Plumbing); Bob = persona.
EOF
cat > "$DEST/05-engineering-infra/README.md" <<'EOF'
# 05-engineering-infra

The substrate: architecture, Redis/Qdrant/FastEmbed, Retell (chosen over VAPI), deployment, hub-and-spoke infra.
EOF
cat > "$DEST/06-agents-orchestration/README.md" <<'EOF'
# 06-agents-orchestration

The partners and how they coordinate: Sam/Clawd (Claude in different jobs), Grok (xAI), multi-agent orchestration, OpenClaw harness.
EOF
cat > "$DEST/07-research/README.md" <<'EOF'
# 07-research

Deep-research reports and comparisons (primary-source backed where cited).
EOF
cat > "$DEST/08-content-marketing/README.md" <<'EOF'
# 08-content-marketing

Substack/LinkedIn/Twitter content, Gary Vee workflow, content calendars. Eli is the INDEPENDENT author — his work is his own, not Amplified's.
EOF
cat > "$DEST/09-transcripts-voice/README.md" <<'EOF'
# 09-transcripts-voice

RAW SOURCE. Voice memos & transcripts (Monologue/Whisper). This is feedstock for the Pipe, not finished work — agents should treat as primary material, not conclusions.
EOF
cat > "$DEST/99-unsorted/README.md" <<'EOF'
# 99-unsorted

Files that did not classify cleanly. Review and re-home.
EOF
cat > "$DEST/_archive/agents-orchestration/README.md" <<'EOF'
# _archive/agents-orchestration

Archived agents-orchestration: superseded versions / older copies. Kept for history, not active use. The current version is in the matching numbered department folder.
EOF
cat > "$DEST/_archive/content-marketing/README.md" <<'EOF'
# _archive/content-marketing

Archived content-marketing: superseded versions / older copies. Kept for history, not active use. The current version is in the matching numbered department folder.
EOF
cat > "$DEST/_archive/doctrine/README.md" <<'EOF'
# _archive/doctrine

Archived doctrine: superseded versions / older copies. Kept for history, not active use. The current version is in the matching numbered department folder.
EOF
cat > "$DEST/_archive/engineering-infra/README.md" <<'EOF'
# _archive/engineering-infra

Archived engineering-infra: superseded versions / older copies. Kept for history, not active use. The current version is in the matching numbered department folder.
EOF
cat > "$DEST/_archive/math-logic/README.md" <<'EOF'
# _archive/math-logic

Archived math-logic: superseded versions / older copies. Kept for history, not active use. The current version is in the matching numbered department folder.
EOF
cat > "$DEST/_archive/methodology/README.md" <<'EOF'
# _archive/methodology

Archived methodology: superseded versions / older copies. Kept for history, not active use. The current version is in the matching numbered department folder.
EOF
cat > "$DEST/_archive/ops-sessions/README.md" <<'EOF'
# _archive/ops-sessions

Archived operational churn: vault-monitor runs, shared-board versions, session reviews. History only.
EOF
cat > "$DEST/_archive/research/README.md" <<'EOF'
# _archive/research

Archived research: superseded versions / older copies. Kept for history, not active use. The current version is in the matching numbered department folder.
EOF
cp -p "$SRC/clean-build/01_truth/schemas/2026-03_validation-methodology_v2.md" "$DEST/02-methodology/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r60.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r32.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r39.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r30.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r29.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r90.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r48.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r134.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r3.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r135.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r48.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r94.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r39.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r33.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r89.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r18.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r63.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r101.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r23.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r94.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r52.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r24.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r31.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r82.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r58.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r42.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r37.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r25.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r77.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r49.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r63.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r51.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r60.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r89.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r75.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r78.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r77.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r58.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r17.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r25.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r91.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r35.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r96.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r34.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r44.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r93.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r51.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r54.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r84.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r81.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r40.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r57.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r16.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r16.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r92.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r94.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r11.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r56.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r82.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r83.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r75.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r45.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r35.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r38.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r32.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r84.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r105.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r80.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r46.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r133.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r137.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r31.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r64.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r148.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r52.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-22-r97.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r65.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r53.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-24-r85.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-23-r64.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r59.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-21-r47.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r88.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-25-r17.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/clean-build/90_archive/vault-monitor-runs/vault-monitor-2026-03-20-r13.md" "$DEST/_archive/ops-sessions/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_staging/12-archive-raw/checklist-week-20260113-v1.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_staging/03-sales-marketing/bdb-weekly-blog-system-v1.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_staging/03-sales-marketing/bdb-website-recipe-v1.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_staging/05-technology/audit-phase1-technical-discovery-v1.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/amplified-partners-overview-feb-2026.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/rubric/README.md" "$DEST/02-methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-2026-02-23-1408.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-2026-02-23-0327.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-test-20260214-145805.md" "$DEST/99-unsorted/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-SUMMARY-2026-02-11-v2.md" "$DEST/02-methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-2026-02-12-RAW-CONVERSATION.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-2026-02-22-RESEARCH-COMPLETE.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-2026-02-25-0600.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-2026-02-16-LANDING-PAGES-LIVE.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-2026-02-21-1415.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/SESSION-SUMMARY-2026-02-11.md" "$DEST/02-methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/gates/AI-REVIEW-REQUEST.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/gates/API-TOKENS-TO-COLLECT.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/gates/COMMITMENT-SYSTEM-REVIEW.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/gates/COMMITMENT-SYSTEM-README.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work/sessions/gates/content-draft-001-linkedin-ai-what-is-it.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/PUBLISHING-SEQUENCE-v2.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v10.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v10.md" "$DEST/_archive/methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v25.md" "$DEST/_archive/research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SOUL-v2.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/TRANSCRIPT-DISCOVERY-FINAL-v2.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/sam-2026-02-12-0220-v2.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/ZAPIER-SEO-STRATEGY-HYPERLOCAL.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/DAVE-AGENT-CREATED.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/DEEP-RESEARCH-OPENCLAW-SUCCESS-STORIES.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/THE-PLAN-v2.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SEO-IMPLEMENTATION-GUIDE-v2.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/sam-2026-02-12-0220.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/AI-REVIEW-REQUEST-v3.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SEO-LANDING-PAGE-FACTORY.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/AGENTS.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v15.md" "$DEST/_archive/methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/LANDING-PAGE-KEYWORD-MATRIX-v2.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/jaunty-kindling-shore-v2.md" "$DEST/_archive/content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v30.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v29.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/content-calendar-2026-02.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/CLAWD-FULL-CAPABILITY-BUILD.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v22.md" "$DEST/_archive/research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/openclaw-skills-security-research-report.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v13.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/PUDDING-RESULTS-INITIAL.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v8.md" "$DEST/_archive/engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/AI-REVIEW-REQUEST-v2.md" "$DEST/_archive/doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/TESTING-PERSONAS-DETAILED.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/REVIEW-v2.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/cuddly-munching-popcorn.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v23.md" "$DEST/_archive/research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/AI-REVIEW-REQUEST.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/PUBLISHING-SEQUENCE.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/jaunty-kindling-shore-v3.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/voice-ai-platform-comparison-2026.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/logical-percolating-swan.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v5.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/COVERED-AI-VOICE-PLATFORM.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v7.md" "$DEST/_archive/engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/sam-2026-02-22-0628.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/ROOM-INFRASTRUCTURE.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/2026-02-19.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/DEPLOY-BLOCKERS.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/HUMAN-COLLABORATION-PATTERNS-RESEARCH.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v13.md" "$DEST/_archive/methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SEO-IMPLEMENTATION-GUIDE.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/ZAPIER-SEO-STRATEGY-HYPERLOCAL-v2.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/TRANSCRIPTION-SOURCES-FOUND.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/API-TOKENS-TO-COLLECT.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/COORDINATION-PLAN-TODAY-v2.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/AGENTS-v2.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/MANIFEST.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/jaunty-kindling-shore.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/TRANSCRIPTION-SOURCES-FOUND-v2.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/PERSONA-TECH-STACKS.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v12.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/TRANSCRIPT-DISCOVERY-FINAL.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/REVIEW.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/content-calendar-2026-02-v2.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v8.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v29.md" "$DEST/_archive/engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SAM-TODO.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/GATE-TEMPLATE.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/2026-02-19-session.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/TODAY-ALPHA-READY-TASKS.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/DAVE-WORKFLOW-SPEC-V1.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/THE-COMPLETE-PICTURE-2026-02-16.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/registered-letter-template-v1-v3.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/AGENTS-v3.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v14.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SEO-LANDING-PAGE-FACTORY-v2.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v15.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/OPENCLAW-ADVANCED-USERS-RESEARCH.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/MATTHEW-BERMAN-DEEP-RESEARCH.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v28.md" "$DEST/_archive/engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v11.md" "$DEST/_archive/methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/COMMITMENT-SYSTEM-REVIEW.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/OPERATIONS-AUTOMATION-SUMMARY.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/LANDING-PAGE-KEYWORD-MATRIX.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/sam-2026-02-11-2052.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/PRODUCT-SPEC-COVERED-AI-HGV-v2.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v6.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/TASK-PROJECT-MANAGEMENT-RESEARCH.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/VOICE-SYSTEM-ACTIVATION.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/QUICK-START-GUIDE.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/THE-PLAN.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v4.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/PUBLISHING-TONE-GUIDE.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/PUDDING-TECHNIQUE-EXTRACTION.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/CLAWD-CAPABILITY-SPEC-NOT-BUILT.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/sam-2026-02-11-2052-v2.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v11.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/COMPLETE-TRANSCRIPT-INVENTORY.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/clawd-reflection-template.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/MATTHEW-BERMAN-26-PROMPTS.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/TODOIST-SETUP-v2.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v9.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SAM-CAPABILITY-SPEC-NOT-BUILT.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v17.md" "$DEST/_archive/research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/TODOIST-SETUP.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/staged-sprouting-sifakis.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/recent-sessions-v6.md" "$DEST/_archive/math-logic/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/sam-reflection-template.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/VAPI-VS-RETELL-DEEP-RESEARCH-2026.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/IDENTITY.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/RETELL-AI-SETUP-GUIDE.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/COORDINATION-PLAN-TODAY.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/abundant-growing-emerson-v2.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/COMPLETE-TRANSCRIPT-INVENTORY-v2.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/SHARED-BOARD-v3.md" "$DEST/_archive/agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/content/content-draft-002-linkedin-play-doh-barbershop.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/content/content-draft-001-linkedin-ai-what-is-it-v2.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/content/content-draft-002-linkedin-play-doh-barbershop-v2.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/content/content-draft-001-linkedin-ai-what-is-it.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox/content/content-draft-004-linkedin-silicone-friction.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0038.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0025.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0019.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0048.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0016.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0022.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0020.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0001.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0029.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0015.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0036.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0027.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0002.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0023.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0014.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0011.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0024.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0049.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0004.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0033.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0028.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0047.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0043.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0041.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0042.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0007.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue/monologue-unknown-0034.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0468-0468.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1997-1997.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2011-2011.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1513-1513.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1565-1565.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0445-0445.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1530-1530.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1885-1885.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1522-1522.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1787-1787.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2022-2022.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1834-1834.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0599-0599.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1870-1870.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1788-1788.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1826-1826.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0756-0756.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1835-1835.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1786-1786.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1681-1681.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1858-1858.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1995-1995.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1506-1506.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1719-1719.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0038-0038.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2012-2012.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0066-0066.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2118-2118.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1686-1686.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2028-2028.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1903-1903.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1527-1527.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0167-0167.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2131-2131.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1833-1833.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1794-1794.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1807-1807.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0679-0679.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1933-1933.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1989-1989.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2005-2005.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1507-1507.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0245-0245.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1830-1830.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0766-0766.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0459-0459.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0400-0400.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1526-1526.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1849-1849.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2135-2135.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1843-1843.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1087-1087.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1653-1653.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0607-0607.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0248-0248.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1825-1825.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2138-2138.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2017-2017.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0757-0757.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1573-1573.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1516-1516.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1993-1993.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1976-1976.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1994-1994.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1694-1694.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1651-1651.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1717-1717.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1848-1848.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-0583-0583.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1999-1999.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1638-1638.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2004-2004.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-2130-2130.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1536-1536.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/transcripts/monologue-full/monologue-unknown-1705-1705.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/INDEX.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/AGENTS.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/content-calendar-2026-02.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/MANIFEST.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/GATE-TEMPLATE.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/clawd-2026-02-12-0220.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/THE-PLAN.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/clawd-2026-02-11-2052.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/CLAWD-TODO.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/content-draft-004-linkedin-silicone-friction.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/imported-business-docs/openclaw-workspace/SESSION-SUMMARY-2026-02-11.md" "$DEST/02-methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/projects/roadmaps/social-media-automation-roadmap.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-voice-ai-platform-comparison-2026.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-delegated-giggling-trinket.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-humming-moseying-acorn.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-openclaw-skills-security-research-report.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-binary-humming-tide.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-majestic-cuddling-yeti.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-vivid-herding-meteor.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-hazy-conjuring-prism-6a1dcd.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-session-2026-02-16-landing-pages-live.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-session-summary-2026-02-11.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-scalable-jumping-nest.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-covered-ai-voice-platform.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-nested-stirring-hanrahan.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-mutable-knitting-hopcroft.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-curious-humming-pnueli.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-piped-purring-cloud.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-imperative-watching-wozniak.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-replicated-exploring-planet.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-idempotent-beaming-biscuit.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-deep-research-openclaw-success-stories.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-vapi-vs-retell-deep-research-2026.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-linear-wibbling-dawn.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-human-collaboration-patterns-research.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-dreamy-napping-stardust.md" "$DEST/02-methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-dave-workflow-spec-v1.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/amplified-taxonomy-and-nomenclature-standard_2026-06-24T0906Z_perplexity.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-logical-stirring-turtle.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-zapier-seo-strategy-hyperlocal.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-eager-plotting-petal.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-dreamy-dazzling-octopus.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-session-2026-02-22-research-complete.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-majestic-whistling-sedgewick.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-openclaw-advanced-users-research.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-quiet-puzzling-lightning.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-jiggly-singing-scott.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-content-draft-001-linkedin-first-post.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-enumerated-napping-mango.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-matthew-berman-deep-research.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-rippling-wobbling-elephant-1.md" "$DEST/08-content-marketing/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-nested-stirring-hanrahan-agent-a4bdfd2.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-dynamic-popping-puddle.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/amplified-canonical-phrase-index_2026-06-24T0850Z_perplexity.md" "$DEST/01-doctrine/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-partitioned-hatching-tarjan.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-session-notes-2026-02-11.md" "$DEST/02-methodology/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-valiant-churning-moon.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-streamed-humming-rain.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-cozy-sniffing-crayon.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-imperative-watching-wozniak-agent-a3117c4.md" "$DEST/05-engineering-infra/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-task-project-management-research.md" "$DEST/06-agents-orchestration/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/research/2026-02-24-kind-splashing-wand.md" "$DEST/07-research/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/work-covered-ai/work-core-principle-v1.md" "$DEST/04-product/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-094105.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-122859.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-235107.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-100658.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-234914.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-001234.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-094210.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-113411.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-153948.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-220805.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-084857.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-094405.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-122407.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-003356.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-072328.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-150726.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-141204.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-053711.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-123033.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-131416.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-000411.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-000809.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-160917.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-120128.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-204732.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-121532.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-054715.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-200733.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-104231.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-005644.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-091046.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-132005.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-001839.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-173018.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-153034.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-205130.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-074835.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-144609.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-141106.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-121045.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-093802.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-122648.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-094605.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-194348.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-120739.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-122811.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-152553.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-203338.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-064349.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-054115.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-154349.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-063836.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-141024.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-101019.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-233250.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-155225.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-072608.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-025859.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-113053.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-161910.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-222312.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-233016.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-115039.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-114957.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-193858.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-102135.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-013526.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-102744.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-072034.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-030243.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-121126.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-201825.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-004129.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-152820.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-121210.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-101821.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-174305.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-082147.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-120945.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-063112.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-082758.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-000522.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-121138.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-123103.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-092209.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-094720.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-102256.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-133527.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-064723.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-005523.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-120908.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-180215.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-011638.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-072500.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-054333.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-122735.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-234108.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-161339.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-163800.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-083016.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-055111.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-113501.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-001443.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-140130.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260225-040533.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-003027.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-170621.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-122853.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-232514.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-064446.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-071801.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-155647.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-062137.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-235017.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-002342.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-113506.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-130105.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-225432.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-155956.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-173900.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-121704.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-143617.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-095319.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-235431.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-074338.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-072416.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-175215.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-152329.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-012459.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-154826.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-140206.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-173118.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-155847.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-115338.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-055853.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-130358.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-112510.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-173405.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-012524.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-234640.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-225221.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-082231.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-061845.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-081301.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-132125.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-091728.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-140907.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-070355.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-135726.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-201429.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-011219.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-102231.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-140000.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-123625.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-125845.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-135250.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-122922.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-170453.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-151651.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-092257.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-112959.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-092834.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-004326.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-181637.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-095040.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-004549.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-093347.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-000342.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-101848.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-000114.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-060927.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-122237.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-120805.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-060759.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-131628.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-091308.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-062946.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-161111.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-161820.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-131908.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-092605.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-143028.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-125310.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-085320.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-123345.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-114925.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-085033.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-151413.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-092220.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-180447.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-005225.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-024228.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-234310.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-063626.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-155855.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-195845.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-130941.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-094339.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-065413.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-205958.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-010111.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-211019.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-150237.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-100541.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-095613.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-094956.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-122748.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-115252.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-020327.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-194723.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-102208.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-211918.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-155419.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260221-115153.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-172735.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260225-035228.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260224-175704.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260225-092119.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-064234.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260222-054849.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260220-211358.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
cp -p "$SRC/Clone Github/corpus-raw/vault/_inbox-voice/voice-20260223-083911.md" "$DEST/09-transcripts-voice/" 2>/dev/null || true
