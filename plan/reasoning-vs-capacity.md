
Self-Model Evaluation Comparison Table
======================================

![Reasoning Power vs. Representational Capacity](images/reasoning-vs-capacity.png)
**Figure 2.** Reasoning Power vs. Representational Capacity (from Table 1).

We evaluate selected self-models of contemporary systems
against two human baseline self-models.

This list provides short descriptions of the selected systems,
the type of self-models evaluated and some of the assumptions taken.
Detailed evaluation reports are available in the companion repository [4].

*   **Map:** A map exhibits very rich spatial data 
    (high $R \approx 40{,}000$), but has no reasoning power at 
    all ($P=0$). For the evaluation we have
    chosen an average municipal city map with ~1,000 geometric
    shapes with ~40 bits each.
*   **Stateless LLM:**
    LLMs (Large Language Models) act as powerful reasoning engines
    with performance similar to humans. We estimate $P \approx 3{,}300$
    by applying Bialek scaling to the ~1,000 effectively attended
    tokens across ~100 Transformer layers. However, without
    persistent state, LLMs score zero in $R$ and thus $FCS = 0$.
    This result is deliberate: FC measures self-modeling capacity,
    not raw intelligence. 
    Each LLM forward pass is a fresh function evaluation
    with no access to prior inferences or internal state history.
    The dramatic leap to ~6.5M for Generative Agents (below)
    confirms that FC correctly identifies the agentic scaffold—memory,
    reflection, and persistent state—not the base model, as the
    locus of functional consciousness.
*   **LIDA Cognitive Architecture [12]:** LIDA models the *conscious
    cycle* of Global Workspace Theory [2]. While it possesses numerous
    self-models, its representations are shallow ($\bar{D}=4$) and its
    symbolic reasoning is limited to simple activation arithmetic
    ($P=33$). Due to this combination, LIDA scores below the Roomba 
    on its best single self-model. This aligns with its design as a 
    theoretical showcase rather than a high-performance inference 
    engine.
*   **Roomba with SLAM:** These robots possess a basic spatial 
    self-model but have limited reasoning power ($P$) [11].
*   **ACT-R:** The ACT-R cognitive architecture models reasoning
    through a tightly constrained central bottleneck of buffers and
    production rules. We evaluate its declarative memory and active
    buffer system (the cognitive domain). Due to its utility-learning
    production selection, its reasoning power ($P \approx 50$) out-scales
    LIDA's activation arithmetic, though its tight working memory
    bottleneck limits its overall capacity ($R \approx 160$).
*   **Waymo L4:** The Waymo possesses sophisticated spatial self-
    models with integrated uncertainty, health monitoring, and
    trajectory simulation. It exhibits cross-domain reasoning (e.g.,
    correlating sensor reliability with trajectory planning).
*   **Generative Agents:** Stanford's "Smallville" agents [19] use
    a LLM with memory streams, reflection, and social interaction.
    They possess rich episodic and social self-models but lack
    embodiment. We score the `episodic` self-model,
    which includes the memory stream, reflection nodes, and retrieval
    system. Please note that the $P$ score is lower than the
    stateless LLM, because the agent architecture acts as a bottleneck.
*   **Human (kinematic):**
    We score the narrowly defined kinematic self-model, which literature
    estimates to have ~550 state variables
    (joint angles, actuator feedback, vestibular data).
    The reasoning power ($P \approx 1{,}826$) reflects the
    cerebellum's role as a predictive forward model for motor planning.
*   **Human (working mem.):**
    Quantifying the human episodic/cognitive self-model requires strict
    boundary assumptions to remain tractable. Rather than scoring the
    entire lifetime store of autobiographical memory, we analyze the
    *active working set* engaged during a single episode of reflective
    reasoning. Drawing on cognitive science estimates of working memory
    and narrative reconstruction [10], we estimate $B \approx 330$
    actively maintained variables (perceptual features, social actors,
    causal links), with $\bar{D} \approx 14$ bits (effective resolution 
    of ~1:16,000 for high-fidelity cognitive nuance) reflecting rich 
    multi-modal content. The resulting reasoning power
    ($P \approx 3{,}000$) reflects the massive parallelism of biological
    associative expansion and is comparable to a transformer LLM
    ($P \approx 3{,}300$). This aligns with the empirical observation
    that LLMs approach human-level reasoning depth.

The following table summarizes the benchmark results.
The specific valuations are intended as order-of-magnitude estimates to
illustrate the discriminatory power of the FCS metric.
Rather than treating these numbers as definitive constants, the primary
contribution here is the metric framework, which allows domain experts
to derive precise measurements based on architectural details.
Details for each evaluation are available in the companion repository [4].

**Table 1. System Self-Model Comparison Table**

| System | B (v) | $\bar{D}$ (bits/v) | P | FCS |
| :--- | ---: | ---: | ---: | ---: |
| Map | ~1k | ~40 | 0 | 0 |
| Stateless LLM | 0 | 0 | ~3.3k | 0 |
| LIDA (cognitive) | ~20 | ~4 | ~33 | ~2.6k |
| Roomba (kinematic) | ~18 | ~8 | ~39 | ~5.6k |
| ACT-R (cognitive) | ~20 | ~8 | ~50 | ~8.0k |
| Waymo (kinematic) | ~40 | ~14 | ~133 | ~74.5k |
| Gen. Agents (episodic) | ~130 | ~100 | ~497 | ~6.5M |
| Human (kinematic) | ~550 | ~10 | ~1.8k | ~10M |
| Human (working mem.) | ~330 | ~14 | ~3.0k | ~13.9M |

