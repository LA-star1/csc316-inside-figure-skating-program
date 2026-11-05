<script>
	import { onMount } from 'svelte';
	import JumpShareChart from './lib/charts/JumpShareChart.svelte';
	import ScoreComparison from './lib/charts/ScoreComparison.svelte';
	import JumpCounts from './lib/charts/JumpCounts.svelte';
	import RotationGoe from './lib/charts/RotationGoe.svelte';
	import SpinStepLevels from './lib/charts/SpinStepLevels.svelte';
	import ProtocolMatrix from './lib/charts/ProtocolMatrix.svelte';
	import BaseVsPanel from './lib/charts/BaseVsPanel.svelte';

	let data = $state(null);
	let loadError = $state('');
	let selectedRank = $state(1);
	let selectedSegment = $state('SP');
	let selectedElementId = $state(null);
	let selectedSkater = $derived(data?.segments.find((d) => d.final_rank === selectedRank)?.skater ?? '');
	let segmentRows = $derived(data?.segments.filter((d) => d.skater === selectedSkater) ?? []);
	let selectedProgram = $derived(segmentRows.find((d) => d.segment === selectedSegment));
	let programElements = $derived((data?.elements ?? [])
		.filter((d) => d.skater === selectedSkater && d.segment === selectedSegment)
		.sort((a, b) => a.element_order - b.element_order));
	let selectedElement = $derived(programElements.find((d) => d.id === selectedElementId) ?? programElements[0] ?? null);
	let jumpShare = $derived(data?.jumpShare ?? []);
	let allElements = $derived(data?.elements ?? []);

	onMount(async () => {
		try {
			const response = await fetch('/data/competition.json');
			if (!response.ok) throw new Error(`Data request failed (${response.status})`);
			data = await response.json();
		} catch (error) {
			loadError = error instanceof Error ? error.message : 'Unable to load the competition data.';
		}
	});

	$effect(() => {
		if (programElements.length && !programElements.some((d) => d.id === selectedElementId)) {
			selectedElementId = programElements[0].id;
		}
	});

	function selectFromChart(element) {
		selectedRank = element.final_rank;
		selectedSegment = element.segment;
		selectedElementId = element.id;
		document.querySelector('#explore')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
	}
</script>

<main>
	<header class="hero">
		<div class="hero-top"><span class="eyebrow">CSC316 · Beijing 2022 · Men’s singles</span><span class="issue">THE SCORE, DECODED</span></div>
		<div class="hero-copy">
			<p class="kicker">Inside a figure-skating program</p>
			<h1>Jumps carry most of the technical score.<br /><em>And more in the free skate.</em></h1>
			<p class="deck">Across the event’s top ten, jump elements account for 67.4% of technical element points in the short program and 77.1% in the free skate.</p>
			<a class="jump-link" href="#explore">Explore one program <span aria-hidden="true">↓</span></a>
		</div>
		<div class="hero-chart panel">
			<div class="panel-heading"><div><span class="section-number">01 / THE PATTERN</span><h2>Jump points take a larger share in the free skate</h2></div><span class="delta">+9.7 pp</span></div>
			{#if loadError}<p class="error" role="alert">{loadError}</p>{:else if jumpShare.length}<JumpShareChart data={jumpShare} />{:else}<p class="loading">Loading official protocol data…</p>{/if}
		</div>
		<div class="source-line">A top-ten cohort analysis · 10 skaters · official ISU element panel scores · <a href="https://results.isu.org/results/season2122/owg2022/" target="_blank" rel="noreferrer">Source: ISU results</a></div>
	</header>

	<section class="explore section-wrap" id="explore">
		<div class="section-intro">
			<div><span class="section-number">02 / FOLLOW THE SCORE</span><h2>One program, three connected views</h2></div>
			<p>Select a skater, switch between programs, then choose an element. The protocol, score breakdown, and reference panel stay in sync.</p>
		</div>
		{#if data}
			<div class="controls panel">
				<label>Skater
					<select bind:value={selectedRank}>
						{#each data.segments.filter((d) => d.segment === 'SP').sort((a,b) => a.final_rank - b.final_rank) as skater (skater.final_rank)}
							<option value={skater.final_rank}>#{skater.final_rank} · {skater.skater} ({skater.NOC})</option>
						{/each}
					</select>
				</label>
				<div class="segment-control" role="group" aria-label="Choose skating program">
					<button class:active={selectedSegment === 'SP'} onclick={() => selectedSegment = 'SP'}>Short program <small>7 elements</small></button>
					<button class:active={selectedSegment === 'FS'} onclick={() => selectedSegment = 'FS'}>Free skate <small>12 elements</small></button>
				</div>
				<div class="program-score"><span>Program total · TSS</span><strong>{selectedProgram?.segment_score_TSS.toFixed(2) ?? '—'}</strong></div>
			</div>

			<div class="three-col">
				<section class="column panel" aria-labelledby="sequence-title">
					<div class="column-head"><span class="section-number">A · SEQUENCE</span><h3 id="sequence-title">Element order</h3><p>Official protocol order; not a timeline or rink map.</p></div>
					<ol class="sequence">
						{#each programElements as element (element.id)}
							<li><button class:selected={selectedElement?.id === element.id} onclick={() => selectedElementId = element.id} aria-pressed={selectedElement?.id === element.id}>
								<span class="order">{String(element.element_order).padStart(2,'0')}</span><span class="element-name"><b>{element.element_code_raw}</b><small>{element.element_group.replace('_',' ')}</small></span><span class="element-score">{element.panel_element_score.toFixed(2)}</span>
							</button></li>
						{/each}
					</ol>
				</section>

				<section class="column panel score-column" aria-labelledby="detail-title">
					<div class="column-head"><span class="section-number">B · ELEMENT SCORE</span><h3 id="detail-title">What the protocol awarded</h3><p>Official panel values for the selected element.</p></div>
					{#if selectedElement}
						<div class="selected-element"><span>ELEMENT {String(selectedElement.element_order).padStart(2,'0')}</span><h4>{selectedElement.element_code_raw}</h4><p>{selectedElement.element_group.replace('_',' ')} · {selectedSegment === 'SP' ? 'Short program' : 'Free skate'}</p></div>
						<div class="score-math"><div><span>Base value</span><b>{selectedElement.base_value.toFixed(2)}</b></div><div><span>GOE</span><b class:negative={selectedElement.goe < 0}>{selectedElement.goe > 0 ? '+' : ''}{selectedElement.goe.toFixed(2)}</b></div><div class="final-score"><span>Panel score</span><b>{selectedElement.panel_element_score.toFixed(2)}</b></div></div>
						{#if selectedElement.info_flag}<p class="flag-note"><strong>Protocol mark: {selectedElement.info_flag}</strong> · Check the official notation key for this call.</p>{/if}
						<div class="program-math"><span>PROGRAM TOTAL</span><strong>{selectedProgram?.TES.toFixed(2)} TES + {selectedProgram?.PCS_factored.toFixed(2)} PCS {selectedProgram?.deductions && selectedProgram.deductions < 0 ? `− ${Math.abs(selectedProgram.deductions).toFixed(2)} deductions` : ''}</strong><b>= {selectedProgram?.segment_score_TSS.toFixed(2)} TSS</b></div>
					{:else}<p class="loading">Choose an element from the sequence.</p>{/if}
					<p class="score-caveat">An element score combines base value and Grade of Execution (GOE). It does not measure the full artistic or athletic performance.</p>
				</section>

				<section class="column panel motion-column" aria-labelledby="motion-title">
					<div class="column-head"><span class="section-number">C · 3D REFERENCE</span><h3 id="motion-title">A movement example</h3><p>Illustrative Single Axel demonstration.</p></div>
					<div class="motion-frame"><iframe src="https://figure-skating-axel-demo.billziang-chen.chatgpt.site/" title="Illustrative 3D Single Axel demonstration" loading="lazy" allow="fullscreen" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
					<p class="motion-caveat">This is a generic reference demo, not motion capture of {selectedSkater || 'the selected skater'} or a Beijing 2022 performance.</p>
					<a class="text-link" href="https://figure-skating-axel-demo.billziang-chen.chatgpt.site/" target="_blank" rel="noreferrer">Open the 3D demo in a new tab ↗</a>
				</section>
			</div>
			<div class="matrix-card panel">
				<div class="panel-heading"><div><span class="section-number">S11 · NOVEL VIEW</span><h2>Protocol marks in {selectedSkater || 'the selected program'}’s {selectedSegment === 'SP' ? 'short program' : 'free skate'}</h2></div><span class="selected-label">Select a marked cell to link the element</span></div>
				{#if programElements.length}<ProtocolMatrix elements={programElements} selectedId={selectedElement?.id} onSelect={(id) => selectedElementId = id} />{/if}
			</div>
		{:else if loadError}<p class="error" role="alert">Could not load program data: {loadError}</p>{:else}<p class="loading">Loading program data…</p>{/if}
	</section>

	<section class="analysis section-wrap">
		<div class="section-intro"><div><span class="section-number">03 / READ THE SCORE</span><h2>Technical points are part of the total</h2></div><p>Compare technical element score with the segment result. The two measures connect by scoring rules, so read them as parts of one total.</p></div>
		<div class="analysis-card panel"><div class="panel-heading"><div><span class="section-number">S12 · SEGMENT SCORE</span><h2>{selectedSkater || 'Selected skater'} · short program and free skate</h2></div><span class="selected-label">Selection linked to explorer ↑</span></div>
			{#if segmentRows.length}<ScoreComparison segments={segmentRows} />{:else}<p class="loading">Loading score summary…</p>{/if}
		</div>
		<div class="analysis-note"><span class="note-mark">i</span><p><strong>How to read this:</strong> TES is the sum of element panel scores. TSS adds program component score (PCS) and deductions. The protocol order does not provide element timestamps or rink positions.</p></div>
		<div class="analysis-grid">
			<article class="analysis-card panel"><div class="panel-heading"><div><span class="section-number">S01 · JUMP ELEMENT COUNTS</span><h2>How many scored jump elements appear in each program?</h2></div></div><JumpCounts elements={allElements} /></article>
			<article class="analysis-card panel"><div class="panel-heading"><div><span class="section-number">S02 · ROTATION & EXECUTION</span><h2>More rotations do not guarantee a higher GOE</h2></div></div><RotationGoe elements={allElements} /></article>
			<article class="analysis-card panel"><div class="panel-heading"><div><span class="section-number">S06 · SPIN & STEP LEVELS</span><h2>Levels and panel scores across this program</h2></div><span class="selected-label">{selectedSegment === 'SP' ? 'Short program' : 'Free skate'}</span></div><SpinStepLevels elements={allElements.filter((d) => d.segment === selectedSegment)} /></article>
			<article class="analysis-card panel"><div class="panel-heading"><div><span class="section-number">S15 · BASE VALUE VS PANEL SCORE</span><h2>Execution can change the final element score</h2></div><span class="selected-label">Click a jump to inspect it ↑</span></div><BaseVsPanel elements={allElements.filter((d) => d.element_group === 'jump')} onSelect={selectFromChart} /></article>
		</div>
	</section>

	<footer><div><span class="section-number">DATA & SCOPE</span><p>Beijing 2022 individual men’s singles · final top ten · 190 protocol elements · 20 segment records</p></div><div class="footer-links"><a href="https://results.isu.org/results/season2122/owg2022/CAT001RS.htm" target="_blank" rel="noreferrer">Final standings ↗</a><a href="https://www.isuresults.com/results/season2122/owg2022/owg2022_protocol.pdf" target="_blank" rel="noreferrer">Official protocol book ↗</a><a href="https://github.com/billchenziang33/csc316-inside-figure-skating-program" target="_blank" rel="noreferrer">Project source ↗</a></div></footer>
</main>
