<script>
	import { scaleLinear } from 'd3';
	let { elements = [], onSelect = () => {} } = $props();
	const x = scaleLinear().domain([0, 22]).range([62, 720]);
	const y = scaleLinear().domain([0, 24]).range([242, 32]);
	const xTicks = [0,5,10,15,20];
	const yTicks = [0,5,10,15,20];
</script>

<div class="viz" role="group" aria-label="Clickable scatterplot of base value versus final panel element score for jump elements across the top-ten cohort.">
	<div class="legend"><span><i class="sp"></i>Short program</span><span><i class="fs"></i>Free skate</span><span>Choose a point to open its workbench</span></div>
	<svg viewBox="0 0 770 300">
		{#each yTicks as t}<line x1="62" x2="720" y1={y(t)} y2={y(t)} stroke="#e7e9e4"/><text x="51" y={y(t)+4} text-anchor="end">{t}</text>{/each}
		{#each xTicks as t}<line x1={x(t)} x2={x(t)} y1="32" y2="242" stroke="#eef0ec"/><text x={x(t)} y="260" text-anchor="middle">{t}</text>{/each}
		<line x1="62" x2="720" y1="242" y2="242" stroke="#819088"/><line x1="62" x2="62" y1="32" y2="242" stroke="#819088"/>
		{#each elements as element (element.id)}
			<g class="point" role="button" tabindex="0" aria-label={`${element.skater}, ${element.segment}, ${element.element_code_raw}, base ${element.base_value.toFixed(2)}, panel score ${element.panel_element_score.toFixed(2)}`} onclick={() => onSelect(element)} onkeydown={(event) => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); onSelect(element); } }}>
				<circle cx={x(element.base_value)} cy={y(element.panel_element_score)} r="4.5" class:sp-dot={element.segment==='SP'} class:fs-dot={element.segment==='FS'}><title>{element.skater} · {element.segment} · {element.element_code_raw} · base {element.base_value.toFixed(2)} · panel score {element.panel_element_score.toFixed(2)}</title></circle>
			</g>
		{/each}
		<text x="394" y="290" text-anchor="middle">Base value (points)</text><text transform="translate(15 140) rotate(-90)" text-anchor="middle">Final panel element score (points)</text>
	</svg>
	<p class="foot">Jump protocol elements only · Final panel score includes GOE and may also reflect calls and bonuses · Clicking a mark selects the same element in the explorer.</p>
</div>

<style>
	.viz{display:grid;gap:.1rem}.legend{display:flex;justify-content:flex-end;gap:1rem;flex-wrap:wrap;font-size:.7rem;color:#58645f}.legend i{display:inline-block;width:.65rem;height:.65rem;border-radius:50%;margin-right:.25rem}.sp{background:#d46b47}.fs{background:#397a74}svg{width:100%;height:auto}svg text{font:10px 'DM Sans',Arial,sans-serif;fill:#6b7770}.point{all:unset;cursor:pointer}.point circle{stroke-width:1;fill-opacity:.7}.point:hover circle,.point:focus-visible circle{r:7;stroke-width:2}.point:focus-visible{outline:none}.sp-dot{fill:#d46b47;stroke:#a64b31}.fs-dot{fill:#397a74;stroke:#285f5a}.foot{margin:.1rem 0 0;color:#707c75;font-size:.69rem;line-height:1.5}
</style>
