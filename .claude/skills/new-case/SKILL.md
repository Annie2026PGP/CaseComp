---
name: new-case
description: Scaffold a new case-competition folder under cases/ from the repo's templates. Use when the user wants to start, begin, or set up a new case, competition, or prompt.
---

# New case

Sets up a new `cases/<case-slug>/` folder so a case competition starts in
the repo's standard structure.

## Steps

1. Ask the user (if not already given): case/competition name, and the due
   date if known.
2. Derive `<case-slug>` as `YYYY-MM-competition-name` (kebab-case, current
   year/month unless the user gives a different date).
3. Create:
   ```
   cases/<case-slug>/brief.md       (from templates/brief.md)
   cases/<case-slug>/research/
   cases/<case-slug>/analysis/
   cases/<case-slug>/deck/
   cases/<case-slug>/submission/
   ```
   Use `.gitkeep` in the empty subfolders so they're tracked by git.
4. Fill in the `brief.md` header fields (competition, received date, due
   date, team) from what the user provided; leave the Prompt section for
   the user to paste in, unless they already gave you the prompt text.
5. Confirm the folder path back to the user.
