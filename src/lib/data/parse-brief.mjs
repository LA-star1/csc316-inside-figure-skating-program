const TABLES = [
	['segments', 'Segment-level scores'],
	['elements', 'Full element-by-element protocol'],
	['components', 'Program components']
];

function tableAfterHeading(markdown, heading) {
	const headingIndex = markdown.indexOf(`### ${heading}`);
	if (headingIndex < 0) throw new Error(`Missing data section: ${heading}`);
	const fenceStart = markdown.indexOf('```tsv', headingIndex);
	if (fenceStart < 0) throw new Error(`Missing TSV table after: ${heading}`);
	const contentStart = markdown.indexOf('\n', fenceStart) + 1;
	const fenceEnd = markdown.indexOf('\n```', contentStart);
	if (fenceEnd < 0) throw new Error(`Unclosed TSV table after: ${heading}`);
	return markdown.slice(contentStart, fenceEnd).trim().split(/\r?\n/);
}

function parseValue(value) {
	const trimmed = value.trim();
	if (trimmed === '') return null;
	if (/^-?(?:\d+\.?\d*|\.\d+)$/.test(trimmed)) return Number(trimmed);
	return trimmed;
}

function parseTable(markdown, heading) {
	const [header, ...rows] = tableAfterHeading(markdown, heading);
	const columns = header.split('\t');
	return rows.map((line, rowIndex) => {
		const values = line.split('\t');
		if (values.length !== columns.length) {
			throw new Error(`${heading} row ${rowIndex + 1}: expected ${columns.length} fields, got ${values.length}`);
		}
		return Object.fromEntries(columns.map((column, index) => [column, parseValue(values[index])]));
	});
}

export function parseBrief(markdown) {
	return Object.fromEntries(TABLES.map(([key, heading]) => [key, parseTable(markdown, heading)]));
}
