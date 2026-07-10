# Fork-flow foundation — working hypothesis

Use this when a discovery would interrupt a parent job.

1. Park it in `fork-park-index.yaml` if it is not independent and bounded.
2. Otherwise copy `fork-contract.template.yaml`, declare one owner, an isolated
   worktree, bounded `file_scope`, actual and compounding goals, checkpoints,
   validation, and a used/discarded return condition.
3. Select explicit hypotheses and pathways from `registry.yaml`. Hooks and
   harnesses are selectable pathways, not substitutes for engineering judgment.
4. Validate and resolve before marking the fork checked:

```sh
python3 perplexity-inbox/harness/fork_flow.py validate /absolute/contract.yaml --require-existing-paths
python3 perplexity-inbox/harness/fork_flow.py validate-index perplexity-inbox/armamentarium/fork-park-index.yaml
python3 perplexity-inbox/harness/fork_flow.py resolve /absolute/contract.yaml perplexity-inbox/armamentarium/registry.yaml --output /absolute/selection-manifest.json
```

The resolver creates a selection manifest; it does not promote hypotheses.
Promotion from `investigating` to `in_use` remains a deliberate, evidence-backed
change after a dogfood run. Preserve used and discarded results in the index.

## Durable lifecycle

The event log is append-only; the index and `FILE_PATH` atoms are reproducible
projections. A completed job can be `used` or `discarded` with its local verdict,
while a working hypothesis remains `investigating` until an independent review
receipt supports a deliberate promotion.

```sh
python3 perplexity-inbox/harness/fork_flow_store.py create /absolute/contract.yaml
python3 perplexity-inbox/harness/fork_flow_store.py claim <fork-id> --owner <agent>
python3 perplexity-inbox/harness/fork_flow_store.py transition <fork-id> running
python3 perplexity-inbox/harness/fork_flow_store.py rebuild-index \
  --output /absolute/fork-park-index.yaml
```

## External review gate

Build a minimal, attributable review pack, then validate the reviewer receipt.
The receipt must name the reviewer, bind to the exact pack hash, preserve
dissent, and contain a `pass` verdict. This is a promotion check, not an
automatic mutation of the registry.

```sh
python3 perplexity-inbox/harness/armamentarium_review.py write-pack \
  /absolute/contract.yaml perplexity-inbox/armamentarium/registry.yaml \
  --output /absolute/review-pack.json
python3 perplexity-inbox/harness/armamentarium_review.py check-promotion \
  <investigating-hypothesis-id> perplexity-inbox/armamentarium/registry.yaml \
  /absolute/review-receipt.yaml /absolute/review-pack.json
```
