# 六个 skill 升级改造起飞（第四轮）

- status: flying
- workspace: autopilot/six-skill-takeoff
- base: 98b1ffea0f093462c88ed7c30d6bb2293cfc6e7c <!-- policy import commit -->
- cut from: 3b2e391eaf1190ccc01d43fa1a1d6df08b3ad010 <!-- main -->
- tested commit: 9c831601ca0f29ceed4a67be02e73d35a9b4a21b
- contract: docs/autopilot.md — in force since 2026-10-10; this run's scope, policy JSON, dependency provisioning and reviewer fallback confirmed by the human 2026-10-24 (AskUserQuestion at takeoff)
- mode: full
- host: strict (bwrap usable; `host-doctor.sh` at 98b1ffe)
- policy: docs/autopilot-policy.json at the pinned commit
- helper pin: 3790b927c7b72d6896ca0ce3d0189e16b5efe750f13c858e2e2232badf1ad3c0
- current: landing review round 2

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
| C1 | research-paper ships `scripts/check_paper.py <draft> --ledger <results_ledger.csv> --bib <references.bib>` that exits 1 and names the offending item for each of: (a) a metric-like number in the draft prose (decimal, percentage, or `n=`/`N=` count) absent from the ledger's value column and not inside a `[PENDING…]` flag; (b) a `[@citekey]` with no bib entry, and a bib entry never cited; (c) a placeholder or AI-tell hit; (d) a `checklist_*.md` table row whose disposition column is empty — and exits 0 on a clean fixture; SKILL.md Phase 5 runs it | `research-paper/tests/test_check_paper.py` in the machine gate; mutants per clause | proven | `gate-landing-r2.md` (research-paper 34 passed); C1 `-land` mutants KILLED incl. adversary and landing-review targets |
| C2 | research-proposal ships `scripts/check_proposal.py <proposal.md>` that exits 1 naming the orphan for an in-text citation without a References entry and for a References entry never cited, in both APA author-year `(Author, Year)` / `(Author et al., Year)` and numeric `[N]` (GB/T 7714) styles; exits 1 on a placeholder or AI-tell hit in the body; does not flag the documented scaffold personalization fields (`[University/Institution Name]`, `[所属学科]`, `[Figure N Suggestion]` …); exits 0 on a clean fixture in each style | `research-proposal/tests/test_check_proposal.py` in the machine gate; mutants per clause | proven | `gate-landing-r2.md` (research-proposal 42 passed); C2 `-land` mutants KILLED |
| C3 | the shared gate core `integrity_gate.py` exists in both `research-paper/scripts/` and `research-proposal/scripts/`, both checkers import it, and a repo-level test fails when the two copies differ by any byte | `tests/test_vendored_gate_core.py` in the machine gate; mutant that edits one copy | proven | `gate-landing-r2.md` (repo tests 8 passed); C3 `-land` mutants KILLED |
| C4 | `lit screen --limit N --sample random --seed S` screens N in-window records chosen by seeded random sampling — same seed ⇒ same set; on a fixture whose prefix differs from the sample the set is not the first-N prefix — and records the sample method and seed in `screening_trial.json`; `--sample random` without `--limit` exits 2; default `--sample head` keeps the existing prefix behavior | `lit-search/tests/test_screen_sample.py` in the machine gate; mutants | proven | `gate-landing-r2.md` (lit-search 885 passed / 15 skipped, ruff clean); C4 `-land` mutants KILLED |
| C5 | scholar-slides QA (`deckTypeAudit` wired into `qa_report.mjs`) emits, by `meta.deck_type`: `journal-club` (also when absent) → a P2 finding per missing `critique-concerns` / `discussion-questions` slide; `defense` → P2 when there is no Backup/Appendix `section` divider followed by at least one slide, and P2 when no slide title names limitations or future work; `conference` → P3 when a `critique-concerns` slide is present; an unknown `deck_type` → P1 naming the allowed values. A conforming deck of each type yields no deck-type finding | `scholar-slides/tests/deck_type.test.mjs` in the machine gate; mutants | proven | `gate-landing-r2.md` (scholar-slides node 97 pass); C5 `-land` mutants KILLED |
| C6 | paper-slide-deck: `generate-slides.py` records every slide it writes (filename + sha256) in `generated.json`; `merge-to-pptx.ts` and `merge-to-pdf.ts` exit non-zero naming each recorded slide that has no `proofread.json` entry or whose entry's sha256 no longer matches the file; `[CHECK]`-status entries are listed but allowed; `--allow-unproofread` turns the refusal into a printed warning; a deck with no `generated.json` (extract-only) is unaffected | `paper-slide-deck/tests/proofread.test.mjs` + `tests/test_generate_slides.py` in the machine gate; mutants | proven | `gate-landing-r2.md` (psd node 32 pass, py 15 passed); C6 `-land` mutants KILLED |
| C7 | medical-imaging-review ships `scripts/import_litsearch.py --project-dir P --run-dir R --searcher-id ID` that copies the lit-search delivery files present (`dois.md`, `references.md`, `PRISMA.md`, `coverage_report.md`, `references.bib`, `topic.yaml`) into `P/search/exports/litsearch-<run_id>/`, refuses (non-zero, nothing written) when that directory already exists or when `PRISMA.md`'s total-identified count is missing/unparseable, and otherwise appends exactly one `search/search_log.csv` row whose `result_count` equals that count and whose strategy/export paths point at the copied files, such that the audit's search-log check reports no search-log problem for that row | `medical-imaging-review/tests/test_import_litsearch.py` in the machine gate; mutants | proven | `gate-landing-r2.md` (MIR 139 passed); C7 `-land` mutants KILLED |

`status` is `open`, `proven`, `failed` or `parked`. At landing none is `open`. `proven` cites current evidence and, for a check the run wrote, the mutant that proves it can fail.

### Independent mutation targets

Full mode: at least one target selected by the adversary for each criterion.

Current wave: every mutant rerun under a `-land` label at 9c83160, after the landing-review fix
R26 changed the shared core (any code change makes earlier mutants stale). The earlier evidence files
(no suffix, `-r2`, all at eced80c/a16bf94 — 100 KILLED, 2 SURVIVED and 2 INCONCLUSIVE repaired as `-r2`)
stay in the evidence directory as history and are superseded by the rows below. Adversary-selected rows
per criterion: C1 15, C2 18, C3 4, C4 13, C5 18, C6 19, C7 16; rows marked `added after landing audit`
are stage-review targets the first wave had left out (R30).

| criterion | selected by | source condition / failure | patch | baseline | result / evidence |
|---|---|---|---|---|---|
| C1 | adversary s1 #1 | check_paper.py: `if value not in covered` → `if value in covered` | 9c48e34669c6… | green | KILLED @ 9c83160 — `mutant-c1a-invert-ledger-land.md` |
| C1 | author (R1 regression) | integrity_gate.py: `r"(?<![A-Za-z0-9_.])(?:[nN]` → `r"(?<![\w.])(?:[nN]` | e87466d9f69d… | green | KILLED @ 9c83160 — `mutant-c1a-cjk-boundary-land.md` |
| C1 | author (R2 regression) | integrity_gate.py: `re.compile(r"\[(?:PENDING\|UNVERIFIED)[^\]]*\]"),` → `re.compile(r"\[[^\]]*\]"),` | 6f2f53064c09… | green | KILLED @ 9c83160 — `mutant-c1a-bracket-strip-land.md` |
| C1 | adversary s1 #7 | integrity_gate.py: `if key not in listed` → `if False` | 491b1732ee8c… | green | KILLED @ 9c83160 — `mutant-c1b-cite-to-bib-land.md` |
| C1 | adversary s1 #8 | integrity_gate.py: `if key not in cited` → `if False` | fe0ad6a4b546… | green | KILLED @ 9c83160 — `mutant-c1b-bib-to-cite-land.md` |
| C1 | adversary s1 #11 | check_paper.py: `pattern_hits(text, PLACEHOLDER_PATTERN)` → `pattern_hits(text, r"(?!)")` | 23c4ce520155… | green | KILLED @ 9c83160 — `mutant-c1c-placeholder-off-land.md` |
| C1 | adversary s1 #12 | check_paper.py: `(warnings if allow_flags and DISCLOSED_FLAG_RE.m` → `(warnings if allow_flags else findin` | b496f0cd6e3b… | green | KILLED @ 9c83160 — `mutant-c1c-disclosure-guard-land.md` |
| C1 | adversary s1 #13 | check_paper.py: `pattern_hits(text, AI_TELL_PATTERN, ignore_case=` → `pattern_hits(text, AI_TELL_PATTERN, ` | c72ac7c6045d… | green | KILLED @ 9c83160 — `mutant-c1c-ai-tell-case-land.md` |
| C1 | adversary s1 #14 | check_paper.py: `cells[1] in UNDISPOSED)` → `cells[1] in UNDISPOSED - {""})` | b372a6057789… | green | KILLED @ 9c83160 — `mutant-c1d-empty-disposition-land.md` |
| C1 | adversary s1 #15 | check_paper.py: `if not checklists:` → `if False:` | 5ffb1d96d00d… | green | KILLED @ 9c83160 — `mutant-c1d-missing-checklist-land.md` |
| C1 | adversary s1 #17 | integrity_gate.py: `EXIT_CLEAN, EXIT_FINDINGS, EXIT_USAGE = 0, 1, 2` → `EXIT_CLEAN, EXIT_FINDINGS, EXIT_USAG` | 79fca6c8f527… | green | KILLED @ 9c83160 — `mutant-c1e-exit-findings-land.md` |
| C1 | adversary s1 #16 | integrity_gate.py: `if findings:         print(f"{gate}: FAIL` → `if findings or warnings:         pri` | 9f3144281fdc… | green | KILLED @ 9c83160 — `mutant-c1e-warnings-fail-land.md` |
| C2 | adversary s2 #1 | integrity_gate.py: `for part in re.split(r"\s*[;；]\s*", group.strip(` → `for part in [group.strip()]:` | b8710439360f… | green | KILLED @ 9c83160 — `mutant-c2-apa-split-land.md` |
| C2 | adversary s2 #4 | integrity_gate.py: `for match in APA_NARRATIVE_RE.finditer(line):` → `for match in []:` | 682e07ade00f… | green | KILLED @ 9c83160 — `mutant-c2-apa-narrative-land.md` |
| C2 | adversary s2 #3 (proposal-only variant) | check_proposal.py: `for key, where in apa_entries(refs).items()}` → `for key, where in apa_entries(body).` | cc3cbad3c3b4… | green | KILLED @ 9c83160 — `mutant-c2-apa-entry-never-cited-land.md` |
| C2 | adversary s2 #5; signature corrected after r1 | integrity_gate.py: `numbers.extend(range(bounds[0], bounds[1] + 1))` → `numbers.extend(range(bounds[0], boun` | 1a91857dfbc1… | green | KILLED @ 9c83160 — `mutant-c2-numeric-range-land.md` |
| C2 | adversary s2 #6 | check_proposal.py: `for key, where in numeric_entries(refs).items()}` → `for key, where in numeric_entries(bo` | 10846a685c48… | green | KILLED @ 9c83160 — `mutant-c2-numeric-entries-body-land.md` |
| C2 | adversary s2 #8 (adapted to fixed code); signature corrected after r1 | check_proposal.py: `style = "numeric" if len(numeric_cited) >= len(a` → `style = "apa"` | 13036bd417a2… | green | KILLED @ 9c83160 — `mutant-c2-auto-style-land.md` |
| C2 | author (R7 regression) | check_proposal.py: `if numeric_cited and apa_cited:` → `if False:` | 8278d32b60ed… | green | KILLED @ 9c83160 — `mutant-c2-mixed-style-land.md` |
| C2 | author (R7 regression) | integrity_gate.py: `(?:\[(\d+)\]\|(\d+)[.)、]\s)")` → `(?:\[(\d+)\]\|(\d+)\]\]\])")` | c525e209bdcb… | green | KILLED @ 9c83160 — `mutant-c2-numbered-entries-land.md` |
| C2 | adversary s2 #7 | integrity_gate.py: `NUMERIC_CITE_RE = re.compile(r"\[(\d+(?:\s*[-–—,` → `NUMERIC_CITE_RE = re.compile(r"\[(\d` | accc727d498e… | green | KILLED @ 9c83160 — `mutant-c2-fullwidth-comma-land.md` |
| C2 | adversary s2 #9 | check_proposal.py: `] if count else []` → `] if False else []` | 4eb0fb6460b2… | green | KILLED @ 9c83160 — `mutant-c2-no-refs-section-land.md` |
| C2 | adversary s2 #10 | check_proposal.py: `pattern_hits(text, PLACEHOLDER_PATTERN)` → `pattern_hits("", PLACEHOLDER_PATTERN` | ec6dae7612f5… | green | KILLED @ 9c83160 — `mutant-c2-placeholder-off-land.md` |
| C2 | adversary s2 #11 | check_proposal.py: `(warnings if allow_flags and DISCLOSED_FLAG_RE.m` → `(warnings if allow_flags else findin` | 7e1189c6fcd0… | green | KILLED @ 9c83160 — `mutant-c2-disclosure-guard-land.md` |
| C2 | adversary s2 #12 | check_proposal.py: `AI_TELL_PATTERN, ignore_case=True)` → `AI_TELL_PATTERN, ignore_case=False)` | 1a6b0088f769… | green | KILLED @ 9c83160 — `mutant-c2-ai-tell-case-land.md` |
| C2 | adversary s2 #13 | check_proposal.py: `body_text = "\n".join(line for _, line in body) ` → `body_text = "\n".join(line for _, li` + `def check_patterns(path: Path, text: str, body, ` → `def check_patterns(path: Path, text:` + `check_patterns(args.proposal, text, body, args.a` → `check_patterns(args.proposal, text, ` | f70bd8d17dad… | green | KILLED @ 9c83160 — `mutant-c2-ai-tell-body-only-land.md` |
| C2 | adversary s2 #14 | check_proposal.py: `if content in EXEMPT_BRACKETS or EXEMPT_BRACKET_` → `if True:` | 89f5960e5325… | green | KILLED @ 9c83160 — `mutant-c2-scaffold-off-land.md` |
| C2 | adversary s2 #15 | check_proposal.py: `"所属学科", "大学/研究机构名称", "年月",` → `"大学/研究机构名称", "年月",` | 2ef9c4ebbf7f… | green | KILLED @ 9c83160 — `mutant-c2-exempt-field-land.md` |
| C2 | adversary s2 #16 | check_proposal.py: `EXEMPT_BRACKET_RE = re.compile(r"^(Figure \d+ Su` → `EXEMPT_BRACKET_RE = re.compile(r"^(F` | 9b7d8e4df777… | green | KILLED @ 9c83160 — `mutant-c2-exempt-anchor-land.md` |
| C2 | author (R10 regression) | check_proposal.py: `if match := REF_INSTRUCTION_RE.match(line):` → `if match := None:` | a2bde1cad6eb… | green | KILLED @ 9c83160 — `mutant-c2-refs-instructions-land.md` |
| C2 | author (R10 regression) | integrity_gate.py: `if refs_level and HEADING_RE.match(line) and hea` → `if refs_level and HEADING_RE.match(l` | 3279da21e37f… | green | KILLED @ 9c83160 — `mutant-c2-refs-subheading-land.md` |
| C2 | adversary s2 #17 | integrity_gate.py: `return EXIT_FINDINGS` → `return EXIT_CLEAN` | adc719e1f256… | green | KILLED @ 9c83160 — `mutant-c2-exit-findings-land.md` |
| C2 | adversary s2 #17 (exit 2 clause) | check_proposal.py: `except InputError as error:         return usage` → `except KeyError as error:         re` | 0f5ee8c85430… | green | KILLED @ 9c83160 — `mutant-c2-non-utf8-land.md` |
| C3 | adversary s2 #18 | integrity_gate.py: `research-proposal/scripts/integrity_gate.py` → `` | 42807aaf0ec3… | green | KILLED @ 9c83160 — `mutant-c3-core-missing-land.md` |
| C3 | adversary s2 #19 | check_proposal.py: `#: 与 SKILL.md Phase 5 的 canonical 占位符 grep` → `def reconcile(*_args, **_kwargs):   ` | 085bf6d4c3a4… | green | KILLED @ 9c83160 — `mutant-c3-shadowed-land.md` |
| C3 | adversary s2 #20 | integrity_gate.py: `EXIT_CLEAN, EXIT_FINDINGS, EXIT_USAGE = 0, 1, 2` → `EXIT_CLEAN, EXIT_FINDINGS, EXIT_USAG` | 58930573dc47… | green | KILLED @ 9c83160 — `mutant-c3-one-byte-land.md` |
| C4 | adversary s3 #1 | sampling.py: `random.Random(seed).sample` → `random.Random(0).sample` | ff7ad28539fa… | green | KILLED @ 9c83160 — `mutant-c4-seed-ignored-land.md` |
| C4 | adversary s3 #2 | cli.py: `records = select_trial(records, limit, sample, s` → `records = select_trial(records, limi` | 40d921fbc70a… | green | KILLED @ 9c83160 — `mutant-c4-cli-seed-land.md` |
| C4 | adversary s3 #3 | sampling.py: `random.Random(seed).sample` → `random.Random().sample` | dd6d4d6cc2b7… | green | KILLED @ 9c83160 — `mutant-c4-unseeded-land.md` |
| C4 | adversary s3 #4 | sampling.py: `if method == "head" or limit >= len(records):` → `if method in ("head", "random") or l` | 6d9eddf134f6… | green | KILLED @ 9c83160 — `mutant-c4-random-as-head-land.md` |
| C4 | adversary s3 #5 | cli.py: `records = select_trial(records, limit, sample, s` → `records = select_trial(records, limi` | 0381198e5f69… | green | KILLED @ 9c83160 — `mutant-c4-cli-head-land.md` |
| C4 | adversary s3 #7 | cli.py: `**sampling,` → `` | c0d5b3eab5f3… | green | KILLED @ 9c83160 — `mutant-c4-api-record-land.md` |
| C4 | adversary s3 #8 | sampling.py: `detail["seed"] = seed` → `pass` | 0f6f336d96d4… | green | KILLED @ 9c83160 — `mutant-c4-seed-record-land.md` |
| C4 | adversary s3 #9 | cli_judge.py: `**(sampling or {}),` → `` | 3119636e1641… | green | KILLED @ 9c83160 — `mutant-c4-jev-record-land.md` |
| C4 | adversary s3 #10 | sampling.py: `raise SampleError("--sample random 必须配合 --limit ` → `pass` | 48873c99ff8c… | green | KILLED @ 9c83160 — `mutant-c4-no-limit-land.md` |
| C4 | adversary s3 #11 | cli.py: `records = select_trial(records, limit, sample, s` → `records = select_trial(records, limi` | 977043f07f98… | green | KILLED @ 9c83160 — `mutant-c4-exit-code-land.md` |
| C4 | adversary s3 #13 | cli.py: `"head",         "--sample",` → `"random",         "--sample",` | e841a9ebb96f… | green | KILLED @ 9c83160 — `mutant-c4-default-random-land.md` |
| C4 | adversary s3 #14 | sampling.py: `return list(records[:limit])` → `return list(records[-limit:])` | 82f955c2bc7a… | green | KILLED @ 9c83160 — `mutant-c4-head-tail-land.md` |
| C4 | author (R15 regression) | cli.py: `if resume and sample == "random":` → `if False:` | 79781aa0b201… | green | KILLED @ 9c83160 — `mutant-c4-resume-guard-land.md` |
| C5 | adversary s4 #1 | qa.mjs: `deck.meta?.deck_type ?? "journal-club"` → `deck.meta?.deck_type ?? "conference"` | 360325b350ff… | green | KILLED @ 9c83160 — `mutant-c5-absent-type-land.md` |
| C5 | adversary s4 #2 | qa.mjs: `for (const layout of ["critique-concerns", "disc` → `for (const layout of ["critique-conc` | 52bd61b02a0d… | green | KILLED @ 9c83160 — `mutant-c5-drop-discussion-land.md` |
| C5 | adversary s4 #4 | qa.mjs: `if (!has(layout)) out.push(` → `if (has(layout)) out.push(` | f9dfa0870a9b… | green | KILLED @ 9c83160 — `mutant-c5-jc-guard-land.md` |
| C5 | adversary s4 #5 | qa.mjs: `const appendix = backup === -1 ? [] :` → `const appendix = backup === -1 ? [1]` | b862b0d2ea33… | green | KILLED @ 9c83160 — `mutant-c5-no-backup-land.md` |
| C5 | adversary s4 #6 | qa.mjs: `if (!appendix.length) {` → `if (backup === -1) {` | c4d040cf4a1f… | green | KILLED @ 9c83160 — `mutant-c5-backup-followed-land.md` |
| C5 | adversary s4 #7 | qa.mjs: `slides.findIndex((s) => s.layout === "section" &` → `slides.findIndex((s) => BACKUP_RE.te` | 199c3aaf4b1b… | green | KILLED @ 9c83160 — `mutant-c5-section-guard-land.md` |
| C5 | adversary s4 #8 | qa.mjs: `(backup\|appendix\|附录\|备用\|备份)` → `(backup\|appendix\|备用\|备份)` | 40f94c26329d… | green | KILLED @ 9c83160 — `mutant-c5-cjk-backup-land.md` |
| C5 | adversary s4 #9 | qa.mjs: `if (!slides.some((s) => LIMITS_RE.test` → `if (slides.some((s) => LIMITS_RE.tes` | d80b95a8ff47… | green | KILLED @ 9c83160 — `mutant-c5-limits-guard-land.md` |
| C5 | adversary s4 #10 | qa.mjs: `\|\bfuture (work\|directions?)\b\|` → `\|` | b57d17f69865… | green | KILLED @ 9c83160 — `mutant-c5-future-work-vocab-land.md` |
| C5 | author (R17 regression) | qa.mjs: `&& !PRIOR_WORK_RE.test(titleOf(s))` → `` | 69437d1619b3… | green | KILLED @ 9c83160 — `mutant-c5-prior-work-land.md` |
| C5 | author (R17 regression) | qa.mjs: `.filter((s) => s.layout !== "section" && !CLOSIN` → `.filter((s) => s.layout !== "section` | 61ce6d9df0bc… | green | KILLED @ 9c83160 — `mutant-c5-closing-land.md` |
| C5 | adversary s4 #11 | qa.mjs: `check: "critique-in-conference", severity: "P3"` → `check: "critique-in-conference", sev` | 0f9cbd27afa6… | green | KILLED @ 9c83160 — `mutant-c5-conference-p3-land.md` |
| C5 | adversary s4 #12 | qa.mjs: `if (type === "journal-club") {` → `if (type !== "defense") {` | 530b2a0865c7… | green | KILLED @ 9c83160 — `mutant-c5-branch-scope-land.md` |
| C5 | adversary s4 #14 | qa.mjs: `if (!DECK_TYPES.includes(type)) {` → `if (false) {` | 3aa05d0fc752… | green | KILLED @ 9c83160 — `mutant-c5-unknown-type-land.md` |
| C5 | adversary s4 #15 | qa_report.mjs: `for (const d of deckTypeAudit(deck)) findings.pu` → `if (false) for (const d of deckTypeA` | 1a388f1642a1… | green | KILLED @ 9c83160 — `mutant-c5-wiring-land.md` |
| C6 | adversary s5 #1 | generate-slides.py: `"sha256": hashlib.sha256(output_path.read_bytes(` → `"sha256": hashlib.sha256(b"").hexdig` | da72cb13c1bd… | green | KILLED @ 9c83160 — `mutant-c6-sha-empty-land.md` |
| C6 | adversary s5 #2 | generate-slides.py: `slides = json.loads(ledger.read_text(encoding="u` → `slides = {}     # A slide` | bbddb1d0b9d5… | green | KILLED @ 9c83160 — `mutant-c6-drop-prior-land.md` |
| C6 | adversary s5 #4 | generate-slides.py: `record_generated(deck_dir, written, slide["promp` → `` | 6179ddc0d889… | green | KILLED @ 9c83160 — `mutant-c6-main-wiring-land.md` |
| C6 | adversary s5 #5 (simpler variant) | proofread.ts: `if (!(slide.filename in generated) && !generated` → `if (slide.filename in generated \|\| g` | 1dd2f6a96295… | green | KILLED @ 9c83160 — `mutant-c6-no-entry-ok-land.md` |
| C6 | adversary s5 #6 (adapted to hash identity) | proofread.ts: `const entry = proofreadByHash.get(hash);` → `const entry = proofread[slide.filena` | f711c316b0b9… | green | KILLED @ 9c83160 — `mutant-c6-sha-binding-land.md` |
| C6 | adversary s5 #7 | proofread.ts: `if (entry && STATUSES.has(entry.status ?? "")) {` → `if (entry) {` | c949d438298f… | green | KILLED @ 9c83160 — `mutant-c6-status-check-land.md` |
| C6 | adversary s5 #8 | merge-to-pptx.ts: `proofreadGate(dir, slides, { allowUnproofread })` → `proofreadGate(dir, slides, { allowUn` | 75c4be65e392… | green | KILLED @ 9c83160 — `mutant-c6-pptx-wiring-land.md` |
| C6 | adversary s5 #9 | merge-to-pdf.ts: `proofreadGate(dir, slides, { allowUnproofread })` → `proofreadGate(dir, slides, { allowUn` | 10de0ac45a8a… | green | KILLED @ 9c83160 — `mutant-c6-pdf-wiring-land.md` |
| C6 | adversary s5 #10 | proofread.ts: `unproofread.push(`${slide.filename} (no proofrea` → `unproofread.push(`${slide.filename} ` | 4cf25481a29d… | green | KILLED @ 9c83160 — `mutant-c6-name-first-only-land.md` |
| C6 | adversary s5 #11 | proofread.ts: `for (const f of result.fatal) console.error(`Err` → `` | b72dcf330ca7… | green | KILLED @ 9c83160 — `mutant-c6-fatal-print-land.md` |
| C6 | adversary s5 #12 | proofread.ts: `if (entry && STATUSES.has(entry.status ?? "")) {` → `if (entry && entry.status === "ok") ` | b7ff49f53ba3… | green | KILLED @ 9c83160 — `mutant-c6-check-as-fatal-land.md` |
| C6 | adversary s5 #13 | proofread.ts: `for (const c of result.checks) console.error(`[C` → `` | d37551192012… | green | KILLED @ 9c83160 — `mutant-c6-check-print-land.md` |
| C6 | adversary s5 #14 | proofread.ts: `(allowUnproofread ? warnings : fatal).push(msg);` → `fatal.push(msg);` | 82ec7f706b4f… | green | KILLED @ 9c83160 — `mutant-c6-allow-ignored-land.md` |
| C6 | adversary s5 #15 | merge-to-pdf.ts: `} else if (args[i] === "--allow-unproofread") {` → `} else if (args[i] === "--allow-unpr` | b4cc640d43c4… | green | KILLED @ 9c83160 — `mutant-c6-flag-parse-land.md` |
| C6 | adversary s5 #16 | proofread.ts: `for (const w of result.warnings) console.error(`` → `` | cdbf13026fea… | green | KILLED @ 9c83160 — `mutant-c6-warning-print-land.md` |
| C6 | adversary s5 #17 | proofread.ts: `return { fatal, warnings, checks };   }   let ge` → `fatal.push("no generated.json");    ` | 9762413d4136… | green | KILLED @ 9c83160 — `mutant-c6-no-ledger-fail-closed-land.md` |
| C6 | adversary s5 #19 | proofread.ts: `slides[filename] = { sha256: sha256File(slidePat` → `slides[filename] = { sha256: "", sta` | d2e93450b0e4… | green | KILLED @ 9c83160 — `mutant-c6-mark-sha-land.md` |
| C6 | author (R20 regression) | proofread.ts: `if (!(slide.filename in generated) && !generated` → `if (!(slide.filename in generated)) ` | a16c0c371d88… | green | KILLED @ 9c83160 — `mutant-c6-rename-identity-land.md` |
| C6 | author (R22 regression) | proofread.ts: `for (const candidate of [join(dir, filename), jo` → `for (const candidate of [join(dir, f` | fd5c7973c003… | green | KILLED @ 9c83160 — `mutant-c6-subdir-land.md` |
| C6 | author (R21 regression) | proofread.ts: `if (existsSync(join(dir, "prompts"))) {` → `if (false) {` | 735c194dc271… | green | KILLED @ 9c83160 — `mutant-c6-prompts-warning-land.md` |
| C7 | adversary s6 #1 | import_litsearch.py: `for name in REQUIRED + OPTIONAL:` → `for name in REQUIRED:` | d02d2bbab792… | green | KILLED @ 9c83160 — `mutant-c7-copy-required-only-land.md` |
| C7 | adversary s6 #2 | import_litsearch.py: `OPTIONAL = ("references.md", "coverage_report.md` → `OPTIONAL = ("references.md", "covera` | 4b1897da4af9… | green | KILLED @ 9c83160 — `mutant-c7-optional-list-land.md` |
| C7 | adversary s6 #4 | import_litsearch.py: `if target.exists() or target.is_symlink():` → `if False:` | 32846bf6475f… | green | KILLED @ 9c83160 — `mutant-c7-exists-guard-land.md` |
| C7 | adversary s6 #6 | import_litsearch.py: `match = IDENTIFIED_RE.search(text)     if not ma` → `match = IDENTIFIED_RE.search(text)  ` | 42add17454e5… | green | KILLED @ 9c83160 — `mutant-c7-prisma-missing-land.md` |
| C7 | adversary s6 #8 | import_litsearch.py: `IDENTIFIED_RE = re.compile(r"合计识别：\*\*(\d[\d,]*)` → `IDENTIFIED_RE = re.compile(r"合计识别：\*` + `except (ImportRefused, OSError, UnicodeDecodeErr` → `except (ImportRefused, OSError, Unic` | 3ed17a89f180… | green | KILLED @ 9c83160 — `mutant-c7-unparseable-land.md` |
| C7 | adversary s6 #9 | import_litsearch.py: `"result_count": str(identified),` → `"result_count": str(canonical),` | 386d820f211d… | green | KILLED @ 9c83160 — `mutant-c7-count-canonical-land.md` |
| C7 | adversary s6 #11 | import_litsearch.py: `log.write_text(prefix + row, encoding="utf-8")` → `log.write_text(prefix + row + row, e` | 5156af5c7398… | green | KILLED @ 9c83160 — `mutant-c7-two-rows-land.md` |
| C7 | adversary s6 #12 | import_litsearch.py: `"strategy_file": f"{relative}/topic.yaml",` → `"strategy_file": f"{relative}/PRISMA` | d1fdc61c5b5d… | green | KILLED @ 9c83160 — `mutant-c7-strategy-path-land.md` |
| C7 | adversary s6 #13 | import_litsearch.py: `"searcher_id": searcher_id,` → `"searcher_id": "",` + `if rejected:` → `if False:` | 36766d6645ed… | green | KILLED @ 9c83160 — `mutant-c7-audit-accepts-land.md` |
| C7 | author (R25 regression) | import_litsearch.py: `"searcher_id": searcher_id,` → `"searcher_id": "",` (attacks: the audit's rejection fires and the import exits 2; the rollback itself is attacked by c7-append-rollback and c7-new-row-index) | 7fa4bcbe2d20… | green | KILLED @ 9c83160 — `mutant-c7-rejection-rollback-land.md` |
| C7 | adversary s6 #14 | checks_artifacts.py: `total_search_results += result_count     if vali` → `total_search_results += 1     if val` | ba1f4d9628b6… | green | KILLED @ 9c83160 — `mutant-c7-refactor-accumulate-land.md` |
| C7 | adversary s6 #16 | checks_artifacts.py: `problems.append(f"search/search_log.csv row {ind` → `pass         try:` | 03f27023b776… | green | KILLED @ 9c83160 — `mutant-c7-refactor-incomplete-land.md` |
| C7 | adversary s6 #16 | checks_artifacts.py: `if result_count < 0 or not path_is_project_owned` → `if not path_is_project_owned_file(pr` | 293bcd9190f4… | green | KILLED @ 9c83160 — `mutant-c7-refactor-negative-land.md` |
| C7 | adversary s6 #17 | import_litsearch.py: `if not SAFE_RUN_ID.fullmatch(run_id):` → `if False:` | 8d32c6c46c7d… | green | KILLED @ 9c83160 — `mutant-c7-run-id-safety-land.md` |
| C7 | author (R25 regression) | import_litsearch.py: `if tuple(header) != SEARCH_LOG_COLUMNS:` → `if False:` | 312fac434586… | green | KILLED @ 9c83160 — `mutant-c7-header-check-land.md` |
| C7 | author (R23 regression) | import_litsearch.py: `# Export first: restoring the log can fail for t` → `# Export first: restoring the log ca` | 8c983c83ed71… | green | KILLED @ 9c83160 — `mutant-c7-append-rollback-land.md` |
| C1 | adversary landing r1 | integrity_gate.py: `heading_level(line) <= refs_level` → `heading_level(line) < refs_level` | 17d251ed94d1… | green | KILLED @ 9c83160 — `mutant-c1-split-level-land.md` |
| C1 | adversary landing r1 (adapted to R26 fix) | integrity_gate.py: `r"\|(\d*\.\d+)(?![0-9_]\|\.\d))"` → `r"\|(\d*\.\d{2,})(?![0-9_]\|\.\d))"` | 4d4edb76313c… | green | KILLED @ 9c83160 — `mutant-c1-decimal-two-places-land.md` |
| C1 | author (R26 regression) | integrity_gate.py: `r"\|(\d*\.\d+)(?![0-9_]\|\.\d))"` → `r"\|(\d*\.\d+)(?![A-Za-z0-9_]\|\.\d))"` | dabc17885916… | green | KILLED @ 9c83160 — `mutant-c1-unit-lookahead-land.md` |
| C1 | author (R26 regression) | integrity_gate.py: `if value.startswith("."):         value = "0" + ` → `` | 61bb3425889b… | green | KILLED @ 9c83160 — `mutant-c1-leading-dot-norm-land.md` |
| C2 | adversary landing r1 | integrity_gate.py: `rf"(?:\s+et al\.?\|\s+(?:and\|&)\s+(?:{_SURNAME})\|` → `rf"(?:\s+(?:and\|&)\s+(?:{_SURNAME})\|` | e3219b146b5b… | green | KILLED @ 9c83160 — `mutant-c2-et-al-land.md` |
| C3 | adversary landing r1 | integrity_gate.py: `# --- 数字对账` → `#  --- 数字对账` | 8d8d4e23e721… | green | KILLED @ 9c83160 — `mutant-c3-trailing-newline-land.md` |
| C4 | adversary landing r1 | sampling.py: `sample(range(len(records)), limit)` → `sample(range(len(records) - 1), limi` | 2ad00a167211… | green | KILLED @ 9c83160 — `mutant-c4-last-record-land.md` |
| C5 | adversary landing r1 | qa.mjs: `.filter((s) => s.layout !== "section" && !CLOSIN` → `.filter((s) => !CLOSING_RE` | 6b81dd4ee86f… | green | KILLED @ 9c83160 — `mutant-c5-section-as-appendix-land.md` |
| C6 | adversary landing r1 | proofread.ts: `STATUSES.has(entry.status ?? "")` → `entry.status !== undefined` | 66b40bfad38b… | green | KILLED @ 9c83160 — `mutant-c6-status-defined-land.md` |
| C7 | adversary landing r1 | import_litsearch.py: `f"row {new_index} "` → `f"row {new_index - 1} "` | 68c68d4ea205… | green | KILLED @ 9c83160 — `mutant-c7-new-row-index-land.md` |
| C1 | adversary s1 #2 (added after landing audit) | integrity_gate.py: `\|(\d+(?:\.\d+)?)\s*%"` → `\|(\d+(?:\.\d+)?)\s*%(?!)"` | 708f6ee01258… | green | KILLED @ 9c83160 — `mutant-c1a-percent-branch-land.md` |
| C1 | adversary s1 #3 (added after landing audit) | integrity_gate.py: `[nN]\s*=\s*(\d[\d,]*)(?![A-Za-z0-9_])\|` → `[nN]\s*=\s*(\d[\d,]*)(?!)\|` | a51259fa5c3e… | green | KILLED @ 9c83160 — `mutant-c1a-n-branch-land.md` |
| C1 | adversary s1 #4 (added after landing audit) | integrity_gate.py: `re.compile(r"\[(?:PENDING\|UNVERIFIED)[^\]]*\]"),` → `re.compile(r"\[(?:XPENDING)[^\]]*\]"` | 68ac4815acc8… | green | KILLED @ 9c83160 — `mutant-c1a-pending-strip-land.md` |
| C5 | adversary s4 #3 (added after landing audit) | qa.mjs: `check: "missing-archetype", severity: "P2"` → `check: "missing-archetype", severity` | 0b7b7c7e25c8… | green | KILLED @ 9c83160 — `mutant-c5-archetype-severity-land.md` |
| C5 | adversary s4 #3 (added after landing audit) | qa.mjs: `check: "missing-backup", severity: "P2"` → `check: "missing-backup", severity: "` | da23b87f3120… | green | KILLED @ 9c83160 — `mutant-c5-backup-severity-land.md` |
| C5 | adversary s4 #3 (added after landing audit) | qa.mjs: `check: "missing-limitations", severity: "P2"` → `check: "missing-limitations", severi` | 0f7cc2e2cac7… | green | KILLED @ 9c83160 — `mutant-c5-limits-severity-land.md` |
| C5 | adversary s4 #3 (added after landing audit) | qa.mjs: `check: "unknown-deck-type", severity: "P1"` → `check: "unknown-deck-type", severity` | 802c8e988f4b… | green | KILLED @ 9c83160 — `mutant-c5-unknown-severity-land.md` |
| C6 | adversary s5 #15 (pptx half) (added after landing audit) | merge-to-pptx.ts: `args[i] === "--allow-unproofread"` → `args[i] === "--allow-unproofed"` | 81b309fbc812… | green | KILLED @ 9c83160 — `mutant-c6-pptx-flag-land.md` |
| C7 | adversary s6 #3 (added after landing audit) | import_litsearch.py: `target = exports / f"litsearch-{run_id}"` → `target = exports / f"{run_id}"` | 6357d737f88f… | green | KILLED @ 9c83160 — `mutant-c7-target-name-land.md` |
| C7 | adversary s6 #5 (added after landing audit) | import_litsearch.py: `identified, canonical = read_identified(` → `(project_dir / "search/exports/junk"` | 2b0cf21349a3… | green | KILLED @ 9c83160 — `mutant-c7-write-before-refusal-land.md` |

### Evidence integrity

- `verify-evidence.sh docs/autopilot/evidence-2026-10-24` after gate-landing-r2: `verified: 252 evidence file(s)`.
- `mutant-status.py --docs '*.md' . docs/autopilot/evidence-2026-10-24` at 9c83160: the 120 `-land` mutants are
  KILLED and current (tested commit 9c83160); every earlier wave row reports `rerun` and is superseded.
- Landing gate `gate-landing-r2` at 9c83160: all 10 commands exit 0 — lit-search 885 passed/15 skipped, ruff
  clean, scholar-slides py 86/8 skipped, node 97/0, MIR 139, psd py 15, psd node 32/0, research-paper 34,
  research-proposal 42, repo 8; sandbox probes PASS, network denied. `gate-landing.md` (a16bf94) is stale.
- Signature corrections disclosed: `c2-numeric-range` / `c2-auto-style` name the test that failed in their
  first run (chosen after seeing it); `c4-resume-guard` / `c7-header-check` survived first and gained
  detector tests (a16bf94) before KILLED reruns.
- Landing reviews registered: `review-landing-r1.json` (+ request, receipt; sealed, `validate-findings.sh`
  valid for base 98b1ffe / head 2adf0ff / scope landing) and `audit-landing-r1.md`.

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
| R26 | landing-r1 | claude subagent | C1(a): METRIC_RE skipped unit-glued decimals (`12.5ms`, `2.5x`, `3.5mm`, `1.5M`), APA leading-dot values (`r = .85`, `p < .001`) and `95%CI` | blocking-fixed | reproduced (finditer → []); fixed 4779438 in both vendored cores, `.85` normalized to `0.85`, versions `2.0.1` still excluded; tests `test_unit_glued_and_leading_dot_numbers_are_checked`, `test_leading_dot_matches_the_ledger_and_versions_are_not_numbers`; mutants c1-unit-lookahead-land, c1-leading-dot-norm-land |
| R27 | landing-r1 | claude subagent | targets: split_body `<=`→`<` and C7 `new_index - 1` survived a local probe; C5 section-divider-as-appendix had no test | minor-fixed | detectors ecb3218 (`test_section_after_references_at_the_same_level_is_checked`, `test_audit_rejecting_the_new_row_rolls_back_after_an_earlier_valid_row`) and 9c83160 (`defense: a Backup divider followed only by another divider is a P2`); all 8 landing targets KILLED in the `-land` wave |
| R28 | audit-r1 | claude subagent (auditor) | landing adversary review not yet recorded at the audited head | minor-fixed | review-landing-r1.* sealed, validated and registered; R26–R27 rows |
| R29 | audit-r1 | claude subagent (auditor) | gate commands and reviewer differ from the contract (offline translations; Claude instead of Codex) | minor-open | disclosed since takeoff; needs the human's ruling — parked P2 |
| R30 | audit-r1 | claude subagent (auditor) | some stage-review adversary targets (s1 #2–#4, s4 #3, s5 #15 pptx half, s6 #3, s6 #5) had no recorded mutant | minor-fixed | added as 10 `-land` mutants (`added after landing audit`), all KILLED |
| R31 | audit-r1 | claude subagent (auditor) | table rows for c7-rejection-rollback / c7-audit-accepts misdescribed what they attack | minor-fixed | table now lists every hunk and states what c7-rejection-rollback attacks |

### Parked

| id | needs | exact action | unblocks | verify afterward |
|---|---|---|---|---|
| P2 | human ruling on the proposed contract changes (offline gate commands, fallback reviewer) | approve or reject the two amendments below; the run never edits `docs/autopilot.md` | gate evidence counts as the contract's own commands | none — contract text only |
| P1 | human decision (landing not pre-authorized by the contract) | review branch `autopilot/six-skill-takeoff`, then merge to `main` and/or push / open a PR | the upgrades reach `main` / origin | rerun the 10 gate commands on `main` after merge |

### Proposed contract changes

1. Machine-gate commands: record the offline-sandbox translations above (absolute venv
   interpreters, `-B -p no:cacheprovider`, `-o pythonpath=src` for lit-search) as the
   contract's gate commands, and add the new test files each stage introduces.
2. Review: the contract names Codex as review gate; this host has no Codex CLI. Name the
   allowed fallback reviewer (fresh-context subagent, same family) explicitly.

### Not verified

- Reviewer independence: every review (stage targets, landing adversary, landing audit) is a fresh-context
  Claude subagent — same model family as the author; no Codex CLI or other-family API was available.
- Docs-only clauses (SKILL.md / README wording, the 开题报告 length guidance, gemini-web instructions) are
  checked by reading, not by a machine gate, except where a test pins a documented pattern to the code.
- scholar-slides: 8 integration tests skip in the sandbox (rendering / network); paper-slide-deck: the real
  Gemini API and Gemini Web generation paths and `bun` were not run — `generate-slides.py main()` is driven
  with a stub client.
- lit-search: 15 tests skip by design (live-source markers); no live retrieval or judge API call was made.
- The proofread gate cannot prove a slide is AI-generated when nobody records it (Gemini Web without
  `proofread.ts --record`); disclosed in SKILL.md, warned at merge when `prompts/` exists without a ledger.

## Acceptance walk

| id | clause | where it is checked | result |
|---|---|---|---|
| C1 | (a) untraced metric number / `n=` / % named, exit 1; flags excluded | `test_untraced_decimal_fails_and_is_named`, Chinese-prose, CI-in-brackets, thousands-separator tests | proven |
| C1 | (b) citekey without bib entry and bib entry never cited | cite↔bib tests; mutants c1b-* | proven |
| C1 | (c) placeholder / AI-tell; patterns equal the SKILL.md greps | pattern tests + `GatePatternsMatchSkillDoc`; mutants c1c-* | proven |
| C1 | (d) empty checklist disposition (incl. missing cell, `- [ ]`, TBD) | checklist tests; mutant c1d-empty-disposition | proven |
| C1 | clean fixture exit 0; SKILL.md Phase 5 runs it | clean test; SKILL.md Phase 5 (read) | proven (doc part by reading) |
| C2 | APA and numeric orphans both directions; mixed/mismatch fail closed | `test_check_proposal.py`; mutants c2-* (2 repaired) | proven |
| C2 | placeholder / AI-tell in body; scaffold fields not flagged; clean fixture per style | exempt-field, body-only, clean tests | proven |
| C3 | byte-identical vendored core, both checkers import their own copy | `tests/test_vendored_gate_core.py`; mutant editing one copy | proven |
| C4 | seeded random sample (same seed ⇒ same set, not the prefix), recorded in `screening_trial.json`; random without `--limit` exits 2; head default unchanged | `test_screen_sample.py` incl. jev path; mutants c4-* (resume guard repaired) | proven |
| C5 | per deck_type findings and severities; unknown type P1; conforming decks clean; wired into qa_report | `deck_type.test.mjs`; mutants c5-* | proven |
| C6 | generated.json by sha256; merges refuse naming each unproofread / changed slide; [CHECK] listed; `--allow-unproofread` warns; extract-only unaffected | `proofread.test.mjs`, `test_generate_slides.py` main() wiring; mutants c6-* | proven |
| C7 | copy present delivery files; refuse existing dir / missing-unparseable total with nothing written; one row with PRISMA count, paths to copies, accepted by the audit | `test_import_litsearch.py`; mutants c7-* (header check repaired) | proven |

All seven criteria are proven at 9c83160 with current mutation evidence (`-land` wave) and gate-landing-r2; no erratum was needed.

## Resume log

| when | saved current | found | repeated |
|---|---|---|---|
