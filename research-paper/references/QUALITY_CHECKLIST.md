# Quality Checklist

Split into **mechanical gates** (paste command output as evidence — a gate
without output is unchecked) and **judgment items** (anchored). The results
ledger reconciliation is the paper-specific gate that has no counterpart in
the proposal skill: your own numbers are the fabrication risk here.

## Mechanical gates

- [ ] Placeholder gate returns 0 hits, or every `[UNVERIFIED]`/`[PENDING]` is
      explicitly disclosed and never presented as real:
      `grep -nE "xxx|XXXX|\[TBD\]|\[PENDING|\[UNVERIFIED\]|10\.xxxx|doi:10\.[a-z]+/x" paper_draft.md`
- [ ] AI-tell gate returns 0 hits (regex in SKILL.md Phase 5).
- [ ] **results_ledger reconciliation**: every number in Abstract/Results
      appears in `results_ledger.csv` with the same value; every ledger row
      backing a claim is actually cited in the text. Diff method: extract
      numeric tokens from Results and compare against the ledger's value
      column — differences are either retyped-from-memory errors (fix) or
      formatting (e.g. percent vs. fraction — unify).
- [ ] Citation reconciliation: in-text ↔ bibliography 1:1 both directions
      (see CITATION_INTEGRITY.md).
- [ ] Abbreviation list complete: every abbreviation defined at first use.
- [ ] Abstract word count within the venue limit (`wc -w`).

## results_ledger.csv (built in Phase 2, checked in Phase 5)

One row per load-bearing number:

```csv
claim_id,section,claim_text,value,unit,dispersion,source_artifact,source_locator,status
R1,Results-3.1,"mean Dice on external test set",0.847,,95% CI 0.82-0.87,results/external_test.csv,row 14,verified
R2,Abstract,"AUC improved by 4.1 points",4.1,points,,results/main_table.tex,Table 1,verified
```

`status` ∈ verified | pending (pending rows must not appear in the draft
without a `[PENDING]` flag).

## Judgment items (anchored scoring)

- **5** — a domain expert reading only this section would not reorder, delete,
  or caveat anything; every claim carries evidence; all gates pass.
- **4** — at most one paragraph needs reweighting or one claim a stronger
  source; gates pass.
- **3** — does its job, but a supervisor would return it with specific line
  comments; gates pass.
- **2** — structural problem (results don't support the claims as ordered;
  any mechanical gate fails).
- **1** — missing/boilerplate content, or **any fabricated-or-untraceable
  number** (caps the whole paper at 1 regardless of other strengths).

| Dimension | Weight |
|---|---|
| Claims ↔ evidence (Results ordering & support) | 25% |
| Methods reproducibility | 20% |
| Reporting-checklist completeness | 20% |
| Writing style / cohesion | 15% |
| Discussion & limitations honesty | 10% |
| Title/abstract fidelity | 10% |

Minimum: nothing below 3 with named anchor evidence; weighted average ≥ 3.5;
all mechanical gates pass.
