import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { parseBrief } from '../src/lib/data/parse-brief.mjs';
import { elementId, segmentScoreAudit, summarizeJumpShare } from '../src/lib/data/derived.mjs';

const sourcePath = new URL('../data/source/Beijing_2022_Mens_Singles_Top10_Data_Brief.md', import.meta.url);
const outputDir = new URL('../static/data/', import.meta.url);
const source = await readFile(sourcePath, 'utf8');
const data = parseBrief(source);
data.elements = data.elements.map((element) => ({ ...element, id: elementId(element) }));
data.jumpShare = summarizeJumpShare(data.elements);
data.segmentAudit = segmentScoreAudit(data);

await mkdir(outputDir, { recursive: true });
await writeFile(new URL('competition.json', outputDir), `${JSON.stringify(data, null, 2)}\n`);
console.log(`Wrote ${data.elements.length} elements, ${data.segments.length} segments, ${data.components.length} components.`);
