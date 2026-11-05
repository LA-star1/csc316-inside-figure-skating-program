# Guided Figure-Skating Site Redesign

**Status:** Draft for user review
**Date:** 2026-11-05

## Goal

Turn the existing long-scrolling site into a short guided experience with one active stage at a time. Keep the three-column program workbench, preserve the verified data and chart set, and make the 3D reference readable by opening it in a dedicated large view.

## User-approved direction

- Keep the three-column workbench as a core screen.
- Add step navigation so visitors can move forward and back between focused screens.
- Preserve the selected skater, program segment, and element when moving between screens.
- Avoid presenting all charts and controls as one long page.

## Audit of the current site

- `src/App.svelte` renders the story, explorer, protocol matrix, five analysis views, and footer in one continuous document. Its only story-to-explorer navigation is an anchor link; there is no progress, back, or next control.
- `.three-col` uses three columns above 1040 px, two columns from 701–1040 px, and one column at 700 px or less. The current controls remain usable, but the narrow layout stacks all panels into the same long page.
- The 3D reference is embedded inside `.motion-frame`, whose height is fixed at 330 px on desktop, 390 px at medium widths, and 300 px on small screens.
- The embedded demo itself uses a full-viewport flex layout and positions its information card absolutely over the 3D canvas. In a short iframe, that card can extend into the separate playback controls. The provided screenshot reproduces this overlap and the nested scrollbar.
- The chart cards are all present, but the five analysis views sit below the explorer with no focused chart navigation or expanded detail mode.
- The existing palette and type system are coherent: navy, warm rust, teal, DM Sans, DM Mono, and Playfair Display. The redesign will keep this identity and improve layout/navigation hierarchy instead of replacing the visual style.

## Navigation model

The application shell shows a compact progress indicator, the current stage name, and persistent **Back** / **Next** controls. Visitors can also jump to a stage from the progress navigation and skip directly from the opening story to the chart gallery. Stage changes update the URL hash and browser history so Back/Forward remains predictable and a stage can be shared. Opening a chart detail view records the active chart in the hash; returning to the gallery restores its previous chart selection.

Only the active stage is displayed. Long chart collections and reference content are not rendered as a continuous vertical sequence. The current selection state remains owned by the page and is shared with every stage.

## Screen plan

### 1. Start with the finding

Show the Q7 result: jump elements contribute 67.4% of element panel points in the short program and 77.1% in the free skate for the top-ten cohort, a difference of 9.7 percentage points. Keep the denominator and cohort visible. Actions: **Explore the programs** and **Skip to charts**.

### 2. Choose a skater and program

Present the existing skater selector and SP/FS controls with the selected program's total score. Continue opens the workbench with the chosen values intact.

### 3. Three-column program workbench

- **Left — Program sequence:** the selected program's official protocol order and element scores.
- **Middle — Element score:** selected element code, family, base value, signed GOE, panel score, and program score arithmetic.
- **Right — Movement reference:** a compact explanation and an **Open the large 3D example** action. Do not put the full interactive demo in this narrow column.

On wide screens, retain the three columns. On tablet and phone widths, present the same columns as three labeled tabs (Sequence, Score, Movement) to avoid a tall stack and preserve the selection.

### 4. Protocol marks (S11)

Give the novel protocol matrix a focused screen with the selected program's elements in order. Selecting an available marked cell updates the shared element selection and offers a return to the workbench. Keep the distinction between protocol marks and score explanations visible.

### 5. Evidence gallery

Provide one chart at a time with labeled chart tabs or a compact chart selector. Include all five remaining selected views:

- **S12:** segment TES and TSS comparison.
- **S01:** scored jump-element counts.
- **S02:** jump rotations versus GOE.
- **S06:** spin/step levels and scores.
- **S15:** base value versus final panel score.

Each chart has an **Expand chart** action that opens a focused detail stage for that chart. The expanded view keeps the chart title, question, units, cohort/sample scope, legend or labels, and a concise reading note together. Where chart marks identify an element, selection updates the shared element and provides a path back to the workbench.

### 6. Full-size movement reference

Open the existing Single Axel demo as a dedicated stage with enough viewport height for the canvas, information card, and controls. Keep a visible back control and a direct **Open demo in a new tab** fallback. State beside the demo that it is a generic reference, not motion capture of the selected Beijing athlete. Do not encode the selected element as if it were a matching animation.

## State and transitions

Keep these shared values across stages:

```text
selectedSkaterId
selectedSegment (SP | FS)
selectedElementId
activeStage
activeChart
```

Changing a skater or segment selects that program's first valid element. Selecting a protocol row or S15 point updates the same `selectedElementId`. Back/Next changes the active stage without clearing the selection. Browser Back/Forward follows the stage history. The URL hash represents the stage and, when practical, the active chart.

## Visual and interaction rules

- Keep the current navy/rust/teal color identity and typography; use consistent spacing and heading levels across stages.
- Use one main question or claim per screen and one primary action. Secondary actions remain visually quieter.
- Make controls keyboard-operable, show focus, use descriptive labels, and announce stage/selection changes accessibly.
- Keep touch controls at least 44 px high and avoid hover-only cues.
- Respect `prefers-reduced-motion`; use a short fade or slide only to clarify a stage change.
- Provide a text/table alternative for chart values and do not rely on color alone.
- Keep source, cohort, units, and limitations close to the relevant data.

## Scope boundaries

- Preserve the Q7 finding, data calculations, selected sketches S12/S01/S02/S06/S11/S15, official scoring semantics, and ISU attribution.
- Do not change dataset values or reframe the generic demo as a performance by the selected skater.
- Do not add new chart types, new datasets, or additional animation models as part of this redesign.
- Keep the public GitHub repository and Codex Sites deployment; each working implementation revision must be tested, committed, pushed, and redeployed.

## Acceptance criteria

1. A visitor can follow the story using Back/Next, see progress, skip ahead, and use browser Back/Forward without losing the selected skater/program/element.
2. Only one main stage is visible at a time; the page no longer requires scrolling through every chart to reach the next part.
3. The desktop workbench retains three columns; narrower screens use Sequence/Score/Movement tabs rather than squeezing or stacking the three panels into a long block.
4. The 3D reference is launched in a dedicated large view; its title, information, playback controls, and caveat do not overlap or require nested scrolling at the tested viewport sizes.
5. S11 and all five remaining selected views are reachable from clear navigation; each chart can open a focused detail view and return without losing shared state.
6. Q7 and all chart denominators, labels, official values, and limitations remain accurate.
7. Keyboard navigation, visible focus, reduced-motion behavior, chart text alternatives, and responsive layouts are checked at desktop, tablet, and phone widths.
8. Tests/build pass, the latest source is pushed to the public repository, and the public Codex Sites deployment is verified in Edge.

## Design-system decision

The existing site already has a consistent editorial sports palette and type system. The UI/UX audit therefore recommends retaining those tokens and focusing the redesign on step hierarchy, navigation state, readable chart modes, and responsive workspace behavior. The product-design lookup suggested a guided experience with a skip route, progress feedback, and a dedicated immersive motion view; those interaction patterns are adopted without replacing the existing color palette.
