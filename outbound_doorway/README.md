# Outbound doorway

Agents drop JSON patches here. **`apply_doorway`** (Rust) verifies and applies — do not edit repo files directly.

**Schema:** `PATCH-SCHEMA.json`  
**Fixtures:** `patch_fixture_good.json`, `patch_fixture_bad.json`

```bash
~/control-centre/bin/apply_doorway verify  outbound_doorway/patch_*.json --repo-root .
~/control-centre/bin/apply_doorway apply    outbound_doorway/patch_*.json --repo-root .
```

**Prior art (fleet):** `harness/shape_gate.py`, `harness/gatekeeper.py`, `clean-build/02_build/enforcer/` (Rust bounds), control-centre constitutional gate. Industry: JSON Patch RFC 6902 (subset), Bazel sandboxed actions, Cedar/Bedrock tool gates.

**Build:** `cd ~/control-centre/crates/apply_doorway && cargo build --release`
