export const stages = [
  { id: 'story', label: 'The finding' },
  { id: 'choose', label: 'Choose a program' },
  { id: 'workspace', label: 'Program workbench' },
  { id: 'protocol', label: 'Protocol marks' },
  { id: 'charts', label: 'Compare the evidence' },
  { id: 'movement', label: 'Movement reference' }
];
export const chartIds = ['S12', 'S01', 'S02', 'S06', 'S15'];
export function readRoute(hash) {
  const [requested, chart] = String(hash).replace(/^#\/?/, '').split('/');
  const stage = stages.some(s => s.id === requested) || requested === 'chart-detail' ? requested : 'story';
  return { stage, chart: chartIds.includes(chart) ? chart : 'S12' };
}
export function routeHash(stage, chart = 'S12') {
  const safe = readRoute(`#${stage}/${chart}`);
  return `#${safe.stage}${['charts', 'chart-detail'].includes(safe.stage) ? `/${safe.chart}` : ''}`;
}
