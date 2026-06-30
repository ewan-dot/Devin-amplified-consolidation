---
document_id: signal-reading-prior-art-synthesis__human__v01__2026-06-25
document_type: readable_research_conclusion
stage: synthesis
reader: human
audience: Ewan
author: subagent-prior-art
created: 2026-06-25T10:35:00Z
version: v01
goal_link: "Ewan/signal-reading-prior-art"
outcome_routing:
  verdict: DESIGN_IS_DEFENSIBLE
  confidence: high
  open_action: "Three decisions listed at the end. Design is ready to implement pending those three."
---

Signal reading is the discipline of looking at the Vellum stream, Opik traces, and Langfuse runs at the moment a job starts and deciding: proceed, warn, or halt — not query-and-dump, but a structured decision process with well-understood prior art behind it.

---

## Where we are

Before looking at any external sources, the first thing to establish is what already exists internally. The file `/opt/amplified/vellum/scripts/friction_monitor.sql` (58KB, 2026-06-03) contains ten named detection queries that implement Shewhart control charts, multi-window burn-rate alerting at exactly the Google SRE parameters (1h at 14.4×, 6h at 6×), EWMA with slope detection, one-sided CUSUM for token counts, process-conformance checking for workflow node sequences, and a dead-man's switch for infrastructure heartbeats. The companion `measurement_worker.py` (24.7KB) implements four monitor classes that run these queries and route outputs to T0–T4 escalation tiers. This means the detection layer is not aspirational — it exists. What does not yet exist is the job-start hook that runs these queries before a job begins and returns a proceed/warn/halt decision.

---

## What the prior art says reading actually looks like

- **Google's Four Golden Signals** ([SRE book, 2016](https://sre.google/sre-book/monitoring-distributed-systems/)): latency, traffic, errors, saturation. All four are already represented in `friction_monitor.sql` — latency via Shewhart and EWMA, errors via burn-rate, saturation via token CUSUM and queue depth. Traffic as a standalone signal (jobs per hour trend) is the one small gap.

- **Multi-window burn-rate** ([Google SRE Workbook Chapter 5](https://sre.google/workbook/alerting-on-slos/)): the key insight is that a single-window alert either fires too early (brief spike) or too late (slow drift). The correct pattern is two windows together: fast (1h, 14.4× threshold) fires only if slow (6h, 6× threshold) also fires. Both conditions together mean the error budget is being consumed fast enough to warrant action. `friction_monitor.sql` query 2 implements this verbatim, with the comment "Google SRE Chapter 5."

- **Statistical Process Control — when a sequence of normal events becomes a signal** ([Shewhart, 1924](https://en.wikipedia.org/wiki/Shewhart_individuals_control_chart); [Nelson rules, 1984](https://en.wikipedia.org/wiki/Nelson_rules)): a single value above 3σ is one kind of signal. Nine values in a row on the same side of the mean (even if each is individually within limits) is a different kind of signal — it indicates the process mean has shifted. Nelson's eight rules formalise this. The EWMA slope detection in query 3 is the automated equivalent of watching for Nelson Rule 3 (six points in a row monotonically increasing).

- **Intelligence-analyst tradecraft** ([Heuer, "Psychology of Intelligence Analysis," CIA 1999](https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/); [ICD 203, ODNI 2015](https://www.dni.gov/files/documents/ICD/ICD-203.pdf)): analysts are required to state their confidence level explicitly (HIGH/MODERATE/LOW/INSUFFICIENT) and to name what drives their uncertainty. Applied to job-start reading: "no alerts" does not mean "no signal" — it means the detection queries found nothing above threshold. The reader must say: "nothing above T2 in the last 15 minutes, HIGH confidence in proceed." The absence of evidence is not evidence of absence, but it is a PROCEED ruling with an explicit basis.

- **Honeycomb's observability discipline** ([Charity Majors, Honeycomb](https://www.honeycomb.io/resources/training-videos/finding-outliers-with-bubbleup)): effective reading requires asking: "what is different about the events I care about vs the baseline?" Her BubbleUp pattern — compute all dimensions inside the anomaly bubble vs outside and rank by statistical difference — is the debugging version of what the job-start reader does at a coarser grain. Currently Amplified does not have a BubbleUp-equivalent; it has named queries that detect specific patterns. This is a natural next step once the job-start hook is working.

- **Drift detection — ADWIN / Page-Hinkley** ([Bifet & Gavalda, 2007](https://riverml.xyz/latest/api/drift/ADWIN/)): tier demotions (STRUCTURED→INTUITED entries in the Vellum stream) are not a continuous metric — they are a categorical distribution. Watching whether the fraction of INTUITED entries is increasing over time is a distribution-drift problem, not a Shewhart problem. Page-Hinkley accumulates directional changes and signals when the accumulation exceeds a threshold. This is the one external technique not yet in `friction_monitor.sql` that is worth adopting.

- **Bayesian base-rate awareness** ([Kahneman, "Thinking Fast and Slow," 2011](https://www.jstor.org/stable/1914185)): if circuit-breaker events are rare (once per 500 jobs) and one occurs in the job-start window, it has high diagnostic value. If validation failures occur at 1 per 5 jobs, a single one is low-diagnostic. The reader must weight signals by their base rate, not treat all T1 events equally. The false-positive budget of ≤1 false halt per 100 reads is achievable because T3+ events (the HALT threshold) are genuinely rare.

- **Process conformance** ([XES/OCEL standards, process-mining tradition](https://www.ocel-standard.org/)): query 4 in `friction_monitor.sql` checks whether the actual node sequence of a completed workflow execution matches the expected normative sequence. "Missing nodes," "extra nodes," "reordered nodes" are distinct deviation types. A job-start reader should check the immediately-preceding execution of the same workflow type for conformance deviations — if the last run had `extra_nodes` (hallucinated tool calls), the next run starts with a WARN.

---

## The job-start protocol in plain English

1. **Determine the time window.** Default: the greater of 15 minutes or time since this IDE last read the witness stream. If no prior read exists, use 30 minutes and flag cold-start.

2. **Run the friction-event query.** Ask `fact_friction_event` for all events in the window, ordered by severity. Also query the five trial boundaries in the Vellum entries table directly for boundary errors, tier demotions, and telemetry gaps.

3. **Check for tier demotions.** Any STRUCTURED→INTUITED demotion on any of the five trial boundaries (`perplexity_ingest.drop`, `research_pipe.staging_emit`, `brain_mcp_writer.ingest`, `cove_temporal.workflow_start_end`, `infisical.secret_read`) is treated as T2 regardless of what the friction-event query says. Tier demotion is evidence degradation, which is a first-class signal.

4. **Check for silence.** If any trial boundary that was active 30 minutes ago produced zero entries in the last 30 minutes, that silence is a signal. A boundary that stops emitting without explanation is a telemetry gap.

5. **Apply the decision.** T4 anywhere: HALT. T3 on a trial boundary: HALT. T3 elsewhere: WARN-BUT-PROCEED. T2 or tier demotion: WARN-BUT-PROCEED. T1 cluster (≥3 events): WARN-BUT-PROCEED. T1 single or T0: PROCEED with note. Nothing: PROCEED clean. Cold start: WARN with flag.

6. **Emit a `witness_read` Vellum entry.** Record what was queried, the window, the highest severity seen, and the ruling. The reader is itself watched. If reads stop, that absence is itself a signal.

7. **Surface to Ewan only if non-trivial.** PROCEED (clean or with T0 note) does not need to reach Ewan. WARN-BUT-PROCEED or HALT gets a one-paragraph synthesis: what fired, which boundary, what the runbook says.

---

## Proceed / warn / halt

| Signal | Ruling |
|---|---|
| T4 event anywhere in window | HALT — do not start job |
| T3 event on trial boundary | HALT |
| T3 event on non-trial boundary | WARN-BUT-PROCEED |
| T2 event, or any tier demotion on trial boundary | WARN-BUT-PROCEED |
| T1 cluster (≥3 events in window) | WARN-BUT-PROCEED |
| Telemetry gap on trial boundary | WARN — cold start or silence |
| T1 single event | PROCEED with log note |
| T0 events only, or no events | PROCEED clean |
| No history (cold start) | WARN — flag cold start, proceed with caution |

False-positive budget: ≤1 false HALT per 100 job starts. T3+ events at current scale are rare; this budget is achievable without tuning.

---

## What is strong / what is thin

**Strong:**
- `friction_monitor.sql` (58KB) already implements Shewhart, EWMA, CUSUM, multi-window burn-rate, and process conformance. The detection layer is not a gap.
- The escalation tier model (T0–T4) maps cleanly onto the proceed/warn/halt decision.
- The `witness_read` entry pattern closes the audit loop — the reader is watched.
- Google SRE's multi-window burn-rate (14.4×/6×) is already implemented with explicit attribution.
- Tier demotion as a first-class signal (SC-6) is Amplified-specific and has no external equivalent. It is internally well-justified by the min-rule.

**Thin:**
- The baseline window for cold start (no 30-day history) is unresolved. The queries require ≥30 observations; new workflows have none.
- ADWIN/Page-Hinkley for tier-distribution drift is not yet implemented. The Shewhart queries cover continuous metrics; the categorical tier-distribution needs a separate accumulator.
- Base-rate estimates per friction type are not stored explicitly — they must be computed post-hoc from `fact_friction_event`. The job-start reader cannot weight signals by base rate without this.
- Nelson rule sequence detectors (the "9 in a row" class of rules) are not yet implemented. They add sensitivity at the cost of false positives; they should wait until each workflow has ≥50 baseline observations.

---

## Next decision Ewan needs to make

Three decisions, all of which are resolving open questions rather than choosing directions:

1. **Cold-start baseline:** Accept a 7-day fallback baseline (smaller N, less reliable control limits, but available immediately for new workflows) or enforce strict 30-day minimum with a cold-start warning that blocks the Shewhart/EWMA queries? Recommendation: 7-day with explicit cold-start flag in the job-start synthesis.

2. **Tier-distribution drift detector:** Adopt one Page-Hinkley accumulator on the INTUITED/(STRUCTURED+PROVEN) ratio in the Vellum stream, or wait and rely on Shewhart queries on the existing `tier_distribution` named query? Recommendation: adopt Page-Hinkley; it is a single accumulator, not a new subsystem.

3. **False-positive budget ratification:** The ≤1 false halt per 100 reads target needs explicit ratification as the operating parameter. If Ewan is comfortable with a tighter budget (e.g., ≤1 per 200 reads), that argues for raising the HALT threshold to T3+T2-cluster rather than T3-alone-on-trial-boundary. Recommendation: ratify ≤1 per 100 reads as stated; adjust after one month of real traffic data.

The design is defensible as stated. None of these decisions block implementation of the job-start hook.
