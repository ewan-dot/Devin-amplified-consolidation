# Batons — active folder

**Active:** `batons/active/` — **last 5 only** (newest by mtime).  
**Archive:** `~/amplified-pipeline/data/batons/archive/YYYY-MM-DD/`  
**Datalake bronze:** `~/amplified-pipeline/data/datalake/bronze/batons/YYYY-MM-DD/`

Write: `python3 harness/baton_lifecycle.py write --title "..." --body-file ...`  
Read: session-start hook `session-start-read-baton.py`  
Rotate: automatic on write when count > 5.
