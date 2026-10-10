# Research Skills

A collection of Claude Code skills for academic research workflows.

## Skills

| Skill | Description | Trigger |
|-------|-------------|---------|
| [medical-imaging-review](./medical-imaging-review/) | Write comprehensive literature reviews for medical imaging AI | `/medical-imaging-review`, "review paper", "survey", "综述" |
| [paper-slide-deck](./paper-slide-deck/) | Stylized slide **images** (17 T2I aesthetic styles) for reading & sharing — any content | `/paper-slide-deck content.md --style watercolor` |
| [research-proposal](./research-proposal/) | Generate PhD research proposals with Nature Reviews-style academic writing | `/research-proposal`, "research proposal", "PhD proposal", "研究计划" |
| [research-paper](./research-paper/) | Draft **original research articles** (IMRaD) from your completed experiments — results-first, reporting-checklist bound | `/research-paper`, "write the paper", "论文写作" |
| [scholar-slides](./scholar-slides/) | Fidelity-first academic decks for a live talk — vector equations, extracted figures, grounded citations, editable PPTX | "make slides", "组会 PPT", "答辩幻灯片", a paper PDF / arXiv / DOI |
| [lit-search](./lit-search/) | Exhaustive time-windowed literature retrieval with **measurable recall** — quality-tiered DOI list + formatted references | `/lit-search`, "systematic review", "开题报告的文献检索/查全部分", "把某方向近 N 年文献检索全" |

> **Slides from a paper? Two different tools, on purpose.** Use **scholar-slides** for a faithful,
> editable *live talk* — equations, numbers, tables, and citations stay exact and projector-ready.
> Use **paper-slide-deck** for *stylized visual images* to read or share, where look-and-feel
> matters more than editable precision (its slides are AI-generated images, so math and data are
> not editable and can be garbled — don't use it for a defense or a results-heavy talk).

> **Doing a review? Two stages, two skills.** **lit-search** builds the *corpus* — it finds the
> papers and proves how complete the search was. **medical-imaging-review** writes the *review* from
> papers you already have. Running a systematic review end to end means lit-search first, then
> medical-imaging-review over its `dois.md`.

> **Shared anti-fabrication core.** All five writing/rendering skills instantiate the same
> five-rule citation-integrity discipline; the variants are reconciled at development time in
> [docs/citation-integrity-core.md](./docs/citation-integrity-core.md).

## Installation

Copy the desired skill folder into your Claude Code skills directory:

```bash
cp -r medical-imaging-review ~/.claude/skills/
cp -r paper-slide-deck       ~/.claude/skills/
cp -r research-proposal      ~/.claude/skills/
cp -r research-paper         ~/.claude/skills/
cp -r scholar-slides         ~/.claude/skills/
cp -r lit-search             ~/.claude/skills/
```

`scholar-slides` and `lit-search` carry their own toolchains; after copying, provision them once:

```bash
cd ~/.claude/skills/scholar-slides && ./install.sh
cd ~/.claude/skills/lit-search     && ./install.sh   # needs uv + Python 3.11+
```

---

## Medical Imaging Review Skill

Plan, conduct, and draft a medical imaging AI review whose every claim audits back to first sources — narrative review, method survey, scoping review, or systematic review **with qualitative synthesis only** (meta-analysis / umbrella review are explicitly out of scope and route out to a specialized methods workflow).

### Features

- **Four-route contract** — `narrative` / `method-survey` / `scoping` / `systematic` route tokens frozen at intake; matching reporting standards (PRISMA 2020/ScR, QUADAS-3, CLAIM 2024, TRIPOD+AI, PROBAST-family, SWiM) per route
- **Immutable project contract** — `init_review_project.py` scaffolds a timestamped project (`review_config.yaml`, `REVIEW_CONTEXT.md`, `claim_ledger.csv`, `references.bib`, `manuscript.md`, route-specific checklists) with atomic staging; the route cannot silently change after collection begins
- **Stable citekeys, never mutable numbers** — the working draft cites `[@smith2024model]`; the target journal's numeric/author-date style is rendered only at final formatting
- **claim_ledger discipline** — one atomic claim–source pair per row (26 columns: metric, direction, evidence excerpt, verification status, …); drafting reads the ledger, not model memory
- **Executable audit with honest semantics** — `scripts/audit_manuscript.py` binds manuscript citekeys ↔ `references.bib` ↔ claim ledger; `gate_status` can be `fail` / `warning` / `not_assessed` but **never `pass`** (a clean audit proves nothing was found wrong, not that the review is correct); exit codes 0/1/2
- **Human gates stay human** — screening, charting/extraction, risk-of-bias, and certainty steps are logged with named roles and never auto-passed

### Route-aware workflow

1. Route and configure (intake gate) → 2. Initialize project → 3. Design methods (protocol + search plan frozen before screening) → 4. Collect and register sources → 5. Pass human gates → 6. Synthesize within scope → 7. Draft from verified records → 8. Validate and report status.

### Files

| Path | Description |
|------|-------------|
| `SKILL.md` | Route contract, project contract, workflow, audit usage |
| `references/REVIEW_TYPES.md` | Route routing + per-route artifacts and gates |
| `references/REPORTING_STANDARDS.md` | PRISMA / QUADAS-3 / CLAIM / TRIPOD+AI / SWiM standards fit |
| `references/WORKFLOW.md` | Phase-by-phase workflow guide (Phase -1 … 6) |
| `references/PARADIGM.md` | Optional exemplar style capture → `style_profile.json` (schema 2.0) |
| `references/CITATION_INTEGRITY.md` | Citekey/claim-ledger verification protocol |
| `references/HALLUCINATION_PATTERNS.md` | LLM hallucination indicators to self-check |
| `references/TEMPLATES.md` | Project file templates (ledger schema, gates, style profile) |
| `references/DOMAINS.md` | Domain-specific method categories and datasets |
| `references/MCP_SETUP.md` | Literature connector configuration and fallbacks |
| `references/QUALITY_CHECKLIST.md` | Pre-submission quality checklist |
| `scripts/init_review_project.py` | Project initializer (atomic, refuses existing targets) |
| `scripts/audit_manuscript.py` | Executable manuscript audit (`scripts/mir_audit/` package) |
| `tests/` | Fixture test suite locking the audit and initializer contracts |

---

## Paper Slide Deck Skill

Transform any content into stylized, shareable slide **images** (AI-generated), with figure detection and high-resolution page rendering from PDFs.

> Text, math, and data are baked into each image and **not editable** — for a faithful, editable academic talk (组会/答辩/results-heavy) use **scholar-slides** instead.

### Features

- **Caption-based figure detection** from PDF papers (locates the page; human confirmation recommended for dense two-column layouts)
- **Figure-to-slide mapping** with full-page high-res render + template container (not per-figure bbox cropping)
- **17 visual styles** (academic-paper, sketch-notes, minimal, etc.)
- **Gemini API integration** (`gemini-3-pro-image`) for AI slide generation, with a post-generation garbled-text proofread pass
- **PPTX/PDF export** with merge scripts

### Workflow

1. Analyze paper and detect figures/tables
2. Generate outline with auto IMAGE_SOURCE mapping
3. Extract figures from PDF (or AI-generate)
4. Apply academic templates
5. Merge to PPTX/PDF

### Files

| Path | Description |
|------|-------------|
| `SKILL.md` | Main skill definition and workflow |
| `references/` | Analysis framework, templates, style definitions |
| `scripts/` | Python/TypeScript automation scripts |

### Scripts

| Script | Purpose |
|--------|---------|
| `generate-slides.py` | Gemini API image generation |
| `detect-figures.ts` | PDF figure/table detection |
| `extract-figure.ts` | PDF page extraction |
| `apply-template.ts` | Academic figure container template |
| `merge-to-pptx.ts` | PPTX generation |
| `merge-to-pdf.ts` | PDF generation |

---

## Research Proposal Skill

Generate high-quality academic research proposals — PhD applications, research plans, 研究计划书 / 开题报告 — following Nature Reviews-style academic writing conventions.

### Features

- **Structured 5-phase workflow** with a **write-with-verify** content stage: Requirements → Literature (+verification gate) → Outline (approval red line) → Content (section-by-section) → Output
- **Citation-integrity guardrails**: every reference verified to exist (DOI/PMID/arXiv or Zotero) with author and year matching the source — unverifiable entries are flagged, never fabricated
- **Multi-source literature integration**: WebSearch, Zotero MCP, arXiv, PubMed (with tool-portable fallbacks)
- **Bilingual support**: English and Chinese (中文)
- **Domain adaptation**: STEM (incl. computational / ML / AI-for-Science), Humanities, Social Sciences
- **Academic writing style**: prose-based, evidence-calibrated language; reference count follows the argument (no padding quota)

### Workflow

1. Gather requirements (topic, domain, language, word count)
2. Collect literature from multiple sources
3. Generate outline for user approval
4. Write full proposal based on approved outline
5. Output Markdown with quality checklist

### Files

| Path | Description |
|------|-------------|
| `SKILL.md` | Main skill definition and 5-phase workflow |
| `references/STRUCTURE_GUIDE.md` | Section-by-section writing guide |
| `references/DOMAIN_TEMPLATES.md` | STEM vs Humanities differences |
| `references/WRITING_STYLE_GUIDE.md` | Nature Reviews academic writing style |
| `references/CITATION_INTEGRITY.md` | Reference verification protocol (5 rules, author-year style) |
| `references/QUALITY_CHECKLIST.md` | Quality verification checklist |
| `references/LITERATURE_WORKFLOW.md` | Literature collection workflow |
| `assets/proposal_scaffold_en.md` | English template scaffold |
| `assets/proposal_scaffold_zh.md` | Chinese template scaffold |

### Output

- Target: 2,000-4,000 words (default ~3,000)
- References: count follows the argument (typically 25–50; no minimum, no padding), each verified
- 3-5 figure suggestions
- Markdown format (convertible to DOCX/PDF via pandoc)

---

## Research Paper Skill

Draft an **original research article** (IMRaD, conference style, or 中文期刊) from work that is
already done. Two disciplines distinguish it from the proposal/review skills:

- **Results-first.** Methods and Results are written from the user's actual materials
  (result tables, metrics, figures); anything not supplied is flagged `[PENDING]`, never
  filled with a plausible number. A `results_ledger.csv` maps every load-bearing number in
  the draft back to its source artifact, and the Phase 5 gates reconcile them.
- **Reporting-checklist bound.** Study type selects a binding checklist at intake
  (CLAIM 2024 / TRIPOD+AI / STROBE / STARD / venue reproducibility statement); absent-but-
  required items resolve as reporting, disclosure, or a user-accepted gap — never silence.

Citation discipline is the repository's shared five-rule core in journal-style form
([docs/citation-integrity-core.md](./docs/citation-integrity-core.md)); the related-work
corpus can be built by **lit-search** and consumed directly.

---

## Scholar Slides Skill

Turn a research paper (or arXiv/DOI link, or a topic) into a **fidelity-first** slide deck — one where every equation, table, number, figure, and citation stays true vector/text and **traceable to the source**, never rasterized by an image model and never fabricated. Where `paper-slide-deck` optimizes visual style via text-to-image, scholar-slides inverts the priority for scholarly work: **source fidelity > polish**, behind an executable integrity gate.

### Features

- **Fidelity-first rendering** — KaTeX vector equations, real `<table>`/OOXML tables, cited figure crops; numbers grounded against the source, no fabrication
- **Integrity QA gate** — number grounding, `[MISSING]`/`[UNVERIFIED]` flags instead of silent fills, PPTX-parity regression, a scoreable aesthetics rubric
- **Two registers** — journal-club (组会, reading-first) and conference (big-room), via a token-based theme system
- **Bilingual** — English default, full 中文 / CJK support
- **Zotero-first citations** with Crossref / arXiv / DOI fallback

### Outputs

- Interactive reveal.js deck (with browser speaker view)
- One-page-per-slide **vector PDF**
- **Editable PPTX** (native text, bullets, tables, speaker notes; equations/figures as flagged images)
- Speaker notes with a bilingual talk-time estimate

### Install & run

```bash
cd ~/.claude/skills/scholar-slides && ./install.sh   # .venv + npm + Chromium, then self-checks
```

Prereqs: **Python 3.11+, Node 18+.** For Chinese decks on Linux: `sudo apt-get install fonts-noto-cjk` (macOS/Windows already have CJK fonts).

### Known limitation

Figure localization is layout-dependent — ~95–100% on single-column / arXiv / Nature-style papers, ~75% on dense IEEE/TPAMI two-column pages. Low-confidence crops are **flagged for you to confirm**, never silently wrong. Stress-tested across cross-layout papers with 0 crashes; on the corpus checked in under `out/*/figures.json` the figure localization rate is reproducibly **60/61 ≈ 98.4%**. See [scholar-slides/README.md](./scholar-slides/README.md) for the full story.

Design rationale and the 6-repo landscape survey behind this skill live in [docs/scholar-slides-design/](./docs/scholar-slides-design/).

---

## Lit Search Skill

Retrieve **everything** published on a topic inside a time window, and be able to say *how much you missed*. Chat-style search returns "the top few by relevance" — not reproducible, and silent about its own gaps. This skill turns retrieval into a deterministic pipeline: **multi-source × full pagination × citation closure × a measurable saturation criterion**, then delivers the corpus.

### Features

- **Recall is measured, not claimed** — gold-set recall, out-of-window leakage controls, per-source unique contribution, snowball saturation curve, PRISMA counts that *refuse to render* when they don't add up
- **Says what it did NOT do** — sources declared but never contacted, unimplemented sources, skipped citation closure: each appears in `coverage_report.md` with a computed reason. "No gaps" is written out as a conclusion, never implied by a blank section
- **Annotates quality, never filters** — CCF grade / journal metric / citation percentile decide *order*, not inclusion. A threshold would conflate "not evaluated" with "low quality" (measured: cutting at 4.0 dropped 340 papers that had *no metric at all*)
- **Reaches closed publishers' metadata** — Elsevier 95.6% / Springer 80.4% / IEEE 98.7% abstract coverage via OpenAlex + PubMed. It does **not** bypass paywalls
- **Human adjudication flows back in** — screening disagreements and boundary dates re-import with reviewer, timestamp, reason, and the prior verdict preserved
- **Three depth tiers** with cost and wall-clock stated *before* you run (`lit depths`)

### Outputs

`dois.md` (full DOI list, sectioned by quality tier, evidence per entry) · `references.md` (same order, GB/T 7714 / APA / IEEE / Nature / AMA) · `references.bib` (with `--bibtex`) · `PRISMA.md` · `coverage_report.md` · `human_queue.csv`

### Install & run

```bash
cd ~/.claude/skills/lit-search && ./install.sh   # uv sync + CLI smoke check
uv run lit depths                                # scale, time and cost per tier
```

Prereqs: **[uv](https://docs.astral.sh/uv/) + Python 3.11+.** **No API key needed to start** — screening can run on the host Claude Code (`lit screen --model host`). For 10k+ record runs, point it at any OpenAI-compatible endpoint instead.

Keep run artifacts out of the skill folder — always pass `--runs-root /your/project/runs`; a systematic run reaches hundreds of MB.

### Not bundled, on purpose

Journal ranking data (JCR quartiles, 中科院分区) is commercially licensed and the CCF catalogue is copyrighted — supply your own via `--ccf`. Without a catalogue the tool marks conferences "unrated" rather than guessing a grade: **a fabricated CCF-A looks exactly like a real one.**

---

## License

MIT License
