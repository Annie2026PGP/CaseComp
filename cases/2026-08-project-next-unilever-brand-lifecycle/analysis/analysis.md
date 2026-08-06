# Analysis — Project NEXT (AI-first brand lifecycle)

## Problem framing

Two problems are nested inside each other. The surface one: a Rexona logo
went viral for three seconds and the conventional agency pipeline (brief →
sentiment testing → shoot → localization → legal) takes 4-6 weeks, so the
moment dies before anything ships. The real one, stated directly in the
brief: Unilever already owns strong point capabilities (social listening,
web scraping, and — in reality — Brand DNAi and a digital-twin production
engine) but they "operate independently," so a human has to manually
stitch signal to decision to asset to publish, every single time. The ask
is explicitly *not* "add more AI features" — competitors can buy the same
foundational models — it's "rewire the process."

## Framework applied

Designed **PULSE** — Perceive, Understand, Localize, Ship, Evaluate — an
always-on closed loop that replaces the linear campaign-brief model, built
as the orchestration layer over Unilever's real existing capabilities
(Brand DNAi as the brand-safety/voice layer, the digital-twin engine and
Desire-at-Scale content pipeline as production capacity) rather than a
greenfield AI buildout. The same loop is run at three different clock
speeds — Moments (minutes-hours), Campaigns (weeks), Strategy
(quarters-years) — sharing one compounding Brand Signal Graph, which is
how the design answers "architect the entire brand lifecycle" rather than
just the reactive hook.

## Findings / design decisions

1. **The bottleneck is synthesis, not sensing.** Unilever isn't short on
   listening tools — social listening and web scraping already exist. The
   brief is explicit that they run independently. So the highest-leverage
   build is a unified real-time Brand Signal Graph per brand, not another
   listening tool.
2. **Speed without a standing war room requires pre-built judgment, not
   faster meetings.** Oreo's 2013 "Dunk in the Dark" proved 15 minutes is
   achievable — but only via an expensive, bespoke 15-person live war room
   for one Super Bowl night. PULSE's Understand stage pre-codifies brand
   judgment into scored "playbooks" *before* the moment happens, so the
   in-the-moment step is a lookup + approval, not a live creative debate.
3. **The moat is the compounding signal graph and codified playbooks, not
   the model.** Since any competitor can buy the same LLM, the defensible
   asset has to be proprietary and time-accumulated: Unilever's own
   history of what moments mattered, how audiences reacted, and what
   played safe per brand/market. That can't be bought off the shelf on
   day one — it has to be built, loop iteration by loop iteration.
4. **Governance has to be structural, not a policy document.** PULSE
   tiers every signal (auto-publish / fast-track human approval /
   full escalation) so speed and brand safety aren't in tension — this is
   the direct answer to the case's "cannot afford to lose his cool"
   framing applied to the process itself, not just the copy.
5. **The Brand Manager role changes.** From campaign coordinator chasing
   agency deliverables to "signal editor" — the human who sets playbook
   strategy in advance and approves/edits AI-drafted output in the
   moment, at a fraction of the cycle time.

## Recommendation

Ship PULSE as Project NEXT's core deliverable: one Brand Signal Graph +
tiered Understand layer + production layer wired to Brand DNAi/digital
twins + one-click Ship interface + a Learn loop that feeds back into the
same graph. Prove it first on the Moments loop (lowest risk, fastest
payback, directly answers the Rexona hook), then extend the same
infrastructure to Campaigns and Strategy rather than building three
separate systems.

## Risks & open questions

- Real-time computer-vision detection of an unscripted brand appearance
  (the Rexona armband) is a genuinely hard sensing problem beyond text/
  social listening — flagged as a build risk, not assumed solved.
- Tiered auto-publish carries brand-safety and legal risk if playbook
  scoring is miscalibrated; recommend starting Tier 1 (auto-publish)
  scope narrow and expanding only as the graph accumulates evidence.
- This is a conceptual architecture case with no dataset provided — all
  time estimates (e.g. "4 hours vs 6 weeks") are illustrative, directional
  claims, not measured figures; real Unilever content-time-reduction
  figures (30-50% from generative AI adoption, per cited sources) are
  markedly more conservative and are the honest reference point.
