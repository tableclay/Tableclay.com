# Consulting Quant QC Cookbook

A paste-ready reference for the math, formulas, and sanity checks used daily at Seurat Group. Every formula is Excel-native so anyone on the team can use it.

---

## Table of Contents
1. [Index Calculations](#1-index-calculations)
2. [Top-2-Box / Bottom-2-Box](#2-top-2-box--bottom-2-box)
3. [Combined Bases](#3-combined-bases)
4. [Household Penetration](#4-household-penetration)
5. [Share Calculations](#5-share-calculations)
6. [Growth & CAGR](#6-growth--cagr)
7. [RYG Threshold System](#7-ryg-threshold-system)
8. [Z-Score Normalization (0-100)](#8-z-score-normalization-0-100)
9. [Data Labels for PowerPoint Charts](#9-data-labels-for-powerpoint-charts)
10. [Survey Quota & Fielding Math](#10-survey-quota--fielding-math)
11. [Rounding Rules](#11-rounding-rules)
12. [Base Size Rules](#12-base-size-rules)
13. [QC Checklist (Run Every Time)](#13-qc-checklist-run-every-time)
14. [Common Pitfalls](#14-common-pitfalls)

---

## 1. Index Calculations

### Basic Index
Measures how a segment compares to a benchmark. 100 = at parity.

**Formula:**
```
Index = (Segment Value / Benchmark Value) × 100
```

**Excel:**
```excel
=ROUND((B2/C2)*100, 0)
```

**Interpretation:**
- **>100** = over-indexes (segment is higher than benchmark)
- **=100** = at parity
- **<100** = under-indexes

**Always state the benchmark.** "Index vs. Total" or "Index vs. Category Average" — never just "Index."

### Index of a Sub-segment vs. Total
When you have column % for a segment and column % for total:

```excel
=ROUND((SegmentPct/TotalPct)*100, 0)
```

**Example:** Gummy candy eats at "Afternoon snack" = 63%, Total = 55%
```
Index = (63% / 55%) × 100 = 115
```

---

## 2. Top-2-Box / Bottom-2-Box

For Likert or bipolar scales, T2B and B2B compress the scale into a single metric.

### Definition
- **Top-2-Box (T2B):** Sum of the top two response options (e.g., "Strongly agree" + "Agree")
- **Bottom-2-Box (B2B):** Sum of the bottom two response options

### Calculation
```
T2B % = Option1 % + Option2 %
T2B Count = Option1 Count + Option2 Count
```

**Excel:**
```excel
=SUM(B2:B3)          // T2B %
=SUM(D2:D3)          // T2B count
```

### Index of T2B (segment vs. total)
```
T2B Index = (Segment T2B % / Total T2B %) × 100
```

**Excel:**
```excel
=ROUND((SegT2B/TotalT2B)*100, 0)
```

### Critical Rule: Weight by Counts, Not Averages
When combining indices across sub-groups, **never average the index numbers directly.** Always go back to counts.

**Wrong:** `(Index_A + Index_B) / 2`
**Right:** `(Count_A + Count_B) / Total_Count × 100 → then index`

---

## 3. Combined Bases

When merging two or more sub-segments into one combined column.

### Steps
1. **Combined count (per row):** `n(seg1) + n(seg2)`
2. **Combined %:** `Combined count / Combined total base`
3. **Index vs. Total:** `(Combined % / Total %) × 100`

**Excel (row-level):**
```excel
// Combined count
=D2+F2

// Combined %
=H2/SUM($H$2:$H$last)

// Index vs Total
=ROUND((I2/J2)*100, 0)
```

**Example:** Packaged sandwich cookies (n=88) + Non-sandwich cookies (n=106) → Combined base n=194

---

## 4. Household Penetration

How to calculate what % of total households fall into a custom group.

### Formula
```
HH Penetration % = (HH in custom group / Total HH universe) × 100
```

### Key Rules
- **Same universe:** Denominator must match the platform's definition (panel universe, active HHs, etc.)
- **Same filters:** Date range, geography, channel must be identical for numerator and denominator
- **Weighted vs. unweighted:** If your platform provides projection weights, use weighted counts

**Excel (unweighted):**
```excel
=COUNTIF(GroupColumn, "Yes") / COUNTA(HouseholdID_Column)
```

**Excel (weighted):**
```excel
=SUMPRODUCT((GroupColumn="Yes")*WeightColumn) / SUM(WeightColumn)
```

---

## 5. Share Calculations

### Basic Share
```
Share % = Part / Whole × 100
```

### Share Change
**Always use percentage points (pp), not percent (%)**

- **Right:** "Share grew 3pp (from 12% to 15%)"
- **Wrong:** "Share grew 3%" (ambiguous — could mean 3% of 12% = 0.36pp)

**Excel:**
```excel
=B2-C2              // pp change (current - prior)
```

### QC: Shares Must Sum to ~100%
```excel
=SUM(B2:B20)        // Should be 99-101% (rounding tolerance)
```
Flag anything outside 98-102%.

---

## 6. Growth & CAGR

### Year-over-Year Growth
```
YoY % = (Current - Prior) / Prior × 100
```

**Excel:**
```excel
=ROUND((B2-C2)/C2*100, 1)
```

### CAGR (Compound Annual Growth Rate)
```
CAGR = (End / Start)^(1/n) - 1
```

**Excel:**
```excel
=ROUND((EndValue/StartValue)^(1/Years)-1, 3)
```

**Always state the time period.** "5-year CAGR 2020-2025" not just "CAGR."

---

## 7. RYG Threshold System

Color-code indices to quickly flag what matters. Two standard options:

### Option A — Balanced (default)
| Color | Index Range | Meaning |
|---|---|---|
| Red | < 105 | Near average or under; not a differentiator |
| Yellow | 105 - 114 | Mild lift; worth noting |
| Green | ≥ 115 | Meaningful over-index; lean in |

### Option B — Stricter (fewer greens)
| Color | Index Range | Meaning |
|---|---|---|
| Red | < 110 | Not significant |
| Yellow | 110 - 119 | Moderate |
| Green | ≥ 120 | Strong over-index |

### Optional: Add a "Green+" Tier
- **Green+:** ≥ 130 = "very strong over-index" (use a darker green or bold)

### How to Choose Thresholds
1. **Look at the data spread.** If most indices are 95-110, use Option A (105/115). If the range is wider (80-150+), use Option B (110/120).
2. **Match existing deck conventions.** If the project already has RYG elsewhere, use those thresholds.
3. **Sanity check:** Green should capture ~20-30% of cells, not 5% (too strict) or 60% (too loose).

### Excel Conditional Formatting Formula
Set up three rules on your index cells (apply in this order):
```excel
// Green (apply first so it takes priority on ties)
=B2>=115

// Yellow
=AND(B2>=105, B2<115)

// Red
=B2<105
```

### Paste-Ready RYG with XLOOKUP (Params Sheet Approach)
If you want thresholds in a separate `Params` sheet so they're easy to change:

**Params sheet (e.g., A1:C2):**
| Metric | Yellow_Floor | Green_Floor |
|---|---|---|
| Default | 105 | 115 |

**Index sheet formula (returns "R", "Y", or "G"):**
```excel
=IF(B2>=INDEX(Params!C:C,MATCH("Default",Params!A:A,0)),"G",
 IF(B2>=INDEX(Params!B:B,MATCH("Default",Params!A:A,0)),"Y","R"))
```

---

## 8. Z-Score Normalization (0-100)

Use when you need to compare metrics on different scales (e.g., WTP in decimals vs. LEC as an index). Converts everything to a common 0-100 scale.

### When to Use
- Scoring / ranking growth drivers across multiple dimensions
- Building composite "compatibility" or "attractiveness" scores
- Any time raw units differ and you need apples-to-apples

### Step 1: Standardize (Z-Score)
For each metric column, across all rows (e.g., all growth drivers):
```
z = (raw value - column mean) / column stdev
```

### Step 2: Convert to 0-100
```
Score = NORM.S.DIST(z, TRUE) × 100
```
Round to whole numbers.

### Step 3: Combine with Weights (if needed)
```
Overall = w1×Score1 + w2×Score2 + ... + wn×ScoreN
```

### Excel (Single Cell, Paste-Ready)
If raw values for one metric are in `B2:B15`, score for row 2:
```excel
=ROUND(NORM.S.DIST((B2-AVERAGE($B$2:$B$15))/STDEV.S($B$2:$B$15),TRUE)*100,0)
```
Drag down. Repeat for each metric column (change column letter).

### Weighted Overall (example: WTP at 2× weight)
```excel
=Importance + (2*WTP) + LEC + UserCreation + UsageCreation
```

### Interpretation Guide (for slides)
- **~50** = average among this set of drivers
- **~84** = roughly top 15%
- **~16** = roughly bottom 15%
- **95-100** = standout high
- **0-5** = standout low

### Slide-Ready Language
"Each 0-100 score reflects where the growth driver ranks on that metric relative to the full set, after standardizing. 50 is about average."

---

## 9. Data Labels for PowerPoint Charts

### Standard Format
```
(Incidence%, Index#)
```

**Example:** `(32%, 115)`

Nothing outside the parentheses. No extra text, no "Inc:" prefix.

### How to Set Up in PowerPoint
1. Right-click chart → **Edit Data** (opens embedded Excel)
2. Create a helper column that builds the label string:
```excel
=CONCATENATE("(", TEXT(B2,"0%"), ", ", TEXT(C2,"0"), ")")
```
3. In PowerPoint chart → right-click data series → **Add Data Labels**
4. Right-click labels → **Format Data Labels** → check **"Value From Cells"** → select your helper column
5. Uncheck "Value" so only the custom label shows

### Automating Across Many Series
If you have multiple segments, build one helper column per segment using the same CONCATENATE pattern. Saves you from manually typing every label.

---

## 10. Survey Quota & Fielding Math

### Target Completes with Slippage
```
Invites Needed = Target Completes / (Incidence Rate × Completion Rate)
```

**Example:** Need 300 completes, 40% IR, 80% completion rate:
```
Invites = 300 / (0.40 × 0.80) = 938
```

### Over-Recruit Buffer
Standard practice: over-recruit by 10-15% to account for bot removal and quality cleaning.
```
Adjusted Target = Target Completes × 1.10 to 1.15
```

### Quota Fill Tracking
At soft launch (typically 10-20% of target), check:
- Are quotas filling proportionally?
- Any cell dramatically over/under?
- Median completion time reasonable? (flag if <1/3 of expected or >3× expected)

### Bot / AI Detection in Open-Ends
Check at 20% fill. Flags:
- Responses that are unusually long and well-structured for the question type
- Copy-paste patterns across respondents
- Generic language that doesn't reference the specific category/brand

---

## 11. Rounding Rules

| What | Precision | Example |
|---|---|---|
| Percentages | 1 decimal | 23.4% |
| Indices | Whole number | 115 |
| Share changes | 1 decimal + "pp" | +2.3pp |
| CAGR | 1 decimal | 4.2% |
| Dollar values | Match source | $1.2B or $1,234M |
| Base sizes | Whole number | n=312 |

**When quoting external data:** Match the source's precision exactly. Don't add false precision.

---

## 12. Base Size Rules

### Minimum Reliable Base: n ≥ 30

| Base Size | Rule |
|---|---|
| **n ≥ 100** | Report normally |
| **n = 30-99** | Report with caution footnote: "small base, interpret directionally" |
| **n < 30** | Flag prominently. Do NOT report percentages as reliable. Use counts only or suppress. |

### How to Flag in Deliverables
- Add asterisk (*) next to any metric based on n<100
- Add double asterisk (**) or suppress for n<30
- Include footnote: "*Caution: small base size (n=XX); interpret directionally"

### Excel Formula to Auto-Flag
```excel
=IF(BaseCell<30, "**SUPPRESS**", IF(BaseCell<100, "*small base", ""))
```

---

## 13. QC Checklist (Run Every Time)

Before sending any quant output, walk through this:

**The Numbers**
- [ ] Do shares sum to 98-102%? (rounding tolerance)
- [ ] Are indices calculated vs. the correct benchmark? (stated clearly)
- [ ] Are growth rates directionally consistent with raw numbers?
- [ ] Are base sizes ≥ 30 for all reported metrics? (flagged if not)
- [ ] Are units consistent? ($ vs. units, calendar vs. fiscal year, etc.)

**The Labels**
- [ ] Is the base definition stated? ("% of total category buyers" not just "%")
- [ ] Are data labels in the right format? `(Incidence%, Index#)`
- [ ] Are footnotes included for small bases?

**The Formulas**
- [ ] Spot-check 2-3 cells by hand (calculator or mental math)
- [ ] Are combined bases using counts, not averaged percentages?
- [ ] Is the denominator correct? (common error: wrong "total" row)

**The Deliverable**
- [ ] Does the RYG coloring match the threshold convention in this deck?
- [ ] Are external data points cited with source + date?
- [ ] Would a partner/VP reading this for the first time understand what the number means?

---

## 14. Common Pitfalls

### 1. Averaging Indices
**Wrong:** Average two indices (e.g., `(110 + 110) / 2 = 110`)
**Right:** Go back to counts, sum them, recalculate the % and index from scratch.
**Why:** Indices from different bases get distorted when averaged.

### 2. Wrong Denominator
Most common error in consulting quant. Always verify:
- What is the "total" in your index? (Total respondents? Total category? Total segment?)
- Did you accidentally use a sub-segment total instead of the full total?

### 3. Confusing % Change vs. pp Change
- **3 percentage points (pp):** went from 12% to 15%
- **3% growth:** went from 12% to 12.36%
These are very different. Always use "pp" for share changes.

### 4. Reporting on Tiny Bases
n=15 does not support "42% of consumers prefer X." It supports "a handful of respondents indicated a preference." Flag and suppress.

### 5. False Precision
Don't report 23.456% when your source says 23%. Don't add decimals that don't exist in the data.

### 6. Over-Indexing ≠ Large
An index of 150 on a base of 2% means the segment is 3% — still tiny in absolute terms. Always pair index with absolute size for context.

### 7. RYG on Wrong Scale
Make sure your RYG thresholds match the type of metric:
- **Indices (around 100):** Use 105/115 or 110/120 thresholds
- **Percentages (0-100%):** Use different thresholds (e.g., 50%/70%)
- **Z-scores (0-100):** Use 40/60 or similar

Don't accidentally apply index thresholds to a percentage column.
