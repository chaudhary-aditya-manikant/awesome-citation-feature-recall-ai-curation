# Missing-title source audit — 31 October 2026

**Scope:** 19 records whose OpenAlex title field was empty in the 2,790-record balanced collection. This document records only source-verifiable findings; it does not invent article titles from abstracts or DOI strings.

## Source-verified issue-level records (6)

These DOI records resolve to an entire journal issue or issue-level paratext record, not an individual research article. They are therefore excluded from the article-level screening pool, with their OpenAlex IDs and source evidence retained in `title_metadata_repair_hold_19.csv` and the private admin crosswalk.

| OpenAlex ID | DOI | Publisher/library page title | Primary source | Decision |
|---|---|---|---|---|
| W4234091750 | `10.15407/kvt197.03` | Issue 3 (197) | https://kvt-journal.org.ua/1322/ | Exclude issue-level paratext |
| W4236425257 | `10.30958/ajms/v5i4` | Volume 5, Issue 4 | https://www.athensjournals.gr/ajms/v5i4 | Exclude issue-level paratext |
| W4245806534 | `10.21661/a-504` | Monthly international scientific journal «Interactive science». Issue 5 (27) | https://interactive-plus.ru/en/action/504/info | Exclude issue-level paratext |
| W4241483880 | `10.26659/pm3.2017.18.4` | Palestrica of the third millennium Civilization and sport Vol 18 no 4, October-December 2017 | https://www.pm3.ro/palestrica-of-the-third-millennium-civilization-and-sport-vol-18-no-4-october-december-2017/ | Exclude issue-level paratext |
| W4414894171 | `10.47329/jurnal_mbe.v11i2` | Vol 11 No 2 (2025): Jurnal Manajemen dan Bisnis Equilibrium | https://ojs.unr.ac.id/index.php/Equilibrium/issue/view/149 | Exclude issue-level paratext |
| W7117301792 | `10.19181/smtp.2025.7.4` | Управление наукой: теория и практика. Том 7 №4 (2025) / Science Management: Theory and Practice, Vol. 7 No. 4 (2025) | https://www.science-practice.ru/index.php/science/issue/view/YLVDXQ | Exclude issue-level paratext |

The page titles are recorded as bibliographic evidence only; they are not inserted into the article title field because these records represent whole issues rather than standalone papers.

## Unresolved source holds (13)

No authoritative publisher/library source was established in this audit that could safely repair the missing title. These records remain excluded from the screening queue until repaired or explicitly excluded as unrecoverable metadata. Do not infer titles from abstracts or DOI patterns.

| OpenAlex ID | DOI | Year |
|---|---|---:|
| W4225268734 | `10.1002/smr.v34.5` | 2022 |
| W4225968120 | `10.17159/2520-9868/2021` | 2021 |
| W4230630295 | `10.35318/mch.20200602` | 2021 |
| W4231874937 | `10.5121/ijaia.2015.6600` | 2015 |
| W4236386265 | `10.37380/jisib.v9i2` | 2019 |
| W4239011082 | `10.17323/2713-2749.2020.3` | 2020 |
| W4239180379 | `10.18689/mjai-v1-i1` | 2016 |
| W4239862309 | `10.17705/1jais.1612` | 2015 |
| W4241261036 | `10.21826/2179-5800201671` | 2016 |
| W4284973659 | `10.17148/iarjset.2022.97` | 2022 |
| W4387308989 | `10.36615/digital_food_energy_water_systems.v4i1` | 2023 |
| W4410869065 | `10.51895/vss/1` | 2021 |
| W7205007890 | `10.9790/5933-1606` | 2025 |

## Effect on the active pool

- Original missing-title records: 19.
- Publisher-source-confirmed issue-level paratext exclusions: 6.
- Unresolved title-metadata holds: 13.
- Human-screening queue remains 2,763 records; it does not include these 19 missing-title records or the eight administrative candidates.
- No relevance labels are assigned to any of the 19 records.

## Integrity rule

A missing title is a metadata problem, not a negative relevance decision. If a publisher/library source cannot establish a standalone article title, retain the record in the hold ledger and exclude it from the article pool only with a documented administrative rationale.
