# Project Guide

- This is an independent Vite static SPA using Svelte 5 runes, JavaScript, D3, and Node's built-in test runner. Keep it buildable to `dist/` for Codex Sites hosting.
- The official source data is the top-ten Beijing 2022 men's singles protocol brief under `data/source/`. Do not edit source values to fit a chart.
- `scripts/prepare-data.mjs` parses the three fenced TSV tables and generates `static/data/competition.json` deterministically.
- Empty source cells are `null`; numeric cells are parsed as numbers. Preserve source names and official order.
- Each record represents the top-ten cohort only. Segment protocol order is not time or rink position. Keep SP and FS distinct.
- Element score uses official panel score. Program arithmetic is `TES + PCS + deductions = TSS`; deductions are negative.
- Q7 jump share uses jump panel points divided by all panel element points within the same segment and cohort.
- The hosted Single Axel demo is generic and illustrative; do not label it as Olympic athlete capture or redistribute its MotionExpert data without permission confirmation.
- D3 computes chart scales and axes; Svelte renders marks and owns shared interactive state.
- Vite serves files from `static/` at the site root and copies them into `dist/`.
- Run `npm run test` and `npm run build` before committing. Do not claim interaction or deployment checks unless performed in a browser.
