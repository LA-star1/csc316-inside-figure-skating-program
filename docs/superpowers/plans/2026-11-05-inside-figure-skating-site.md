# Inside a Figure-Skating Program — Implementation Plan

> **Execution:** Use the `executing-plans` workflow and deliver each verified phase as its own commit and push.

**Goal:** Build and publish the CSC316 Beijing 2022 men's singles scoring story, linked three-column explorer, and six selected analysis views from the official top-ten protocol data.

**Architecture:** A static Vite/Svelte 5 page owns the selected skater, segment, and element. This replaces the initial SvelteKit wrapper because local npm registry DNS is unavailable and the environment lacks `adapter-static`; Vite emits the `dist/index.html` package that Codex Sites can host directly. A repeatable Node script extracts official TSV tables from the source brief; D3 computes scales while Svelte renders accessible marks. The 3D column embeds the already-hosted Single Axel demonstration as a clearly labeled generic reference, not as an Olympic replay.

**Tech Stack:** Vite, Svelte 5 runes, JavaScript, D3 7, Node's built-in test runner, Codex Sites for public hosting, and GitHub for source history.

## Global Constraints

- GitHub repository: `https://github.com/billchenziang33/csc316-inside-figure-skating-program`; currently Public per the user's latest instruction.
- Do not commit passwords, tokens, personal Process Book source files, unrelated workspace files, or local build output.
- Preserve the source-backed top-ten scope: 10 skaters, 20 programs, 190 element rows (70 SP and 120 FS), 100 component rows.
- Keep SP and FS comparisons separated or explicitly comparable; never treat element order as time or rink position.
- Program score is `TES + PCS + deductions`; deductions are negative in the source. Element score is the official panel score, not the sum of judge marks.
- Q7 percentages use jump panel scores divided by all element panel scores within each segment for the top-ten cohort: 67.3885% SP and 77.0515% FS, displayed as 67.4% and 77.1%.
- The MotionExpert demo's pelvis-centred coordinates are not Olympic athlete capture; travel, height, and flight phase are illustrative. Do not redistribute MotionExpert data until its data license is established.
- Every meaningful change follows test-first for behavior, build/browser verification, a focused commit, and a push to `origin/main`.

## File Map

- `src/App.svelte`: story opener, shared Svelte state, explorer and analysis composition.
- `src/lib/data/parse-brief.mjs`: pure parser for the three embedded TSV data tables.
- `src/lib/data/derived.mjs`: stable IDs, Q7 aggregates, and chart-ready groupings.
- `src/lib/charts/*.svelte`: Q7, S12, S15, S01, S02, S06, S11 charts; D3 scales/axes and Svelte-rendered marks.
- `src/lib/explorer/*.svelte`: skater/segment controls, sequence, score detail, and motion reference panel.
- `scripts/prepare-data.mjs`: extracts the official source tables to `static/data/` without editing source values.
- `data/source/Beijing_2022_Mens_Singles_Top10_Data_Brief.md`: retained primary data brief and source links.
- `test/*.test.mjs`: parser, score arithmetic, and aggregate invariants, run with `node --test`.
- `docs/process-book-milestone7.md`: current implementation status, screenshots, design drafts, attribution and test evidence.
- `.openai/hosting.json`: Codex Sites project identity and static output directory after registration.

## Task 1 — Bootstrap the independent Vite + Svelte project

**Files:** `package.json`, `package-lock.json`, `vite.config.js`, `svelte.config.js` (only if required by the installed kit), `src/app.html`, `src/routes/+layout.svelte`, `.gitignore`, `README.md`.

- Create a clean Vite + Svelte single-page app in this directory; do not copy Lab 4's `.git`, generated state, or source page.
- Use the installed Lab 4 package manifest as a version reference; pin project dependencies through the generated lockfile.
- Keep `node_modules`, `.svelte-kit`, `.env*`, screenshots not approved for publication, and build output out of Git.
- Confirm the app starts and the source-only baseline builds before chart implementation.

**Verification:** `npm run check` and `npm run build`; then open `/` in Edge and confirm the starter page loads.

## Task 2 — Extract and validate official data (test first)

**Files:** create `test/data.test.mjs` first, then `src/lib/data/parse-brief.mjs`, `src/lib/data/derived.mjs`, `scripts/prepare-data.mjs`, and `data/source/Beijing_2022_Mens_Singles_Top10_Data_Brief.md`.

- Write tests for counts (190 elements; 70 SP, 120 FS; 20 programs; 100 component rows), 10 unique skaters, stable element IDs, and the official score equations.
- Write tests for Q7 shares: SP 67.3885% within 0.0001 percentage points and FS 77.0515% within 0.0001 percentage points, using panel element scores.
- Run `node --test` and observe expected missing-module failures before implementation.
- Implement a pure parser that locates each fenced TSV under its named Markdown heading and preserves blank fields as `null`; do not infer missing values or rewrite official fields.
- Generate JSON data with a deterministic script and compare its counts and score arithmetic with the source brief.

**Interfaces:** `parseBrief(markdown) -> { segments, elements, components }`; `summarizeJumpShare(elements) -> [{ segment, jumpPoints, totalElementPoints, share }]`.

**Verification:** `node --test`; run the extraction twice and confirm identical output hashes; run the score checks against all 20 segment records.

## Task 3 — Prototype the story and two selected D3 views

**Files:** create Q7, S12, S15 chart components, page composition, and focused chart/data tests before implementation.

- Q7 opener: paired horizontal share bars for SP and FS, a 9.7 percentage-point callout, cohort and denominator labels, and a short story caption.
- S12: show TES and TSS per skater, separated by SP and FS; include PCS and negative deductions in tooltip/detail so their arithmetic is transparent.
- S15: compare base value and official final element score, grouped by segment and skater; show GOE and element code on hover/focus, and make no cross-segment ranking that hides the different program lengths.
- Use D3 for scales, axes, and layout calculations; render marks and labels in Svelte with keyboard-accessible buttons/controls where selection is supported.
- Add loading, error, and empty states for the data pipeline.

**Verification:** `npm run check`, `node --test`, `npm run build`; in Edge verify the correct Q7 values and confirm changing a program filter updates S12/S15 without changing the all-top-ten story aggregate.

## Task 4 — Add skater/program selection and the three-column explorer

**Files:** `src/routes/+page.svelte`, `src/lib/explorer/SkaterControls.svelte`, `ProgramSequence.svelte`, `ElementScoreDetail.svelte`, `MotionReference.svelte`, and interaction tests.

- Shared state: `selectedSkaterId`, `selectedSegment`, `selectedElementId`; derive selected program and selected element from parsed data.
- Column 1 lists the selected program's ordered protocol elements. Selecting an item updates the one stable element ID.
- Column 2 shows raw code, readable family, base value, signed GOE, and official panel score with units and a compact score comparison.
- Column 3 embeds `https://figure-skating-axel-demo.billziang-chen.chatgpt.site/` only if the target allows framing. If blocked, provide a prominent open-demo link and a static labeled reference card; never imply the motion matches the selected skater.
- When changing skater or segment, select its first valid element and clear stale hover; link chart selections to the same element ID.
- Add keyboard operation, visible focus, descriptive labels, and a reset action.

**Verification:** in browser change skater, change SP/FS, select an element from sequence and chart, and verify all three columns refer to the same selection; test no-match motion state; check console.

## Task 5 — Implement the remaining four selected views, including novel S11

**Files:** `src/lib/charts/S01JumpCounts.svelte`, `S02RotationsGOE.svelte`, `S06SpinStepLevels.svelte`, `S11ProtocolMatrix.svelte`, shared chart helpers, and focused tests.

- S01 compares SP/FS jump counts using the same count unit and explains how combinations are counted.
- S02 separates solo and combination jumps; displays sample sizes and leaves missing groups missing rather than zero.
- S06 compares spin/step levels and scores with segment and sample-size context.
- S11 uses a protocol matrix: rows are elements in program order, columns are technical protocol flags, cells identify the actual protocol mark; selecting a flagged cell highlights its stable element ID in the sequence and S15. Program-level falls remain program-level unless the source ties one to a specific element.
- Keep overall top-ten aggregates separate from selected-athlete views and state the denominator beside every aggregate.

**Verification:** unit tests for grouping and missing values; browser interaction checks for chart-to-sequence linking; inspect at least one complete SP and FS path.

## Task 6 — Responsive, accessibility, source credits, and Process Book

**Files:** `src/app.css`, affected chart/explorer components, `README.md`, `docs/ATTRIBUTION.md`, `docs/process-book-milestone7.md`, screenshots in `docs/evidence/`.

- Test wide three-column layout and narrow stacked layout; preserve sequence → score → motion order.
- Check keyboard-only selection, focus indicators, chart text labels, non-color cues, reduced-motion behavior, heading order, and readable contrast.
- Cite ISU results book and list the motion demo as an external reference; include CesiumMan and skate credit only when those external model assets are actually embedded or redistributed.
- Record which two D3 views are implemented for Prototype 1 and which additional designs remain drafts; do not describe drafts as built.
- Capture final page screenshots and add them to the Process Book evidence.

**Verification:** `npm run check`, `node --test`, `npm run build`; browser checks at desktop and narrow viewport; validate every citation and permission statement.

## Task 7 — Publish and verify the deployable site

**Files:** `svelte.config.js`, `.github/workflows/pages.yml`, `README.md`.

- Register a Codex Site after the project source is pushed. Preserve the returned Site ID in `.openai/hosting.json`, configure the static directory as `dist`, package the verified output, and publish the Site with public URL access as requested.
- Keep GitHub as the project's public source repository; push each verified source state there and synchronize the exact commit to the Site source before saving its version.
- Do not publish MotionExpert frame data or copied 3D assets while their data license is unresolved; embed the existing external demo only if framing and its attribution remain accurate.
- Push only after local checks pass; inspect the Actions result and the deployed public URL.

**Verification:** `npm run build` creates a deployable `dist/index.html`; deployed root loads; data fetch succeeds; Q7 renders; S12/S15 and the explorer work; no asset 404s; test keyboard and narrow layout on the deployed page.

## Commit and Push Boundaries

1. `docs: record implementation plan and data contract`
2. `feat: add verified data pipeline and Q7 S12 S15 prototype`
3. `feat: add linked skater and program explorer`
4. `feat: add selected analysis views and novel protocol matrix`
5. `docs: complete Milestone 7 evidence and accessibility checks`
6. `deploy: publish static site with Codex Sites` (only after deployment gate checks)

At each boundary, inspect `git diff --check`, run the relevant verification, commit the focused update, push to `origin/main`, and confirm the pushed commit hash on GitHub before proceeding.
