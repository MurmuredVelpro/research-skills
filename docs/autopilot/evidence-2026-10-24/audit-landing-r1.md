# Landing audit: six-skill-takeoff (base 98b1ffe, head 2adf0ff)

Scope: landing (C1–C7). I read everything from a `git archive` of the head, extracted to
`/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/audit/head`. I made no changes to the repository.

**No blocking findings.** Every criterion is carried by current evidence and by KILLED mutants. Four minor record gaps follow.

## Findings (most severe first)

1. **minor: independent mutation targets (C1, C5, C6, C7). The run dropped some of the adversary's targets without saying so.**
   - **Claim:** the record says each criterion was proven by mutants selected per clause ("adversary-selected per criterion: C1 10, …").
   - **What I checked:** the target lists in `review-s1..s6-targets.json` against the mutation table. The run left out some adversary targets that attack criterion sub-conditions, and gave no reason:
     - s1 #2–#4: the C1(a) percentage branch, the `n=` branch, and the `[PENDING…]` exclusion.
     - s4 #3: the C5 P2 severity.
     - s6 #3: the C7 `litsearch-<run_id>` destination name.
     - s6 #5: the C7 rule that a refusal writes nothing.
     - s5 #15, pptx half: the `--allow-unproofread` flag parse in merge-to-pptx.
   - In the run's own evidence these conditions fail only through broader mutants. For example, `c1a-invert-ledger-r2` fails the percentage, sample-size and pending tests through a global inversion of the ledger check, not through the conditions themselves.
   - **What I found when I reran them:** I applied each of these mutants to a scratch copy, using plain python3 and node rather than run-mutant.sh or bwrap. Every one was killed by the expected test. Results are in `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/audit/rerun-mutants.txt`.
   - **Conclusion:** the claims hold, but no committed evidence shows them.
   - **Fix:** run these through `run-mutant.sh` and add them to the table, or record in the table which adversary targets were skipped and why.

2. **minor: merge prerequisite (decision D3 / human-confirmed scope). The landing adversary review is not recorded at the head.**
   - **Claim:** the run's scope says "adversary review deferred to landing (≤2 rounds)". The *Not verified* section lists a "landing adversary" review as one of the reviews done.
   - **What I checked:** the evidence directory and the ledger. The evidence holds only the six stage-targets requests, receipts and findings. They are consistent: each receipt's job_id matches its request, and all base and scope fields are correct. There is no landing-round request, receipt or findings file, and the ledger has no landing-round rows.
   - **Fix:** record the landing adversary review before landing settles:
     - its request and receipt;
     - its findings, entered in the ledger with a status for each;
     - a `blocking-fixed` entry with commit and test for any blocking finding.

3. **minor: machine gate and reviewer versus the contract.** The gate and the reviewer differ from what `docs/autopilot.md` names.
   - **Gate commands:** `gate-landing.md` ran offline translations of the contract's commands, not the commands themselves. For example, it ran the lit-search venv python with `-o pythonpath=src` instead of `uv run pytest -q`.
   - **Reviewer:** the contract names Codex. The run used a Claude subagent from the same model family.
   - **Disclosure:** both are disclosed and offered as "Proposed contract changes". The human confirmation is claimed (AskUserQuestion at takeoff), but nothing in the repository shows it.
   - **Fix:** the human approves the amendment, or confirms at landing that the translated commands are acceptable as the gate.

4. **minor: mutation table labels (C7).**
   - **`mutant-c7-rejection-rollback`:** the record calls this the "R25 audit rejection rolls back" check. Its patch only blanks `searcher_id`. That proves the audit rejection fires and the import exits non-zero; it does not attack the rollback.
   - **`mutant-c7-audit-accepts`:** the table shows only the patch's first hunk. The second hunk, `if rejected:` → `if False:`, is the condition this mutant actually attacks.
   - Neither affects C7's wording.
   - **Fix:** correct the two table rows.

## What I checked and found sound

- **Evidence integrity:** `verify-evidence.sh docs/autopilot/evidence-2026-10-24` on the head snapshot reported `verified: 127 evidence file(s)`, both for the whole directory and with every cited file named explicitly. There are no `.partial` files. All 105 mutant files are cited in the record. Every evidence header carries helper inventory `3790b927…3c0`, which matches the pin.
- **Gate evidence is current:** `git diff --stat a16bf94 2adf0ff -- . ':(exclude)<evidence dir>' ':(exclude)<run record>'` is empty. So `gate-landing.md`, at tested commit a16bf94, is current at the head.
- **Gate-landing result:** its footer reads `result: passed`. All 10 commands exited 0 with these counts:

  | Suite | Result |
  |---|---|
  | lit-search | 885 passed / 15 skipped; ruff clean |
  | scholar-slides python | 86 passed / 8 skipped |
  | scholar-slides node | 96 pass / 0 fail |
  | medical-imaging-review | 138 passed |
  | paper-slide-deck python | 15 passed |
  | paper-slide-deck node | 32 pass / 0 fail |
  | research-paper | 31 passed |
  | research-proposal | 42 passed |
  | repo tests | 8 passed |

  The sandbox was bwrap with network denied, which `deny_network: true` in the policy forces.
- **Mutant status:** I ran `mutant-status.py --docs '*.md' --check <repo> <snapshot evidence> 2adf0ff` and got:
  - 100 KILLED, all current.
  - 1 KILLED needing a rerun: `c1a-invert-ledger`, at 60ff5e9. It is superseded by `-r2`, which is current.
  - 2 INCONCLUSIVE and 2 SURVIVED, all superseded by `-r2` reruns that are KILLED. This matches the record.
  - Commit a16bf94 only appends tests, so earlier mutants stay current.
- **Mutant results:** all footers are read from the final `- finished:` / `- result:` lines. Each KILLED mutant:
  - exited 1, with no timeout;
  - was killed by the test named in its failure signature;
  - patches the condition its row names.
- **Adversary provenance:** each criterion has at least one adversary-selected target that was KILLED, traceable to `review-sN-targets.json`.
- **Gate rerun:** I did not rerun the gate through `run-gate.sh`. That script adds and prunes git worktrees in the repository, and the repository's checkout may be newer than the head, so it would conflict with the no-modification constraint. Instead I ran the 10 gate commands directly on the head snapshot, without a sandbox, using the pre-installed dependencies. All exited 0 with the same counts. Output: `/tmp/claude-1000/-home-ubuntu-jason-research/b455df85-0c58-44bd-8246-2c341fc47f8d/scratchpad/audit/rerun-direct.txt`.
- **Ledger:**
  - All findings R1–R25 use `blocking-fixed` or `minor-fixed`.
  - Each `blocking-fixed` row (R1, R2, R7, R18, R19) cites a commit that is an ancestor of the head, and a test that exists at the head.
  - No criterion is `open`, and no finding is `open` or `blocking-open`.
  - The erratum table is empty.
  - Parked item P1 (landing) is correctly parked.
- **Red lines:**
  - No tracked file was deleted or renamed between base and head.
  - `docs/autopilot.md`, `docs/autopilot-policy.json` and `.github` are unchanged.
  - Local `main` and `origin/main` are both 3b2e391, the commit the run branch was cut from. I could not check the remote itself without network access.
  - The gates ran with network denied.
  - The `checks_artifacts.py` refactor is small and is exercised by C7's audit-acceptance clause; it is not an architectural rewrite.
- **C1 SKILL.md clause:** "SKILL.md Phase 5 runs it" is checked by reading. `research-paper/SKILL.md` Phase 5 (line 104 onward) invokes `scripts/check_paper.py`.

## Per-criterion verdicts

- C1: carried. Gate-landing (research-paper 31 passed) is current; mutants c1a–c1e are KILLED. The auditor's reruns also killed the %/n=/PENDING sub-condition mutants.
- C2: carried. Gate-landing (42 passed) is current; all clauses have KILLED mutants, including the APA/numeric orphans, scaffold exemptions and the two `-r2` repairs.
- C3: carried. Repo tests (8 passed) are current; c3-core-missing, c3-shadowed and c3-one-byte are KILLED.
- C4: carried. lit-search 885/15 is current; every clause has a KILLED mutant (seed, prefix, record, no-limit exit 2, head default), with the resume guard repaired as `-r2`.
- C5: carried. scholar-slides node 96/0 is current; all clauses have KILLED mutants. The auditor's reruns also killed the severity mutants.
- C6: carried. paper-slide-deck node 32/0 and python 15 passed are current; all clauses have KILLED mutants. The auditor's rerun also killed the pptx flag-parse mutant.
- C7: carried. medical-imaging-review 138 passed is current; all clauses have KILLED mutants, with the header check repaired as `-r2`. The auditor's reruns also killed the destination-name and nothing-written mutants.
