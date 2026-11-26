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

// Additional integrity checks on the written PNG itself: the 8-byte PNG
// signature must be present and the IHDR header must report dimensions
// within the 1024x1024 bound this entry is built to. These guard against a
// truncated or non-PNG file slipping through the byte-equality check above
// if the source itself were ever corrupted.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (written.length < 33 || !written.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error(`output is not a PNG: missing PNG signature in ${target}`);
}
if (written.subarray(12, 16).toString("ascii") !== "IHDR") {
  throw new Error(`output is not a PNG: missing IHDR chunk in ${target}`);
}
const pngWidth = written.readUInt32BE(16);
const pngHeight = written.readUInt32BE(20);
if (pngWidth < 1 || pngWidth > 1024 || pngHeight < 1 || pngHeight > 1024) {
  throw new Error(
    `output PNG dimensions ${pngWidth}x${pngHeight} outside 1-1024 bound`,
  );
}

console.log(
  `wrote ${target} (${size} bytes, verified byte-identical, PNG ${pngWidth}x${pngHeight})`,
);
