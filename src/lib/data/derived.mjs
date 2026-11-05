export function elementId(element) {
	return `${element.segment}:${element.final_rank}:${element.element_order}`;
}

export function countJumpElements(elements) {
	const groups = new Map();
	for (const element of elements.filter((item) => item.element_group === 'jump')) {
		const key = `${element.segment}:${element.final_rank}:${element.skater}`;
		const group = groups.get(key) ?? { segment: element.segment, final_rank: element.final_rank, skater: element.skater, count: 0 };
		group.count += 1;
		groups.set(key, group);
	}
	return [...groups.values()];
}

export function jumpRotations(element) {
	return [...element.element_code_raw.matchAll(/([1-4])(?=[A-Z])/g)].reduce((sum, match) => sum + Number(match[1]), 0);
}

export function protocolMarks(element) {
	const code = element.element_code_raw;
	const info = element.info_flag ?? '';
	return ['<<', '<', 'e', 'q', '!', '*'].filter((mark) => {
		if (mark === '<<') return info.includes('<<') || code.includes('<<');
		if (mark === '<') return info === '<' || (code.includes('<') && !code.includes('<<'));
		if (info.includes(mark)) return true;
		if (mark === 'e') return /[1-4][A-Z]+e/.test(code);
		return code.includes(mark);
	});
}

export function summarizeJumpShare(elements) {
	return ['SP', 'FS'].map((segment) => {
		const rows = elements.filter((element) => element.segment === segment);
		const totalElementPoints = rows.reduce((sum, element) => sum + element.panel_element_score, 0);
		const jumpPoints = rows
			.filter((element) => element.element_group === 'jump')
			.reduce((sum, element) => sum + element.panel_element_score, 0);
		return { segment, jumpPoints, totalElementPoints, share: jumpPoints / totalElementPoints };
	});
}

export function segmentScoreAudit({ segments, elements }) {
	return segments.map((segment) => {
		const rows = elements.filter((element) => element.skater === segment.skater && element.segment === segment.segment);
		const elementSum = rows.reduce((sum, element) => sum + element.panel_element_score, 0);
		return {
			...segment,
			calculated_element_sum: Number(elementSum.toFixed(2)),
			calculated_tss: Number((segment.TES + segment.PCS_factored + segment.deductions).toFixed(2)),
			element_count_matches: rows.length === segment.element_count,
			tes_matches: Math.abs(elementSum - segment.TES) <= 0.01,
			tss_matches: Math.abs(segment.TES + segment.PCS_factored + segment.deductions - segment.segment_score_TSS) <= 0.01
		};
	});
}
