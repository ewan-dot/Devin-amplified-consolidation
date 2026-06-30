# Git Repository Sharing Policy

TIER: MEASURED (architect-approved policy)
PROVENANCE: Design review and verification of SMB file locks, IDE latencies, and git database constraints (2026-06-24)
STATUS: completed
COMPONENT_REF: out-of-list

---

### What was built/changed

Established the official system policy for handling Git repositories in the shared Tailscale network folder:

1. **Active Repositories Stay Local:** 
   * Active code development repositories must be kept on local disks (e.g., `/Users/one/Projects/` on the Mac Mini, and `/Users/ewansair/Projects/` on the M5 Air).
   * This prevents database corruption from SMB concurrent locks, IDE indexing/file watcher lag, and slow container build performance.
2. **Syncing via GitHub:** 
   * GitHub remains the canonical repository hub for synchronizing code changes across nodes.
3. **Shared Folder for Communal Data Only:** 
   * The shared `ingestion-to-research-pipe` folder is reserved strictly for communal assets, the Perplexity inbox, completed reports, logs, and shared documentation.

---

### What was verified
* Confirmed that mounting `/Users/ewansair/ingestion-to-research-pipe` on the Mac Mini via SMB works successfully for static documentation, but attempting active git repository compilation or file watching over the network mount degrades performance.

---

[CLOSURE] branch=ACTION | proxy=none | gates=none | inbox=none | tier=MEASURED
