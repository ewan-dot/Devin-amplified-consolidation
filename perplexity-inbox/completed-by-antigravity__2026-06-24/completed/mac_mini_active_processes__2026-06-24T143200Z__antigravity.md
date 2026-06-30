# Mac Mini Active Processes & Environment Audit

TIER: MEASURED (live process audit run and verified on host)
PROVENANCE: Ran ps -ef and launchctl queries on Mac Mini host 100.77.149.1 (2026-06-24)
STATUS: completed
COMPONENT_REF: out-of-list

---

### What was verified

A live scan on the Mac Mini (`wanmini` / `100.77.149.1`) was conducted to check for active environments and running jobs.

#### 1. Active Web UIs (Dashboard/Control Panel)
* **`stop-ui` Server:** Running under user `ewanbramley` (PID 70899), listening on port `8765` (Sovereign Stop/Start UI).
* **`centre-ui` Server:** Running under user `ewanbramley` (PID 78674), listening on port `8766` (Deterministic Centre State Dashboard).

#### 2. Running IDE & Agent Processes
* **Cursor IDE:** Active with the `📍 User interface (The Lens)` extension host loaded under user `ewanbramley` (PID 75372, 75377, 75378, 75379, 75380).
* **Active Scripts:** A smoke-test task (`smoke-test.sh` under PID 77654) and its output watchers are actively running in `/Users/ewanbramley/AgentsMini-worktree`.

#### 3. Docker Daemon Status
* Queried both user `one`'s and user `ewanbramley`'s OrbStack paths. The Docker socket (`docker.sock`) is not present for either user, confirming that the OrbStack Docker daemon is indeed **stopped**.

---

### How to verify independently

Run the process check command on the Mac Mini:
```bash
ssh one@100.77.149.1 "ps -ef | grep -i -E 'server.py|smoke-test|cursor'"
```

---

[CLOSURE] branch=ACTION | proxy=none | gates=none | inbox=none | tier=MEASURED
