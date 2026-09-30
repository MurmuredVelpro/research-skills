# Citation Integrity Core

Development-time single source of truth for the anti-fabrication discipline shared by this
repository's research skills. **Each skill ships a self-contained variant** (skills install by
whole-directory copy, so cross-skill relative links would dangle); this file is where the
variants are reconciled, not something any skill reads at runtime. When editing a variant,
update its derivation marker and this core so drift is visible.

## The shared rules

Every variant instantiates the same five rules. Wording differs by citation convention; the
discipline does not.

1. **Existence before use.** A source enters the bibliography / references slide only after
   its existence is confirmed against a first source: a resolvable DOI, a PMID, an arXiv id,
   Zotero metadata, or the publisher/repository record. Verification happens at collection
   time, never "later".
2. **Identity must match verbatim.** Author names, year, and venue as cited must match the
   source exactly — not "close enough", not silently corrected, not normalized by memory.
3. **Unverifiable → flag, never include silently.** Anything that cannot be verified emits a
   visible `[UNVERIFIED]` marker and an explicit disclosure to the user. The user decides;
   the skill never launders a maybe into a yes.
4. **Never invent the furniture.** DOIs, journal names, volume/issue, page numbers, author
   lists, registry ids, and numbers are never fabricated to make an entry "look real".
   Fabricated metadata is indistinguishable from real metadata to a reader — that is exactly
   why it is forbidden.
5. **Claims match their source.** Every quantitative or directional claim carried by a
   citation matches the source in magnitude and direction; scope conditions and hedges
   survive the paraphrase.

Governing principle, inherited by every variant: **宁可少，不可假** — better fewer references
than one fake. Count follows the argument; there is no quota and no padding.

## Shared flag taxonomy

Literal markers the gates scan for (each variant uses the subset that applies):

- `[UNVERIFIED: …]` — a citation or value could not be resolved against a first source.
- `[MISSING: …]` — a referenced asset could not be extracted/located.
- `[CHECK]` — a generated slide failed visual proofreading after retries.
- `[REDRAWN]` / `[GENERATED]` — an asset is not from the source and is labeled as such.

A deliverable ships with flags **only** after the user has seen and accepted each one.

## Variant registry

| Skill | Variant file | Convention | Enforcement gate |
|---|---|---|---|
| medical-imaging-review | `references/CITATION_INTEGRITY.md` | stable citekeys `[@key]` + `claim_ledger.csv` (schema 2.0) | executable audit (`scripts/audit_manuscript.py`, exit 0/1/2) |
| research-proposal | `references/CITATION_INTEGRITY.md` | (Author, Year) / GB/T 7714 顺序编码制 | Phase 2 verification gate + Phase 5 grep citation gate |
| scholar-slides | `references/integrity.md` | Zotero-grounded citations, `[Figure N]` attribution | CKPT-3 self-review + integrity QA (number grounding, flag scan) |
| paper-slide-deck | `SKILL.md` Step 6.5 | citations baked into images | post-generation visual proofread, `[CHECK]` escalation |

Variant-specific extensions stay in the variant: the medical ledger's split/comparator/
uncertainty columns, the proposal's (Author, Year) reconciliation regex, the slides' figure
provenance rules, and the T2I garble protocol are **not** part of the core.

## When a fifth variant appears

Copy the closest existing variant, mark its header `Derived from docs/citation-integrity-core.md
(convention: …)`, add the row above, and keep the five core rules intact — conventions differ,
the rules do not.
