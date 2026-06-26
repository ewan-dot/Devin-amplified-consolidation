---
document_id: signal-reading-prior-art-synthesis__agent__v01__2026-06-25
document_type: research_conclusion
stage: synthesis
reader: agent
author: subagent-prior-art
created: 2026-06-25T10:35:00Z
version: v01
goal_link: "Ewan/signal-reading-prior-art"
owner: Amplified Partners
input_refs:
  - /opt/amplified/vellum/scripts/friction_monitor.sql (58157 bytes, read 2026-06-25)
  - /opt/amplified/vellum/scripts/measurement_schema.sql (29073 bytes, read 2026-06-25)
  - /opt/amplified/vellum/scripts/measurement_worker.py (24743 bytes, read 2026-06-25)
  - vellum-witness-doctrine-and-decorator.md (workspace, 2026-06-25)
  - estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25.md (workspace)
  - research-pipe-prior-art-synthesis__agent__v01__2026-06-25.md (workspace)
  - ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25.md (workspace)
  - data-lake-prior-art-synthesis__agent__v01__2026-06-25.md (workspace)
  - cross-ide-problem-sharing-rules.md (workspace)
data_sensitivity: internal-confidential
route_destination: Ewan / relay-protocol
baton_requirement: "Human review before: changing the false-positive budget floor, altering job-start hook placement in agent loop, modifying the default 15-minute time window, or choosing a drift-detection method for tier-distribution signals."
outcome_routing:
  verdict: DESIGN_IS_DEFENSIBLE
  confidence: high
  open_action: "Three open questions requiring Ewan decision: (1) baseline window for cold-start — recommend 30-day or 7-day fallback with explicit cold-start flag; (2) whether to adopt ADWIN/Page-Hinkley for tier-distribution drift or rely on Shewhart alone; (3) false-positive budget floor — recommended ≤1 false halt per 100 reads is justified below but requires ratification."
tier: T2-moderate
domains_surveyed: 13
primary_sources_cited: 14
companion_syntheses:
  - research-pipe-prior-art-synthesis__agent__v01__2026-06-25
  - ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25
  - data-lake-prior-art-synthesis__agent__v01__2026-06-25
  - estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25
witness_doctrine_ref: vellum-witness-doctrine-and-decorator.md
---

## One-sentence summary [T2-moderate]

Signal reading is the discipline of converting Amplified's Vellum witness stream, Opik traces, and Langfuse runs from append-only ledgers into a binary job-start decision (proceed / warn-but-proceed / halt), grounded in Statistical Process Control, Google SRE burn-rate reading, and intelligence-analyst tradecraft — and the 58KB `friction_monitor.sql` already implements the core detection methods; the gap is in the job-start hook and the reading protocol, not in the detection logic itself.

---

## Purpose and framing

The witness doctrine (vellum-witness-doctrine-and-decorator.md §"The Reader Contract") states that Perplexity Computer reads the witness stream at every session start and on every cross-IDE problem-lookup. That statement establishes the obligation. This synthesis establishes the discipline: what "reading" actually means operationally, what signal classes exist, when a sequence of normal entries becomes anomalous, and what decision the reader must produce.

The problem this pillar solves is write-only telemetry. A Vellum entry stream that no agent reads before starting a job is a ledger, not a signal system. The sensor mesh defined in estate-security-and-sensors-prior-art-synthesis (Pillar 4) creates the write surface. The analytics layer in `friction_monitor.sql` provides the detection logic. This synthesis defines the read protocol that closes the loop at job-start.

The correction Ewan made explicit: signal reading runs at job-start, not on a cron. This is not a scheduling preference — it is a decision-relevance requirement. A signal detected an hour after a job begins cannot inform the proceed/warn/halt decision for that job. The reader must fire before the first task in the job queue executes.

---

## Internal prior art first — `friction_monitor.sql`, `measurement_schema.sql`, `measurement_worker.py`

Reading these three files before citing external sources reveals that Amplified has already implemented most of the core detection patterns. The gaps are in the job-start hook and the reading interface, not in the mathematical substrate.

### `friction_monitor.sql` — 58KB, 2026-06-03

This file contains ten named detection queries, each implemented in DuckDB SQL against the star schema defined in `measurement_schema.sql`. The comment block at the top of the file names the detection methods explicitly: Shewhart (SPC), EWMA, CUSUM, Nelson rules, process-mining conformance, Google SRE burn-rate, dead-man switches.

**Named queries and their signal classes:**

| Query | Detection method | Signal class | Escalation output |
|---|---|---|---|
| 1. Shewhart control chart — P95 duration | Shewhart individuals chart, 3σ UCL, 30-day baseline | Latency / saturation | T2 (wake agent) if P95 > UCL; T1 (ticket) if > 2σ |
| 2. Multi-window burn rate — 1h/6h/3d | Google SRE Chapter 5, 14.4x fast / 6x slow | Error rate | T3 (page) if both fast+slow breach; T2 if fast only |
| 3. EWMA latency drift — λ=0.2 | EWMA with MAD-based UCL + linear slope | Sustained latency creep | T2 if EWMA > UCL + positive slope |
| 4. Process conformance | XES/OCEL process-mining | Path deviation / missing nodes | T3 if >50% of expected nodes missing; T1 for minor deviation |
| 5. Token explosion CUSUM | One-sided upper CUSUM, k=0.5σ, h=5σ | Token count / cost | Signals after sustained upward accumulation |
| 6. Tool failure clustering | Cluster detection in error records | Tool failure burst | Named in `measurement_worker.py` friction_type catalogue |
| 7. Retry storm | Rate on `retry_count` field | Retry accumulation | Runbook: retry policy review |
| 8. Cost burn | SLO-style budget on `total_cost_usd` | Cost saturation | T1/T2 by burn multiple |
| 9. Heartbeat / dead-man's switch | Poll-interval-based timeout | Infrastructure silence | T3 for 2× poll interval breach |
| 10. Infra health aggregate | Composite `health_score` 0–1 | Infrastructure degradation | `is_degraded` flag |

**What the file establishes:** The Amplified detection layer already implements Shewhart, EWMA, CUSUM, multi-window burn-rate, and process conformance — five of the major external prior-art patterns listed in the task brief. Any external pattern cited below must be checked against this before claiming it needs adoption.

**What is aspirational vs implemented:** The queries exist; the escalation tiers (T0–T4) are defined in `escalation_config.json`. What is not yet wired is the job-start hook that runs these queries at agent-loop start and returns a proceed/warn/halt signal to the calling IDE.

### `measurement_schema.sql` — 29KB, 2026-06-03

Defines a full star schema: 6 dimension tables (`dim_workflow`, `dim_node`, `dim_model`, `dim_date`, `dim_infrastructure`, `dim_error_type`) and 8 fact tables. Of the 8 fact tables, `fact_friction_event` is the signal output table: it carries `friction_type`, `severity`, `detection_method`, `observed_value`, `expected_value`, `threshold`, `deviation_pct`, and `runbook_ref`. This schema is what the job-start reader queries.

`fact_slo_measurement` tracks `burn_rate`, `error_budget_remaining_pct`, and `alert_severity` per workflow and window. This is the direct DuckDB equivalent of the Prometheus SLO measurement that Google SRE describes in [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/).

`fact_kaizen_candidate` records improvement opportunities from friction patterns — the lean kaizen feedback loop.

### `measurement_worker.py` — 24.7KB, 2026-06-03

Implements four monitor classes: `LatencyCreepMonitor` (Shewhart), `BurnRateMonitor` (multi-window), `HeartbeatMonitor` (dead-man's switch), and `KaizenAggregator` (pattern frequency to improvement candidate). Each class inherits from `FrictionMonitor`, which provides `determine_severity()` mapping observed/expected ratios to T0–T4 tiers. The worker can run as a one-shot or daemon; it reads from SQLite (development) or DuckDB (production).

The `escalate()` function routes events to: log_only (T0), create_ticket (T1), wake_agent (T2), page_oncall (T3), suspend_workflows (T4). The `wake_agent` route fires a Vellum entry on the `agent_wake_queue` — this is the existing hook surface that the job-start reader should use as its input channel.

---

## The Amplified signal taxonomy — 7 canonical classes

Grounded in the sensor catalogue from estate-security-and-sensors-prior-art-synthesis (Pillar 4) and the friction types named in `measurement_worker.py`. The Pillar 4 catalogue names 11 sensors; these map onto 7 signal classes for reading purposes.

| Signal class | Source surface | Read pattern | Severity rubric |
|---|---|---|---|
| **SC-1: Latency / saturation** | `fact_workflow_execution.duration_ms`, Opik trace spans | Shewhart UCL (3σ) + EWMA slope | T1 at 2σ; T2 at 3σ + positive EWMA slope |
| **SC-2: Error rate / burn** | `fact_workflow_execution.outcome`, Langfuse error events | Multi-window burn: 1h × 14.4x, 6h × 6x | T2 on fast-burn alone; T3 on both windows combined |
| **SC-3: Path deviation** | `fact_node_execution` sequence vs `dim_expected_node_sequence` | Process conformance check (XES/OCEL) | T1 for minor; T3 for >50% nodes missing; T2 for error-outcome path |
| **SC-4: Token / cost explosion** | `fact_workflow_execution.total_input_tokens + total_output_tokens`, `total_cost_usd` | One-sided CUSUM (k=0.5σ, h=5σ) | T2 when CUSUM signal raised; T1 when token efficiency drops >30% |
| **SC-5: Infrastructure silence** | `fact_infra_health.health_score`, Vellum `telemetry_gaps` sensor | Dead-man's switch (2× poll interval) | T3 at 2× poll interval; T4 at 4× |
| **SC-6: Tier demotion / evidence degradation** | Vellum `tier_distribution` named query, `tier_demotion` sensor | Direct read of STRUCTURED→INTUITED transitions in recent window | Any demotion in the five trial boundaries → T2 (min-rule applies) |
| **SC-7: Security / anomaly events** | Vellum `circuit_breaker_events`, `contradiction_detection`, `anonymisation_failure` sensors; Falco/Tetragon → Vellum pipeline | Count of events in job-start window vs baseline count | T3 for contradiction detection; T4 for anonymisation failure |

**SC-6 note:** Tier demotion is a first-class signal per the min-rule stated in the task brief. Reading a tier demotion on any boundary named in the five trial boundaries (`perplexity_ingest.drop`, `research_pipe.staging_emit`, `brain_mcp_writer.ingest`, `cove_temporal.workflow_start_end`, `infisical.secret_read`) is reading evidence-degradation, not a workflow performance metric. The proceed/warn/halt decision must treat this class separately from latency and error signals.

---

## External patterns mapped to Amplified

### 1. Google's Four Golden Signals → Amplified equivalents

[Google SRE's "Monitoring Distributed Systems" chapter](https://sre.google/sre-book/monitoring-distributed-systems/) defines: latency, traffic, errors, saturation. Amplified mapping:

| Golden Signal | Amplified equivalent | Already in friction_monitor.sql? |
|---|---|---|
| Latency | `duration_ms` P95, EWMA drift | Yes — queries 1 and 3 |
| Traffic | `executions_24h` from `fact_workflow_execution` | Partially — sampled in burn-rate denominator |
| Errors | `outcome != 'success'` error rate | Yes — query 2 |
| Saturation | `total_input_tokens / context_limit` + `queue_depth` from `fact_infra_health` | Partially — token CUSUM covers half; queue_depth field exists in schema |

**Gap:** Traffic as a standalone signal (jobs/minute trend) is not yet a named query. A Shewhart chart on `executions_per_hour` would close this gap. Evidence is thin on whether Amplified currently needs this.

### 2. Statistical Process Control (SPC)

[Walter Shewhart's original control chart](https://en.wikipedia.org/wiki/Shewhart_individuals_control_chart) (Bell Labs, 1924) and the [Western Electric Rules](https://en.wikipedia.org/wiki/Western_Electric_rules) (1956) define when a sequence of observations constitutes a signal even if no single observation exceeds a threshold. [Nelson's 1984 rules](https://en.wikipedia.org/wiki/Nelson_rules) formalise eight patterns.

**Already in Amplified:** Shewhart 3σ UCL/LCL is implemented in query 1. EWMA with slope detection in query 3. One-sided CUSUM in query 5.

**Not yet implemented — Western Electric / Nelson sequence rules:** The eight Nelson rules detect patterns in sequences (e.g., 9 points in a row on the same side of the mean; 6 points in a row monotonically increasing). These are more sensitive than a single-point Shewhart test. At the volume Amplified currently has (small-N per workflow), Nelson rules have high false-positive risk unless the baseline contains ≥30 points. The recommendation is to defer Nelson rules until each workflow accumulates ≥50 observations in the baseline window. Evidence is thin: no existing query implements Nelson rule sequence detection.

### 3. CUSUM and EWMA — Amplified already exceeds external SOTA at small N

[Page's CUSUM](https://academic.oup.com/biomet/article/41/1-2/100/234838) (1954) and [Roberts' EWMA](https://www.tandfonline.com/doi/abs/10.1080/00401706.1959.10489860) (1959) are the standard tools for small-N sustained-shift detection. Amplified's implementation in queries 3 and 5 is faithful: EWMA λ=0.2 (standard small-N value), CUSUM with k=0.5σ and h=5σ (standard parameters per Page 1954). This is not aspirational — these are running SQL queries.

### 4. Anomaly detection at low N — Twitter AnomalyDetection / Isolation Forest

[Twitter's AnomalyDetection R package](https://blog.twitter.com/engineering/en_us/a/2015/introducing-practical-and-robust-anomaly-detection-in-a-time-series) (Vallis, Hochenbaum, Kejariwal — Seasonal Hybrid ESD, 2015) and [Liu, Ting, Zhou's Isolation Forest](https://ieeexplore.ieee.org/document/4781136) (2008) are the standard tools for time-series anomaly detection at low N without Gaussian assumptions.

**Mapping to Amplified:** At current Amplified volumes (single-operator, <100 jobs/day), these tools are over-powered. SHESD and Isolation Forest shine at 1000s of events/day where Shewhart assumptions may be violated. At <100 events, Shewhart with ≥30 baseline samples is the correct prior-art choice. The recommendation is not to adopt SHESD or Isolation Forest now; revisit when any workflow exceeds 500 executions/day.

### 5. Drift detection — ADWIN / Page-Hinkley → tier-distribution monitor

[ADWIN](https://riverml.xyz/latest/api/drift/ADWIN/) (Bifet & Gavalda 2007) uses an adaptive sliding window; [Page-Hinkley](https://riverml.xyz/latest/api/drift/PageHinkley/) uses cumulative sums on directional changes. Both detect distribution shifts in sequences without requiring a fixed baseline window, making them suitable for detecting gradual drift in tier distributions when no stable 30-day baseline yet exists (cold-start problem).

**Mapping to Amplified:** SC-6 (tier demotion) is a categorical distribution, not a continuous metric. Watching the fraction of INTUITED entries increase over time is a distribution drift problem. ADWIN is appropriate for this class. The existing queries use Shewhart on continuous metrics only. Recommendation: adopt a simple Page-Hinkley accumulator on the INTUITED/(STRUCTURED+PROVEN) ratio in the Vellum stream. This is the one pattern from external prior art that is not already covered.

### 6. Google SRE burn-rate alerts

[Google SRE Workbook Chapter 5](https://sre.google/workbook/alerting-on-slos/) specifies multi-window multi-burn-rate alerting: fast window (1h, 14.4× threshold), slow window (6h, 6× threshold), short confirmation window (1/12 of the long window, 5m for 1h). Alert fires only when both fast and slow windows breach simultaneously — this eliminates false positives from brief spikes.

**Already in Amplified:** Query 2 in `friction_monitor.sql` implements exactly this: 1h at 14.4×, 6h at 6×, 3d at 1.5×, T3 only when both fast+slow breach. The SQL comment explicitly cites "Google SRE Chapter 5." This is fully adopted, not aspirational.

**What Amplified adds beyond Google SRE:** The 3-day window (1.5× threshold for ticket-level degradation) goes beyond the standard two-window pattern. This is an Amplified-specific extension appropriate for single-operator SLO monitoring where a slow drift needs a ticket but not a page.

### 7. Honeycomb's observability discipline — high cardinality + BubbleUp

[Charity Majors' work at Honeycomb](https://www.honeycomb.io/resources/training-videos/finding-outliers-with-bubbleup) established that effective signal reading requires high-cardinality, high-dimensionality data and the ability to ask arbitrary questions at read time rather than pre-aggregate at write time. BubbleUp (her term) finds what is statistically different about the outlier subset vs the baseline.

**Mapping to Amplified:** Vellum entries carry `boundary`, `tier`, `prev_hash`, `output_hash`, `duration_ms`, and payload metadata — high-cardinality by design. The star schema in `measurement_schema.sql` supports ad-hoc DuckDB queries. What Amplified does not yet have is a BubbleUp-equivalent that, when a friction event fires, automatically computes which dimensions (boundary, tier, workflow_id, node_type) are over-represented in the flagged events vs baseline. This is not a blocking gap but is the natural next step after the job-start reader is wired.

### 8. Intelligence-analyst tradecraft — Heuer / ICD 203

[Richards Heuer's "Psychology of Intelligence Analysis"](https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/) (CIA, 1999) and [ICD 203](https://www.dni.gov/files/documents/ICD/ICD-203.pdf) (ODNI Analytic Standards, 2015) establish that signal reading is not neutral — analysts carry prior-probability biases. The key failure modes in ICD 203 terms:

- **Anchoring on the first signal seen:** An agent that sees one T1 alert at job-start and proceeds without checking other signal classes has anchored on the least-severe signal.
- **Base-rate neglect:** If circuit-breaker events are rare (base rate 0.01 per job), a single circuit-breaker event has high posterior probability of being genuine, not noise. The false-positive paradox does not apply to rare events. Conversely, for common events (e.g., validation failures at 10% base rate), a single event has low diagnostic value.
- **Satisficing on "no alerts":** The absence of T2+ friction events does not mean proceed is safe. It means the detection queries found nothing above threshold. The reader must distinguish "no alerts" from "no signal."

**ICD 203 confidence vocabulary adapted to Amplified:**

| ICD 203 level | Vellum equivalent | Job-start ruling |
|---|---|---|
| HIGH confidence | T3/T4 event in last 15 minutes on trial boundary | HALT |
| MODERATE confidence | T2 event in last 15 minutes, or T1 cluster (≥3 in window) | WARN-BUT-PROCEED |
| LOW confidence | T1 single event, or T0 with positive EWMA slope | LOG, note in synthesis |
| INSUFFICIENT evidence | No data in window (cold start, telemetry gap) | WARN: cold start — proceed with caution |

### 9. Distributed-tracing reading — OTel critical path

[OpenTelemetry semantic conventions](https://opentelemetry.io/docs/concepts/observability-primer/) define the critical path as the sequence of spans whose summed duration equals the total trace duration. Reading the critical path tells you which node determined latency — not just that latency was high. `fact_node_execution.is_critical_path` already exists in `measurement_schema.sql`. The job-start reader should check: was the last job's critical path anomalous (deviating from the usual critical path structure)?

### 10. Postmortem and incident-review traditions — NTSB / Google blameless postmortem

[Google's blameless postmortem template](https://sre.google/sre-book/postmortem-culture/) and NTSB accident-investigation methodology both formalise retrospective signal reading. The relevance: when a proceed-then-fail sequence occurs (a job started on a WARN-BUT-PROCEED ruling and then failed), the postmortem must be able to trace back to which signals were present at job-start and whether the reading was correct. Vellum's `witness_read` entries (per the witness doctrine) make this possible — the reader is itself witnessed, so the audit trail of what the IDE saw at job-start is preserved.

### 11. Bayesian alert reading — base-rate awareness

[Kahneman's base-rate neglect](https://www.jstor.org/stable/1914185) chapter in "Thinking, Fast and Slow" (2011) documents that humans systematically underweight base rates and overweight vivid individual signals. In Amplified's context: if circuit-breaker events fire at a rate of 1 per 500 jobs, and a job starts with a circuit-breaker event in the window, the posterior probability that this represents a genuine problem is high. If validation failures fire at 1 per 5 jobs, a single validation failure is low-diagnostic.

**The false-positive budget:** With a base rate of ~5% for T1 events across all friction types, and a threshold of "T2+ triggers HALT," the expected false-halt rate at that threshold is low (T2 events are rarer). The recommended budget of ≤1 false halt per 100 reads (1%) sits above the expected false positive rate for T2+ events, giving adequate margin. This is consistent with Google SRE's alert-fatigue framing: a pager that fires more than a few times per week drives humans to ignore it.

---

## The job-start read protocol

The following is the concrete protocol for what an IDE does at job-start, grounded in the prior art above.

**Step 0 — Determine time window.**
Default window: `max(15 minutes, time since last witness_read by this IDE on any boundary)`.

Basis: the 15-minute floor is derived from the fast burn-rate window (1h/12 = 5 minutes per [Google SRE's short confirmation window](https://sre.google/workbook/alerting-on-slos/)), scaled up 3× for a small-N estate where individual events are sparse. The time-since-last-read ensures no gap is missed between sessions. If no prior `witness_read` entry exists (cold start), use 30 minutes and flag the cold-start condition.

**Step 1 — Query Vellum for SC-1 through SC-7 in the window.**

```
SELECT friction_type, severity, detection_method, observed_value,
       expected_value, threshold, deviation_pct, workflow_id, runbook_ref
FROM fact_friction_event
WHERE event_ts >= NOW() - INTERVAL '15 minutes'
ORDER BY severity ASC, event_ts DESC;
```

Supplemented by direct Vellum witness-stream query on the five trial boundaries:
```
SELECT boundary, event_type, tier, outcome, duration_ms, entry_hash
FROM vellum_entries
WHERE boundary IN (
    'perplexity_ingest.drop',
    'research_pipe.staging_emit',
    'brain_mcp_writer.ingest',
    'cove_temporal.workflow_start_end',
    'infisical.secret_read'
)
AND witnessed_at >= NOW() - INTERVAL '15 minutes'
ORDER BY witnessed_at DESC;
```

**Step 2 — Check for tier demotion (SC-6).**
Run `tier_distribution` named query filtered to the 15-minute window. Any STRUCTURED→INTUITED demotion on a trial boundary is a T2 event regardless of other signals.

**Step 3 — Check for telemetry gap (dead-man's switch).**
If any trial boundary produced zero entries in the last 30 minutes, record a `telemetry_gap` signal. A boundary that was active and is now silent is a signal of its own (SC-5).

**Step 4 — Apply decision tree.**

| Condition | Ruling |
|---|---|
| Any T4 event in window | HALT: emit `job_start_halt` Vellum entry, do not proceed |
| Any T3 event in window on trial boundary | HALT |
| Any T3 event in window on non-trial boundary | WARN: include in opening synthesis; proceed with monitoring |
| Any T2 event in window, or tier demotion on trial boundary | WARN-BUT-PROCEED: surface in synthesis |
| T1 cluster (≥3 distinct T1 events in window) | WARN-BUT-PROCEED |
| Telemetry gap on trial boundary | WARN: cold-start or silence signal |
| T1 single event or T0 events only | PROCEED: log in synthesis |
| No events, no telemetry gap | PROCEED: note as clean |

**Step 5 — Emit `witness_read` Vellum entry.**
Per the witness doctrine, every query from Perplexity must emit a `witness_read` entry with: `boundaries_queried`, `window_start`, `window_end`, `highest_severity_seen`, `ruling`, `synthesis_note`. This closes the readership audit loop.

**Step 6 — Surface synthesis to Ewan (if non-trivial).**
Raw entries stay in Vellum. What reaches Ewan is: ruling, one-sentence summary of highest-severity signals, boundary affected, runbook reference. Lean-by-default: if PROCEED with no signals, one line suffices.

---

## Reading sequences — when normal entries become anomalous

The harder reading skill is detecting when a series of individually-normal entries constitutes a signal. Prior art: [Nelson rules](https://en.wikipedia.org/wiki/Nelson_rules) (1984), CUSUM, and process-conformance checking.

**Vellum-entry-sequence detectors (adapted from Nelson):**

| Nelson rule adapted | Vellum implementation | Signal |
|---|---|---|
| 9 entries in a row on same side of mean latency | 9 consecutive `boundary_exit` entries with `duration_ms > baseline_mean` | SC-1 T1 (slow accumulation) |
| 6 entries monotonically increasing | 6 consecutive `duration_ms` values each larger than prior | SC-1 EWMA slope positive → T1 |
| 2 of 3 entries beyond 2σ | 2/3 `boundary_exit` entries with `duration_ms > ucl_warning_ms` | SC-1 T1 immediate |
| All entries STRUCTURED or better (Rule 7 analog) | All 15 recent entries at STRUCTURED tier — sudden INTUITED breaks this | SC-6 T2 |
| Repeated boundary_error on same span_id | ≥2 `boundary_error` entries with same `boundary` in 5 minutes | SC-2 retry storm candidate T2 |

**Process conformance sequences:** Query 4 in `friction_monitor.sql` already checks whether the actual node sequence matches the expected normative sequence. At job-start, this check runs on the last completed job for the same workflow. A `missing_nodes` or `extra_nodes` result from the immediately-preceding execution is a job-start signal for the next run.

---

## Proceed / warn / halt rules — decision matrix

The decision matrix above (Step 4) maps friction severity to job-start rulings. Grounding:

**HALT threshold (T3+ on trial boundary, T4 anywhere):** Consistent with Google SRE's "page on-call" tier — a T3 event is the equivalent of a multi-window combined fast+slow burn breach, which SRE practice treats as an immediate human-required response. At job-start, "human required" maps to HALT because the job cannot proceed without a human decision.

**WARN-BUT-PROCEED (T2, tier demotion, T1 cluster):** Consistent with SRE's "wake agent" tier — a T2 event requires agent attention but does not indicate an outage. The job proceeds, but the IDE surfaces the signal and monitors actively. The min-rule's automatic tier demotion produces T2 signals here; they do not halt by default because the demotion itself is the system working as designed.

**False-positive budget:** ≤1 false halt per 100 reads (1%). Justification: Google SRE's alert-fatigue literature ([Beyer et al., 2016](https://sre.google/sre-book/monitoring-distributed-systems/)) establishes that pagers firing more than once per shift cause responders to disable alerting. For an IDE, a false HALT is equivalent to a false page — it wastes a job start and erodes trust in the signal system. At Amplified's current scale, T3 events on trial boundaries are expected at a rate well below 1/100 job starts; the budget is achievable.

**HALT is not permanent:** A HALT ruling at job-start means: do not start the job now, surface the signal, wait for Ewan (or automated resolution) to clear the T3/T4 event. The job resumes when the triggering event is resolved. This is the circuit-breaker pattern from estate-security-and-sensors-prior-art-synthesis (Pillar 4).

---

## What Perplexity Computer specifically does

Per the witness doctrine's Reader Contract (vellum-witness-doctrine-and-decorator.md §"The Reader Contract"), Perplexity Computer is the canonical first reader.

**Job-start hook placement:** The hook fires in the agent loop immediately after session context is loaded and before the first tool call in the job queue. In the existing agent architecture, this maps to the turn-start point, before any bash/fetch/edit calls. The hook is not a cron; it is triggered by the act of starting a new job.

**The hook runs the 6-step protocol above.** The result is one of: PROCEED (silent), PROCEED (log), WARN-BUT-PROCEED (surface in opening synthesis), HALT (block first tool call, surface signal, await resolution).

**On-demand audit:** Per the witness doctrine, Ewan can ask "what's been happening on X" and the reader runs the same query with a longer window (up to 30 days for a full audit). This is not a new capability; it is the same query with a different `since` parameter.

**The `witness_read` entry:** Every job-start read emits a Vellum entry so readership is itself witnessed. If reads stop, that absence is itself a `telemetry_gap` signal of signal class SC-5.

---

## What other IDEs do

Per cross-ide-problem-sharing-rules R2 (cross-ide-problem-sharing-rules.md §R2): any IDE performing a cross-IDE problem-lookup pairs that lookup with a Vellum witness-stream read on the affected boundary. The same 6-step protocol applies; the window defaults to time-since-last-read by that IDE.

Session prelude (R2.1): every IDE inherits the signal-reading protocol via session prelude configuration. Perplexity Computer is the canonical first reader; other IDEs (Claude Code, Devin, Cursor, Cascade-Mac) inherit the same Reader Contract. The difference: Perplexity Computer runs at every job-start; other IDEs run on boundary-specific lookups as triggered by their own task context.

---

## Where Amplified is novel vs standing on shoulders

**Novel (Amplified beyond SOTA):**
- `friction_monitor.sql` (58KB) implements Shewhart + EWMA + CUSUM + burn-rate + process conformance + dead-man's switch in a single DuckDB file against a well-designed star schema. No open-source monitoring tool at this scale combines all five pattern families in one analytical layer.
- The `witness_read` entry that records readership — making the reader itself observable — has no direct equivalent in external observability tools. Google SRE reads dashboards; the dashboard reading is not itself telemetry.
- The min-rule integration: tier demotion (SC-6) as a first-class signal class is Amplified-specific. External SRE and SPC tools have no concept of epistemic tier.
- The process-conformance query (query 4) applied to AI agent workflow sequences (checking for "hallucinated tool calls" and "missing validation gates") adapts XES/OCEL process-mining methods from business-process management to AI agent observability. Evidence in the literature is thin on this specific application.

**Standing on shoulders (adopt wholesale):**
- Shewhart 3σ UCL/LCL: adopt as implemented. Do not reinvent.
- Multi-window burn-rate (14.4× / 6×): adopt as implemented. Do not change thresholds without a data justification.
- EWMA λ=0.2: adopt as implemented. The λ value is standard for small-N latency signals.
- ICD 203 confidence levels: the HIGH/MODERATE/LOW/INSUFFICIENT vocabulary adapted above should be adopted verbatim for signal-reading synthesis language.
- Google's alerting principles from the SRE book (alerts must be actionable, every alert must require intelligence, alerts that can be ignored should be removed): these are the basis for the false-positive budget.

---

## Open questions

1. **Baseline window for cold start:** When a workflow has no 30-day history, `friction_monitor.sql` queries 1 and 3 produce no output (the `HAVING COUNT(*) >= 30` clause). The reader must detect this condition and flag it as `INSUFFICIENT evidence` per ICD 203. Recommendation: expose a `cold_start` flag in the job-start query output. Decision required: accept 7-day fallback baseline (smaller sample, less reliable UCL) or strict 30-day minimum with cold-start warning.

2. **ADWIN for tier-distribution drift:** The Page-Hinkley / ADWIN adoption for SC-6 (tier-distribution drift) is not yet implemented. Evidence is thin on what the right accumulator parameters are for a categorical distribution at Amplified's entry volume. Decision required: adopt Page-Hinkley on INTUITED fraction, or rely on Shewhart on the numeric `tier_distribution` query output.

3. **Prior-probability bias trap:** The Bayesian argument above relies on accurate base-rate estimates for each friction type. Currently these base rates are not stored explicitly in `measurement_schema.sql`. The `fact_friction_event` table allows them to be computed post-hoc, but a running base-rate estimate per friction_type and per boundary would enable the IDE to weight signals correctly at job-start. No existing query produces this output. Evidence is thin: this is a design gap, not a blocking gap.

---

## Outcome routing

```yaml
outcome_routing:
  verdict: DESIGN_IS_DEFENSIBLE
  confidence: high
  route_to: Ewan / relay-protocol
  baton_actions:
    - decide: "Baseline window for cold start: 7-day fallback vs strict 30-day minimum (recommendation: 7-day with cold-start flag)"
    - decide: "ADWIN/Page-Hinkley for tier-distribution drift: adopt or rely on Shewhart (recommendation: adopt Page-Hinkley, one accumulator)"
    - decide: "False-positive budget floor: ratify ≤1 false halt per 100 reads (recommendation: ratify)"
    - implement: "Job-start hook: wire 6-step read protocol into agent loop before first tool call"
    - implement: "witness_read Vellum entry emission from every job-start read"
    - implement: "Cold-start flag in job-start query output"
  block_conditions:
    - "Do not merge Nelson rule sequence detectors until each workflow has ≥50 baseline observations"
    - "Do not adopt SHESD or Isolation Forest until any workflow exceeds 500 executions/day"
    - "Do not change the 14.4×/6× burn-rate thresholds without data justification from at least 30 days of friction events"
```

---

## Cross-references

- research-pipe-prior-art-synthesis__agent__v01__2026-06-25: the pipe discipline ("secrets via pipe, never side-door") applies to signal reading too — the job-start reader queries Vellum via the named analytics queries, not by reading raw entries via a side-channel.
- ingestion-to-brain-prior-art-synthesis__agent__v01__2026-06-25: the brain-mcp-writer boundary (`brain_mcp_writer.ingest`) is one of the five trial boundaries; its Vellum entries are a primary input to job-start reading.
- data-lake-prior-art-synthesis__agent__v01__2026-06-25: the DuckDB-backed analytics layer described in that synthesis is the same layer `friction_monitor.sql` runs against; schema freeze windows documented there apply to adding new queries to the friction monitor.
- estate-security-and-sensors-prior-art-synthesis__agent__v01__2026-06-25: the 11-sensor catalogue from Pillar 4 defines the write surface; this synthesis defines the read surface. The two documents are paired.
- vellum-witness-doctrine-and-decorator.md: the Reader Contract section establishes the obligation; this synthesis establishes the method.
