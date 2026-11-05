# Beijing 2022 Men's Singles - Top 10 Competition Data Pack

**Purpose:** A shareable, source-backed overview for the CSC316 figure-skating visualization project. This covers the **individual men's singles event** at the Beijing 2022 Olympic Winter Games, not the separate team event.

## What this data covers

The ten skaters below are the final top ten after the short program (SP) and free skating (FS). The ISU's official results book contains the full event protocols, including element-by-element scoring. It includes all competitors, so use the final standings to filter the top ten when extracting records.

| Final rank | Skater | NOC | SP rank | SP score | FS rank | FS score | Overall score |
|---:|---|:---:|---:|---:|---:|---:|---:|
| 1 | Nathan Chen | USA | 1 | 113.97 | 1 | 218.63 | 332.60 |
| 2 | Yuma Kagiyama | JPN | 2 | 108.12 | 2 | 201.93 | 310.05 |
| 3 | Shoma Uno | JPN | 3 | 105.90 | 5 | 187.10 | 293.00 |
| 4 | Yuzuru Hanyu | JPN | 8 | 95.15 | 3 | 188.06 | 283.21 |
| 5 | Junhwan Cha | KOR | 4 | 99.51 | 7 | 182.87 | 282.38 |
| 6 | Jason Brown | USA | 6 | 97.24 | 6 | 184.00 | 281.24 |
| 7 | Daniel Grassl | ITA | 12 | 90.64 | 4 | 187.43 | 278.07 |
| 8 | Evgeni Semenenko | ROC | 7 | 95.76 | 9 | 178.37 | 274.13 |
| 9 | Boyang Jin | CHN | 11 | 90.98 | 8 | 179.45 | 270.43 |
| 10 | Morisi Kvitelashvili | GEO | 5 | 97.98 | 11 | 170.64 | 268.62 |

The two segments took place on 8 February (SP) and 10 February (FS). All ten listed skaters completed both segments.

## Official source links

- [ISU Beijing 2022 event page](https://results.isu.org/results/season2122/owg2022/) - official competition reports and segment links.
- [Final men's singles standings](https://results.isu.org/results/season2122/owg2022/CAT001RS.htm) - final rank, overall score, and SP/FS placements.
- [Men's short-program results](https://results.isu.org/results/season2122/owg2022/SEG001.htm) - SP segment score, TES, PCS, component marks, and deductions.
- [Men's free-skating results](https://results.isu.org/results/season2122/owg2022/SEG002.htm) - FS segment score, TES, PCS, component marks, and deductions.
- [Official ISU Figure Skating Results Book (PDF)](https://www.isuresults.com/results/season2122/owg2022/owg2022_protocol.pdf) - includes the detailed SP and FS judges' protocols by skater. Search within it for **"Men Single Skating"**, then **"Short Program"** or **"Free Skating"**, and **"Judges Details per Skater"**.

## What the element-level protocol contains

For each skater and segment, the official protocol provides a sequence of performed elements. The element rows include:

- element order (`#`)
- executed element code/name (for example, jump combinations, spins, and step sequences)
- technical-panel `Info` notation where present
- base value
- GOE
- individual judges' GOE marks (J1-J9)
- final panel score for the element

The protocol also reports segment totals such as total element score (TES), program component score (PCS), deductions, and total segment score (TSS). The final standings provide the combined overall result.

For the visualization data model, a useful table shape is one row per **skater x segment x element**:

```text
event, final_rank, skater, NOC, segment, segment_rank,
element_order, element_code, info, base_value, GOE,
J1, J2, J3, J4, J5, J6, J7, J8, J9, panel_element_score
```

Keep the actual official element code and the original order. Do not infer timestamps or rink locations from element order: the protocol does not provide those fields.

## Verified data volume for the planned scope

The extracted official protocols contain exactly **190 element rows** for the final top ten: `10 skaters x (7 SP + 12 FS)`. The complete row-level tables and validation checks are embedded below. The event has **20 skater-segment records** (10 skaters x 2 segments).

The 10 skaters x 2 segments also yield 20 segment-level records. They can carry TES, PCS, deductions, and TSS, while the final table supplies the overall total and final rank.

## How this connects to the 3D-motion sources

The official ISU protocols are the source for **who performed which element, in what order, and how it was scored**. They are not 3D motion capture: they do not provide joint trajectories, exact start/end timestamps, or the skater's position on the rink.

- [FineFS dataset](https://github.com/yanliji/FineFS-dataset) provides full-program videos and estimated 17-joint skeleton sequences, plus action-category and time-boundary annotations. Its public README does not establish that samples can be matched to these ten Beijing Olympic skaters, so do not claim that its skeletons are their exact performances.
- [FS-Jump3D dataset](https://github.com/ryota-skating/FS-Jump3D) provides 3D pose/motion data for jumps from four skaters. It is useful as a jump-motion reference, but it is not this Olympic event's top-ten dataset and does not fill the spin/step motion gap.
- For spins and step sequences, verify the exact labels and motion coverage in FineFS files before promising specific 3D examples. These elements are continuous movements, so a short pose sequence or clip is more suitable than a single static model.

### Recommended project interpretation

Use the Olympic protocols as the factual competition layer. Make the left panel show each skater's ordered element codes, and the middle panel show the corresponding official values and scores. The right panel can reuse a representative 3D motion example for the selected **element type**. Label it as a representative example unless you have a verified, synchronized motion capture of that exact athlete and Olympic performance.

This means the project does **not** require one unique 3D model for each of approximately 190 element rows. Build or source a smaller reusable motion library, and map many competition rows to an appropriate representative example. Keep any unmatched spin or step element visible in the sequence and scores even if no 3D example is available yet.

## Notes for anyone continuing the data work

1. Use the final top-ten table above to define the athlete cohort.
2. Extract the matching athlete pages from both individual-event protocols; do not accidentally use the earlier team-event SP/FS reports.
3. Preserve the original element code, order, info flags, score values, and segment identity.
4. Keep official scoring data and motion-reference data as separate linked tables; only join them where the action label match is defensible.
5. Cite the ISU results book as the scoring source and cite FineFS/FS-Jump3D separately as motion references.

## Source and scope note

Scores and placements in this brief are transcribed from the official ISU Beijing 2022 individual-event results. The protocol schema is from the official ISU results book. The approximate element-row count is explicitly an estimate; it must be replaced by a count from extracted rows before presenting it as a measured statistic.

## Complete extracted data tables (official ISU protocols)

This section embeds the detailed individual-event protocol data for the final top ten. It was transcribed from the official ISU results-book PDF, not from the separate team event. The tables below are self-contained; the source links above are retained for provenance and verification.

### Exact coverage and validation

- **190 element rows verified:** 70 SP rows (7 per skater) + 120 FS rows (12 per skater).
- **20 segment rows:** one SP and one FS summary for each of the ten final top-ten skaters.
- **100 program-component rows:** five components for each of the 20 skater-segments, including factor, all nine judge marks, and the official panel mark.
- For every skater-segment, the extracted element panel scores sum to the printed TES, and `TES + PCS + deductions = segment score` within 0.01 points.
- J1-J9 are the nine judges' element GOE marks as printed. They are not the panel GOE score; the `GOE` field is the official averaged/trimmed panel value.
- The `protocol_pdf_page` field is the physical PDF page number (not the printed mini-report page number).

### Segment-level scores

One record per skater and program. `deductions` is negative when points were deducted.

```tsv
segment	final_rank	skater	NOC	segment_rank	segment_score_TSS	TES	PCS_factored	deductions	falls_count	deduction_detail_raw	element_count	element_score_sum	protocol_pdf_page
FS	1	Nathan Chen	USA	1	218.63	121.41	97.22	0.00	0	0.00	12	121.41	32
FS	2	Yuma Kagiyama	JPN	2	201.93	107.99	93.94	0.00	0	0.00	12	107.99	32
FS	3	Shoma Uno	JPN	5	187.10	96.24	91.86	-1.00	1	Falls -1.00 (1) -1.00	12	96.24	34
FS	4	Yuzuru Hanyu	JPN	3	188.06	99.62	90.44	-2.00	2	Falls -2.00 (2) -2.00	12	99.62	33
FS	5	Junhwan Cha	KOR	7	182.87	93.59	90.28	-1.00	1	Falls -1.00 (1) -1.00	12	93.59	35
FS	6	Jason Brown	USA	6	184.00	87.66	96.34	0.00	0	0.00	12	87.66	34
FS	7	Daniel Grassl	ITA	4	187.43	103.35	84.08	0.00	0	0.00	12	103.35	33
FS	8	Evgeni Semenenko	ROC	9	178.37	94.81	83.56	0.00	0	0.00	12	94.81	36
FS	9	Boyang Jin	CHN	8	179.45	97.23	82.22	0.00	0	0.00	12	97.23	35
FS	10	Morisi Kvitelashvili	GEO	11	170.64	85.92	84.72	0.00	0	0.00	12	85.92	37
SP	1	Nathan Chen	USA	1	113.97	65.98	47.99	0.00	0	0.00	7	65.98	15
SP	2	Yuma Kagiyama	JPN	2	108.12	60.91	47.21	0.00	0	0.00	7	60.91	15
SP	3	Shoma Uno	JPN	3	105.90	59.05	46.85	0.00	0	0.00	7	59.05	16
SP	4	Yuzuru Hanyu	JPN	8	95.15	48.07	47.08	0.00	0	0.00	7	48.07	18
SP	5	Junhwan Cha	KOR	4	99.51	54.30	45.21	0.00	0	0.00	7	54.30	16
SP	6	Jason Brown	USA	6	97.24	49.95	47.29	0.00	0	0.00	7	49.95	17
SP	7	Daniel Grassl	ITA	12	90.64	48.70	41.94	0.00	0	0.00	7	48.70	20
SP	8	Evgeni Semenenko	ROC	7	95.76	55.23	40.53	0.00	0	0.00	7	55.23	18
SP	9	Boyang Jin	CHN	11	90.98	51.62	39.36	0.00	0	0.00	7	51.62	20
SP	10	Morisi Kvitelashvili	GEO	5	97.98	55.69	42.29	0.00	0	0.00	7	55.69	17
```

### Full element-by-element protocol (all 190 rows)

This is the central sketch-ready table. `element_code_raw` preserves the official code, including combinations and attached symbols; `info_flag` preserves the separate protocol flag when it appears in its own column. `base_value`, `goe`, and `panel_element_score` are points. `element_group` is a derived convenience label based on the code, while `element_code_raw` is the source value. Blank flags mean no separate info flag was printed.

```tsv
segment	final_rank	skater	NOC	segment_rank	element_order	element_group	element_code_raw	info_flag	base_value	goe	J1	J2	J3	J4	J5	J6	J7	J8	J9	panel_element_score	protocol_pdf_page
FS	1	Nathan Chen	USA	1	1	jump	4F+3T		15.20	4.40	4	4	4	4	4	4	4	4	4	19.60	32
FS	1	Nathan Chen	USA	1	2	jump	4F		11.00	4.24	4	4	3	4	4	5	3	4	4	15.24	32
FS	1	Nathan Chen	USA	1	3	jump	4S		9.70	1.80	0	1	2	3	2	3	1	2	2	11.50	32
FS	1	Nathan Chen	USA	1	4	spin	CCSp4		3.20	0.96	3	3	2	3	3	4	3	3	3	4.16	32
FS	1	Nathan Chen	USA	1	5	jump	4Lz		11.50	4.93	4	4	4	5	4	5	5	4	4	16.43	32
FS	1	Nathan Chen	USA	1	6	step_sequence	StSq4		3.90	1.62	4	3	3	4	5	5	4	4	5	5.52	32
FS	1	Nathan Chen	USA	1	7	jump	4T+1Eu+1F	x	11.55	1.63	2	1	2	0	2	2	1	2	2	13.18	32
FS	1	Nathan Chen	USA	1	8	jump	3A	x	8.80	2.17	3	2	3	3	3	3	2	2	3	10.97	32
FS	1	Nathan Chen	USA	1	9	jump	3Lz+3T	x	11.11	1.35	3	1	1	3	3	3	1	2	3	12.46	32
FS	1	Nathan Chen	USA	1	10	spin	CCoSp2V		1.88	0.64	4	3	2	3	4	4	3	3	4	2.52	32
FS	1	Nathan Chen	USA	1	11	choreographic_sequence	ChSq1		3.00	1.93	3	3	5	4	3	5	5	3	4	4.93	32
FS	1	Nathan Chen	USA	1	12	spin	FCCoSp4		3.50	1.40	4	4	3	4	4	4	4	4	4	4.90	32
FS	2	Yuma Kagiyama	JPN	2	1	jump	4S		9.70	4.43	4	5	4	5	4	5	5	5	4	14.13	32
FS	2	Yuma Kagiyama	JPN	2	2	jump	4Loq	q	10.50	-4.65	-5	-5	-4	-3	-5	-3	-4	-5	-5	5.85	32
FS	2	Yuma Kagiyama	JPN	2	3	jump	4T		9.50	3.80	4	4	4	4	4	5	4	4	4	13.30	32
FS	2	Yuma Kagiyama	JPN	2	4	jump	3A+2T		9.30	2.74	3	3	3	3	3	4	4	4	4	12.04	32
FS	2	Yuma Kagiyama	JPN	2	5	spin	CSSp4		3.00	0.90	3	3	3	3	3	3	3	3	3	3.90	32
FS	2	Yuma Kagiyama	JPN	2	6	step_sequence	StSq4		3.90	1.56	4	4	5	3	4	4	4	4	4	5.46	32
FS	2	Yuma Kagiyama	JPN	2	7	jump	4T+1Eu+2S	x	12.43	2.58	2	3	3	3	3	2	3	3	2	15.01	32
FS	2	Yuma Kagiyama	JPN	2	8	jump	3F+3Lo	x	11.22	1.97	3	4	4	4	3	4	5	4	3	13.19	32
FS	2	Yuma Kagiyama	JPN	2	9	jump	3A	x	8.80	1.83	2	2	3	3	3	1	2	1	3	10.63	32
FS	2	Yuma Kagiyama	JPN	2	10	choreographic_sequence	ChSq1		3.00	1.93	4	5	5	3	3	4	4	3	4	4.93	32
FS	2	Yuma Kagiyama	JPN	2	11	spin	CCoSp4		3.50	1.30	4	3	4	4	3	4	4	3	4	4.80	32
FS	2	Yuma Kagiyama	JPN	2	12	spin	FCCoSp4		3.50	1.25	3	3	4	4	4	4	3	4	3	4.75	32
FS	3	Shoma Uno	JPN	5	1	jump	4Lo		10.50	3.45	3	4	4	3	3	3	3	4	3	13.95	34
FS	3	Shoma Uno	JPN	5	2	jump	4Sq	q	9.70	-2.77	-4	-4	-3	-2	0	-4	-2	-2	-3	6.93	34
FS	3	Shoma Uno	JPN	5	3	jump	4F		11.00	-5.34	-5	-5	-4	-4	-5	-5	-5	-5	-5	5.66	34
FS	3	Shoma Uno	JPN	5	4	jump	3A		8.00	2.63	3	4	5	3	3	4	3	3	3	10.63	34
FS	3	Shoma Uno	JPN	5	5	spin	FCSp4		3.20	0.96	4	3	3	3	3	3	2	3	3	4.16	34
FS	3	Shoma Uno	JPN	5	6	choreographic_sequence	ChSq1		3.00	1.79	4	3	4	2	4	4	3	4	3	4.79	34
FS	3	Shoma Uno	JPN	5	7	jump	4T	x	10.45	-0.95	0	-1	-2	-2	-1	0	-2	-1	1	9.50	34
FS	3	Shoma Uno	JPN	5	8	jump	4T+2T	x	11.88	2.85	3	3	3	3	3	3	3	3	3	14.73	34
FS	3	Shoma Uno	JPN	5	9	jump	3A+1Eu+1F	x	9.90	0.91	1	1	2	0	2	1	2	1	0	10.81	34
FS	3	Shoma Uno	JPN	5	10	spin	FCCoSp4		3.50	1.10	3	3	3	2	3	4	3	4	3	4.60	34
FS	3	Shoma Uno	JPN	5	11	spin	CCoSp4		3.50	1.30	4	3	3	3	4	4	4	4	4	4.80	34
FS	3	Shoma Uno	JPN	5	12	step_sequence	StSq4		3.90	1.78	4	4	5	5	5	5	4	5	4	5.68	34
FS	4	Yuzuru Hanyu	JPN	3	1	jump	4A<	<	10.00	-5.00	-5	-5	-5	-5	-5	-5	-5	-5	-5	5.00	33
FS	4	Yuzuru Hanyu	JPN	3	2	jump	4Sq	q	9.70	-4.85	-5	-5	-5	-5	-5	-5	-5	-5	-5	4.85	33
FS	4	Yuzuru Hanyu	JPN	3	3	jump	3A+2T		9.30	2.40	4	3	3	3	3	3	2	3	3	11.70	33
FS	4	Yuzuru Hanyu	JPN	3	4	jump	3F		5.30	1.51	3	4	2	3	3	3	3	3	2	6.81	33
FS	4	Yuzuru Hanyu	JPN	3	5	spin	FCCoSp4		3.50	1.00	3	3	2	3	3	3	2	4	3	4.50	33
FS	4	Yuzuru Hanyu	JPN	3	6	step_sequence	StSq4		3.90	1.67	4	4	5	5	4	4	4	5	4	5.57	33
FS	4	Yuzuru Hanyu	JPN	3	7	jump	4T+3T	x	15.07	2.44	2	3	3	3	3	2	2	2	3	17.51	33
FS	4	Yuzuru Hanyu	JPN	3	8	jump	4T+1Eu+3S	x	15.73	3.12	3	3	4	4	4	3	3	3	3	18.85	33
FS	4	Yuzuru Hanyu	JPN	3	9	jump	3A	x	8.80	3.20	4	3	4	4	4	4	4	4	4	12.00	33
FS	4	Yuzuru Hanyu	JPN	3	10	choreographic_sequence	ChSq1		3.00	2.14	5	4	5	4	4	4	4	5	4	5.14	33
FS	4	Yuzuru Hanyu	JPN	3	11	spin	FCSSp4		3.00	1.20	5	3	3	4	4	4	4	5	4	4.20	33
FS	4	Yuzuru Hanyu	JPN	3	12	spin	CCoSp4V		2.63	0.86	4	3	3	3	3	3	4	4	3	3.49	33
FS	5	Junhwan Cha	KOR	7	1	jump	4T<	<	7.60	-3.80	-5	-5	-5	-5	-5	-5	-5	-5	-5	3.80	35
FS	5	Junhwan Cha	KOR	7	2	jump	4S		9.70	3.19	3	3	4	4	4	3	3	3	3	12.89	35
FS	5	Junhwan Cha	KOR	7	3	jump	3Lz+3Lo		10.80	1.77	3	3	3	3	3	3	2	3	3	12.57	35
FS	5	Junhwan Cha	KOR	7	4	spin	FCSp4		3.20	1.01	3	3	3	4	3	3	2	3	4	4.21	35
FS	5	Junhwan Cha	KOR	7	5	step_sequence	StSq4		3.90	1.45	4	3	4	5	4	3	3	4	4	5.35	35
FS	5	Junhwan Cha	KOR	7	6	jump	3A+2T		9.30	1.83	3	2	3	2	2	1	2	2	3	11.13	35
FS	5	Junhwan Cha	KOR	7	7	jump	3A	x	8.80	1.94	3	2	3	3	2	2	1	2	3	10.74	35
FS	5	Junhwan Cha	KOR	7	8	jump	3Lz+1Eu+3S	x	11.77	0.42	-1	1	2	1	2	-1	0	0	2	12.19	35
FS	5	Junhwan Cha	KOR	7	9	jump	3F	x	5.83	1.36	3	2	3	3	2	3	1	2	3	7.19	35
FS	5	Junhwan Cha	KOR	7	10	choreographic_sequence	ChSq1		3.00	2.29	5	5	5	5	4	4	5	4	4	5.29	35
FS	5	Junhwan Cha	KOR	7	11	spin	CSSp4		3.00	0.99	4	3	3	3	3	4	3	4	3	3.99	35
FS	5	Junhwan Cha	KOR	7	12	spin	CCoSp3		3.00	1.24	4	5	4	4	4	5	4	4	4	4.24	35
FS	6	Jason Brown	USA	6	1	jump	3F		5.30	2.35	5	5	4	4	4	5	5	4	4	7.65	34
FS	6	Jason Brown	USA	6	2	jump	3A+2T		9.30	2.17	3	3	4	3	3	2	2	2	3	11.47	34
FS	6	Jason Brown	USA	6	3	jump	3A		8.00	2.51	4	3	5	3	3	3	3	2	3	10.51	34
FS	6	Jason Brown	USA	6	4	spin	CCoSp4		3.50	1.45	5	4	4	4	4	5	3	4	4	4.95	34
FS	6	Jason Brown	USA	6	5	jump	3Lo		4.90	0.98	2	1	3	3	2	1	1	2	3	5.88	34
FS	6	Jason Brown	USA	6	6	jump	3F+3T	x	10.45	1.97	4	4	4	4	3	4	4	3	3	12.42	34
FS	6	Jason Brown	USA	6	7	jump	3Lz+1Eu+2S	x	8.47	1.18	2	2	4	2	2	2	2	2	2	9.65	34
FS	6	Jason Brown	USA	6	8	choreographic_sequence	ChSq1		3.00	2.50	4	5	5	5	5	5	5	5	5	5.50	34
FS	6	Jason Brown	USA	6	9	jump	2A	x	3.63	0.61	2	1	3	3	2	1	2	1	2	4.24	34
FS	6	Jason Brown	USA	6	10	spin	FCCoSp4		3.50	1.35	4	3	4	3	4	5	4	4	4	4.85	34
FS	6	Jason Brown	USA	6	11	step_sequence	StSq4		3.90	1.84	4	4	5	5	5	5	4	5	5	5.74	34
FS	6	Jason Brown	USA	6	12	spin	CCSp4		3.20	1.60	5	5	5	4	5	5	5	5	5	4.80	34
FS	7	Daniel Grassl	ITA	4	1	jump	4Lz!	!	11.50	0.82	2	1	1	1	0	1	0	1	0	12.32	33
FS	7	Daniel Grassl	ITA	4	2	jump	4F		11.00	2.67	3	2	2	3	2	2	2	3	3	13.67	33
FS	7	Daniel Grassl	ITA	4	3	jump	4Lo+1Eu+3S		15.30	1.80	3	1	1	1	2	2	2	2	2	17.10	33
FS	7	Daniel Grassl	ITA	4	4	jump	3A		8.00	1.71	3	1	2	3	2	2	2	2	2	9.71	33
FS	7	Daniel Grassl	ITA	4	5	spin	CSSp4		3.00	0.77	3	2	3	3	2	3	2	3	2	3.77	33
FS	7	Daniel Grassl	ITA	4	6	jump	3Lz+3T	x	11.11	1.10	3	1	2	3	2	1	1	2	2	12.21	33
FS	7	Daniel Grassl	ITA	4	7	jump	3F+3T<	x	9.53	-0.45	-1	-2	0	-1	-1	-1	-1	-1	0	9.08	33
FS	7	Daniel Grassl	ITA	4	8	jump	3Lz	x	6.49	1.10	3	1	3	2	2	1	1	2	2	7.59	33
FS	7	Daniel Grassl	ITA	4	9	spin	FCCoSp4		3.50	0.75	3	2	1	2	2	2	2	3	2	4.25	33
FS	7	Daniel Grassl	ITA	4	10	step_sequence	StSq4		3.90	1.06	3	1	3	2	3	2	3	3	3	4.96	33
FS	7	Daniel Grassl	ITA	4	11	choreographic_sequence	ChSq1		3.00	1.14	2	1	3	2	2	3	2	2	3	4.14	33
FS	7	Daniel Grassl	ITA	4	12	spin	CCoSp4		3.50	1.05	4	3	3	2	3	3	3	3	3	4.55	33
FS	8	Evgeni Semenenko	ROC	9	1	jump	4T		9.50	-4.21	-3	-4	-5	-4	-5	-4	-4	-5	-5	5.29	36
FS	8	Evgeni Semenenko	ROC	9	2	jump	4S		9.70	2.63	3	3	2	3	3	3	2	2	3	12.33	36
FS	8	Evgeni Semenenko	ROC	9	3	jump	4T+3T		13.70	2.58	3	2	1	3	3	3	2	3	3	16.28	36
FS	8	Evgeni Semenenko	ROC	9	4	jump	3F+2T		6.60	-0.08	-2	0	0	0	1	0	-1	0	0	6.52	36
FS	8	Evgeni Semenenko	ROC	9	5	spin	CCoSp4		3.50	0.60	3	1	1	2	2	1	1	3	2	4.10	36
FS	8	Evgeni Semenenko	ROC	9	6	jump	3A+1Eu+3S	x	14.08	2.40	3	3	1	3	3	3	3	3	4	16.48	36
FS	8	Evgeni Semenenko	ROC	9	7	jump	3A	x	8.80	2.17	3	3	1	3	3	3	2	2	3	10.97	36
FS	8	Evgeni Semenenko	ROC	9	8	step_sequence	StSq4		3.90	0.84	1	1	2	3	3	2	2	2	3	4.74	36
FS	8	Evgeni Semenenko	ROC	9	9	choreographic_sequence	ChSq1		3.00	1.36	3	2	2	4	3	3	1	3	3	4.36	36
FS	8	Evgeni Semenenko	ROC	9	10	jump	3Lo	x	5.39	0.91	2	1	2	3	2	1	2	2	2	6.30	36
FS	8	Evgeni Semenenko	ROC	9	11	spin	CSSp4		3.00	0.69	3	1	1	4	2	3	2	3	2	3.69	36
FS	8	Evgeni Semenenko	ROC	9	12	spin	FCSp4		3.20	0.55	3	1	0	3	2	2	1	2	1	3.75	36
FS	9	Boyang Jin	CHN	8	1	jump	4Lz		11.50	4.11	4	4	3	4	4	3	3	3	4	15.61	35
FS	9	Boyang Jin	CHN	8	2	jump	4T+2T		10.80	2.04	2	2	2	3	2	1	2	2	3	12.84	35
FS	9	Boyang Jin	CHN	8	3	jump	3A+1Eu+3S		12.80	1.71	2	2	2	3	2	2	2	2	3	14.51	35
FS	9	Boyang Jin	CHN	8	4	spin	FCSp4		3.20	0.64	3	1	2	3	2	1	2	2	2	3.84	35
FS	9	Boyang Jin	CHN	8	5	jump	4T		9.50	1.76	2	2	1	4	2	2	1	2	2	11.26	35
FS	9	Boyang Jin	CHN	8	6	jump	3Lz+2T	x	7.92	0.17	-1	0	1	2	1	0	0	0	0	8.09	35
FS	9	Boyang Jin	CHN	8	7	jump	3A	x	8.80	1.03	0	1	2	2	2	2	1	1	0	9.83	35
FS	9	Boyang Jin	CHN	8	8	jump	3F	x	5.83	-1.67	-4	-3	-4	-2	-3	-3	-3	-3	-3	4.16	35
FS	9	Boyang Jin	CHN	8	9	spin	CSSp4		3.00	0.60	2	1	2	3	2	2	2	2	2	3.60	35
FS	9	Boyang Jin	CHN	8	10	step_sequence	StSq4		3.90	1.00	3	2	3	4	2	2	3	2	3	4.90	35
FS	9	Boyang Jin	CHN	8	11	choreographic_sequence	ChSq1		3.00	1.14	2	1	3	2	2	2	3	2	3	4.14	35
FS	9	Boyang Jin	CHN	8	12	spin	CCoSp4		3.50	0.95	3	2	3	3	3	3	3	2	2	4.45	35
FS	10	Morisi Kvitelashvili	GEO	11	1	jump	4S+2T		11.00	0.42	1	1	0	1	1	0	0	-1	0	11.42	37
FS	10	Morisi Kvitelashvili	GEO	11	2	jump	3A		8.00	2.17	3	3	2	2	3	3	3	2	3	10.17	37
FS	10	Morisi Kvitelashvili	GEO	11	3	jump	4T		9.50	-3.26	-4	-3	-4	-3	-3	-2	-4	-4	-3	6.24	37
FS	10	Morisi Kvitelashvili	GEO	11	4	jump	3Lo		4.90	1.26	3	2	2	3	2	3	3	2	3	6.16	37
FS	10	Morisi Kvitelashvili	GEO	11	5	spin	FCSp4		3.20	0.59	3	1	0	2	2	2	1	2	3	3.79	37
FS	10	Morisi Kvitelashvili	GEO	11	6	step_sequence	StSq4		3.90	1.00	3	2	2	3	4	3	2	2	3	4.90	37
FS	10	Morisi Kvitelashvili	GEO	11	7	jump	4T+3T	x	15.07	1.09	2	1	0	1	2	2	2	0	0	16.16	37
FS	10	Morisi Kvitelashvili	GEO	11	8	jump	2F+1Eu+3S	x	7.26	0.12	0	1	0	1	2	0	0	0	0	7.38	37
FS	10	Morisi Kvitelashvili	GEO	11	9	jump	3F	x	5.83	0.83	2	2	1	2	2	2	1	1	1	6.66	37
FS	10	Morisi Kvitelashvili	GEO	11	10	spin	FCCoSp4		3.50	0.90	3	2	2	2	3	3	3	2	3	4.40	37
FS	10	Morisi Kvitelashvili	GEO	11	11	choreographic_sequence	ChSq1		3.00	1.29	3	2	2	2	3	3	3	2	3	4.29	37
FS	10	Morisi Kvitelashvili	GEO	11	12	spin	CCoSp4		3.50	0.85	3	1	3	2	3	2	3	1	3	4.35	37
SP	1	Nathan Chen	USA	1	1	jump	4F		11.00	4.40	4	4	5	4	4	4	4	4	4	15.40	15
SP	1	Nathan Chen	USA	1	2	jump	3A		8.00	2.29	3	3	3	3	4	2	2	2	4	10.29	15
SP	1	Nathan Chen	USA	1	3	spin	CCSp4		3.20	1.05	4	4	3	4	3	3	3	3	3	4.25	15
SP	1	Nathan Chen	USA	1	4	jump	4Lz+3T	x	17.27	3.94	4	4	4	3	4	2	2	3	4	21.21	15
SP	1	Nathan Chen	USA	1	5	step_sequence	StSq4		3.90	1.95	5	5	5	5	5	5	4	5	5	5.85	15
SP	1	Nathan Chen	USA	1	6	spin	FSSp4		3.00	1.03	3	4	4	3	4	3	3	3	4	4.03	15
SP	1	Nathan Chen	USA	1	7	spin	CCoSp4		3.50	1.45	4	4	4	5	4	4	4	5	4	4.95	15
SP	2	Yuma Kagiyama	JPN	2	1	jump	4S		9.70	4.02	4	4	4	4	4	4	4	5	5	13.72	15
SP	2	Yuma Kagiyama	JPN	2	2	jump	4T+3T		13.70	3.94	4	4	4	5	4	3	4	4	5	17.64	15
SP	2	Yuma Kagiyama	JPN	2	3	spin	CCSp4		3.20	1.14	3	4	5	4	3	3	4	4	3	4.34	15
SP	2	Yuma Kagiyama	JPN	2	4	jump	3A	x	8.80	2.86	4	3	3	5	4	3	3	4	4	11.66	15
SP	2	Yuma Kagiyama	JPN	2	5	spin	FSSp4		3.00	0.94	3	4	3	3	3	3	3	3	4	3.94	15
SP	2	Yuma Kagiyama	JPN	2	6	step_sequence	StSq3		3.30	1.46	4	5	5	5	4	4	4	5	3	4.76	15
SP	2	Yuma Kagiyama	JPN	2	7	spin	CCoSp4		3.50	1.35	3	4	4	4	4	4	3	4	5	4.85	15
SP	3	Shoma Uno	JPN	3	1	jump	4F		11.00	3.77	3	4	3	5	4	3	3	2	4	14.77	16
SP	3	Shoma Uno	JPN	3	2	jump	4T+3T		13.70	-0.14	1	-1	-1	1	0	-1	0	0	0	13.56	16
SP	3	Shoma Uno	JPN	3	3	spin	FCSp4		3.20	0.91	3	3	3	3	3	3	2	2	3	4.11	16
SP	3	Shoma Uno	JPN	3	4	jump	3A	x	8.80	3.20	3	4	4	5	4	4	4	4	4	12.00	16
SP	3	Shoma Uno	JPN	3	5	spin	CSSp4		3.00	1.03	3	5	4	3	4	3	3	3	4	4.03	16
SP	3	Shoma Uno	JPN	3	6	step_sequence	StSq4		3.90	1.78	5	5	4	5	5	4	4	5	4	5.68	16
SP	3	Shoma Uno	JPN	3	7	spin	CCoSp4		3.50	1.40	4	4	4	4	4	4	3	4	4	4.90	16
SP	4	Yuzuru Hanyu	JPN	8	1	jump	1S*	*	0.00	0.00	-	-	-	-	-	-	-	-	-	0.00	18
SP	4	Yuzuru Hanyu	JPN	8	2	jump	4T+3T		13.70	4.07	4	4	3	4	5	5	4	4	5	17.77	18
SP	4	Yuzuru Hanyu	JPN	8	3	spin	FCSp4		3.20	1.01	3	3	3	4	4	3	3	3	3	4.21	18
SP	4	Yuzuru Hanyu	JPN	8	4	jump	3A	x	8.80	2.63	3	5	3	5	3	3	3	3	3	11.43	18
SP	4	Yuzuru Hanyu	JPN	8	5	spin	CSSp4		3.00	1.03	4	4	3	4	3	3	3	3	4	4.03	18
SP	4	Yuzuru Hanyu	JPN	8	6	step_sequence	StSq4		3.90	1.78	4	4	4	5	5	5	5	5	4	5.68	18
SP	4	Yuzuru Hanyu	JPN	8	7	spin	CCoSp4		3.50	1.45	4	4	4	4	4	4	5	5	4	4.95	18
SP	5	Junhwan Cha	KOR	4	1	jump	4S		9.70	3.33	3	4	3	3	4	3	4	3	4	13.03	16
SP	5	Junhwan Cha	KOR	4	2	jump	3Lz+3Lo		10.80	1.69	3	3	3	2	3	2	3	3	3	12.49	16
SP	5	Junhwan Cha	KOR	4	3	spin	FCSp4		3.20	1.01	4	3	3	3	4	3	3	3	3	4.21	16
SP	5	Junhwan Cha	KOR	4	4	jump	3A	x	8.80	1.37	2	2	1	1	1	2	2	2	3	10.17	16
SP	5	Junhwan Cha	KOR	4	5	spin	CSSp4		3.00	0.99	4	3	3	2	3	3	3	4	4	3.99	16
SP	5	Junhwan Cha	KOR	4	6	step_sequence	StSq4		3.90	1.56	4	4	3	5	4	4	4	5	3	5.46	16
SP	5	Junhwan Cha	KOR	4	7	spin	CCoSp4		3.50	1.45	4	4	5	4	4	4	4	5	4	4.95	16
SP	6	Jason Brown	USA	6	1	jump	3F		5.30	1.89	3	4	4	4	4	2	3	3	4	7.19	17
SP	6	Jason Brown	USA	6	2	jump	3A		8.00	2.17	3	4	2	4	3	2	3	2	2	10.17	17
SP	6	Jason Brown	USA	6	3	spin	FSSp4		3.00	1.03	3	4	4	3	4	3	3	3	4	4.03	17
SP	6	Jason Brown	USA	6	4	jump	3Lz+3T	x	11.11	1.94	3	2	3	4	4	3	3	3	4	13.05	17
SP	6	Jason Brown	USA	6	5	step_sequence	StSq4		3.90	1.95	5	5	5	5	5	4	5	5	5	5.85	17
SP	6	Jason Brown	USA	6	6	spin	CCoSp4		3.50	1.50	4	4	4	5	4	4	4	5	5	5.00	17
SP	6	Jason Brown	USA	6	7	spin	CCSp4		3.20	1.46	5	4	5	5	5	4	4	5	4	4.66	17
SP	7	Daniel Grassl	ITA	12	1	jump	4Lz!q	!	11.50	-1.64	0	-2	-2	-1	-1	-1	-1	-3	-2	9.86	20
SP	7	Daniel Grassl	ITA	12	2	jump	3Lz!+3T	!	10.10	0.17	1	0	0	0	1	0	0	0	1	10.27	20
SP	7	Daniel Grassl	ITA	12	3	spin	FSSp4		3.00	0.51	2	3	1	0	2	0	2	2	3	3.51	20
SP	7	Daniel Grassl	ITA	12	4	jump	3A	x	8.80	2.29	3	3	2	3	3	2	3	3	3	11.09	20
SP	7	Daniel Grassl	ITA	12	5	step_sequence	StSq4		3.90	1.17	3	3	3	3	4	2	3	3	3	5.07	20
SP	7	Daniel Grassl	ITA	12	6	spin	CCSp4		3.20	1.05	3	4	4	2	4	3	3	3	3	4.25	20
SP	7	Daniel Grassl	ITA	12	7	spin	CCoSp4		3.50	1.15	3	4	3	3	3	3	3	4	4	4.65	20
SP	8	Evgeni Semenenko	ROC	7	1	jump	4T+3T		13.70	2.17	3	3	2	1	3	1	3	2	2	15.87	18
SP	8	Evgeni Semenenko	ROC	7	2	jump	4S		9.70	2.36	3	3	2	2	3	2	3	2	2	12.06	18
SP	8	Evgeni Semenenko	ROC	7	3	spin	CCoSp4		3.50	0.60	2	2	2	1	2	2	1	1	3	4.10	18
SP	8	Evgeni Semenenko	ROC	7	4	jump	3A	x	8.80	2.06	2	3	3	1	3	3	2	2	3	10.86	18
SP	8	Evgeni Semenenko	ROC	7	5	spin	CSSp4		3.00	0.64	2	3	2	2	2	2	1	2	4	3.64	18
SP	8	Evgeni Semenenko	ROC	7	6	step_sequence	StSq4		3.90	0.78	2	3	2	2	2	2	2	1	2	4.68	18
SP	8	Evgeni Semenenko	ROC	7	7	spin	FCSp4		3.20	0.82	2	4	3	1	2	3	3	2	3	4.02	18
SP	9	Boyang Jin	CHN	11	1	jump	4Lz+3T		15.70	3.12	3	4	2	2	4	2	3	2	3	18.82	20
SP	9	Boyang Jin	CHN	11	2	jump	4T		9.50	2.31	2	3	1	3	3	2	0	3	3	11.81	20
SP	9	Boyang Jin	CHN	11	3	spin	FCSp4		3.20	0.41	1	3	1	1	2	1	1	1	2	3.61	20
SP	9	Boyang Jin	CHN	11	4	jump	3Aq	x	8.80	-4.00	-5	-5	-5	-3	-5	-5	-5	-5	-5	4.80	20
SP	9	Boyang Jin	CHN	11	5	spin	CSSp4		3.00	0.47	2	2	1	1	3	1	1	3	1	3.47	20
SP	9	Boyang Jin	CHN	11	6	step_sequence	StSq4		3.90	1.06	3	4	2	3	3	2	2	3	3	4.96	20
SP	9	Boyang Jin	CHN	11	7	spin	CCoSp4		3.50	0.65	1	3	1	2	3	2	2	1	2	4.15	20
SP	10	Morisi Kvitelashvili	GEO	5	1	jump	4S+3T		13.90	2.08	2	2	1	1	3	2	3	2	3	15.98	17
SP	10	Morisi Kvitelashvili	GEO	5	2	jump	3A		8.00	2.17	3	4	2	2	3	2	3	3	3	10.17	17
SP	10	Morisi Kvitelashvili	GEO	5	3	spin	FCSp4		3.20	0.73	2	3	1	0	3	2	2	3	3	3.93	17
SP	10	Morisi Kvitelashvili	GEO	5	4	jump	4T	x	10.45	2.71	3	3	2	2	4	3	3	3	3	13.16	17
SP	10	Morisi Kvitelashvili	GEO	5	5	step_sequence	StSq3		3.30	0.94	3	3	2	3	3	2	3	3	3	4.24	17
SP	10	Morisi Kvitelashvili	GEO	5	6	spin	CSSp4		3.00	0.81	3	3	2	2	3	2	3	3	4	3.81	17
SP	10	Morisi Kvitelashvili	GEO	5	7	spin	CCoSp4		3.50	0.90	2	3	2	2	3	2	3	3	3	4.40	17
```

### Program components (all 100 rows)

The official components are Skating Skills, Transitions, Performance, Composition, and Interpretation of the Music. `factor` is 1.00 for SP and 2.00 for FS. Judge marks and panel mark are kept separately so the chart can show either the awarded component or judge variation.

```tsv
segment	final_rank	skater	component	factor	J1	J2	J3	J4	J5	J6	J7	J8	J9	panel_mark
FS	1	Nathan Chen	Composition	2.00	9.50	9.50	9.75	9.75	9.75	10.00	9.75	9.75	9.75	9.71
FS	1	Nathan Chen	Interpretation of the Music	2.00	10.00	9.75	9.75	10.00	9.75	10.00	9.50	9.75	10.00	9.86
FS	1	Nathan Chen	Performance	2.00	9.75	9.50	9.75	10.00	9.75	10.00	9.75	9.75	9.75	9.79
FS	1	Nathan Chen	Skating Skills	2.00	9.75	9.75	9.50	9.75	9.75	9.50	9.75	9.75	9.75	9.71
FS	1	Nathan Chen	Transitions	2.00	9.50	9.50	9.50	9.50	9.75	9.50	9.25	9.50	9.75	9.54
FS	2	Yuma Kagiyama	Composition	2.00	9.50	9.50	9.50	9.50	9.50	9.50	9.50	9.25	9.50	9.50
FS	2	Yuma Kagiyama	Interpretation of the Music	2.00	9.50	9.50	9.50	9.25	9.50	9.50	9.50	9.25	9.25	9.43
FS	2	Yuma Kagiyama	Performance	2.00	9.50	9.50	9.50	9.00	9.25	9.25	9.50	9.25	9.25	9.36
FS	2	Yuma Kagiyama	Skating Skills	2.00	9.50	9.50	9.50	9.50	9.50	9.50	9.50	9.75	9.50	9.50
FS	2	Yuma Kagiyama	Transitions	2.00	9.25	9.00	9.25	9.00	9.25	9.25	9.00	9.25	9.25	9.18
FS	3	Shoma Uno	Composition	2.00	9.50	9.25	9.25	9.25	9.25	9.25	9.25	9.50	9.25	9.29
FS	3	Shoma Uno	Interpretation of the Music	2.00	9.25	9.25	9.50	8.75	9.25	9.25	9.00	9.50	9.00	9.21
FS	3	Shoma Uno	Performance	2.00	9.25	9.00	9.00	8.50	9.00	9.00	9.25	9.50	8.75	9.04
FS	3	Shoma Uno	Skating Skills	2.00	9.25	9.50	9.50	9.25	9.25	9.25	9.25	9.50	9.25	9.32
FS	3	Shoma Uno	Transitions	2.00	9.25	9.00	9.00	9.00	9.25	9.00	8.50	9.25	9.00	9.07
FS	4	Yuzuru Hanyu	Composition	2.00	9.25	9.00	9.25	9.25	9.25	9.25	9.25	9.25	9.25	9.25
FS	4	Yuzuru Hanyu	Interpretation of the Music	2.00	8.75	8.75	8.75	8.75	8.75	9.00	8.75	8.75	9.00	8.79
FS	4	Yuzuru Hanyu	Performance	2.00	8.75	8.75	8.75	8.75	8.75	8.75	8.75	8.75	8.75	8.75
FS	4	Yuzuru Hanyu	Skating Skills	2.00	9.25	9.50	9.25	9.25	9.25	9.25	8.75	9.25	9.25	9.25
FS	4	Yuzuru Hanyu	Transitions	2.00	9.25	9.25	9.25	9.00	9.25	9.00	8.75	9.25	9.25	9.18
FS	5	Junhwan Cha	Composition	2.00	9.00	9.25	9.25	9.50	9.00	9.00	8.75	9.00	9.25	9.11
FS	5	Junhwan Cha	Interpretation of the Music	2.00	9.00	9.25	9.25	9.25	9.00	8.75	8.50	9.00	9.25	9.07
FS	5	Junhwan Cha	Performance	2.00	9.00	9.25	9.00	9.00	8.75	8.75	8.50	9.00	9.00	8.93
FS	5	Junhwan Cha	Skating Skills	2.00	9.00	9.25	9.25	9.00	8.75	9.00	8.75	9.25	9.50	9.07
FS	5	Junhwan Cha	Transitions	2.00	8.75	9.00	9.00	9.25	8.75	9.00	8.00	9.25	9.00	8.96
FS	6	Jason Brown	Composition	2.00	9.50	9.75	9.75	10.00	9.50	9.25	9.50	9.50	10.00	9.64
FS	6	Jason Brown	Interpretation of the Music	2.00	9.75	9.75	10.00	10.00	9.75	9.25	9.75	9.75	10.00	9.82
FS	6	Jason Brown	Performance	2.00	9.75	9.75	10.00	10.00	9.50	9.25	9.50	9.75	10.00	9.75
FS	6	Jason Brown	Skating Skills	2.00	9.50	9.50	9.75	9.50	9.25	9.25	9.00	9.50	9.75	9.46
FS	6	Jason Brown	Transitions	2.00	9.50	9.50	9.50	9.50	9.50	9.50	9.25	9.50	9.50	9.50
FS	7	Daniel Grassl	Composition	2.00	8.50	8.50	8.75	8.25	8.50	8.50	8.25	8.75	8.50	8.50
FS	7	Daniel Grassl	Interpretation of the Music	2.00	8.75	8.50	8.50	8.25	8.25	8.50	8.25	8.75	8.25	8.43
FS	7	Daniel Grassl	Performance	2.00	8.75	8.25	8.75	8.50	8.50	8.50	8.25	8.75	8.50	8.54
FS	7	Daniel Grassl	Skating Skills	2.00	8.50	8.25	8.25	8.75	8.50	8.50	8.25	8.50	8.25	8.39
FS	7	Daniel Grassl	Transitions	2.00	8.25	8.25	8.25	8.25	8.00	8.25	8.00	8.50	8.00	8.18
FS	8	Evgeni Semenenko	Composition	2.00	8.50	8.50	8.00	8.50	8.50	8.50	8.00	8.50	8.25	8.39
FS	8	Evgeni Semenenko	Interpretation of the Music	2.00	8.50	8.50	8.25	8.75	8.25	8.50	8.25	8.50	8.25	8.39
FS	8	Evgeni Semenenko	Performance	2.00	8.50	8.75	8.00	8.75	8.50	8.50	8.00	8.50	8.25	8.43
FS	8	Evgeni Semenenko	Skating Skills	2.00	8.25	8.75	8.00	9.00	8.50	8.50	8.50	8.25	8.50	8.46
FS	8	Evgeni Semenenko	Transitions	2.00	8.25	8.25	7.50	8.50	8.00	8.25	7.75	8.25	8.00	8.11
FS	9	Boyang Jin	Composition	2.00	8.50	7.75	8.25	9.25	8.25	8.00	7.75	8.00	8.50	8.18
FS	9	Boyang Jin	Interpretation of the Music	2.00	8.25	7.75	8.50	9.50	8.25	8.00	8.25	8.00	8.25	8.21
FS	9	Boyang Jin	Performance	2.00	8.25	7.75	8.75	9.50	8.50	8.25	8.50	8.50	8.75	8.50
FS	9	Boyang Jin	Skating Skills	2.00	8.25	8.50	8.75	9.25	8.25	8.00	8.50	8.25	8.50	8.43
FS	9	Boyang Jin	Transitions	2.00	8.00	7.50	8.00	9.00	7.50	7.75	7.50	8.00	7.75	7.79
FS	10	Morisi Kvitelashvili	Composition	2.00	8.50	8.50	8.25	8.75	8.50	8.50	8.50	8.50	8.75	8.54
FS	10	Morisi Kvitelashvili	Interpretation of the Music	2.00	8.50	8.50	8.50	8.50	8.50	8.50	8.25	8.50	8.50	8.50
FS	10	Morisi Kvitelashvili	Performance	2.00	8.50	8.50	8.50	8.75	8.50	8.50	8.25	8.50	8.50	8.50
FS	10	Morisi Kvitelashvili	Skating Skills	2.00	8.25	8.75	8.50	8.50	8.50	8.25	8.25	8.50	8.75	8.46
FS	10	Morisi Kvitelashvili	Transitions	2.00	8.25	8.50	8.00	8.25	8.25	8.50	8.50	8.25	8.50	8.36
SP	1	Nathan Chen	Composition	1.00	9.75	9.50	10.00	9.75	9.75	9.75	9.25	9.50	9.75	9.68
SP	1	Nathan Chen	Interpretation of the Music	1.00	10.00	9.75	10.00	9.75	9.50	9.50	9.50	9.50	9.50	9.64
SP	1	Nathan Chen	Performance	1.00	10.00	9.50	9.75	10.00	9.50	9.75	9.50	9.50	10.00	9.71
SP	1	Nathan Chen	Skating Skills	1.00	9.75	9.25	9.50	9.75	9.50	9.75	9.50	9.50	9.50	9.57
SP	1	Nathan Chen	Transitions	1.00	9.75	9.25	9.25	9.50	9.50	9.50	9.25	9.00	9.50	9.39
SP	2	Yuma Kagiyama	Composition	1.00	9.50	9.25	9.50	9.50	9.50	9.50	9.50	9.75	9.25	9.46
SP	2	Yuma Kagiyama	Interpretation of the Music	1.00	9.25	9.25	9.75	9.50	9.50	9.50	9.50	9.75	9.25	9.46
SP	2	Yuma Kagiyama	Performance	1.00	9.50	9.50	9.75	9.50	9.50	9.50	9.50	10.00	9.50	9.54
SP	2	Yuma Kagiyama	Skating Skills	1.00	9.50	9.50	9.75	9.25	9.25	9.50	9.50	10.00	9.50	9.50
SP	2	Yuma Kagiyama	Transitions	1.00	9.25	9.25	9.50	9.25	9.00	9.25	9.25	9.50	9.00	9.25
SP	3	Shoma Uno	Composition	1.00	9.75	9.50	9.25	9.50	9.50	9.50	9.25	9.25	9.25	9.39
SP	3	Shoma Uno	Interpretation of the Music	1.00	9.75	9.50	9.25	9.75	9.50	9.25	9.50	9.50	9.00	9.46
SP	3	Shoma Uno	Performance	1.00	9.50	9.50	9.00	9.50	9.25	9.25	9.50	9.50	9.00	9.36
SP	3	Shoma Uno	Skating Skills	1.00	9.25	9.50	9.25	9.50	9.50	9.50	9.50	9.50	9.25	9.43
SP	3	Shoma Uno	Transitions	1.00	9.25	9.25	9.00	9.25	9.50	9.25	9.00	9.25	9.25	9.21
SP	4	Yuzuru Hanyu	Composition	1.00	9.50	9.50	9.00	9.75	9.50	9.75	9.75	9.50	9.25	9.54
SP	4	Yuzuru Hanyu	Interpretation of the Music	1.00	9.25	9.50	8.75	9.75	9.25	9.75	9.75	9.50	9.00	9.43
SP	4	Yuzuru Hanyu	Performance	1.00	9.25	9.25	8.75	9.75	8.75	9.50	9.50	9.50	9.00	9.25
SP	4	Yuzuru Hanyu	Skating Skills	1.00	9.50	9.25	9.00	9.50	9.50	9.50	9.75	9.25	9.50	9.43
SP	4	Yuzuru Hanyu	Transitions	1.00	9.25	9.50	9.00	9.50	9.25	9.75	9.50	9.50	9.50	9.43
SP	5	Junhwan Cha	Composition	1.00	9.50	9.00	9.00	9.00	8.75	9.25	9.25	9.75	9.00	9.14
SP	5	Junhwan Cha	Interpretation of the Music	1.00	9.25	9.00	8.75	9.25	8.75	9.25	9.50	9.75	8.50	9.11
SP	5	Junhwan Cha	Performance	1.00	9.50	9.00	9.00	9.25	8.75	9.00	9.00	9.75	8.75	9.07
SP	5	Junhwan Cha	Skating Skills	1.00	9.50	8.75	8.75	8.75	8.75	9.00	9.25	9.75	8.50	8.96
SP	5	Junhwan Cha	Transitions	1.00	9.25	8.75	8.75	8.75	8.50	9.00	9.00	9.25	9.00	8.93
SP	6	Jason Brown	Composition	1.00	9.75	9.50	9.25	9.25	9.50	9.50	9.50	9.75	9.50	9.50
SP	6	Jason Brown	Interpretation of the Music	1.00	10.00	9.50	9.25	9.50	9.75	9.50	9.50	9.75	9.50	9.57
SP	6	Jason Brown	Performance	1.00	9.75	9.50	9.25	9.50	9.50	9.50	9.50	9.75	9.50	9.54
SP	6	Jason Brown	Skating Skills	1.00	9.75	9.50	9.00	9.25	9.50	9.00	9.25	9.50	9.00	9.29
SP	6	Jason Brown	Transitions	1.00	9.75	9.25	9.50	9.25	9.75	9.25	9.00	9.25	9.50	9.39
SP	7	Daniel Grassl	Composition	1.00	8.50	8.50	8.25	8.25	8.50	8.50	8.75	8.75	8.75	8.54
SP	7	Daniel Grassl	Interpretation of the Music	1.00	8.50	8.75	8.25	8.25	8.50	8.00	8.75	8.50	8.50	8.46
SP	7	Daniel Grassl	Performance	1.00	8.25	8.50	8.25	8.25	8.75	8.25	8.25	8.50	8.50	8.36
SP	7	Daniel Grassl	Skating Skills	1.00	8.75	8.25	8.25	8.00	8.50	8.25	8.25	8.25	8.25	8.29
SP	7	Daniel Grassl	Transitions	1.00	8.25	8.25	8.00	8.00	8.50	8.00	8.50	8.50	8.50	8.29
SP	8	Evgeni Semenenko	Composition	1.00	8.25	8.25	8.25	8.00	8.25	8.00	8.00	7.75	8.50	8.14
SP	8	Evgeni Semenenko	Interpretation of the Music	1.00	8.00	8.50	8.25	8.00	8.00	7.75	8.25	7.25	8.25	8.07
SP	8	Evgeni Semenenko	Performance	1.00	8.00	8.50	8.00	7.75	8.25	8.50	8.25	7.50	8.50	8.18
SP	8	Evgeni Semenenko	Skating Skills	1.00	8.50	8.50	8.00	8.25	8.00	8.25	8.25	7.75	8.25	8.21
SP	8	Evgeni Semenenko	Transitions	1.00	8.00	8.25	7.75	7.75	7.75	8.00	8.00	7.50	8.50	7.93
SP	9	Boyang Jin	Composition	1.00	8.00	8.25	7.75	8.25	8.50	8.00	7.00	7.50	8.25	8.00
SP	9	Boyang Jin	Interpretation of the Music	1.00	8.25	8.50	7.75	8.00	8.25	7.75	7.25	7.50	8.00	7.93
SP	9	Boyang Jin	Performance	1.00	8.25	8.50	7.50	8.25	8.25	8.00	7.00	7.75	8.25	8.04
SP	9	Boyang Jin	Skating Skills	1.00	8.00	8.25	7.75	8.25	8.25	8.25	7.50	7.75	8.25	8.07
SP	9	Boyang Jin	Transitions	1.00	7.25	8.00	7.25	7.25	7.75	7.50	6.75	6.75	7.50	7.32
SP	10	Morisi Kvitelashvili	Composition	1.00	8.25	8.75	8.25	8.50	8.75	8.25	8.50	8.50	8.50	8.46
SP	10	Morisi Kvitelashvili	Interpretation of the Music	1.00	8.25	8.50	8.25	8.50	8.75	8.25	8.75	8.25	8.50	8.43
SP	10	Morisi Kvitelashvili	Performance	1.00	8.25	8.50	8.00	8.50	8.75	8.50	8.75	8.75	8.50	8.54
SP	10	Morisi Kvitelashvili	Skating Skills	1.00	8.50	8.50	8.00	8.50	8.75	8.50	8.75	8.50	8.50	8.54
SP	10	Morisi Kvitelashvili	Transitions	1.00	8.25	8.25	7.75	8.25	8.50	8.25	8.50	8.75	8.25	8.32
```

### How to read the official notation

- Official legend: `x` = credit for highlight distribution (base value multiplied by 1.1); `!` = not-clear edge; `e` = wrong edge; `q` = jump landed on the quarter; `<` = under-rotated jump; `<<` = downgraded jump; `*` = invalid element; `F` = fall. Keep these as protocol calls, separate from GOE. The full legend is printed in the ISU book.
- A combination such as `4T+3T` is one protocol element and receives one base value / GOE / panel score. If counting jump types, split its code into its component jumps for a frequency chart, but do not copy the combination's GOE onto each jump as if each had its own score.
- The protocol marks sequences in the order performed, but has no element timestamps, elapsed seconds, rink coordinates, jump height, takeoff edge/foot, or landing position. Do not invent those fields from order.

### Dataset-to-sketch guide for the 15 project questions

Use these field mappings as the starting point. The same protocol rows can support multiple distinct sketches; use the specified aggregation rather than treating every row as an independent athlete or program.

| Q | Sketchable question / comparison | Use these fields and operation | Important boundary |
|---:|---|---|---|
| 1 | Which elements appear most often? | Count `element_code_raw` or `element_group`, separately for SP/FS; optionally count spin/step level codes. | State whether combinations count as one protocol element or are split into component jumps. |
| 2 | How is jump rotation associated with GOE? | Filter `element_group=jump`; parse rotation from each jump token in `element_code_raw`; plot rotation vs row-level `goe`, color by SP/FS or jump family. | Combination GOE belongs to the whole combination, not to each jump within it. This is association, not causation. |
| 3 | Do higher-rotation jumps always score more? | For jump rows compare rotation with `base_value` and `panel_element_score`; show `goe` separately. | No: score also depends on jump type, combinations, second-half bonus, calls, and GOE. Avoid a blanket rule from raw totals. |
| 4 | Which jump types are most common? | Split jump tokens (e.g. 4T, 3A, 3Lz) from `element_code_raw`; count across element rows; facet by segment. | A multi-jump combination contributes multiple jump tokens but remains one scored element row. Document both counting views if used. |
| 5 | Which spin types appear most frequently? | Filter `element_group=spin`; count code prefixes/types and levels from `element_code_raw` (e.g. CCSp, FCSp, CCoSp, CSSp, FSSp, FCCoSp). | These are protocol codes; translate with a skating glossary only if the sketch needs expanded names. |
| 6 | How do step-sequence and spin levels relate to score / standing? | Extract level digit from `StSq` and `Sp` codes; compare row scores and link to segment/overall rank via `final_rank`. | A level code is not a causal measure of score; compare like element families and note the top-ten-only cohort. |
| 7 | Which technical elements contribute most to TES? | Sum `panel_element_score` by element group/type, skater, or segment; compute share of `TES` from the segment table. | Compare both totals and per-occurrence averages so frequent elements do not dominate only by count. |
| 8 | How does element sequence differ SP vs FS? | Sort by `element_order`; compare element-group sequences or a skater's exact codes across `segment`. | Program formats have different required element counts/content; SP and FS are not equal-length sequences. |
| 9 | Where in the program are the highest-value elements? | Plot `element_order` against `base_value` or `panel_element_score`; separate SP/FS. | “Where” means sequence position only. No timestamps or rink locations are in this dataset. |
| 10 | Which elements receive highest/lowest GOE? | Rank rows by `goe`; group/facet by `element_code_raw` or `element_group`; include J1-J9 if showing panel spread. | GOE is a judged evaluation; small sample and repeated rows should remain visible. |
| 11 | How often do protocols flag errors / falls? | Count rows whose `element_code_raw` or `info_flag` contains `!`, `e`, `q`, `<`, `<<`, `*`; use `falls_count` and `deduction_detail_raw` from the segment table for falls. | Fall count is segment-level in this report and is not assigned to a particular element row. Flags describe calls, not the full reason for every score. |
| 12 | How does TES compare with final segment / overall score? | Segment table: plot TES vs `segment_score_TSS`; join final total from the top-ten standings by skater and compare TES share or rank. | Segment TSS is not the combined overall score; label them distinctly. |
| 13 | What are the technical components of selected skaters' programs? | Use each skater's ordered `element_code_raw`, `base_value`, `goe`, panel score, plus `element_group`; optionally add component data. | Describes recorded elements and scoring—not body mechanics, artistry explanations, or exact 3D movement. |
| 14 | How does the jump/spin/sequence mix differ SP vs FS? | Count rows by `element_group` per skater/segment; optionally split jump combinations into jump tokens and spins/sequences by code. | Normalize to share of elements when comparing programs with 7 vs 12 rows. |
| 15 | Can a lower-base-value element score higher after GOE than a higher-base-value element? | Compare pairs/rows using `base_value`, `goe`, `panel_element_score`; identify cases where lower base + positive GOE exceeds higher base + negative GOE. | Use actual panel scores, not base value alone; second-half bonus and calls affect comparisons. |

### What this pack does and does not cover

With the embedded standings, 20 segment records, 190 element records, judge GOEs, 100 component records, and the question-to-field map above, a reader can make the planned competition-score sketches without reopening the source pages. The source links remain useful for auditing and definitions. This is not a full movement-capture dataset: it cannot supply exact performance video timestamps, positions on the ice, body/joint trajectories, or synchronized 3D animations. The FineFS and FS-Jump3D links above remain separate motion-reference datasets and must not be presented as these ten Beijing performances unless an exact match is independently verified.

### Extraction provenance

Extracted from the [official ISU results-book PDF](https://www.isuresults.com/results/season2122/owg2022/owg2022_protocol.pdf), individual men's singles short-program protocol pages 15–29 and free-skating protocol pages 32–43 (physical PDF numbering). The protocol pages themselves label the relevant skater and segment. Tables were checked with row counts and score-sum invariants described above.
