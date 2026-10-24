// deckTypeAudit tests (node --test tests/deck_type.test.mjs): each deck type's required content
// roles (references/deck-types.md) — a conforming deck of each type is clean, each missing role is
// named, an unknown type is P1.
import { test } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import { deckTypeAudit, DECK_TYPES } from "../scripts/lib/qa.mjs";

const s = (layout, title, extra = {}) => ({ layout, action_title: title, ...extra });

const JOURNAL_CLUB = {
  meta: { deck_type: "journal-club" },
  slides: [
    s("paper-title", "Paper"), s("bullets", "Claims", { points: ["a"] }),
    s("critique-concerns", "Concerns", { points: ["c"] }),
    s("discussion-questions", "Discussion", { questions: ["q"] }),
  ],
};
const DEFENSE = {
  meta: { deck_type: "defense" },
  slides: [
    s("paper-title", "Thesis"), s("section", undefined, { title: "Contribution 1" }),
    s("bullets", "Limitations and future work", { points: ["l"] }),
    s("section", undefined, { title: "Backup" }),
    s("results-table", "Extra ablation", { table: { rows: [["a", "1"]] } }),
  ],
};
const CONFERENCE = {
  meta: { deck_type: "conference" },
  slides: [s("paper-title", "Talk"), s("assertion-evidence", "Main result")],
};
const checks = (findings) => findings.map((f) => `${f.severity}:${f.check}`).sort();
const without = (deck, layout) => ({ ...deck, slides: deck.slides.filter((x) => x.layout !== layout) });

test("a conforming deck of each type has no deck-type finding", () => {
  for (const deck of [JOURNAL_CLUB, DEFENSE, CONFERENCE]) {
    assert.deepEqual(deckTypeAudit(deck), [], deck.meta.deck_type);
  }
});

test("journal-club: each missing critique / discussion slide is a P2 naming the layout", () => {
  const noCritique = deckTypeAudit(without(JOURNAL_CLUB, "critique-concerns"));
  assert.deepEqual(checks(noCritique), ["P2:missing-archetype"]);
  assert.match(noCritique[0].detail, /critique-concerns/);
  const noDiscussion = deckTypeAudit(without(JOURNAL_CLUB, "discussion-questions"));
  assert.deepEqual(checks(noDiscussion), ["P2:missing-archetype"]);
  assert.match(noDiscussion[0].detail, /discussion-questions/);
});

test("absent deck_type is audited as journal-club", () => {
  const deck = { slides: [s("paper-title", "Paper")] };
  assert.deepEqual(checks(deckTypeAudit(deck)), ["P2:missing-archetype", "P2:missing-archetype"]);
});

test("defense: no Backup divider is a P2", () => {
  const deck = { ...DEFENSE, slides: DEFENSE.slides.filter((x) => x.title !== "Backup") };
  assert.deepEqual(checks(deckTypeAudit(deck)), ["P2:missing-backup"]);
});

test("defense: a Backup divider with nothing after it is a P2", () => {
  const deck = { ...DEFENSE, slides: DEFENSE.slides.slice(0, -1) };
  assert.deepEqual(checks(deckTypeAudit(deck)), ["P2:missing-backup"]);
});

test("defense: Chinese 附录 divider counts as Backup", () => {
  const slides = DEFENSE.slides.map((x) => (x.title === "Backup" ? { ...x, title: "附录" } : x));
  assert.deepEqual(deckTypeAudit({ ...DEFENSE, slides }), []);
});

test("defense: no limitations / future-work slide is a P2", () => {
  const slides = DEFENSE.slides.map((x) =>
    x.action_title === "Limitations and future work" ? { ...x, action_title: "Summary" } : x);
  assert.deepEqual(checks(deckTypeAudit({ ...DEFENSE, slides })), ["P2:missing-limitations"]);
});

test("defense: Chinese 局限与展望 title counts", () => {
  const slides = DEFENSE.slides.map((x) =>
    x.action_title === "Limitations and future work" ? { ...x, action_title: "局限与展望" } : x);
  assert.deepEqual(deckTypeAudit({ ...DEFENSE, slides }), []);
});

test("conference: a critique slide is a P3 on that slide", () => {
  const deck = { ...CONFERENCE, slides: [...CONFERENCE.slides, s("critique-concerns", "Concerns", { points: ["c"] })] };
  const findings = deckTypeAudit(deck);
  assert.deepEqual(checks(findings), ["P3:critique-in-conference"]);
  assert.equal(findings[0].slide, 3);
});

test("conference does not demand journal-club archetypes", () => {
  assert.deepEqual(deckTypeAudit(CONFERENCE), []);
});

test("unknown deck_type is P1 naming the allowed values", () => {
  const findings = deckTypeAudit({ meta: { deck_type: "poster" }, slides: [] });
  assert.deepEqual(checks(findings), ["P1:unknown-deck-type"]);
  for (const t of DECK_TYPES) assert.match(findings[0].detail, new RegExp(t));
});

test("qa_report wires deckTypeAudit into the CKPT-3 report", () => {
  const src = fs.readFileSync(new URL("../scripts/qa_report.mjs", import.meta.url), "utf-8");
  assert.match(src, /for \(const d of deckTypeAudit\(deck\)\) findings\.push\(\{ stage: "deck-type", \.\.\.d \}\)/);
});
