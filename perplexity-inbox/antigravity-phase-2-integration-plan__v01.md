# Implementation Plan — Phase 2: Worktree, Epistemic Status & Pre-Production Gate

This plan details the steps to implement the deterministic epistemic status core and the 9-item pre-production gate inside the `antigravity` repository on the Mac Mini, centralizing all Python and infrastructure logic in a shared, read-accessible location and pushing it to GitHub, while routing all plans through the Perplexity inbox.

---

## Strategic Context & User Request

### Sovereign IDE Units & Centralization
* **Sovereign IDE Vision:** Each IDE operates as an independent, sovereign unit that can take tasks from start to finish. Development of tools and skills happens inside task-specific worktrees within these IDEs.
* **Centralization:** Once a skill or tool is developed, it is committed to the central `antigravity` repository on the Mac Mini and pushed to GitHub (`Amplified-Partners/antigravity`) so all agents and humans have read visibility into the changes.
* **Perplexity Integration:** No independent architectural decisions are finalized without review. All plans and decisions must be written back to the Perplexity inbox (`/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/`) so Perplexity can synthesize them into the global system state.

---

## Proposed Changes

### Antigravity Repository (`/Users/one/Projects/antigravity`)

#### [NEW] [python/epistemic_status.py](file:///Users/one/Projects/antigravity/python/epistemic_status.py)
* Holds the core `EpistemicStatus` IntEnum, `StatusedValue`, `Layer` base class, `AuditLog`, `DriftDetector`, and promotion gate logic.
* Configures local fallback file logging for the audit log when PostgreSQL is not connected.

#### [NEW] [python/pre_production_gate.py](file:///Users/one/Projects/antigravity/python/pre_production_gate.py)
* Implements the `TaskSpecification` dataclass holding the 9-item properties:
  1. `goal_link`
  2. `owner`
  3. `input_refs`
  4. `acceptance_test`
  5. `allowed_tools`
  6. `data_sensitivity`
  7. `route_destination`
  8. `stop_condition`
  9. `baton_requirement`
* Implements the `PreProductionGateLayer` wrapping these checks as a deterministic `Layer` that emits a `STRUCTURED` status if all checks pass, and demotes to `INTUITED` on failures.

#### [NEW] [python/tests/test_epistemic_status.py](file:///Users/one/Projects/antigravity/python/tests/test_epistemic_status.py)
* Contains unit tests for:
  - Input/precondition min-rule propagation.
  - Staleness-based demotions.
  - Verification of the 9-item task specification properties (checking that invalid cells, empty links, or wrong sensitivities trigger failed preconditions and demote the status).

### Perplexity Inbox (`/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox`)

#### [NEW] [antigravity-phase-2-integration-plan__v01.md](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/antigravity-phase-2-integration-plan__v01.md)
* A complete copy of this implementation plan published to the Perplexity inbox to allow Perplexity to read, analyze, and integrate it.

#### [DELETE] [amplified_harness.py](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/amplified_harness.py)
* Removed to prevent naming conflict with the broader harness suite.

#### [NEW] [amplified_permissions.py](file:///Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/amplified_permissions.py)
* Renamed target containing the action classifier and permission checks.

### Mac Mini Repository Configurations

#### [MODIFY] [hooks/pre_commit_gate.py](file:///Users/one/Projects/antigravity/hooks/pre_commit_gate.py)
* Update imports to refer to `amplified_permissions` instead of `amplified_harness`.

---

## Verification Plan

### Automated Tests
* Run pytest on the Mac Mini inside the worktree directory:
  ```bash
  pytest python/tests/test_epistemic_status.py
  ```
* Run the self-test for `amplified_permissions.py` on the Mac Mini:
  ```bash
  python3 hooks/amplified_permissions.py
  ```

### Manual Verification
* Verify the file `/Users/ewansair/ingestion-to-research-pipe/perplexity-inbox/antigravity-phase-2-integration-plan__v01.md` exists and is populated.
* Verify the git status and branches on GitHub to ensure they contain the centralized work.
