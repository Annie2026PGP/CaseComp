---
name: case-writeup
description: Draft or update the analysis write-up for an existing case, following the repo's standard analysis template. Use when the user wants to write up findings, draft a recommendation, or turn research into an analysis doc for a case.
---

# Case write-up

Turns research/notes for a case into a structured `analysis/` write-up
following `templates/analysis.md`.

## Steps

1. Identify which `cases/<case-slug>/` the user means (ask if ambiguous or
   there are multiple in-progress cases).
2. Read `cases/<case-slug>/brief.md` and everything under
   `cases/<case-slug>/research/` to ground the write-up in the actual
   prompt and sourced findings — don't invent facts not in the research.
3. Produce or update `cases/<case-slug>/analysis/write-up.md` using the
   structure in `templates/analysis.md` (problem framing, framework
   applied, findings, recommendation, risks & open questions).
4. Keep the recommendation section to one clear recommendation with its
   top supporting reasons — not a list of options.
5. Point out any question from `brief.md` that the current research
   doesn't yet answer.
