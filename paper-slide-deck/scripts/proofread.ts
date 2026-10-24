// Proofread gate for AI-generated slides (SKILL.md Step 6.5).
//
// Text-to-image bakes text into pixels and garbles math, numbers and spelling. Step 6.5 asks the
// agent to open every generated slide and check it; this module makes skipping that visible:
//
//   generated.json  — written by generate-slides.py: every slide it produced, with its sha256
//   proofread.json  — written by `proofread.ts --mark`: a disposition per slide, bound to the
//                     sha256 of the bytes that were actually looked at
//
// merge-to-pptx / merge-to-pdf refuse a deck in which a recorded slide has no disposition, or
// whose bytes changed after it was proofread (a regenerated slide is a new image). `check`
// dispositions are allowed but listed — they are the [CHECK] slides of the Step 8 summary.
// A deck without generated.json (extract-only, or generated before this gate) is not gated.
//
//   bun proofread.ts --mark <deck-dir> <NN-slide-x.png> ok|check [--note "garbled σ in eq. 2"]

import { createHash } from "crypto";
import { existsSync, readFileSync, writeFileSync, renameSync } from "fs";
import { join } from "path";

export const GENERATED = "generated.json";
export const PROOFREAD = "proofread.json";
const STATUSES = new Set(["ok", "check"]);

interface Entry { sha256?: string; status?: string; note?: string }

export function sha256File(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function readSlides(path: string): Record<string, Entry> {
  if (!existsSync(path)) return {};
  const parsed = JSON.parse(readFileSync(path, "utf-8"));
  return (parsed && typeof parsed.slides === "object" && parsed.slides) || {};
}

export function proofreadGate(
  dir: string,
  slides: Array<{ filename: string; path: string }>,
  { allowUnproofread = false }: { allowUnproofread?: boolean } = {}
): { fatal: string[]; warnings: string[]; checks: string[] } {
  const fatal: string[] = [];
  const warnings: string[] = [];
  const checks: string[] = [];
  const generatedPath = join(dir, GENERATED);
  if (!existsSync(generatedPath)) return { fatal, warnings, checks };
  let generated: Record<string, Entry>;
  let proofread: Record<string, Entry>;
  try {
    generated = readSlides(generatedPath);
    proofread = readSlides(join(dir, PROOFREAD));
  } catch (err: any) {
    // An unreadable ledger must not read as "nothing to proofread".
    fatal.push(`cannot read ${GENERATED}/${PROOFREAD}: ${err?.message ?? err}`);
    return { fatal, warnings, checks };
  }
  const unproofread: string[] = [];
  for (const slide of slides) {
    if (!(slide.filename in generated)) continue; // extracted figure / hand-made slide
    const entry = proofread[slide.filename];
    if (!entry || !STATUSES.has(entry.status ?? "")) {
      unproofread.push(`${slide.filename} (no proofread disposition)`);
    } else if (entry.sha256 !== sha256File(slide.path)) {
      unproofread.push(`${slide.filename} (changed since it was proofread — re-check the new image)`);
    } else if (entry.status === "check") {
      checks.push(`${slide.filename}${entry.note ? ` — ${entry.note}` : ""}`);
    }
  }
  if (unproofread.length) {
    const msg = `${unproofread.length} AI-generated slide(s) not proofread (SKILL.md Step 6.5): ${unproofread.join("; ")}`;
    (allowUnproofread ? warnings : fatal).push(msg);
  }
  return { fatal, warnings, checks };
}

/** Print the gate result; return the exit code the merge should use (0 or 1). */
export function reportProofread(result: ReturnType<typeof proofreadGate>, allowUnproofread: boolean): number {
  for (const c of result.checks) console.error(`[CHECK] ${c}`);
  for (const w of result.warnings) console.error(`Warning: ${w} — merging anyway (--allow-unproofread)`);
  for (const f of result.fatal) console.error(`Error: ${f}`);
  if (result.fatal.length) {
    console.error(
      "Open each listed slide, check spelling / math / numbers, then record it:\n" +
        "  bun proofread.ts --mark <deck-dir> <slide-file> ok|check [--note \"…\"]\n" +
        (allowUnproofread ? "" : "Or pass --allow-unproofread to merge anyway (the deck then ships unchecked).")
    );
    return 1;
  }
  return 0;
}

export function markProofread(dir: string, filename: string, status: string, note?: string): void {
  if (!STATUSES.has(status)) throw new Error(`status must be ok or check, got "${status}"`);
  const slidePath = join(dir, filename);
  if (!existsSync(slidePath)) throw new Error(`slide not found: ${slidePath}`);
  const path = join(dir, PROOFREAD);
  const slides = readSlides(path);
  slides[filename] = { sha256: sha256File(slidePath), status, ...(note ? { note } : {}) };
  const tmp = `${path}.tmp`;
  writeFileSync(tmp, JSON.stringify({ slides }, null, 2) + "\n");
  renameSync(tmp, path);
}

if ((import.meta as any).main) {
  const args = process.argv.slice(2);
  const noteAt = args.indexOf("--note");
  const note = noteAt >= 0 ? args[noteAt + 1] : undefined;
  const positional = args.filter((a, i) => a !== "--mark" && a !== "--note" && i !== noteAt + 1);
  if (args[0] !== "--mark" || positional.length !== 3) {
    console.error('Usage: bun proofread.ts --mark <deck-dir> <slide-file> ok|check [--note "…"]');
    process.exit(2);
  }
  try {
    markProofread(positional[0], positional[1], positional[2], note);
    console.log(`Recorded: ${positional[1]} → ${positional[2]}`);
  } catch (err: any) {
    console.error(`Error: ${err.message}`);
    process.exit(2);
  }
}
