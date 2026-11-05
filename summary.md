# Current project state

Updated 2026-11-05. Branch: `codex/site-implementation`.

- Public GitHub: https://github.com/billchenziang33/csc316-inside-figure-skating-program
- Public Site: https://inside-figure-skating-program.eagercoast2.chatgpt.site/
- Sites project: `appgprj_6aecd6a078508191aa59d74b91ff44c9` (preserve public audience and identity).
- Guided navigation implementation: `src/App.svelte`, `src/lib/navigation.mjs`, `src/app.css`. Six stages preserve athlete/program/element state; desktop has three columns, narrow screens have three workspace tabs. Five gallery charts have dedicated expanded stages and data tables; S11 retains the linked protocol matrix.
- Data invariants: 10 final top-ten athletes, 20 segment records, 190 elements. Q7 jump point shares: 67.4% SP, 77.1% FS. Source values and calculations unchanged.
- Checks: `npm run check` runs six Node tests and the Vite build. Edge verified SP/FS selection, workspace scores, all chart tabs, expansion, keyboard S15-to-workbench selection, S11 row-to-workbench selection, browser Back, phone workspace tabs and tablet layout.
- Movement: external URL works full-window; its simulated-apex control showed frame 74/200, 0.44m lift and 0.96/1.92m illustrative travel. Both local/public embeds remained blank; minimal static iframe confirmed this is independent of Svelte. Dedicated movement stage now uses an actual screenshot plus a full-window launch link. `static/movement-reference.png` was captured from that working demo. No new motion data/model is included.
- Public version 4 deployed implementation commit `aa32321be2e99fb73a36bf43e19bd248d75b5b6a` successfully. Final documentation/evidence revision preserves the same built application. Public QA confirmed all six stages, all five charts, chart expansion/return, history, Previous/Next and the keyboard skip link. At 390px and 820px, exactly one workspace panel is visible and document width does not exceed viewport width. No console warnings/errors were captured. Screenshots: `docs/evidence/guided-desktop.png`, `docs/evidence/guided-phone.png`.
- Design: `docs/superpowers/specs/2026-11-05-guided-figure-skating-site-design.md`; execution plan: `docs/superpowers/plans/2026-11-05-guided-redesign.md`.
