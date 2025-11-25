# https://claude.ai/public/artifacts/aa7b525a-efc4-455f-b656-43e50a7b6cc9

import io
import zipfile
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# The markdown content (same as before)
markdown_content = """# VCF Research — Formula Analysis & Evaluation
## All Proposed Metrics for Vector Configuration Framework

**Document Purpose:** Comprehensive analysis of all mathematical formulas and normalization techniques proposed for the VCF project, including rationale, pros/cons, and measurement descriptions.

**Date:** November 22, 2024  
**Version:** 1.0 - Full Project Scope

---

## Overview

The VCF system aims to capture multi-dimensional financial market relationships through geometric/harmonic analysis. To do this effectively, we need inputs that are:
- **Stationary** (bounded, don't drift over time)
- **Comparable** (similar scales across different data types)
- **Harmonically balanced** (no single type of input dominates)
- **Information-rich** (capture both position and momentum)

This document evaluates all formulas proposed for transforming raw financial data into normalized vector components.

---

## Part 1: Position/Oscillation Metrics

These metrics capture **where** a data series is relative to its own historical context.

### 1.1 Moving Average Ratio (MA Ratio)

**Formula:**
```
MA_Ratio = MA_Short / MA_Long
Example: MA_50 / MA_200
```

**What It Measures:**
The moving average ratio compares a shorter-term average to a longer-term average, creating a bounded oscillator around 1.0. When the ratio is above 1.0, the short-term trend is stronger than the long-term trend (bullish positioning). When below 1.0, the short-term is weaker (bearish positioning). This is essentially asking: "Is the recent trend moving faster or slower than the established trend?"

This metric naturally captures mean reversion behavior — when markets get too far from their long-term average, the ratio becomes extreme, and typically prices eventually revert back. It's a positioning indicator that tells you whether you're in the upper or lower part of a trend cycle.

**Pros:**
- ✅ Naturally stationary (oscillates around 1.0)
- ✅ Easy to interpret (>1.0 = uptrend, <1.0 = downtrend)
- ✅ Works across all asset types (stocks, bonds, commodities, currencies)
- ✅ Bounded range makes normalization straightforward
- ✅ Mean-reversion signal built in
- ✅ Removes absolute price levels (works for $50 stocks and $5000 stocks equally)

**Cons:**
- ❌ Lagging indicator (uses historical averages)
- ❌ Can stay elevated/depressed for extended periods during strong trends
- ❌ Doesn't capture magnitude of trend (just direction relative to history)
- ❌ Slow to recognize regime changes
- ❌ Loses information about absolute momentum/power

**Use Case:** Primary positioning metric for all market data sources

---

### 1.2 Z-Score (Rolling Window)

**Formula:**
```
Z = (Current_Value - Rolling_Mean) / Rolling_StdDev
Example: (Price - Mean_100d) / StdDev_100d
```

**What It Measures:**
Z-score answers the question: "How unusual is the current value compared to recent history?" It measures the number of standard deviations away from the average. A Z-score of +2.0 means the current value is 2 standard deviations above normal — this happens only about 2.5% of the time in a normal distribution, so it's statistically unusual.

This metric is particularly good at identifying extremes and potential reversals. When a market reaches a Z-score of +3 or -3, it's in the tail of the distribution — these are the moments when "overbought" or "oversold" conditions are most likely to snap back. Unlike the MA ratio which just says "above trend," the Z-score says "above trend by THIS much relative to normal volatility."

**Pros:**
- ✅ Statistically rigorous (based on standard deviation)
- ✅ Self-adjusting to volatility (high volatility periods don't distort the reading)
- ✅ Clear extreme thresholds (|Z| > 2 or 3 indicates unusual conditions)
- ✅ Works well for oscillating data (yields, volatility indices)
- ✅ Can detect regime changes (when volatility itself changes)

**Cons:**
- ❌ Assumes normal distribution (markets have fat tails — extreme events more common than Z-score suggests)
- ❌ Sensitive to window length (100-day vs 200-day gives different results)
- ❌ Can produce very large values during extreme events (unbounded in theory)
- ❌ Requires sufficient history to calculate meaningful statistics
- ❌ Not intuitive for non-technical users

**Use Case:** Alternative positioning metric, especially for volatility and yields

---

### 1.3 Percentile Rank (Rolling Window)

**Formula:**
```
Percentile = (Count of values below current) / (Total count in window)
Range: 0.0 to 1.0
```

**What It Measures:**
Percentile rank asks: "What percentage of recent history was lower than right now?" If the S&P 500 is at the 90th percentile, it means current prices are higher than 90% of the prices in the lookback window. This is purely ordinal ranking — it doesn't care about the magnitude of moves, only the relative position.

This is excellent for comparing completely different asset classes because everything gets ranked on the same 0-1 scale regardless of units (dollars, percentages, index points). A 90th percentile reading means "near the top of recent range" whether you're measuring stock prices, interest rates, or volatility.

**Pros:**
- ✅ Always bounded 0-1 (perfect for normalization)
- ✅ No distribution assumptions (works with any data shape)
- ✅ Handles outliers gracefully (extreme values don't distort the scale)
- ✅ Directly comparable across completely different assets
- ✅ Intuitive interpretation (percentile = "how high is this compared to recent history")

**Cons:**
- ❌ Loses magnitude information (90th percentile could be 1% above median or 100% above)
- ❌ Requires sufficient data points (minimum ~100 for meaningful percentiles)
- ❌ Step function behavior (small price change can cause percentile jumps)
- ❌ Window dependency (results change dramatically with different lookback periods)

**Use Case:** Alternative for comparing disparate asset classes in same vector space

---

### 1.4 Deviation from Moving Average (Normalized)

**Formula:**
```
Deviation = (Price - MA) / MA
Range: Typically -0.5 to +0.5 (−50% to +50%)
```

**What It Measures:**
This measures the percentage distance between current price and its moving average. If the S&P 500 is at 5,000 and the 200-day MA is 4,500, the deviation is +11%. This tells you how "stretched" the market is from its established trend line.

Think of the moving average as a rubber band center point — this metric measures how far you've stretched the rubber band. When deviation gets extreme (say +20% or -20%), the rubber band is very stretched and likely to snap back toward the center. Unlike the MA ratio which divides two moving averages, this compares current price directly to the trend.

**Pros:**
- ✅ Shows magnitude of divergence from trend
- ✅ Mean reversion signal (extreme values tend to revert)
- ✅ Works for both trending and ranging markets
- ✅ Percentage-based (comparable across different price levels)
- ✅ Simple calculation and interpretation

**Cons:**
- ❌ Not truly bounded (can exceed ±50% in extreme markets)
- ❌ Still somewhat lagging (uses historical MA)
- ❌ Normalization range must be chosen carefully
- ❌ Less effective in strong trending markets (can stay extended for long periods)

**Use Case:** Supplementary metric for mean reversion analysis

---

## Part 2: Momentum/Trend Strength Metrics

These metrics capture **how fast** and **in what direction** a data series is moving.

### 2.1 Rate of Change (ROC)

**Formula:**
```
ROC = (Price_Today - Price_N_Days_Ago) / Price_N_Days_Ago
Example: (Price - Price_90d_ago) / Price_90d_ago
Range: Normalize to -1.0 to +1.0
```

**What It Measures:**
Rate of change is simply: "What percentage has the price moved over the last N days?" If the S&P 500 was at 5,000 ninety days ago and is now at 5,500, the 90-day ROC is +10%. This is pure momentum — it doesn't care about trend lines or averages, just raw directional movement.

The key insight is that this metric is **symmetric around zero**. A +10% move and a -10% move have equal magnitude in opposite directions. This makes it perfect for harmonic analysis because it doesn't have an inherent bullish bias the way "days above moving average" would. Strong positive momentum and strong negative momentum are treated as equally "strong" just in different directions.

**Pros:**
- ✅ Symmetric around zero (no directional bias)
- ✅ Clear momentum signal (positive = uptrend, negative = downtrend)
- ✅ Captures trend strength directly
- ✅ Simple percentage-based calculation
- ✅ Naturally oscillates (momentum reverses, doesn't drift forever)
- ✅ Can detect momentum shifts early

**Cons:**
- ❌ Sensitive to window length (30-day vs 90-day vs 180-day gives very different signals)
- ❌ Susceptible to sharp one-day moves (a single outlier day can distort reading)
- ❌ Doesn't account for path (volatile up/down vs smooth trend both show same ROC)
- ❌ Can produce very large values during crashes (may need clamping)

**Use Case:** Primary momentum metric for capturing trend strength

---

### 2.2 Moving Average Slope

**Formula:**
```
Slope = (MA_Today - MA_N_Days_Ago) / MA_N_Days_Ago
Example: (MA_200_today - MA_200_30d_ago) / MA_200_30d_ago
```

**What It Measures:**
This asks: "Is the long-term trend itself rising or falling?" Instead of comparing price to the moving average, you're looking at whether the moving average itself is trending up or down. If the 200-day moving average was at 4,500 a month ago and is now at 4,600, the MA slope is positive — the underlying trend is strengthening.

This is smoother than raw rate-of-change because the moving average filters out short-term noise. It tells you about trend quality — a rising 200-day MA with price above it is a high-quality uptrend. A falling 200-day MA with price below it is a confirmed downtrend. This metric captures the momentum of the trend itself, not just the momentum of price.

**Pros:**
- ✅ Smoothed momentum signal (less noise than raw ROC)
- ✅ Captures trend quality/persistence
- ✅ Identifies regime changes (when long-term trend shifts direction)
- ✅ Less affected by short-term volatility
- ✅ Symmetric around zero

**Cons:**
- ❌ Very lagging (slow to respond to changes)
- ❌ Can miss important short-term momentum shifts
- ❌ Requires sufficient time for MA to change meaningfully
- ❌ Somewhat redundant with MA ratio (both measure MA relationships)

**Use Case:** Secondary momentum metric for trend quality assessment

---

### 2.3 Momentum Acceleration

**Formula:**
```
Acceleration = ROC_Today - ROC_N_Days_Ago
Example: ROC_30d_today - ROC_30d_30days_ago
```

**What It Measures:**
Acceleration measures "momentum of momentum" — is the rate of price change itself accelerating or decelerating? If the 30-day ROC was +5% a month ago and is now +10%, momentum is accelerating (positive acceleration). If ROC was +10% and is now +5%, momentum is decelerating even though price is still rising (negative acceleration).

This is critical for identifying trend exhaustion. In late-stage bull markets, prices might still be rising but at a slower and slower rate — that's negative acceleration, a warning sign. Conversely, when a market bottoms, prices might still be falling but the rate of decline slows (negative ROC becoming less negative) — that's positive acceleration signaling a potential reversal.

**Pros:**
- ✅ Early warning of momentum shifts (leading indicator)
- ✅ Detects trend exhaustion before reversals
- ✅ Captures market "energy" changes
- ✅ Symmetric (positive/negative acceleration equally meaningful)
- ✅ Works well for identifying regime transitions

**Cons:**
- ❌ Noisy signal (second derivative amplifies volatility)
- ❌ Difficult to interpret (acceleration is less intuitive than momentum)
- ❌ Requires smoothing or filtering to be useful
- ❌ Can produce false signals in choppy markets
- ❌ Complex calculation (derivative of derivative)

**Use Case:** Advanced metric for detecting momentum inflection points

---

### 2.4 Price Distance from MA (Velocity)

**Formula:**
```
Velocity = (Price - MA) / MA_StdDev
Range: Typically -3 to +3 (number of standard deviations)
```

**What It Measures:**
This combines position and momentum: "How far is price from its moving average, measured in units of typical volatility?" If the S&P 500 is currently 5% above its 200-day MA, but typical deviation is only 2%, then velocity is +2.5 (it's 2.5x more extended than normal). This is like Z-score but specifically measuring distance from the trend line rather than distance from mean.

The insight here is that it accounts for volatility regimes. A 10% deviation in a low-volatility environment (2020) is extreme, but a 10% deviation in a high-volatility environment (2022) might be normal. By dividing by standard deviation, you get an apples-to-apples comparison across different volatility regimes.

**Pros:**
- ✅ Volatility-adjusted (accounts for changing market conditions)
- ✅ Combines position and momentum information
- ✅ Natural bounds (rarely exceeds ±3)
- ✅ Statistically meaningful thresholds
- ✅ Mean reversion signal built in

**Cons:**
- ❌ More complex calculation (requires rolling standard deviation)
- ❌ Lagging (uses historical MA and volatility)
- ❌ Can be distorted during volatility regime changes
- ❌ Assumes relationship between price and MA is stable

**Use Case:** Volatility-adjusted momentum metric

---

## Part 3: Normalization Techniques

These are methods for scaling different metrics to comparable ranges.

### 3.1 Min-Max Normalization (0 to 1)

**Formula:**
```
Normalized = (Value - Min) / (Max - Min)
Result: 0.0 to 1.0 range
```

**What It Measures:**
Min-max normalization asks: "Where does this value fall between the historical minimum and maximum?" A normalized value of 0.75 means you're 75% of the way from the historical low to the historical high. This is pure relative positioning — it takes any data series and squashes it into a 0-1 range.

The challenge with growing data (like stock prices that trend up over decades) is that the "maximum" keeps changing. If you normalize the S&P 500 using data from 1950-2024, current prices will always be near 1.0 because they're near the all-time high. This is why min-max works better for oscillating data (yields, ratios) than trending data (prices).

**Pros:**
- ✅ Simple, intuitive calculation
- ✅ Guaranteed output range (always 0-1)
- ✅ Preserves relative relationships in data
- ✅ Works well for oscillating/bounded data
- ✅ Easy to visualize

**Cons:**
- ❌ Sensitive to outliers (one extreme value distorts entire scale)
- ❌ Unstable for trending data (range keeps expanding)
- ❌ Historical normalization becomes invalid as new data arrives
- ❌ Loses information about distribution shape
- ❌ Not suitable for real-time systems with growing data

**Use Case:** Best for stationary, oscillating metrics like MA ratios and percentiles

---

### 3.2 Symmetric Normalization (-1 to +1)

**Formula:**
```
Normalized = 2 * ((Value - Min) / (Max - Min)) - 1
Result: -1.0 to +1.0 range (centered at 0)
```

**What It Measures:**
This is min-max normalization recentered at zero. Instead of 0-1, you get -1 to +1 with zero as the midpoint. This is crucial for momentum metrics because it preserves the **directional meaning** of the data. Positive values mean upward momentum, negative values mean downward momentum, and zero means no momentum.

For harmonic analysis, having metrics centered at zero is important because it means "no signal" is truly neutral. If you normalized momentum to 0-1, a value of 0.5 would be ambiguous — is that neutral momentum or mild positive momentum? With -1 to +1, zero is unambiguously neutral, +0.5 is moderately positive, and -0.5 is moderately negative.

**Pros:**
- ✅ Preserves directional meaning (positive/negative/neutral clear)
- ✅ Zero-centered (true neutral point)
- ✅ Symmetric contribution to vector space
- ✅ Ideal for momentum and rate-of-change metrics
- ✅ Prevents bias in geometric analysis

**Cons:**
- ❌ Slightly more complex than 0-1 normalization
- ❌ Still sensitive to outliers (like all min-max approaches)
- ❌ Requires careful handling of asymmetric data
- ❌ Historical range still an issue for trending data

**Use Case:** Essential for momentum metrics to maintain harmonic balance

---

### 3.3 Rolling Window Normalization

**Formula:**
```
Normalized = (Value - Min_N_Days) / (Max_N_Days - Min_N_Days)
Uses only recent N days for min/max, not all history
```

**What It Measures:**
Instead of using all historical data to find min/max, this uses only the most recent N days (say, 252 days = one trading year). This asks: "Where does the current value fall within the recent range?" This solves the trending data problem — if the S&P 500 has been rising for a year, you're measuring position within the current regime, not position since 1950.

The rolling window makes normalization **adaptive**. As the market moves into a new range, the normalization adjusts to that new range. This keeps normalized values distributed across 0-1 even when the underlying data is trending. However, it also means your normalized values are regime-dependent — a normalized value of 0.8 in 2020 represents different absolute values than a 0.8 in 2024.

**Pros:**
- ✅ Adapts to regime changes (normalization stays relevant)
- ✅ Works for trending data (solves the growth problem)
- ✅ Maintains distribution across full 0-1 range
- ✅ Real-time compatible (doesn't need full history)
- ✅ Captures relative positioning within current market regime

**Cons:**
- ❌ Window length is critical (too short = noisy, too long = lags regime changes)
- ❌ Less comparable across time (0.8 in 2020 ≠ 0.8 in 2024)
- ❌ Can produce discontinuities when old extremes roll out of window
- ❌ Requires sufficient data in window

**Use Case:** Best approach for normalizing trending market data in real-time systems

---

### 3.4 Z-Score Normalization

**Formula:**
```
Normalized = (Value - Mean) / StdDev
Result: Typically -3 to +3 (unbounded in theory)
```

**What It Measures:**
As described in section 1.2, Z-score measures distance from mean in units of standard deviation. For normalization purposes, the key is that it's **statistically meaningful** — you know that 68% of values fall within ±1, 95% within ±2, and 99.7% within ±3. This gives you natural thresholds for "normal" vs "extreme" conditions.

Unlike min-max which guarantees 0-1 output, Z-scores are unbounded in theory but naturally stay in -3 to +3 range for normal data. This is both a feature (extreme events can show values beyond ±3, making them obvious) and a bug (you need to handle outliers carefully in geometric calculations).

**Pros:**
- ✅ Statistically rigorous and meaningful
- ✅ Self-adjusting to volatility (high volatility = larger denominator)
- ✅ Clear thresholds (|Z| > 2 is unusual, |Z| > 3 is extreme)
- ✅ Works for both oscillating and trending data
- ✅ Can use rolling windows for adaptive behavior

**Cons:**
- ❌ Unbounded (extreme events can produce very large values)
- ❌ Assumes normal distribution (markets have fat tails)
- ❌ Requires clamping or clipping for geometric analysis
- ❌ Not intuitive for non-technical users
- ❌ Zero doesn't mean "bottom of range," it means "average"

**Use Case:** Best for identifying statistical extremes; requires clamping for harmonic analysis

---

## Part 4: Hybrid Approaches

### 4.1 Dual-Input Architecture (Recommended)

**Structure:**
```
For each market source, create TWO inputs:
1. Position metric (MA ratio, percentile, etc.) → 0 to 1
2. Momentum metric (ROC, acceleration, etc.) → -1 to +1
```

**What It Measures:**
This is the architecture we've been discussing: capture both WHERE you are (position) and HOW FAST you're moving (momentum). For the S&P 500, you'd have `sp500_position` (MA ratio normalized 0-1) and `sp500_momentum` (90-day ROC normalized -1 to +1). This gives you a 2D representation of each market.

The power of this approach is that you can detect different market regimes: bullish position + positive momentum = strong uptrend; bullish position + negative momentum = losing steam; bearish position + positive momentum = potential reversal forming; bearish position + negative momentum = confirmed downtrend. You need both dimensions to understand the full picture.

**Pros:**
- ✅ Captures both oscillation and trend strength
- ✅ Balanced contribution to harmonic analysis (no momentum dominance)
- ✅ Can detect regime transitions and exhaustion
- ✅ Richer information than single metrics alone
- ✅ Maintains interpretability (each input has clear meaning)

**Cons:**
- ❌ Doubles input dimensionality (4 sources → 8 inputs)
- ❌ Increases computational complexity
- ❌ Requires careful balancing of normalization scales
- ❌ More parameters to tune (window lengths for both position and momentum)

**Use Case:** Recommended primary architecture for VCF system

---

### 4.2 Composite Momentum Score

**Formula:**
```
Composite = w1*ROC_30d + w2*ROC_90d + w3*Acceleration
Weights sum to 1.0
```

**What It Measures:**
Instead of choosing one momentum metric, combine multiple timeframes and types into a weighted average. This might be 40% short-term ROC (30-day), 40% medium-term ROC (90-day), and 20% acceleration. The idea is to capture momentum at multiple scales simultaneously — short-term shifts, medium-term trends, and momentum changes.

This is like taking a committee vote from different momentum indicators. If all three agree (all positive or all negative), you have high confidence. If they disagree (short-term positive but medium-term negative), you're in a transitional phase. The weights let you tune which timeframes matter most for your application.

**Pros:**
- ✅ Multi-scale momentum capture
- ✅ More robust than single-metric momentum
- ✅ Can tune weights based on empirical testing
- ✅ Reduces noise through averaging
- ✅ Single output (simpler than separate momentum inputs)

**Cons:**
- ❌ Loses information about timeframe disagreements
- ❌ Weight selection is somewhat arbitrary
- ❌ Harder to interpret than simple ROC
- ❌ Potentially over-fitting if weights are optimized too aggressively

**Use Case:** Alternative to separate momentum metrics for simpler architecture

---

## Part 5: Recommended Formula Set for VCF

Based on the analysis above, here's the recommended approach for the full VCF system:

### Core Architecture: Dual-Input per Source

**For each of the 4 market sources (S&P 500, 10Y Treasury, VIX, DXY):**

#### Position Input (0 to 1 scale):
- **Primary:** Moving Average Ratio (50-day / 200-day)
- **Normalization:** Rolling window min-max (252-day window)
- **Rationale:** Stationary, intuitive, captures mean reversion

#### Momentum Input (-1 to +1 scale):
- **Primary:** Rate of Change (90-day)
- **Normalization:** Symmetric normalization with ±3 sigma clipping
- **Rationale:** Captures trend strength, symmetric around zero, harmonically balanced

### Total Input Dimensionality: 8 Inputs

1. sp500_position (MA ratio, 0-1)
2. sp500_momentum (90d ROC, -1 to +1)
3. treasury_position (MA ratio, 0-1)
4. treasury_momentum (90d ROC, -1 to +1)
5. vix_position (MA ratio, 0-1)
6. vix_momentum (90d ROC, -1 to +1)
7. dxy_position (MA ratio, 0-1)
8. dxy_momentum (90d ROC, -1 to +1)

### Why This Configuration:

1. **Harmonic Balance:** Position (0-1) and momentum (-1 to +1) have equal geometric weight
2. **Stationarity:** All inputs oscillate, none drift over time
3. **Interpretability:** Each input has clear financial meaning
4. **Completeness:** Captures both state and rate-of-change
5. **Consistency:** Same formula applied to all four market sources
6. **Simplicity:** Only two formula types (MA ratio + ROC), easy to maintain

### Alternative Formulas (When to Use):

- **Z-Score:** If you want more rigorous statistical thresholds for extremes
- **Percentile Rank:** If you need to add non-financial data sources later (easier to compare apples/oranges)
- **Acceleration:** If detecting trend exhaustion becomes critical priority
- **Composite Momentum:** If you want to reduce dimensionality back to 4-6 inputs

---

## Part 6: Special Considerations

### 6.1 Window Length Selection

All rolling metrics require choosing a lookback window. Guidelines:

**Short-term (20-50 days):**
- Pros: Responsive, catches tactical shifts
- Cons: Noisy, more false signals
- Use for: High-frequency trading signals, short-term momentum

**Medium-term (50-100 days):**
- Pros: Balance of responsiveness and stability
- Cons: Can still whipsaw in volatile markets
- Use for: Primary tactical signals, swing trading

**Long-term (150-252 days):**
- Pros: Smooth, fewer false signals, captures major trends
- Cons: Slow to respond, lags regime changes
- Use for: Strategic positioning, trend confirmation

**Recommended for VCF:**
- Position (MA ratio): 50-day / 200-day (industry standard, well-tested)
- Momentum (ROC): 90-day (medium-term, balances response vs stability)
- Normalization windows: 252-day (one year, captures seasonal patterns)

### 6.2 Data Frequency Considerations

**Daily data:**
- Standard for most financial analysis
- Sufficient for tactical and strategic signals
- Recommended for VCF prototype and production

**Intraday data (hourly, minute):**
- Only needed for high-frequency applications
- Adds complexity and data volume
- Not recommended unless required by use case

**Weekly/Monthly data:**
- Too coarse for momentum metrics
- Acceptable for very long-term strategic analysis
- Not recommended for VCF (loses timing precision)

### 6.3 Missing Data / Market Closures

Financial markets have gaps (weekends, holidays). Handling:

- **Forward fill:** Use last valid value (simple, works for most cases)
- **Interpolation:** Estimate missing values (can create artificial smoothness)
- **Skip/ignore:** Leave gaps as-is (safest for statistical integrity)

**Recommended:** Forward fill for short gaps (<5 days), flag longer gaps for manual review

### 6.4 Outlier Handling

Extreme events (crashes, flash crashes) can distort metrics:

**For normalization:**
- Clip values beyond ±3 sigma before normalizing
- Use robust statistics (median, IQR) instead of mean/std if necessary
- Consider separate handling for known events (COVID crash, etc.)

**For momentum metrics:**
- Cap ROC at reasonable bounds (e.g., ±50% for equities)
- Use log returns instead of simple returns for large moves
- Flag but don't remove outliers (they contain real information)

---

## Conclusion

The recommended **dual-input architecture** with MA ratios for position and ROC for momentum provides:

1. **Mathematical rigor:** Stationary, bounded, statistically sound
2. **Financial interpretability:** Clear meaning for each input
3. **Harmonic balance:** Position and momentum contribute equally
4. **Practical feasibility:** Standard calculations, reliable data sources
5. **Extensibility:** Easy to add new market sources or alternative metrics

This foundation supports the geometric/harmonic analysis goals of the VCF system while maintaining clarity and robustness.

**Next steps:**
1. Implement dual-input architecture in prototype
2. Test normalization stability over various market regimes
3. Validate harmonic balance in vector space
4. Iterate based on empirical results

---

**End of Document**"""

# Create DOCX
doc = Document()

# Set document properties
sections = doc.sections
for section in sections:
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

# Title
title = doc.add_heading('VCF Research — Formula Analysis & Evaluation', 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Subtitle
subtitle = doc.add_heading('All Proposed Metrics for Vector Configuration Framework', level=2)
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Document metadata
doc.add_paragraph('Document Purpose: Comprehensive analysis of all mathematical formulas and normalization techniques proposed for the VCF project, including rationale, pros/cons, and measurement descriptions.')
doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('Date: ').bold = True
p.add_run('November 22, 2024')
p = doc.add_paragraph()
p.add_run('Version: ').bold = True
p.add_run('1.0 - Full Project Scope')

doc.add_page_break()

# Overview
doc.add_heading('Overview', level=1)
doc.add_paragraph('The VCF system aims to capture multi-dimensional financial market relationships through geometric/harmonic analysis. To do this effectively, we need inputs that are:')
doc.add_paragraph('Stationary (bounded, don\'t drift over time)', style='List Bullet')
doc.add_paragraph('Comparable (similar scales across different data types)', style='List Bullet')
doc.add_paragraph('Harmonically balanced (no single type of input dominates)', style='List Bullet')
doc.add_paragraph('Information-rich (capture both position and momentum)', style='