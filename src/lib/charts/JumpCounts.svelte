<script>
	import { scaleBand, scaleLinear } from 'd3';
	import { countJumpElements } from '../data/derived.mjs';
	let { elements = [] } = $props();
	let groups = $derived(countJumpElements(elements).sort((a,b) => a.final_rank - b.final_rank));
	const x = scaleLinear().domain([0, 13]).range([0, 100]);
	const y = scaleBand().domain(Array.from({length:10}, (_,i) => i + 1)).range([0, 330]).padding(0.28);
	const ticks = [0, 4, 8, 12];
</script>

<div class="viz" role="img" aria-label="Count of jump protocol elements per skater, comparing short program and free skate. A combination counts as one scored protocol element.">
	<div class="legend"><span><i class="sp"></i>Short program</span><span><i class="fs"></i>Free skate</span></div>
	<div class="axis"><span>Final rank</span><div>{#each ticks as t}<small style={`left:${x(t)}%`}>{t}</small>{/each}<b>Scored jump elements per program</b></div></div>
	{#each Array.from({length:10}, (_,i)=>i+1) as rank (rank)}
		<div class="row"><span class="rank">#{rank}</span><div class="plot">
			{#each ['SP','FS'] as segment (segment)}
				{@const item = groups.find((d) => d.final_rank === rank && d.segment === segment)}
				<div class:sp-bar={segment === 'SP'} class:fs-bar={segment === 'FS'} class="bar" style={`width:${x(item?.count ?? 0)}%`}><span>{item?.count ?? 0}</span></div>
			{/each}
		</div></div>
	{/each}
	<p class="foot">Each official scored jump element is one count. A combination such as 4F+3T remains one protocol row.</p>
</div>

<style>
	.viz{display:grid;gap:.3rem}.legend{display:flex;gap:1rem;justify-content:flex-end;font-size:.72rem;color:#58645f}.legend span{display:flex;align-items:center;gap:.35rem}.legend i{width:.65rem;height:.65rem;border-radius:2px}.sp{background:#d46b47}.fs{background:#397a74}.axis,.row{display:grid;grid-template-columns:48px minmax(0,1fr);gap:.7rem;align-items:center}.axis>span{font-size:.68rem;color:#77827d}.axis>div{position:relative;height:1.55rem;border-bottom:1px solid #cfd6d0}.axis small{position:absolute;bottom:.2rem;transform:translateX(-50%);font-size:.65rem;color:#77827d}.axis b{position:absolute;right:0;bottom:.2rem;font-size:.62rem;color:#77827d;background:#fffefa;padding-left:.25rem}.row{height:29px}.rank{font: .7rem var(--mono);color:#69756f;text-align:right}.plot{position:relative;display:grid;gap:3px}.plot::before{content:'';position:absolute;inset:0;background:linear-gradient(to right,transparent 0%,transparent calc(30.77% - 1px),#e6e9e4 calc(30.77% - 1px),#e6e9e4 30.77%,transparent 30.77%,transparent calc(61.54% - 1px),#e6e9e4 calc(61.54% - 1px),#e6e9e4 61.54%,transparent 61.54%,transparent calc(92.3% - 1px),#e6e9e4 calc(92.3% - 1px),#e6e9e4 92.3%,transparent 92.3%);pointer-events:none}.bar{height:10px;min-width:16px;border-radius:2px;position:relative}.sp-bar{background:#d46b47}.fs-bar{background:#397a74}.bar span{position:absolute;left:calc(100% + 5px);top:50%;transform:translateY(-50%);font: .65rem var(--mono);color:#41504a}.foot{margin:.55rem 0 0;color:#707c75;font-size:.69rem;line-height:1.5}
</style>
