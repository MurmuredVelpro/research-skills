# Landing audit, round 2: six-skill-takeoff (base 98b1ffe, head 5247c99)

Scope: landing (C1–C7). I read everything from a `git archive` of head 5247c991 (extracted to `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/audit2`). I did not change the repository, its branches, the evidence or the record. All reruns were done on a separate copy, `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/gaterun/tree`.

**No blocking findings.** Every criterion is carried by current gate evidence and current KILLED `-land` mutants. There are three minor findings.

## Findings (most severe first)

1. **minor: ledger rows R1–R25 and the mutation-table provenance "adversary sN #k". Five of the six stage-review findings files fail their sealed receipts.**
   - **Claim:** the stage-target reviews are registered evidence, and the table's adversary provenance cites them.
   - **What I checked:** I ran `review_identity.py verify <findings> <request> <repo> 98b1ffe <request head> <record> "<scope>" ~/.claude/skills/autopilot` for every review:
     - rc 70 (fail): `review-s1-targets.json`, `review-s2-targets.json`, `review-s4-targets.json`, `review-s5-targets.json`, `review-s6-targets.json`.
     - rc 0 (pass): `review-s3-targets.json` and `review-landing-r1.json`.
   - **What is wrong:** in each failing file, the receipt's `findings_sha256` does not match the committed file. `git log` shows each file was committed only once, already in its current form.
   - **What I found when I tested the cause:** the receipt hash matches the committed bytes once the final `\n` is removed. So a trailing newline was added after sealing, and the findings content itself is unchanged.
   - **Why this is not blocking:** the per-criterion adversary requirement is still met through the verified `review-landing-r1.json`. It supplies one KILLED target for each of C1–C7: split-level, et-al, trailing-newline, last-record, section-as-appendix, status-defined and new-row-index.
   - **Fix:** add a note to the Evidence-integrity section that the s1/s2/s4/s5/s6 seals fail only on a trailing newline added after sealing, and stop rewriting findings files after `seal`. Do not edit the committed files or receipts.

2. **minor: C1 "names the offending item", C2 "naming the orphan", C5 unknown type "naming the allowed values". No recorded mutant breaks the naming itself.**
   - **Claim:** every clause has a mutant that was seen to fail.
   - **What I checked:** the 120 `-land` patches. Every C1 and C2 mutant disables a detection; none removes the name from the output. The `Finding.render` / `finish` output in `integrity_gate.py` is never mutated. For C5, `c5-unknown-type` and `c5-unknown-severity` attack the condition and the severity, but not the allowed-values text. (C6's naming clause does have its own mutants: `c6-name-first-only` and `c6-fatal-print`.)
   - **What I found when I ran probes:** I applied three probe mutants by hand with bwrap `--unshare-net`, not through `run-mutant.sh`. Results are in `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/gaterun/naming-probes.md`. All three were killed:
     - `render` without `{self.detail}`, in research-paper: killed (exit 1, `test_bib_entry_never_cited_fails` and others).
     - The same change in research-proposal: killed (exit 1, `test_apa_entry_never_cited_fails` and others).
     - qa.mjs detail without `DECK_TYPES.join`: killed (`not ok 11 - unknown deck_type is P1 naming the allowed values`).
   - **Conclusion:** the claim holds, but no committed evidence shows it. I rate this minor rather than blocking because the auditor saw each sub-clause fail.
   - **Fix:** run these three through `run-mutant.sh` as `-land` labels and add them to the table.

3. **minor: contract Evidence section and preflight, versus the record.**
   - **What I checked:** `docs/autopilot.md` against the run.
     - **Evidence location:** the contract says evidence lives in `docs/autopilot/evidence/` and is named `<stage>-<label>.txt`. The run used `docs/autopilot/evidence-2026-10-24/*.md`, as set by the policy JSON.
     - **Preflight:** the contract lists `codex --version` and the `acceptance-auditor.md` check, plus the `uv run` commands. The run's Preflight table has no rows for them.
   - **What is wrong:** R29 and P2 propose amendments only for the gate commands and the reviewer. The evidence path and naming, and the two skipped preflight rows, are not disclosed as deviations.
   - **Fix:** add these to *Proposed contract changes* / P2, or to *Not verified*.

## What I checked and found sound

- **Helper pin:** `integrity.py` over the helper scripts gives `3790b927…3c0`, which matches the record. Every evidence header carries that inventory.
- **Evidence integrity:**
  - `verify-evidence.sh docs/autopilot/evidence-2026-10-24` reported `verified: 252`.
  - Naming all 127 cited files explicitly also verified.
  - There are no `.partial` files and no duplicate MANIFEST entries.
- **Currency:** `git diff --stat 9c83160 5247c99 -- . ':(exclude)<evidence dir>' ':(exclude)<run record>'` is empty. So `gate-landing-r2.md` and all `-land` mutants, at tested commit 9c83160, are current at the head.
- **Mutant status:** `mutant-status.py <repo> <snapshot evidence> 5247c99` (strict, without `--docs`) reports:
  - 120 `-land` files, all KILLED and current.
  - Every earlier-wave file is `rerun` and superseded, as the record says.
  - The table rows and the evidence files are the same set of 120. The patch sha prefixes all match.
  - Adversary row counts match the record: C1 15, C2 18, C3 4, C4 13, C5 18, C6 19, C7 16.
- **Mutant validity:** I scanned all 120 `-land` files and read each verdict from its footer only. Every file shows:
  - tested commit 9c83160;
  - baseline exit 0;
  - mutant exit equal to the expected exit;
  - no timeout;
  - patch hash equal to the table's.
  - For 114 files the failure-signature line appears in the saved output. The `FileNotFoundError` / `ModuleNotFoundError` hits in four of them (c3-core-missing, c6-main-wiring, c7-target-name, c7-run-id-safety) are behavioral consequences the tests assert, not setup failures.
  - **The other six** (c5-backup-severity, c5-jc-guard, c5-limits-guard, c6-allow-ignored, c6-mark-sha, c6-no-entry-ok) keep only an output tail that hides the signature line, so I reran them on the snapshot from the committed patches. Each baseline exited 0, each mutant exited 1, and each signature matched. Results: `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/gaterun/mutant-reruns.md`.
- **Landing gate:** `gate-landing-r2.md`, at 9c83160, reads `result: passed` in its footer. The sandbox was bwrap with network denied, and the sandbox probes passed. All 10 commands exited 0, and the counts match the record:

  | Suite | Result |
  |---|---|
  | lit-search | 885 passed / 15 skipped; ruff clean |
  | scholar-slides python | 86 passed / 8 skipped |
  | scholar-slides node | 97 pass / 0 fail |
  | medical-imaging-review | 139 passed |
  | paper-slide-deck python | 15 passed |
  | paper-slide-deck node | 32 pass / 0 fail |
  | research-paper | 34 passed |
  | research-proposal | 42 passed |
  | repo tests | 8 passed |

- **Gate rerun:** I did not use `run-gate.sh`, as instructed. I reran all 10 translated gate commands directly on the head snapshot, under `bwrap --unshare-net`, with the deps in `.autopilot-deps`. All exited 0 with the same counts. Output: `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/gaterun/gate-audit-r2.md`.
- **Landing review r1:**
  - `validate-findings.sh` with the 7-argument form (base 98b1ffe, head 2adf0ff, scope landing) reports valid, and `review_identity.py verify` returns rc 0.
  - The request's file hashes match the record, contract and policy at 2adf0ff.
  - Its one blocking finding is R26, and its "INDEPENDENT MUTATION TARGETS" text lists exactly the 8 landing-r1 table rows.
- **Ledger:**
  - Statuses are all `blocking-fixed`, `minor-fixed` or `minor-open`. The one `minor-open` (R29) says why it stays open and points to P2.
  - Each `blocking-fixed` row (R1, R2, R7, R18, R19, R26) cites a commit that is an ancestor of the head, and a test that exists at the head.
  - No criterion is `open`, and the errata table is empty.
  - R28, R30 and R31 (from audit r1) are addressed: the review is registered, the 10 added mutants are KILLED, and the table rows are corrected.
- **Red lines:**
  - No tracked file was deleted or renamed between base and head.
  - `docs/autopilot.md` and `docs/autopilot-policy.json` are unchanged.
  - The head is only on `autopilot/six-skill-takeoff`. It is not in `main`, and `origin/main` is 3b2e391. I could not check the remote itself without network access.
  - All gates and mutants ran with network denied.
- **Lite mode:** not claimed (`mode: full`), so I did not run `check-lite.sh`.
- **Doc clauses:**
  - `research-paper/SKILL.md` Phase 5 (line 104 onward) runs `scripts/check_paper.py`.
  - `research-proposal/SKILL.md` runs `check_proposal.py`.
  - `medical-imaging-review/SKILL.md` runs `import_litsearch.py`.
- **C4 "in-window":** the in-window filter before `select_trial` was already in the code at base (`cli.py`). It is not a check the run wrote, and the tests sample only in-window keys.

## Per-criterion verdicts

- C1: carried — gate-landing-r2 (research-paper 34 passed) is current; 19 KILLED `-land` mutants cover (a)–(d), exit 1 and the clean fixture. Naming was killed only in an auditor probe (finding 2).
- C2: carried — gate-landing-r2 (research-proposal 42 passed) is current; 22 KILLED `-land` mutants cover APA/numeric orphans in both directions, placeholder/AI-tell, scaffold exemptions and clean fixtures in both styles. Naming was killed only in an auditor probe (finding 2).
- C3: carried — repo tests (8 passed) are current; core-missing, shadowed, one-byte and trailing-newline are KILLED.
- C4: carried — lit-search 885/15 and ruff are current; 14 KILLED mutants cover the seed, not-prefix, record, no-limit exit 2 and the head default.
- C5: carried — scholar-slides node 97/0 is current; 20 KILLED mutants cover every type rule, the severities, unknown type P1, conforming decks and the wiring. The allowed-values naming was killed only in an auditor probe (finding 2).
- C6: carried — paper-slide-deck node 32/0 and python 15 passed are current; 22 KILLED mutants cover generated.json sha, both merges' refusal and naming, [CHECK], `--allow-unproofread` and extract-only.
- C7: carried — medical-imaging-review 139 passed is current; 19 KILLED mutants cover the copy, both refusals with nothing written, one row with the PRISMA count and paths, and audit acceptance.
