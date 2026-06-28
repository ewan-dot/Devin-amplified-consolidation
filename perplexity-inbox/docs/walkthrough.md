# Walkthrough - Estate Taxonomy, Connection Guards, and Terminology Gate

We have successfully designed and deployed the architectural safety gates, continuous workflows, and terminology translation systems requested by the architect.

## Accomplishments

### 1. Estate Taxonomy ([ESTATE-TAXONOMY.md](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/ESTATE-TAXONOMY.md))
*   **AI-Only Master Directory:** Established a comprehensive, structured mapping of our entire infrastructure layout designed purely for machine parsing and self-orientation.
*   **Signposted Targets:** Explicitly details the purpose of each database (e.g., `amplified_brain` vs `cove` vs `vellum`), active extensions, node counts, and host ports to eliminate connection ambiguities.

### 2. Database Connection Guard ([db_harness.py](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/harness/db_harness.py))
*   **Deterministic Safety Harness:** Implemented pre-flight assertions that parse database connection URIs and raise a hard `AssertionError` if a script targets the orchestrator database (`cove`) for Business Brain writes.
*   **Production Graph Verification:** Queries Apache AGE to confirm that the target graph name (`business_brain`) exists and has at least `10,000` nodes, preventing agents from running in empty dummy sandbox sandboxes.

### 3. Terminology Alignment Gate ([term_gate.py](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/harness/term_gate.py))
*   **AI-Facing Translation Algorithm:** Created an interceptor that maps imprecise human inputs (e.g., "query the brain", "write to cove") into absolute technical targets (`amplified_brain`, `/cove` database, `Beast` hosts).
*   **Context-Based Resolution (Diagnostic Pathways):** Refactored the disambiguation engine. Instead of asking you database names directly (which increases error potential and cognitive load), the AI runs a sequence of simple context-based questions (Domain, Location, Operation Type) to deduce the correct target from your intent, acting as a complete AI-facing shield.

### 4. Global Agent Rule Injection ([AGENTS.md](file:///Users/ewansair/.gemini/config/AGENTS.md))
*   **AI-Facing Shield Enforcement:** Appended the **Terminology & Intent Verification Rule** to the global config file. 
*   **Look Deeper Mandate:** The rule explicitly instructs all future AI agents to **look deeper than ambiguous surface names**. Agents must not rely on simple string matching; they are bound to check target execution contexts, active schema signatures, and record volume sizes directly in the database containers to verify correctness.

### 5. Continuous Background Watcher ([inbox_watcher.py](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/inbox_watcher.py))
*   **Continuous Segmenter:** Automatically monitors the `/inbox` folder, chunks text/markdown files into 300-line blocks, injects structured YAML frontmatter, and moves the originals to `/archive`.
*   **Graceful Degradation:** Integrates the `db_harness` connection check at startup, warning the user and degrading gracefully to local-only chunking operations if the Beast SSH tunnel is offline.

### 6. Single-Pass Watcher for macOS Integration ([inbox_watcher_single_pass.py](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/inbox_watcher_single_pass.py))
*   **Deterministic Trigger Execution:** Created a single-pass script designed specifically for integration with macOS Folder Watchers (like **Hazel** or native **launchd**) so that file ingestion consumes 0% background CPU/RAM and triggers instantly on file events.

### 7. Database Cleanup & Rule Injection
*   **Orchestrator DB Purification:** Tunneled to the Beast database port and dropped the polluted duplicate `business_brain` AGE graph and `business_brain_storage_slots` table from the `/cove` database. This ensures the `cove` database remains purely for deterministic pipeline orchestration, completely separate from the `amplified_brain` knowledge graphs.
*   **Non-Destructive Ingestion & Data Lake Codification:** Formally updated [ai_native_data_organization.md](file:///Users/ewansair/.gemini/antigravity/brain/a3fb2a4c-0b97-48a0-81af-8ee11c0ee103/ai_native_data_organization.md) to define the anonymous database firewall and non-destructive ingestion model. All inputs are preserved in the Data Lake (`/archive/` or MinIO S3) rather than deleted, while the gatekeeper pipeline acts as an epistemic classifier.
*   **Global Structural Enforcement:** Added the **Structural Discipline & Execution Separation Rule** to [AGENTS.md](file:///Users/ewansair/.gemini/config/AGENTS.md) to enforce strict naming boundaries, predictabilities, and the firewalling of operational data from running AIs.

---

## Verification Results

*   **Database Cleanup:** Verified that querying graphs inside `cove` database returns an empty list, and the `business_brain_storage_slots` table no longer exists.
*   **Safety Port Closure:** Verified that the Beast SSH tunnel is closed and the local database connection is refused, securing the database port.
*   **Terminology Shield Test:** Ran `"drop the polluted business_brain graph and tables in the cove database"` through `term_gate.py` and verified it successfully flagged the database domain crossover ambiguity, preventing accidental schema deletions.

---

## macOS Deterministic Integration Guides (Won't-Break Setup)

To prevent terminal-session crashes, we map out the two bulletproof macOS options to run the file chunker:

### Option A: The Hazel Integration (Recommended)
Hazel watches folders natively at the OS level (via FSEvents) and is exceptionally robust. 
1.  Open **Hazel Preferences** and add the folder: `/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/`
2.  Create a new rule:
    *   **Conditions:** `Extension is txt` OR `Extension is md`
    *   **Ignore Files:** Add rules to ignore `README.md`, `brief.md`, `ESTATE-TAXONOMY.md` (or set a condition `Name does not start with INBOX-INDEX`).
    *   **Action:** Select **Run Shell Script** -> click **Edit script** -> set shell to `/bin/bash` -> paste:
    ```bash
    /Users/ewansair/ingestion-to-research-pipe/clean-build/02_build/scripts/.venv/bin/python3 /Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/inbox_watcher_single_pass.py "$1"
    ```
3.  Hazel will automatically pass the dropped file path to python, chunk it, and move the original to `/archive`, cleaning the inbox.

### Option B: The launchd Integration (Native Headless Daemon)
We have written a LaunchAgent configuration at: [/scratch/ai.amplified.inbox.watcher.plist](file:///Users/ewansair/.gemini/antigravity/brain/a3fb2a4c-0b97-48a0-81af-8ee11c0ee103/scratch/ai.amplified.inbox.watcher.plist)
To register this as a persistent OS service that starts on boot:
1.  Copy the plist to your LaunchAgents directory:
    ```bash
    cp /Users/ewansair/.gemini/antigravity/brain/a3fb2a4c-0b97-48a0-81af-8ee11c0ee103/scratch/ai.amplified.inbox.watcher.plist ~/Library/LaunchAgents/ai.amplified.inbox.watcher.plist
    ```
2.  Register and start the daemon:
    ```bash
    launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.amplified.inbox.watcher.plist
    ```
3.  macOS will now manage the python script, automatically restarting it if it crashes. Log files will be written to `/harness/watcher_stdout.log` and `/harness/watcher_stderr.log`.

