# Autopilot contract — research-skills

Standing rules for unattended runs (the `autopilot` skill). The human owns this file: a run
reads it and never edits it.

Status: in force since 2026-10-10 (human confirmed at takeoff: base = feat/design-round2)

## Workspace

How a run stays reversible: a fresh branch `autopilot/<slug>` from the run's declared base.
Runs default their base to `main`; a run may declare a different base (e.g. an unmerged
feature branch that holds the skills' current state) only with the human's confirmation at
takeoff.

Nothing runs from the main checkout itself — this repo is a skills library plus offline
test suites; no service serves its files.

## Preflight

Checks that must pass before takeoff. One row each: the command, and the result that counts
as ready.

| check | command | ready when |
|---|---|---|
| working tree clean | `git status --porcelain` | empty output |
| lit-search suite | `cd lit-search && uv run pytest -q && uv run ruff check .` | exit 0 |
| scholar-slides python | `cd scholar-slides && python3 -m pytest -p no:warnings -q` | exit 0 |
| scholar-slides node | `cd scholar-slides && node --test tests/*.test.mjs` | fail count 0 |
| medical-imaging-review | `cd medical-imaging-review && python3 -m pytest tests/ -q` | exit 0 |
| paper-slide-deck python | `cd paper-slide-deck && python3 -m pytest tests/ -q` | exit 0 |
| paper-slide-deck node | `cd paper-slide-deck && node --test tests/*.mjs` | fail count 0 |
| codex CLI (review gate) | `codex --version` | prints a version |
| auditor brief (review gate) | `ls ~/.claude/agents/acceptance-auditor.md` | file exists |

## Machine gate

Commands run after every stage; all must pass. `rerun` says whether a reviewer may run the
command again (`safe`) or must rely on the saved output (`no`: slow, costly, or changes
state). All gate commands are offline and fixture-based, so every one is `safe`.

| command | proves | rerun |
|---|---|---|
| `cd lit-search && uv run pytest -q` | lit-search python behavior | safe |
| `cd lit-search && uv run ruff check .` | lit-search style/lint | safe |
| `cd scholar-slides && python3 -m pytest -p no:warnings -q` | scholar-slides python behavior | safe |
| `cd scholar-slides && node --test tests/*.test.mjs` | scholar-slides node behavior | safe |
| `cd medical-imaging-review && python3 -m pytest tests/ -q` | medical-imaging-review behavior | safe |
| `cd paper-slide-deck && python3 -m pytest tests/ -q` | paper-slide-deck python behavior | safe |
| `cd paper-slide-deck && node --test tests/*.mjs` | paper-slide-deck node behavior | safe |
| `cd research-paper && python3 -m pytest tests/ -q` | research-paper doc contracts（门禁正则/派生标记/相位映射，第三轮起） | safe |
| `cd research-proposal && python3 -m pytest tests/ -q` | research-proposal doc contracts（AI-tell 覆盖/豁免/链接验存，第三轮起） | safe |
| `python3 -m pytest tests/ -q` | 跨 skill 共享层：citation-core 注册表↔变体↔README、旗标分类（第三轮起） | safe |

## Pre-authorized

What a run does without asking:

- Edit and add files anywhere in this repo, and commit, on the run's `autopilot/<slug>`
  branch only.
- Run the machine-gate commands any number of times.
- Run any skill script offline against local fixtures/synthetic inputs (e.g.
  `audit_manuscript.py`, `qa_report.mjs`) to verify behavior, including deliberately
  breaking inputs to prove checks can fail.
- Create files under `docs/` (review records, run records, evidence) — `docs/` is the
  established location for design/process documents.
- Write `learnings/*.md` entries inside a skill folder after non-trivial fixes (the repo's
  learning law).
- Dispatch read-only review agents and the two review-gate reviewers.

Landing is NOT pre-authorized. The human decides at landing whether to merge
`feat/design-round2` and/or the run branch into `main`.

## Red lines

What a run parks. For each, the action and what the run prepares instead.

| red line | prepare instead |
|---|---|
| Delete any tracked file (user global rule: file deletion needs confirmation) | In-file fix where possible; otherwise ledger a parked row with the exact `git rm` command and the finding it resolves |
| Push, merge, or open a PR to `main` | Land on the run branch; run record lists the exact commands in order |
| Paid or network-mutating API calls (Gemini image generation, JEV screening, Crossref/OpenAlex live writes) | Offline fixture verification; live verification parked with a dry run |
| Database operations (user global rule) | None exist in this repo; any that appear are parked |
| Edit this contract | Never; the human owns `docs/autopilot.md` |
| Architectural rewrite of a skill not justified by a review finding | Ledger the decision with rejected alternatives; if undoing it costs more than one stage, convene the review gate before building |

## Evidence

Evidence files live in `docs/autopilot/evidence/`, named `<stage>-<label>.txt`. Each records
the command, its exit status, timestamp, and the commit it ran against (the run-gate script
writes this header automatically). Evidence is committed on its own after each gate run.

## Review heuristics

Paths to project-specific rules the reviewers apply:

- `docs/citation-integrity-core.md` — the shared five-rule anti-fabrication core
- `README.md` — the top-level contract with users (skill boundaries, routing)
- each skill's `SKILL.md`, plus `IMPLEMENTATION_PLAN.md` where present
- `.github/workflows/ci.yml` — what CI enforces (and what it misses)
- this contract and the current run record

## Run records

Run records live in `docs/autopilot/runs/`, named `YYYY-MM-DD-<slug>.md`.
