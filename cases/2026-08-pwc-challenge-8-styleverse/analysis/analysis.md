# Analysis — PwC Challenge 8.0 / StyleVerse Global

## Problem framing

StyleVerse is growing (₹5,600 Cr, 15% growth target) but not converting growth
into profit (EBITDA 9.5%, ₹380 Cr markdowns). The case states the conclusion
itself: the **operating model**, not any single function, is the constraint.
Functions each built their own systems, so the handoffs between them are owned
by nobody and bridged manually. The four deliverables — task audit, phase-1
priority + operating model + CoE shape, workforce strategy, governance +
change — all hang off that single diagnosis.

## Framework applied

Built a reproducible model (`analysis/task_audit_model.py`) that derives every
figure in the deck from case Exhibits 3–5, so the numbers can be re-run and
audited rather than asserted.

1. **Three-gate test** for the task audit — rule stability, consequence of
   error, human premium — applied identically to all six functions instead of
   classifying by intuition.
2. **Adoption readiness index** = mean(awareness, willingness, digital skill)
   − 0.5 × (fear − 2.0), from Exhibit 5.
3. **Weighted prioritization score** on exactly the five criteria the case
   names (business impact 25%, customer value 20%, workforce scale 15%,
   automation potential 20%, feasibility 20%).

## Findings

1. **Exhibit 4's "Organization Average" is an unweighted mean.** It reports
   48% routine work — the simple average of the six functions. Weighted by
   headcount the true load is **54.1%**, because the two largest functions
   (Manufacturing 11,000 at 60%; Retail 10,000 at 55%) are the most
   routine-heavy. That 5.7-point gap is ~1,600 FTE-equivalents of routine work
   — larger than the entire Corporate function — that would be missing from a
   plan sized off the headline number.
2. **Target task architecture: 22% Automatable / 60% Augmentable / 18%
   Fundamentally Human.** Applying the case's own 40%-of-routine automation
   cap releases **6,056 FTE-equivalents** (21.6% of the workforce). The
   headline that falls out: *AI touches 82% of the work and replaces 0% of the
   people.* Under Zero-Layoff this is capacity **converted, not cost cut** —
   so no labour saving is claimed anywhere in the value bridge.
3. **The prioritization model independently reproduces leadership's own
   ranking.** The two functions the case marks "Very High" score #1 (Marketing
   & CX, 4.05) and #2 (Retail Operations, 3.95); "High" scores #3
   (Merchandising, 3.55). The model does not overturn management judgment — it
   explains and sizes it, which is a stronger position than contradicting it.
4. **The Readiness Paradox.** Retail Operations is #2 on value but scores
   1.35/5 on readiness (fear 4.3/5, digital skill 2.2/5). Value alone cannot
   set the sequence. Retail therefore enters Phase 1 as a **20-store
   readiness pilot with adoption gates**, not a 200-store rollout.
5. **Manufacturing is deferred despite being the largest prize by headcount.**
   11,000 people, 60% routine — but readiness 0.98/5 and fear 4.5/5.
   Sequencing it early would confirm employees' worst fear and stall the whole
   programme. It moves to Phase 3, paired with EPR traceability so AI arrives
   creating compliance roles rather than removing inspection roles.
6. **One AI policy across five brands would damage the most valuable one.**
   Maison Luxe earns the highest NPS (62) and lowest return rate (8%) because
   customers believe a person made it. Governance is therefore
   brand-differentiated: Maison Luxe back-office only; EcoWeave
   transparency-first; SpeedStyle/UrbanEdge/ThreadBasics AI-forward.

## Recommendation

Phase 1 = **Marketing & CX + Merchandising & Planning at scale, Retail
Operations as a gated pilot**, on a **federated hub-and-spoke AI CoE** (central
platform/standards hub, embedded squads, rotating AI Translators drawn from
existing staff). Fully embedded AI is rejected specifically because it would
recreate the fragmentation that caused the problem. ₹200 Cr allocated 30%
platform / 28% use cases / 22% reskilling / 10% governance / 10% change.

**Value:** ₹311 Cr annual run-rate (markdown ₹133 Cr, returns ₹40 Cr,
attrition ₹20 Cr, AI-attributed revenue ₹118 Cr) against ₹200 Cr one-time —
payback under 12 months, EBITDA 9.5% → 13.1%.

## Risks & open questions

- All value figures are **directional planning estimates built only from case
  exhibits**, not audited data. Key assumptions: markdown reduction at 35%
  pass-through; return cost at 25% of item value; ₹1.2 L replacement cost per
  exit; 5pp of the 15% growth target attributed to AI. All are stated in slide
  footers and Appendix A3, as the brief requires.
- The 40% automation cap is treated as a constraint given by the case, not a
  derived optimum; a function-by-function feasibility study could move it.
- Retail's readiness gates could delay the largest capacity release. The
  mitigation (champions seeded from high-willingness functions first) is
  proposed but unproven at this scale.
- Cycle-time target of 8 weeks assumes concurrent design–merchandising review
  replaces three sequential approval cycles; competitors run under 4 weeks, so
  8 weeks is a deliberately conservative first-phase target.

## Format compliance (verified programmatically)

- Executive Summary 2 slides · Body 10 slides · Appendix 4 slides (limit 50)
- Minimum font size 10.0 pt, zero violations (asserted at build time)
- Fonts used: Georgia (headers, 47 runs) and Arial (content, 591 runs) only
- APA references and stated assumptions in slide footers and Appendix A4
