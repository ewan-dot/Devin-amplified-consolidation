# Instruction: Governed Worker Registration & Hook Activation

<!-- AI-IGNORE: Bracketed terms are for human reference only. Do not parse or extract. -->
**Date:** 2026-06-30  
**Author:** Antigravity  
**Audience:** Claude / Cursor (Execution Agents)  
**Status:** Actionable Implementation Brief  

This document instructs the executing agent to register the governed worker (`temporal/workers/governed_main.py`) in the Docker-compose stacks on the high-capacity server host `[Beast]` and activate the deterministic validation hooks.

---

## 1. Execution Setup & Git Worktree Discipline

You MUST operate within an isolated Git worktree. Do not commit or execute changes on dirty or shared branches.

1.  **Create isolated worktree:**
    ```bash
    git worktree add -b task/governed-worker-activation .worktrees/governed-worker-activation
    ```
2.  **Navigate to the worktree directory:**
    All modifications, testing, and staging must happen inside:
    `/Users/ewansair/ingestion-to-research-pipe/.worktrees/governed-worker-activation/`

---

## 2. Implementation Steps

### Step 2.1: Locate the Governed Worker & Configuration
1.  Identify the governed worker file: `temporal/workers/governed_main.py` on the high-capacity server host `[Beast]`.
2.  Verify the worker initializes the deterministic checks using `/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/harness/agentic_checks.py`.

### Step 2.2: Docker-compose Registration
1.  Locate the production Docker-compose file on the high-capacity server host `[Beast]` (typically at `/opt/amplified-machine/docker-compose.yml` or check paths in `ESTATE-TAXONOMY.md`).
2.  Add a new service definition `governed-worker`:
    ```yaml
    governed-worker:
      image: vellum-worker:latest # Or appropriate python environment image
      container_name: governed-worker
      restart: unless-stopped
      environment:
        - TEMPORAL_ADDRESS=temporal:7233
        - DATABASE_URL=postgresql://cove:lTJhzWncfPNVCAomIFtkyVoxPrIENLtE@cove-postgres:5432/cove
        - VELLUM_URL=http://vellum:8400
      volumes:
        - /opt/amplified/temporal:/app/temporal
        - /opt/amplified/harness:/app/harness
      networks:
        - amplified-net
    ```
3.  Ensure the worker has access to `/app/harness/agentic_checks.py` for executing deterministic checks.

---

## 3. Verification & Validation Rules

You must verify that your implementation is correct before completing the task. 

### Rule 1: Docker Config Validation
Run the configuration validator on the high-capacity server host `[Beast]`:
```bash
docker compose config
```
Ensure there are no syntax or volume mapping errors.

### Rule 2: Connection & Telemetry Verification
1.  Start the container:
    ```bash
    docker compose up -d governed-worker
    ```
2.  Check the logs to verify the worker successfully registers with the Temporal server and does not crash:
    ```bash
    docker compose logs -f governed-worker
    ```
    *Success Signal:* Log line showing connection to `temporal:7233` and listening on task queue (e.g., `governed-tasks`).

### Rule 3: Gating Loop Check
Trigger a test workflow execution that invokes the governed worker. Verify that:
1.  The worker runs the pre-flight checks in `agentic_checks.py`.
2.  The worker runs the sandbox rollback transaction.
3.  The write to the semantic graph index `[amplified_brain]` succeeds ONLY when `sandbox_verified=True`, `semantic_entropy < 0.4`, and `conformal_set_size <= 2`.
4.  A write violating these bounds returns `HTTP 400 Bad Request` and logs `brain_write_blocked` in Vellum telemetry.

---

## 4. Finalization & Handover

1.  Stage all changes made inside the worktree:
    ```bash
    git add -A
    ```
2.  Commit the changes with a descriptive message:
    ```bash
    git commit -m "feat: register governed worker in docker-compose and activate safety hooks"
    ```
3.  Push the branch to the remote repository:
    ```bash
    git push origin task/governed-worker-activation
    ```
4.  Write a walkthrough documenting the validation logs and success signals, and update the baton before concluding.
