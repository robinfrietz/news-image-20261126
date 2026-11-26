// news-image-20261126 entry (Node 22+, standard library only).
//
// The entry image is the entry.png beside this file: a 1024x1024 infographic
// summing up the world news of Thursday 26 November 2026. This program copies
// it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png outside the
// grader's container) and then verifies the copy by reading it back: the
// bytes must match the source exactly and stay within the competition's
// 1 MiB limit.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1_048_576; // 1 MiB, the competition limit

const source = new URL("./entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");

copyFileSync(source, target);

// Verify the output by reading it back: same bytes as the source image,
// and no larger than the 1 MiB cap the gate enforces.
const written = readFileSync(target);
const expected = readFileSync(source);
if (!written.equals(expected)) {
  throw new Error(
    `output mismatch: ${target} bytes differ from entry.png (${written.length} vs ${expected.length})`,
  );
}
const { size } = statSync(target);
if (size < 1 || size > MAX_BYTES) {
  throw new Error(`output size ${size} bytes outside 1-${MAX_BYTES} limit`);
}

console.log(`wrote ${target} (${size} bytes, verified byte-identical)`);
