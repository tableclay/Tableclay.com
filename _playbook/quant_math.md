# Quant Math Rules

## Every Calculation Must Include
1. **Base definition**: what the denominator is (e.g., "% of total category volume," "% of respondents who purchased in P12M")
2. **Formula**: written out briefly (e.g., `Brand A volume / Total category volume`)
3. **QC / sanity check**: does the number pass a gut check? Compare to known benchmarks or adjacent data points

## Index Calculations
- Index = (Value / Benchmark) x 100
- Index 100 = at parity; >100 = over-indexes; <100 = under-indexes
- Always state the benchmark clearly

## Share Calculations
- Share = Part / Whole x 100
- Shares within a group must sum to 100% (flag if they don't within rounding)
- When showing share change: use "pp" (percentage points), not "%"

## Growth / CAGR
- YoY growth = (Current - Prior) / Prior x 100
- CAGR = (End / Start)^(1/n) - 1
- Always state the time period

## Rounding
- Default: 1 decimal place for percentages
- Whole numbers for indices
- Match the source's precision when quoting external data

## Common QC Checks
- Do shares sum to ~100%?
- Is the growth rate directionally consistent with the raw numbers?
- Does the base size support the precision shown? (small bases = wide error bars)
- Are units consistent ($ vs. units, calendar year vs. fiscal year)?
