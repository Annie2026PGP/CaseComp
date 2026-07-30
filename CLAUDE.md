# CaseComp

This repo holds prep work for business case competitions: research, analysis,
financial models, deck outlines, and final submissions. It's organized so
that every case's work is self-contained and easy to pick back up.

## Folder structure

```
cases/<case-slug>/       One folder per competition/case. See below.
templates/                Reusable templates copied into new cases.
resources/                 Cross-case reference material (frameworks,
                            industry notes, past learnings) that isn't
                            specific to one case.
```

Each case folder under `cases/` follows this layout:

```
cases/<case-slug>/
  brief.md          The case prompt/problem statement as given.
  research/          Source notes, market data, company background.
  analysis/          Frameworks applied, calculations, financial models.
  deck/              Slide outline and drafts.
  submission/        Final deliverables as actually submitted.
```

`<case-slug>` convention: `YYYY-MM-competition-name`, e.g.
`2026-07-acme-strategy-case`.

## Working conventions

- Keep research and analysis as plain markdown (or linked files) inside the
  case folder, not scattered elsewhere — this repo is the source of truth
  for what was done on each case.
- Cite sources inline in `research/` notes (link + one-line takeaway).
- Don't overwrite `brief.md` once a case starts — it's the fixed prompt.
- Final submitted materials go in `submission/`, distinct from drafts in
  `deck/`.

## Skills

Home-grown:
- **new-case** — scaffolds a new `cases/<case-slug>/` folder from
  `templates/` when starting a new competition.
- **case-writeup** — drafts/updates a case's `analysis` write-up in the
  repo's standard structure from research notes.

Vendored from the community (each folder has a `NOTICE.md` with source repo,
commit, and license — see that file before redistributing any of these):
- **management-consultant** — 129 reference modules (case-interview coaching,
  market sizing, M&A/governance case studies) from
  [DogInfantry/claude-skill-management-consultant-B1](https://github.com/DogInfantry/claude-skill-management-consultant-B1)
  (Apache-2.0).
- **management-consulting** — 40+ strategy/financial/operations frameworks
  with worked examples and memo variants, from
  [gcamilo/management-consulting](https://github.com/gcamilo/management-consulting)
  (MIT).
- **market-research** — McKinsey/BCG/Bain-style market research methodology,
  4-level pyramid analysis, source validation, from
  [birne-sk/claude-skills](https://github.com/birne-sk/claude-skills) (MIT).
- **mece** — MECE (Mutually Exclusive, Collectively Exhaustive) validation
  and issue-tree decomposition, from
  [uxderrick/mece-skill](https://github.com/uxderrick/mece-skill) (MIT).
- **clean-slides** — generates clean, McKinsey-style PowerPoint decks from
  YAML (`pptx` CLI), from
  [tmustier/clean-slides](https://github.com/tmustier/clean-slides) (MIT).
  One-time setup: `pip install -e .claude/skills/clean-slides`.

Invoke these by asking Claude Code naturally (e.g. "start a new case for
the XYZ competition", "size this market McKinsey-style", "check this issue
tree is MECE", "build the deck") — no need to remember exact skill names.
