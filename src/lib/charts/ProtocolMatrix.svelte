<script>
	import { protocolMarks } from '../data/derived.mjs';
	let { elements = [], selectedId = null, onSelect = () => {} } = $props();
	const flags = ['!', 'e', 'q', '<', '<<', '*'];
</script>

<div class="matrix-wrap">
	<table class="matrix">
		<thead><tr><th scope="col">Order / element</th>{#each flags as flag (flag)}<th scope="col" title={`Protocol mark ${flag}`}>{flag}</th>{/each}</tr></thead>
		<tbody>
			{#each elements as element (element.id)}
				{@const marks = protocolMarks(element)}
				<tr class:chosen={selectedId === element.id}>
					<th scope="row"><button class="row-button" onclick={() => onSelect(element.id)} aria-pressed={selectedId === element.id}><span>{String(element.element_order).padStart(2,'0')}</span><b>{element.element_code_raw}</b><small>{element.panel_element_score.toFixed(2)}</small></button></th>
					{#each flags as flag (flag)}<td><button class:marked={marks.includes(flag)} class="cell" aria-label={`${element.element_code_raw}, ${flag}: ${marks.includes(flag) ? 'marked' : 'not marked'}`} aria-pressed={marks.includes(flag)} onclick={() => marks.includes(flag) && onSelect(element.id)} disabled={!marks.includes(flag)}>{marks.includes(flag) ? '●' : '·'}</button></td>{/each}
				</tr>
			{/each}
		</tbody>
	</table>
	<p class="note">Novel view · Rows follow protocol order; flagged cells link back to the selected element. These marks identify protocol notation and do not explain every score change.</p>
</div>

<style>
	.matrix-wrap{overflow:auto;border:1px solid #e6e8e2;border-radius:4px;margin-top:.8rem}.matrix{border-collapse:collapse;width:100%;min-width:420px;font-size:.72rem}.matrix th,.matrix td{border-bottom:1px solid #eceee9;padding:.12rem .22rem;text-align:center}.matrix thead th{position:sticky;top:0;background:#f4f5f0;color:#59665f;height:29px;font:500 .68rem var(--mono)}.matrix tbody th{padding:0;text-align:left}.row-button{border:0;background:transparent;color:var(--ink);width:100%;height:32px;display:flex;align-items:center;gap:.45rem;text-align:left;padding:.2rem .4rem;cursor:pointer}.row-button span{font: .62rem var(--mono);color:#818c86}.row-button b{font-size:.7rem}.row-button small{margin-left:auto;color:#6e7b75;font: .62rem var(--mono)}.matrix tr.chosen{background:#edf2ed}.cell{border:0;background:transparent;color:#c4cac4;width:28px;height:28px;cursor:not-allowed}.cell.marked{color:#bd6248;cursor:pointer}.cell.marked:hover{background:#f4e8df;border-radius:50%}.note{margin:.55rem 0 .1rem;color:#707c75;font-size:.68rem;line-height:1.5}
</style>
