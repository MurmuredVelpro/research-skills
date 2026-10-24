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
- current: full mutant wave C1–C7 at code freeze

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

1. [x] research-paper executable gate — owns C1 (8243c27, fixes f71400c)
2. [x] research-proposal executable gate + shared core + 开题报告篇幅 — owns C2, C3 (540e4fd)
3. [x] lit-search seeded random calibration sample — owns C4 (b42d040)
4. [x] scholar-slides deck-type audit — owns C5 (a138810)
5. [x] paper-slide-deck proofread gate — owns C6 (3e56794)
6. [x] medical-imaging-review lit-search import + duplicated sentence — owns C7 (see git log)

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
| R1 | s1-targets | claude subagent (same family) | C1(a): `\w` boundaries in METRIC_RE match CJK, so numbers in Chinese prose (`AUC为0.912`) were never checked | blocking-fixed | reproduced (metric_numbers → []); fixed f71400c, test `test_numbers_in_chinese_prose_are_checked` |
| R2 | s1-targets | claude subagent | C1(a): every `[...]` stripped before number matching, so bracketed CIs / link text escaped | blocking-fixed | reproduced; fixed f71400c (strip only flags, citations, URLs), test `test_bracketed_confidence_interval_is_checked` |
| R3 | s1-targets | claude subagent | disclosure guard untested: `--allow-disclosed-flags` could downgrade fake DOIs | minor-fixed | f71400c, test `test_disclosure_flag_does_not_excuse_other_placeholders` |
| R4 | s1-targets | claude subagent | ledger `1,204` read as 1 and 204 → false number-not-in-ledger | minor-fixed | reproduced; f71400c NUMBER_RE, test `test_thousands_separator_matches_the_ledger` |
| R5 | s1-targets | claude subagent | checklist row missing its disposition cell accepted; `- [ ]` and TBD branches untested | minor-fixed | reproduced (`| 3. Data sources |` → []); f71400c, test `test_checklist_unchecked_box_tbd_and_missing_cell_fail` |
| R6 | s1-targets | claude subagent | references-section exclusion not exercised by any test | minor-fixed | f71400c, test `test_references_section_numbers_are_excluded` |
| R7 | s2-targets | claude subagent | C2: auto mode fell back to APA when References were `1. …` / `\[1\]` / `［1］`, silently ignoring every numeric citation (exit 0 with orphans) | blocking-fixed | reproduced (exit 0 with orphan [5]); fixed 60ff5e9 (mixed/mismatch fail closed, numbered-list entries, bracket normalization); tests `test_numbered_list_references_are_reconciled_not_skipped`, `test_escaped_and_fullwidth_brackets_are_normalized`, `test_mixed_citation_styles_fail`, `test_explicit_style_mismatch_fails` |
| R8 | s2-targets | claude subagent | C2: CJK `\w` boundary hid `根据Smith (2020)`; `张伟等, 2020` keyed as 张伟等 | minor-fixed | reproduced; 60ff5e9 ASCII lookbehind, lazy CJK; Chinese narrative author-year documented as unsupported (use GB/T); tests `test_latin_narrative_after_cjk_and_diacritic_surnames`, `test_chinese_et_al_is_keyed_by_the_surname` |
| R9 | s2-targets | claude subagent | C2: Müller/Çelik, `(Smith et al. 2024)`, `(Smith, 2020, 2022)` not parsed | minor-fixed | 60ff5e9; test `test_no_comma_and_multi_year_apa_forms` + diacritic test |
| R10 | s2-targets | claude subagent | C2: leftover instructions under References unchecked; `### 外文文献` sub-heading ended the references section early | minor-fixed | 60ff5e9 (heading-level aware split_body, REF_INSTRUCTION_RE); tests `test_references_subheadings_stay_in_the_references_section`, `test_leftover_instruction_in_references_fails_but_apa_descriptors_pass` |
| R11 | s2-targets | claude subagent | targets marked expected survivors: full-width comma, disclosure guard, AI-tell body-only, figure-label anchor, non-UTF-8 → exit 2 | minor-fixed | 60ff5e9 tests `test_fullwidth_comma_in_numeric_citation`, `test_disclosure_flag_does_not_excuse_other_placeholders`, `test_ai_tell_inside_references_titles_is_not_body`, `test_figure_label_exemption_is_exact`, `test_non_utf8_file_is_usage_error` (+ research-paper `test_non_utf8_draft_is_usage_error`) |
| R12 | s2-targets | claude subagent | C3: import test text-only; local redefinition would pass | minor-fixed | 60ff5e9 `test_each_gate_uses_its_own_copy_without_shadowing` (module identity) |
| R13 | s3-targets | claude subagent | C4: judge-API (jev) path's `parameters.sample` untested | minor-fixed | 2f9d568 test `TestScreenSampleJev::test_jev_random_trial_records_the_sample` |
| R14 | s3-targets | claude subagent | C4: CLI test could not tell whether the given seed reaches selection (seed 5 and default 0 pick the same record) | minor-fixed | 2f9d568 test `test_the_given_seed_reaches_the_selection` (seed 1 picks a different record than seed 0) |
| R15 | s3-targets | claude subagent | C4: `--resume` with a random sample could mix two samples; `--seed` silently accepted with head | minor-fixed | 2f9d568 both refused with exit 2, test `test_seed_without_random_and_resume_with_random_are_refused` |
| R16 | s4-targets | claude subagent | C5: qa_report wiring test only matched source text | minor-fixed | 6322428 spec-only findings split into `specFindings`; test `qa_report carries deck-type findings into the CKPT-3 report` |
| R17 | s4-targets | claude subagent | C5: "Limitations of existing methods" satisfied the defense rule; a divider merely mentioning backup, or followed only by Q&A, counted as an appendix | minor-fixed | 6322428 PRIOR_WORK_RE, anchored BACKUP_RE, CLOSING_RE; five regression tests in deck_type.test.mjs |
| R18 | s5-targets | claude subagent | C6: generate-slides.py main() wiring untested — removing the record_generated call disables the gate with all tests green | blocking-fixed | a4ffe68 test `test_main_records_every_slide_it_generates` drives main() with a stub client |
| R19 | s5-targets | claude subagent | C6: merge-level output untested (naming each slide, [CHECK] listing, --allow-unproofread warning) | blocking-fixed | a4ffe68 tests `<merge> names every unproofread slide on stderr`, `<merge> lists [CHECK] slides and the --allow-unproofread warning` (two-slide fixture, stderr captured) |
| R20 | s5-targets | claude subagent | C6: filename-keyed ledger — renumbered / re-slugged / case-renamed generated slides escape the gate | minor-fixed | a4ffe68 identity by sha256; test `a renamed generated slide is still gated, and its disposition follows its bytes`; recorded-but-missing slides warned |
| R21 | s5-targets | claude subagent | C6: fail-open paths — Gemini Web never writes generated.json; skipped existing slides unrecorded; deleted ledger silent | minor-fixed | a4ffe68 `proofread.ts --record` + SKILL/gemini-web docs; prompts-without-ledger warning; generate-slides names unrecorded skipped slides (`test_unrecorded_existing_...`). The gate still cannot prove a slide is AI-generated when nobody records it — disclosed in SKILL.md wording |
| R22 | s5-targets | claude subagent | C6: slides/ subdirectory slides gated but not markable | minor-fixed | a4ffe68 locateSlide; test `slides in the slides/ subdirectory can be recorded and marked` |
| R23 | s6-targets | claude subagent | C7: failure after rename (window read, log append) leaves an un-retryable half import | minor-fixed | a1d2f2d all refusals before writes, rollback on append failure/audit rejection; test `test_failed_log_append_rolls_back_the_export` |
| R24 | s6-targets | claude subagent | C7: untested guards — unparseable total, optional files, unsafe run id (`$` vs fullmatch), empty leftover dirs, empty pre-existing export, validate_search_log branches | minor-fixed | a1d2f2d + test commit eced80c; tests `test_unparseable_prisma_total_is_refused`, `test_optional_delivery_files_are_copied`, `test_unsafe_run_id_is_refused`, snapshot includes dirs, `test_empty_preexisting_export_dir_is_refused`, `ValidateSearchLogBranches` |
| R25 | s6-targets | claude subagent | C7: post-import check only warned; foreign search_log header accepted | minor-fixed | a1d2f2d audit rejection of the new row rolls back (exit 2); foreign header refused before writing (`test_foreign_search_log_header_is_refused_before_writing`) |

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
