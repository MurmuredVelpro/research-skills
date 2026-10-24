# 六个 skill 升级改造起飞（第四轮）

- status: flying
- workspace: autopilot/six-skill-takeoff
- base: 98b1ffea0f093462c88ed7c30d6bb2293cfc6e7c <!-- policy import commit -->
- cut from: 3b2e391eaf1190ccc01d43fa1a1d6df08b3ad010 <!-- main -->
- tested commit: 98b1ffea0f093462c88ed7c30d6bb2293cfc6e7c
- contract: docs/autopilot.md — in force since 2026-10-10; this run's scope, policy JSON, dependency provisioning and reviewer fallback confirmed by the human 2026-10-24 (AskUserQuestion at takeoff)
- mode: full
- host: strict (bwrap usable; `host-doctor.sh` at 98b1ffe)
- policy: docs/autopilot-policy.json at the pinned commit
- helper pin: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- current: stage 1 build

## Goal

「对这6个skill进行升级改造起飞。」——在上一轮打分（lit-search 8.5 / scholar-slides 8.0 /
medical-imaging-review 8.0 / research-proposal 7.5 / research-paper 6.5 / paper-slide-deck 6.5）
基础上，补每个 skill 最明显的短板：把只存在于文字里的门禁变成可执行、可证伪的检查。

Human-confirmed scope (2026-10-24): six stages below; dependency provisioning with network into
`/home/ubuntu/jason/research/.autopilot-deps` (outside the repo) before takeoff only; reviewer =
fresh-context Claude subagent (same model family — disclosed), targets-only adversary request per
stage, adversary review deferred to landing (≤2 rounds), plus an independent landing audit.

## Preflight

| check | how | result | evidence |
|---|---|---|---|
| working tree clean | `git status --porcelain` | only this record untracked | (terminal) |
| host sandbox | `host-doctor.sh .` | strict — bwrap usable | (terminal; recorded here) |
| dry run | `run-gate.sh --dry-run` | sandbox bwrap, 10 commands, helper pin 3790b927… | (terminal; recorded here) |
| machine gate at base | `run-gate.sh` label `gate-base` (10 contract commands, offline-translated) | FAILED: lit-search venv python symlinked to uv-managed CPython outside `read_paths` (exit 127, environmental) | `gate-base.md` |
| machine gate at base, venv rebuilt on /usr/bin/python3 | label `gate-base-r2` | all 10 green, but doubled `-q` hid two pytest summaries | `gate-base-r2.md` |
| machine gate at base, final command set | label `gate-base-r3` | all 10 green: lit-search 868 passed/15 skipped, ruff clean, scholar-slides py 86/8 skipped, node 79/0, MIR 120, psd py 11, psd node 12/0, research-paper 7, research-proposal 6, repo 4; sandbox probes PASS | `gate-base-r3.md` |

Machine gate translation (contract commands → offline sandbox form; semantics unchanged —
proposed as a contract amendment below):

1. `cd lit-search && $DEPS/lit-venv/bin/python -B -m pytest -p no:cacheprovider -o pythonpath=src`
2. `cd lit-search && $DEPS/lit-venv/bin/ruff check --no-cache .`
3. `cd scholar-slides && $DEPS/ss-venv/bin/python -B -m pytest -p no:warnings -p no:cacheprovider`
4. `cd scholar-slides && node --test tests/*.test.mjs`
5. `cd medical-imaging-review && python3 -B -m pytest tests/ -q -p no:cacheprovider`
6. `cd paper-slide-deck && python3 -B -m pytest tests/ -q -p no:cacheprovider`
7. `cd paper-slide-deck && node --test tests/*.mjs`
8. `cd research-paper && python3 -B -m pytest tests/ -q -p no:cacheprovider`
9. `cd research-proposal && python3 -B -m pytest tests/ -q -p no:cacheprovider`
10. `python3 -B -m pytest tests/ -q -p no:cacheprovider`

`DEPS=/home/ubuntu/jason/research/.autopilot-deps`; `GATE_SETUP` copies the pre-installed
`node_modules` (npm ci from the committed lockfiles) into the two policy `write_dirs`;
`PLAYWRIGHT_BROWSERS_PATH=$DEPS/ms-playwright`. lit-search venv was built with
`uv sync --frozen --no-install-project --group dev` so the gate imports `src/` of the pinned
worktree, never an editable install of the original checkout.

## Acceptance criteria

Frozen at takeoff. A run changes `status` and `evidence`, never the criterion; a criterion that turns out wrong gets an erratum below.

| id | criterion | proven by | status | evidence |
|---|---|---|---|---|
| C1 | research-paper ships `scripts/check_paper.py <draft> --ledger <results_ledger.csv> --bib <references.bib>` that exits 1 and names the offending item for each of: (a) a metric-like number in the draft prose (decimal, percentage, or `n=`/`N=` count) absent from the ledger's value column and not inside a `[PENDING…]` flag; (b) a `[@citekey]` with no bib entry, and a bib entry never cited; (c) a placeholder or AI-tell hit; (d) a `checklist_*.md` table row whose disposition column is empty — and exits 0 on a clean fixture; SKILL.md Phase 5 runs it | `research-paper/tests/test_check_paper.py` in the machine gate; mutants per clause | open | |
| C2 | research-proposal ships `scripts/check_proposal.py <proposal.md>` that exits 1 naming the orphan for an in-text citation without a References entry and for a References entry never cited, in both APA author-year `(Author, Year)` / `(Author et al., Year)` and numeric `[N]` (GB/T 7714) styles; exits 1 on a placeholder or AI-tell hit in the body; does not flag the documented scaffold personalization fields (`[University/Institution Name]`, `[所属学科]`, `[Figure N Suggestion]` …); exits 0 on a clean fixture in each style | `research-proposal/tests/test_check_proposal.py` in the machine gate; mutants per clause | open | |
| C3 | the shared gate core `integrity_gate.py` exists in both `research-paper/scripts/` and `research-proposal/scripts/`, both checkers import it, and a repo-level test fails when the two copies differ by any byte | `tests/test_vendored_gate_core.py` in the machine gate; mutant that edits one copy | open | |
| C4 | `lit screen --limit N --sample random --seed S` screens N in-window records chosen by seeded random sampling — same seed ⇒ same set; on a fixture whose prefix differs from the sample the set is not the first-N prefix — and records the sample method and seed in `screening_trial.json`; `--sample random` without `--limit` exits 2; default `--sample head` keeps the existing prefix behavior | `lit-search/tests/test_screen_sample.py` in the machine gate; mutants | open | |
| C5 | scholar-slides QA (`deckTypeAudit` wired into `qa_report.mjs`) emits, by `meta.deck_type`: `journal-club` (also when absent) → a P2 finding per missing `critique-concerns` / `discussion-questions` slide; `defense` → P2 when there is no Backup/Appendix `section` divider followed by at least one slide, and P2 when no slide title names limitations or future work; `conference` → P3 when a `critique-concerns` slide is present; an unknown `deck_type` → P1 naming the allowed values. A conforming deck of each type yields no deck-type finding | `scholar-slides/tests/deck_type.test.mjs` in the machine gate; mutants | open | |
| C6 | paper-slide-deck: `generate-slides.py` records every slide it writes (filename + sha256) in `generated.json`; `merge-to-pptx.ts` and `merge-to-pdf.ts` exit non-zero naming each recorded slide that has no `proofread.json` entry or whose entry's sha256 no longer matches the file; `[CHECK]`-status entries are listed but allowed; `--allow-unproofread` turns the refusal into a printed warning; a deck with no `generated.json` (extract-only) is unaffected | `paper-slide-deck/tests/proofread.test.mjs` + `tests/test_generate_slides.py` in the machine gate; mutants | open | |
| C7 | medical-imaging-review ships `scripts/import_litsearch.py --project-dir P --run-dir R --searcher-id ID` that copies the lit-search delivery files present (`dois.md`, `references.md`, `PRISMA.md`, `coverage_report.md`, `references.bib`, `topic.yaml`) into `P/search/exports/litsearch-<run_id>/`, refuses (non-zero, nothing written) when that directory already exists or when `PRISMA.md`'s total-identified count is missing/unparseable, and otherwise appends exactly one `search/search_log.csv` row whose `result_count` equals that count and whose strategy/export paths point at the copied files, such that the audit's search-log check reports no search-log problem for that row | `medical-imaging-review/tests/test_import_litsearch.py` in the machine gate; mutants | open | |

`status` is `open`, `proven`, `failed` or `parked`. At landing none is `open`. `proven` cites current evidence and, for a check the run wrote, the mutant that proves it can fail.

### Independent mutation targets

Full mode: at least one target selected by the adversary for each criterion.

| criterion | selected by | source condition / failure | patch | baseline | result / evidence |
|---|---|---|---|---|---|

### Evidence integrity

(filled at landing)

### Criterion errata

Append only. The human rules on each at landing.

| id | criterion | what is wrong | evidence | proving instead |
|---|---|---|---|---|

## Stages

1. [ ] research-paper executable gate — owns C1
2. [ ] research-proposal executable gate + shared core + 开题报告篇幅 — owns C2, C3
3. [ ] lit-search seeded random calibration sample — owns C4
4. [ ] scholar-slides deck-type audit — owns C5
5. [ ] paper-slide-deck proofread gate — owns C6
6. [ ] medical-imaging-review lit-search import + duplicated sentence — owns C7

## Ledger

### Decisions

| id | stage | chose | rejected | wrong if |
|---|---|---|---|---|
| D1 | takeoff | strict bwrap policy with `deny_network: true` (contract red line: no paid/network API calls; every gate is fixture-based) | `env-clean` without network denial | a gate legitimately needs network |
| D2 | takeoff | dependencies pre-installed outside the repo, read via `read_paths`; node_modules copied into new `write_dirs` by `GATE_SETUP` | `share_dirs` (only top-level dirs allowed; ours are nested) | copied node_modules diverge from the lockfiles |
| D3 | takeoff | adversary: targets-only request per stage; full adversary review deferred to landing | per-stage full adversary review | a stage defect is only catchable before later stages build on it |

### Review findings

| id | round | reviewer | finding | status | note |
|---|---|---|---|---|---|

### Parked

| id | needs | exact action | unblocks | verify afterward |
|---|---|---|---|---|

### Proposed contract changes

1. Machine-gate commands: record the offline-sandbox translations above (absolute venv
   interpreters, `-B -p no:cacheprovider`, `-o pythonpath=src` for lit-search) as the
   contract's gate commands, and add the new test files each stage introduces.
2. Review: the contract names Codex as review gate; this host has no Codex CLI. Name the
   allowed fallback reviewer (fresh-context subagent, same family) explicitly.

### Not verified

(filled at landing)

## Acceptance walk

(filled at landing)

## Resume log

| when | saved current | found | repeated |
|---|---|---|---|
