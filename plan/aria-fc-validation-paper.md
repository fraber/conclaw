
# The ARIA Experiment

## What the Experiment Actually Provides

The experiment gives you something rare in consciousness research: a **controlled system where ground truth is known**. You built ARIA. You know exactly what self-model infrastructure exists at each phase. You know which files are populated, when reflection runs, what the trust dynamics are. This is the equivalent of a lesion study — you can turn components on and off and measure the effect.

This is fundamentally different from studying humans or black-box AI systems, where the existence of self-models must be inferred. Here, **architectural presence of self-models is ground truth**, and the battery measures whether FCS tracks that ground truth.

This licenses claims that FC's existing paper cannot make.

---

## Desirable Metric Properties That Can Be Addressed

Let me first list the psychometric properties and assess what the experiment can do for each:

**Construct validity** — does FCS measure what it claims?
The experiment provides the strongest possible evidence here. You can show that FCS scores increase monotonically as self-model infrastructure is added (Phase 0 → 1 → 2 → 3 → 4). The architecture IS the construct — so tracking FCS against architecture is direct construct validation, not just face validity.

**Criterion validity** — does FCS predict outcomes it theoretically should?
The economic layer provides an external criterion: food security, trade balance, knowledge accumulation. If higher-FCS agents outperform lower-FCS agents economically, this is criterion validity evidence. The causal story is clean: richer self-models → better decisions → better outcomes.

**Reliability** — does FCS produce consistent results?
The snapshot + multi-run protocol addresses this directly. You can compute inter-run reliability (same architecture, different simulation histories) and show the variance is bounded.

**Structural validity / slice-invariance** — the errata page problem.
The ablation design lets you test whether FCS scores are stable under different variable individuation choices. This is the most technically novel contribution — an empirical test of a formal property that the original paper could only assert.

**Discriminant validity** — does FCS not merely track general capability?
All three agents use the same LLM (Qwen2.5). General reasoning capability is held constant. Any FCS differences between agents must come from self-model infrastructure differences, not raw intelligence. This is a clean experimental control that few other FC validation attempts could achieve.

**Sensitivity** — can FCS detect meaningful differences at the relevant scale?
The Mode A tests give you a fine-grained richness measure. You can show the minimum self-model configuration change that produces a detectable FCS difference.

**The one property you cannot address**: phenomenal consciousness. The paper must be disciplined about this — the experiment validates FC as a metric of self-modeling infrastructure, not as evidence of subjective experience.

---

# Paper


## Paper Outline

**Title**: *Validating Functional Consciousness as a Metric: Evidence from a Controlled Multi-Agent Simulation*


### Abstract (what the paper claims)

We present the first controlled empirical validation of the Functional Consciousness Score (FCS) using ARIA — a purpose-built multi-agent simulation where self-model infrastructure is architecturally controlled and ground truth is known. By systematically varying self-model components across four implementation phases and measuring FCS against both architectural ground truth and economic performance outcomes, we provide evidence for FCS's construct validity, criterion validity, discriminant validity, and structural stability. We further introduce a 41-test evaluation battery (Mode A: file-reading; Mode B: interview) that operationalizes FC measurement for artificial agents without requiring phenomenal claims.

### 1. Introduction

**Argumentation**: The FC metric (Bergmann, AGI-2026) proposed a computable scalar for self-modeling capacity but acknowledged the absence of empirical validation. Psychometric theory requires that any metric demonstrate construct validity, criterion validity, reliability, and structural stability before its scores can be meaningfully interpreted. No existing FC study has provided this validation because the required ground truth — known self-model architecture — is unavailable for biological agents and opaque for most AI systems. We close this gap using a controlled simulation where self-model presence is an architectural fact, not an inference.

### 2. Background

Two sections:

**2.1 FC metric essentials** — FCS = R × P, the 10 self-model domains, FSMA, the known formal gaps (aggregation formula, slice-invariance). Keep this short — assume reader knows the original paper.

**2.2 Psychometric requirements for metrics** — construct validity, criterion validity, reliability, structural validity, discriminant validity. One paragraph each. This section establishes the evaluation framework against which the experiment's results will be interpreted. This framing is what transforms "we ran a simulation" into "we conducted a validation study."

### 3. ARIA Architecture

**Argumentation**: ARIA is designed as a validation instrument, not merely a cognitive architecture. Three design choices are scientifically load-bearing:

First, **architectural control**: self-model components are added in discrete, documented phases (0-4). FCS can therefore be measured at each phase against a known ground truth of which self-models exist.

Second, **constant capability**: all agents use the same LLM (Qwen2.5 7B). Differences in FCS scores between agents or phases cannot be attributed to differences in raw reasoning capability — discriminant validity by design.

Third, **external criterion**: the economic layer (food, tools, knowledge tokens, trade) provides an outcome measure theoretically predicted to correlate with FCS. This is not circular — economic performance is logically independent of self-model richness, but theoretically connected through the mechanism that better self-models enable better decisions.

Describe the file structure, world model, social layer, and economic layer concisely. The key point is that every self-model is a readable file — ground truth is inspectable without inference.

### 4. The Evaluation Battery

**Argumentation**: Existing FC measurement relies on white-box architectural inspection (the Waymo calculation) or abductive inference from behavior (FSMA). Both are manual and non-reproducible. The 41-test battery introduced here provides the first systematic, partially-automatable FC measurement instrument for artificial agents.

Present the battery structure: Mode A (file-reading, 24 tests, no LLM) and Mode B (interview, 17 tests, LLM required). Explain the four tiers and the scoring scheme (exact match / calibrated / confabulation penalty). Explain the ground truth procedure — battery runner reads both agent answer and agent files simultaneously.

Key claim: **Mode A tests measure R directly** (breadth and depth of self-model content). **Mode B tests measure P** (reasoning power over that content). The battery therefore provides the first operationalization of FCS's two components as separable, independently measurable quantities.

### 5. Results

Four subsections, each addressing one psychometric property:

**5.1 Construct Validity**

Show FCS scores by phase (Phase 0 through 4) for all three agents. The prediction is monotonic increase as self-model infrastructure is added. Present as a table and a trajectory plot. If Mode A scores track architectural phase correctly — SOUL.md present → A1.1 passes; reflection running → A3.1 passes — this is direct construct validity evidence.

Key result: FCS score increases are discontinuous, not gradual. Large jumps occur at specific phase boundaries (Phase 1→2 when social layer activates, Phase 2→3 when economics creates cross-model reasoning pressure). This discontinuity is theoretically predicted by the multiplicative aggregation — adding a new self-model domain multiplies rather than adds to P under cross-reasoning — and its empirical appearance strengthens the formula's justification.

**5.2 Criterion Validity**

Show correlation between FCS score (at tick 50 snapshot) and economic outcomes (food security ticks + knowledge holdings + trade balance) across agents. Three agents × multiple simulation runs = a small but interpretable dataset. The prediction: rank ordering of FCS matches rank ordering of economic performance.

This is the paper's most consequential result. Even a modest positive correlation (Spearman ρ > 0.6 across runs) would be significant given N is small. A perfect rank preservation across all runs would be striking. Report honestly — if the correlation is weak, that is also informative and should be interpreted rather than buried.

**5.3 Discriminant Validity**

Show that FCS differences between agents are not explained by LLM capability differences. Since all agents use Qwen2.5, capability is held constant. The Mode B interview scores (which require LLM reasoning) should track Mode A infrastructure scores (which do not) — if they do, self-model infrastructure is the driver, not raw intelligence.

Additionally: show that a stateless Qwen2.5 call (no file context) scores near zero on Mode A tests and produces confabulated answers on Mode B tests. This is the cleanest discriminant validity demonstration — same model, zero self-model infrastructure, zero meaningful FCS score.

**5.4 Structural Validity and Reliability**

Two analyses:

*Slice-invariance test*: score the same agent files under two different variable individuation choices (e.g., count INVENTORY.md resources as 3 variables vs. 1 aggregate variable). If FCS rank ordering across agents is preserved under both choices, the metric is ordinally stable even if absolute values differ. This directly addresses the errata page gap.

*Inter-run reliability*: run the simulation 5 times from identical starting conditions. At tick 50, compute FCS for each agent in each run. Report mean ± standard deviation per agent per phase. Low standard deviation relative to mean = reliable metric. High standard deviation = metric is simulation-history-dependent and requires the multi-run protocol.

### 6. The Battery as a Measurement Instrument

**Argumentation**: Beyond validating FCS, the battery itself is a contribution. Present precision and recall for Mode A tests (how often does a passing Mode A score correctly predict architectural ground truth?). Present calibration of Mode B scores (does the confabulation penalty correctly penalize fabricated answers?).

Introduce the **two-mode separation** as a theoretical contribution: Mode A measures R independently of P, and Mode B measures P independently of R (by holding file content constant across questions). This separability means FCS's two components can be empirically disentangled for the first time — previously R and P were estimated jointly from the same architectural inspection.

### 7. Limitations and Scope

Be explicit about four limitations:

**Scale**: three agents, one LLM, one hardware configuration. Results are proof-of-concept, not population-level statistics. The correlation between FCS and economic outcomes is suggestive, not definitive.

**The simulation-as-construct problem**: ARIA was designed to maximize FCS. Its architecture was built by the same researcher who proposed the FC metric. There is an inherent circularity risk — ARIA might validate FCS because it was built to implement FC's self-model taxonomy, not because FC is tracking something real. Address this honestly: the validation is strongest as a consistency check (FC scores track what the architecture says should be there) and weaker as an independence check.

**Economic criterion limitations**: food security and trade balance are reasonable proxies for adaptive performance but are not the only possible criteria. A future study with a richer criterion battery would strengthen the criterion validity claim.

**Phenomenal consciousness**: nothing in this experiment bears on whether ARIA has subjective experience. FCS measures functional self-modeling capacity. The experiment validates that measurement. The hard problem remains untouched.

### 8. Conclusion

**The argumentation chain in one paragraph**: FC proposed a metric but lacked empirical grounding. Psychometric theory specifies what grounding requires. ARIA provides the experimental conditions under which those requirements can be tested — known ground truth, constant capability, external criterion, architectural control. The 41-test battery provides the measurement instrument. The results show: FCS tracks architectural ground truth (construct validity), FCS predicts economic performance (criterion validity), FCS differences survive capability control (discriminant validity), and FCS rank ordering is stable under variable individuation (structural validity). The metric is not fully validated — scale is small, circularity risk is acknowledged, phenomenal claims are absent — but it is substantially hardened. The battery and snapshot protocol provide a replication target for future work.

---

# What This Paper Accomplishes for FC

To summarize the contribution directly:

The original FC paper was a **metric proposal**. This paper is a **metric validation study**. The distinction matters for how the community receives it — a validated metric can be used; a proposed metric can only be discussed.

The four properties addressed (construct, criterion, discriminant, structural) are exactly the four that were identified as missing in the original paper's audit. The experiment closes all four gaps at proof-of-concept scale, which is appropriate for a first validation study. It explicitly does not claim full validation — that would require larger scale, multiple LLMs, multiple research groups replicating the battery. But it moves FC from "interesting theoretical proposal" to "empirically grounded instrument with known properties and a replication protocol."

That is a meaningful and publishable scientific step.

