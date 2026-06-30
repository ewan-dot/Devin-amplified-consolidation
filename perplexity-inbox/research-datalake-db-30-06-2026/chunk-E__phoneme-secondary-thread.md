---
title: "Chunk E — Phoneme Secondary Thread + 3 Touchpoints"
document_type: research_chunk
chunk_id: E
parent_extraction: INDEX__THREAD-EXTRACTION__atom-chunk-label-chronology__v01__2026-06-30__cursor.md
partner: partner-E__source-context.md
date_utc: 2026-06-30
author: cursor
epistemic_tier: INTUITED
priority: SECONDARY
---

# Chunk E — Phoneme secondary thread + 3 touchpoints

**Source:** Thread L8–18; RESEARCH-CAPTURE phoneme; RESEARCH-PIPE-RUN.

> **Priority:** SECONDARY to DB/lake structure (Chunk A). Do not lead Pass 2 with phoneme work.

| Type | Extraction | STATUS |
|------|------------|--------|
| **Architect intent** | Phoneme = sounds; accents in transcription (STT: phemone/Beemones) | needs research |
| **Architect intent** | Same deterministic normalizer at **audio→text, ingest→lake, query→search** | needs research |
| **Architect intent** | Guard byte-dedup led astray by fat fingers / poor spelling | partially encoded (Levenshtein only) |
| **Architect intent** | Real-time audio→transcription reduces token cascade | needs research |
| **Architect intent** | Internal failure-pattern corpus sufficient for algorithmic fix | GAP (corpus not inventoried) |
| **Architect intent** | NOT Russian maths interpretation — no corrupting natural language | needs research (dual-stream) |
| **Tension** | Verbatim Acoustic Intake Valve vs phoneme canonicalization | partially encoded (dual-stream proposed) |
| **Recommendation** | Bronze verbatim immutable + Silver normalized + phonetic keys; LLM above normalizer | INTUITED — not ratified |
| **Survivors** | WFST G2P W12-6208, Mlphon, Double Metaphone, NeMo ITN, EDC, FastCorrect | cited in phoneme capture |

## Three touchpoints

1. **Audio→text** (Monologue / real-time transcription)
2. **Ingest→lake** (Silver promotion gate)
3. **Query→search** (`search_autocorrect.py` — grapheme only today)

## Dual-stream resolution (proposed)

| Stream | Preserves | Use |
|--------|-----------|-----|
| **Bronze** | Verbatim transcript (typos, false starts, certainty flags) | Verbatim Acoustic Intake Valve |
| **Silver** | Normalized grapheme + phonetic keys | Dedup, search join, multi-DB projection |

Chronology links both via `source_atom_bronze_id`.
