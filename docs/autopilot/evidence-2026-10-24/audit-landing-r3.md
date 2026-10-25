# Landing audit, round 3: six-skill-takeoff (base 98b1ffe, head b00e709)

Scope: landing (C1–C7). Everything was read as of head b00e7095. I used a `git archive` extract at `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/audit3` and a private clone checked out at the head (`.../scratchpad/audit3-git`). I did not modify the repository, its branches, the evidence or the record, and I did not use `run-gate.sh`. All reruns ran on a separate copy (`.../scratchpad/gate3/tree`) under `bwrap --unshare-net`, using the deps in `.autopilot-deps`.

**No blocking findings.** All seven criteria are carried by current evidence: `gate-landing-r3` and the `-land2` KILLED mutants, all at tested commit 1811dc6. There is no code diff between 1811dc6 and the head. I found four minor record issues.

## Findings (most severe first)

1. **minor: ledger R32 and parked row P1. A blocking fix nobody reviewed is not attached to the merge decision.**
   - **Claim:** R32 is `fixed-unreviewed`, and its note says "Blocking". *Not verified* discloses it. P1 asks the human to merge.
   - **What I checked:**
     - `review-landing-r2.json` (identity verified, rc 0) rates the full-width ％/＝ finding as blocking.
     - Fix 0a4dd4e is an ancestor of the head, and test `test_fullwidth_percent_and_equals_are_checked` exists.
     - Mutants `c1-fullwidth-percent-land2` and `c1-fullwidth-equals-land2` are KILLED. I reran both from the committed patches: exit 1, signature matched.
     - An end-to-end probe of `check_paper.py` on `准确率为95％，样本量n＝120` exits 1 and names both numbers.
   - **What is wrong:** the fix holds. But the skill's rule is that a merge requires "no blocking fixed-unreviewed item", and the P1 row (needs / exact action / verify afterward) does not mention R32. Merge is not pre-authorized, so no red line was crossed. Still, the human's merge decision should state this condition.
   - **Fix:** add to P1's *needs* that R32, a blocking `fixed-unreviewed` item, must be accepted by the human or re-reviewed before merge.

2. **minor: ledger R33 and R34. These `fixed-unreviewed` notes do not state a severity.**
   - **What I checked:** the template defines `fixed-unreviewed` as "the note gives its severity". R32's note says "Blocking". The notes for R33 and R34 give no severity.
   - **What it should say:** the landing-r2 reviewer rated R33 MINOR. R34 came from that reviewer's mutation-target list, not from a rated finding.
   - **Fix:** append "minor" to the R33 note, and "minor (targets)" to the R34 note.

3. **minor: the mutation-table summary. Two counts are off, and one duplicate row is not disclosed.**
   - **Claim:** "KILLED adversary/auditor-selected rows per criterion: C1 17, C2 19, C3 5, C4 13, C5 19, C6 20, C7 17".
   - **What I checked:** I counted the table rows that are KILLED and selected by an adversary or the auditor.
   - **What is wrong:**
     - For C1, C2 and C5 the counts are 18, 20 and 20. The stated numbers count adversary rows only and leave out the three R36 auditor rows.
     - `c5-no-future-work-land2` (landing r2) and `c5-future-work-vocab-land2` (s4 #10) carry the same patch, `b57d17f69865…`. The table discloses the equivalent case for C4 ("one row"), but not this one.
   - The per-criterion adversary requirement is met either way.
   - **Fix:** correct the counts, or relabel them "adversary-selected". Note that the C5 landing-r2 target is identical to s4 #10.

4. **minor: six `-land2` mutant files. The committed output does not show the failure signature.**
   - **Affected files:** `c5-backup-severity`, `c5-jc-guard`, `c5-limits-guard`, `c6-allow-ignored`, `c6-mark-sha`, `c6-no-entry-ok`.
   - **What I checked:** for each file, the footer reads KILLED, the baseline exits 0 and the mutant exits 1. But the saved mutant output is a tail that does not contain the `not ok … <name>` line the signature names. Audit r2 noted the same for the `-land` wave.
   - **What I found when I reran them:** I reran all six from their committed patches at the head snapshot. Each exited 1 with its signature matched. Results: `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/gate3/mutant-reruns-r3.md`.
   - **Conclusion:** the claim holds, but the committed evidence alone does not show it.
   - **Fix:** future mutant runs should keep the signature-matching lines in the saved output. Do not rewrite these files; the record could mention that the auditor confirmed them.

## What I checked and found sound

- **Evidence integrity:**
  - `verify-evidence.sh docs/autopilot/evidence-2026-10-24` reports `verified: 390`.
  - Naming all 172 cited or registered files explicitly also verified. That set covers every `.md` and `.json` evidence name in the record, plus all `review-*`, `audit-*` and `gate-landing*` files.
  - There are no `.partial` files and no duplicate MANIFEST entries.
  - The names in the record that are not evidence files (`dois.md`, `PRISMA.md` and others) are criterion text.
- **Currency:** `git diff --stat 1811dc6 b00e709 -- . ':(exclude)<evidence dir>' ':(exclude)<run record>'` is empty.
- **Mutant status:** `mutant-status.py --docs '*.md' . <evidence> b00e709` reports 132 `-land2` KILLED current and 1 INCONCLUSIVE current (`c2-key-case-land2`, superseded by `-land2-r2`, KILLED). Every earlier-wave file is `rerun` and superseded.
- **Table versus evidence:** the table's 133 rows and the 133 `-land2` files are the same set.
- **Mutant validity scan:** I scanned all 133 `-land2` files and read each verdict from its footer. Every file shows:
  - tested commit 1811dc6;
  - baseline exit 0, with no timeout;
  - mutant exit equal to the expected exit;
  - patch sha equal to the table prefix.
  - The signature appears in the output in 126 files; the six exceptions are covered in finding 4.
  - The `ModuleNotFoundError` in `c3-core-missing` is the asserted consequence of deleting a core copy, not a setup failure.
- **Mutant reruns:** besides the six in finding 4, I also reran `c1-fullwidth-equals`, `c1-ledger-leading-dot` and `c7-symlink-guard`, plus `c1-fullwidth-percent` from finding 1. All were killed with their signature matched.
- **Clause coverage:**
  - Every criterion clause has a KILLED mutant, including the naming sub-clauses (R36: `c1-names-item`, `c2-names-orphan`, `c5-names-allowed`) and the C6 naming, C7 nothing-written and C7 symlink clauses.
  - Each criterion has KILLED adversary-selected targets from the stage reviews and from the verified landing reviews r1 and r2.
  - The landing-r2 targets list matches its table rows. Its C4 target equals `c4-unseeded`, as disclosed.
- **Landing gate:** `gate-landing-r3.md` footer: `result: passed`.
  - Tested commit 1811dc6, sandbox bwrap, network denied, probes PASS.
  - All 10 commands exited 0, with counts as recorded: lit-search 885 passed / 15 skipped; ruff clean; scholar-slides py 86 passed / 8 skipped; node 97 pass / 0 fail; medical-imaging-review 140; paper-slide-deck py 15; paper-slide-deck node 32 pass / 0 fail; research-paper 36; research-proposal 42; repo tests 8.
- **Gate rerun:** I reran all 10 translated gate commands directly on the head snapshot under `bwrap --unshare-net`, and got identical counts with every command at exit 0. Output: `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/gate3/gate-audit-r3.md`.
- **Shared core:** the two `integrity_gate.py` copies are byte-identical at the head (`cmp`).
- **SKILL.md:** research-paper Phase 5 runs `check_paper.py`.
- **Reviews:**
  - `review_identity.py verify` returns rc 0 and `validate-findings.sh` (7-argument form) reports valid for `review-landing-r1` (head 2adf0ff), `review-landing-r2` (head 5247c99) and `review-s3-targets`.
  - The s1/s2/s4/s5/s6 receipts match their findings only with the final `\n` removed. Request hashes and input hashes match. This is disclosed as R35 (`minor-open`, reason given).
  - Every landing-r2 finding is in the ledger: the blocking ％/＝ finding as R32, the minor ledger leading-dot finding as R33, and the C7 symlink target as R34.
  - Audit r1 findings are recorded as R28–R31, and audit r2 findings as R35–R37.
- **Ledger:**
  - All statuses come from the template set.
  - Every `blocking-fixed` row (R1, R2, R7, R18, R19, R26) cites a commit that is an ancestor of the head, and a test that exists at the head.
  - There are no `blocking-open` or plain `open` rows.
  - The `minor-open` rows R29, R35 and R37 each state why they stay open.
  - No criterion is `open`, and the errata table is empty.
- **Red lines:**
  - The base..head diff has no deletions, and `docs/autopilot.md` and the policy are unchanged.
  - Run commits exist only on `autopilot/six-skill-takeoff`. `main` and `origin/main` stay at 3b2e391, and no push or PR shows.
  - The gates ran with network denied.
  - The `checks_artifacts.py` refactor is scoped to C7 and attacked by the `c7-refactor-*` mutants.
- **Helper pin:** every evidence header carries inventory `3790b927…3c0`, which matches the pin in the record.

C1: carried — gate-landing-r3 (36 passed) is current, and the `-land2` mutants cover every clause including ％/＝ and naming. R32 is fixed-unreviewed (see finding 1).
C2: carried — gate-landing-r3 (42 passed) is current, the `-land2` mutants cover both styles, both directions, scaffold, placeholder/AI-tell and naming, and `c2-key-case` was repaired with disclosure.
C3: carried — the repo test (8 passed) is current, the cores are byte-identical, and the one-byte, missing and shadowed mutants are KILLED.
C4: carried — gate-landing-r3 (885/15, ruff clean) is current, and the `-land2` mutants cover seed, prefix, record, no-limit exit 2 and head default.
C5: carried — gate-landing-r3 (node 97) is current, and the `-land2` mutants cover every deck type, severity, allowed-values naming and the wiring.
C6: carried — gate-landing-r3 (node 32, py 15) is current, and the `-land2` mutants cover the sha ledger, both merges, [CHECK], the flag and extract-only.
C7: carried — gate-landing-r3 (MIR 140) is current, and the `-land2` mutants cover copy, refusals with nothing written, the symlink case, one row, count/paths and audit acceptance.
