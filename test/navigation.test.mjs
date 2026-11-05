import test from 'node:test';
import assert from 'node:assert/strict';
import { readRoute, routeHash, stages, chartIds } from '../src/lib/navigation.mjs';
test('unknown and malformed links fall back to the finding', () => {
  for (const hash of ['', '#not-a-stage', '#%zz']) assert.equal(readRoute(hash).stage, 'story');
  assert.equal(readRoute('#charts/unknown').chart, 'S12');
});
test('all stages and expanded charts survive direct-link round trips', () => {
  for (const stage of stages) assert.equal(readRoute(routeHash(stage.id)).stage, stage.id);
  for (const chart of chartIds) assert.deepEqual(readRoute(routeHash('chart-detail', chart)), { stage: 'chart-detail', chart });
});
