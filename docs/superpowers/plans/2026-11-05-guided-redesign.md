# Guided Redesign Implementation Plan

> Execute in the current user-authorized checkout; verify each working revision before committing and pushing.

**Goal:** Retain the three-column workbench and deliver six focused navigation stages with readable charts and movement reference.

**Architecture:** Keep page-owned skater/program/element selection. Add hash-based stage/chart routing, accessible progress controls and responsive workspace tabs. Reuse the existing data and chart components. Move the external demo to a dedicated large stage.

**Tech Stack:** Svelte 5, Vite, D3, Node tests, Codex Sites.

## Constraints and review

The design specification dated 2026-11-05 has been checked against App.svelte, app.css and the existing data plan. The user's selected direction is three columns plus navigation. Preserve 190 elements, 20 programs, 10 skaters, Q7 shares and the six selected sketches. No new data or motion models. Existing implementation plan remains historical; this plan supersedes its continuous-page and small-iframe layout.

## Task 1 — Navigation and composition

- [x] Add src/lib/navigation.mjs with six valid stage names and five valid gallery IDs. Parse unknown hashes safely; encode chart detail routes.
- [x] Add test/navigation.test.mjs covering malformed/direct links and chart detail round-trips.
- [x] Update src/App.svelte to display one stage at a time. Keep selection at page level; use hash/history events for Back/Forward. Focus the active stage heading after a user navigation.
- [x] Keep the workspace's sequence/score panels; replace its cramped iframe with a movement reference launcher. Use labeled tabs below 1040px.
- [x] Render one gallery chart at a time and provide a dedicated expanded chart stage, selection links and readable data table.
- [x] Verify with npm run check, inspect diff, commit and push.

## Task 2 — Visual and interaction review

- [x] Style progress, Back/Next, stage headings, workspace tabs and expanded charts in src/app.css. Retain palette/fonts. Use visible focus, 44px controls, reduced motion and live stage announcements.
- [x] Give 3D its own wide stage, with an external full-window link, explicit generic-reference label and sufficient iframe dimensions; inspect actual demo behavior.
- [x] Preview in Edge: follow all stages; change athlete/segment/element; visit S11/S15; navigate back; inspect all charts and expanded views; check selection persists.
- [x] Check desktop, tablet and phone rendering, navigation by keyboard and browser console. Correct observed issues, then rerun affected checks.
- [x] Record evidence and current state in summary.md and docs/process-book-milestone7.md.

## Task 3 — Publish and completion audit

- [x] Commit/push final verified source to GitHub and synchronize the existing Sites source using its helper.
- [x] Package dist with the existing hosting manifest; save the pushed SHA and deploy to the existing public Site.
- [x] Verify the deployed guided stages in Edge and compare the result with all design acceptance criteria. Report any unmet requirement; keep goal active until resolved.
