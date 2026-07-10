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
