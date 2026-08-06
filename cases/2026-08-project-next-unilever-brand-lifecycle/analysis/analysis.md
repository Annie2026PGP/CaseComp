# Analysis — Techtonic Season 8 / Project NEXT

## Problem framing

Two problems nested inside each other. Surface: a Rexona logo went viral
for three seconds; the conventional agency pipeline (brief → sentiment
testing → shoot → localization → legal) takes ~6 weeks, so the moment dies
before anything ships. Real, per the brief: Unilever already has strong
point capabilities (social listening, web scraping, and in reality Brand
DNAi and a digital-twin production engine) but they "operate
independently" — a human manually stitches signal → decision → asset →
publish, every time. The official ask (unlike the earlier working
version) is explicit and structured: (1) redefine the end-to-end lifecycle
and find where AI creates value, (2) propose a *portfolio* of AI products
across it, (3) prioritize with rationale, (4) design ONE product in depth
— user journey, capabilities, AI agents, architecture/governance, human
oversight, cost/timeline — with a mandatory prototype.

## Framework applied

**PULSE** (Perceive-Understand-Localize-Ship-Evaluate) stays as the shared
backbone — one Brand Signal Graph + Brand DNAi orchestration layer — but
is now explicitly the *platform*, not "the product." On top of it sits a
**portfolio of six distinct products**, each owning one lifecycle stage:

| Product | Lifecycle stage | Area of solution | Core tech |
|---|---|---|---|
| **Signal Radar** | Perceive | Unified real-time sensing | Multi-source ingestion, brand/logo recognition, velocity scoring |
| **Playbook Studio** | Understand (pre-built) | Governance & knowledge codification | Rules+ML brand-fit/risk scoring, Brand DNAi rule authoring |
| **Moment Studio** | Localize + Ship (reactive) | Real-time creative production & approval | Multi-agent generation pipeline + human review console |
| **Campaign Composer** | Localize + Ship (planned) | Planned content production | Same generation agents, brief-driven not event-driven |
| **Brand Pulse Dashboard** | Evaluate | Measurement & feedback | Real-time analytics, closed-loop playbook re-scoring |
| **Strategy Compass** | Strategy | Long-cycle positioning | Longitudinal signal analysis, competitive synthesis |

## Prioritization (dependency + time-to-value)

- **Phase 1 — Foundation + first win:** Signal Radar + Playbook Studio are
  prerequisites (nothing downstream works without unified signal and
  pre-codified governance); build them alongside **Moment Studio** as the
  first user-facing product, because it's the fastest, highest-visibility
  proof of value (directly answers the Rexona hook) and forces the
  infrastructure to be built well under real pressure.
- **Phase 2 — Scale production:** Campaign Composer (reuses Moment
  Studio's generation agents at near-zero incremental build cost) +
  Brand Pulse Dashboard (closes the loop, needed to justify further
  investment with real numbers).
- **Phase 3 — Compounding advantage:** Strategy Compass, deliberately
  last — it needs the longest accumulated signal history to be
  trustworthy; building it first would mean shipping strategic
  recommendations off a thin data foundation.

## Deep-dive selection: Moment Studio

Chosen because it's the direct, demoable answer to the case's hook, has
the shortest path to a believable prototype, and touches every required
sub-section concretely:

- **User journey:** Signal Radar detects the armband moment → Playbook
  Studio's pre-scored rules tier it (Tier 1: on-strategy, low-risk,
  high-velocity) → generation agents draft 3 on-brand variants per
  priority market → the "signal editor" reviews on one screen, edits or
  picks a variant, taps approve → one-click multi-market publish → Brand
  Pulse Dashboard closes the loop and updates the playbook's confidence.
- **AI agents (multi-agent pipeline):** Classifier/Tiering Agent (brand-fit
  + risk scoring vs. Brand DNAi), Copy Generation Agent (LLM on Brand
  DNAi voice corpus), Visual Generation Agent (digital-twin compositing),
  Localization Agent (market/language adaptation), Orchestrator Agent
  (sequencing + tier gating + escalation fallback), Learning Agent
  (updates playbook weights from post-publish performance).
- **Governance / human oversight:** revised from the earlier freeform
  version — **no tier auto-publishes without a human tap.** Tier 1 gets a
  single-tap fast-track approval (target SLA: reviewed within 15 minutes,
  not truly zero-touch); Tier 2 requires full review+edit; Tier 3
  escalates to the brand/legal team with no AI auto-drafting. Every
  decision is logged (who approved what, against which playbook version)
  with a kill-switch to recall published content.
- **Cost & roadmap:** illustrative only (no real Unilever cost data
  available) — MVP in ~3 months on one brand/market with a small
  cross-functional squad (~$250-400K illustrative), pilot expansion
  months 4-6, Phase 2 products months 7-12, global rollout year 2.

## Recommendation

Ship the Phase 1 bundle (Signal Radar + Playbook Studio + Moment Studio)
as Project NEXT's first deliverable, prove it on Rexona, then extend the
same backbone to Campaign Composer and Brand Pulse Dashboard before
attempting Strategy Compass — one platform, six products, compounding in
that order rather than six parallel builds.

## Risks & open questions

- Real-time computer-vision detection of an unscripted brand appearance
  (a logo on a match official's armband) is a genuinely hard sensing
  problem beyond text/social listening — flagged as build risk, not
  assumed solved.
- Human-tap approval (even fast-tracked) means "minutes," not literally
  zero seconds — the honest trade-off against a fully autonomous Tier 1,
  made deliberately in favor of governance rigor.
- Cost figures are illustrative planning placeholders, not sourced
  estimates — flagged explicitly rather than presented as researched.
- The prototype is a UI/flow mock-up demonstrating the intended
  experience and decision logic; it is not wired to real Unilever data,
  Brand DNAi, or distribution systems.
