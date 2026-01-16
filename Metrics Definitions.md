# Metric Definitions  
UIDAI Aadhaar Lifecycle Risk Analytics Platform

This document provides **complete definitions for all metrics** used across datasets, dashboards, geographic heatmaps, and risk scoring frameworks in this project.

All metrics are:
- Derived strictly from UIDAI-provided data
- Aggregated at district/state level
- Explainable and policy-aligned
- Free from individual-level identifiers

---

# I. CORE ENROLMENT METRICS

---

## 1. Total Enrolments

### Definition  
Total number of Aadhaar enrolments recorded for a given district/state within a specific time period.

### Purpose  
Acts as the base activity measure for all downstream analysis.

---

## 2. Monthly Enrolment Volume

### Definition  
Total enrolments aggregated at **district × month** level.

### Purpose  
Enables trend analysis, growth computation, and volatility detection.

---

## 3. Growth Rate (Month-on-Month)

### Definition  
Percentage change in enrolments between consecutive months.

### Interpretation  
- Positive → growth or expansion
- Negative → decline or disengagement

### Purpose  
Identifies momentum loss, stagnation, or sudden drops in enrolment activity.

---

## 4. Enrolment Volatility Score

### Definition  
Statistical variation in monthly enrolment volumes over time.

### Interpretation  
- Low volatility → persistent stagnation
- High volatility → instability or event-driven spikes

### Purpose  
Detects structurally stagnant districts versus unstable ones.

---

# II. AGE-BASED LIFECYCLE METRICS

---

## 5. Child Enrolment Share (Age 0–5)

### Definition  
Proportion of enrolments belonging to children aged 0–5.

### Interpretation  
- High → healthy early enrolment
- Low → delayed onboarding risk

---

## 6. Youth Enrolment Share (Age 5–17)

### Definition  
Proportion of enrolments from school-age population.

### Purpose  
Signals school-linked enrolment coverage and continuity.

---

## 7. Adult Enrolment Share (Age 18+)

### Definition  
Proportion of enrolments from adult population.

### Interpretation  
- High share → delayed enrolment or migration-driven enrolment

---

## 8. Late Enrolment Ratio

### Definition  
Ratio of adult enrolments (18+) to total enrolments.

### Purpose  
Used as a direct proxy for **delayed Aadhaar onboarding**.

---

# III. LIFECYCLE HEALTH & BALANCE METRICS

---

## 9. ALHS — Aadhaar Lifecycle Health Score

### Definition  
Composite score measuring how balanced the enrolment lifecycle is across age groups.

### Interpretation  
- High ALHS → timely, healthy enrolment lifecycle
- Low ALHS → delayed, skewed lifecycle

### Policy Relevance  
Early enrolment is critical for uninterrupted access to welfare and services.

---

## 10. Early Warning Youth Instability Indicator

### Definition  
Detects irregular or declining youth enrolment patterns over time.

### Purpose  
Signals risk of **future adult-heavy enrolment cycles**.

---

# IV. BIOMETRIC & OPERATIONAL METRICS

---

## 11. BCI — Biometric Coverage Index

### Definition  
Measures completeness and consistency of biometric enrolment relative to total enrolments.

### Interpretation  
- High BCI → strong biometric compliance
- Low BCI → biometric access or quality issues

---

## 12. Biometric Flag Indicator

### Definition  
Binary/label-based signal indicating biometric stress or anomalies.

### Purpose  
Highlights districts requiring biometric infrastructure or operational review.

---

# V. SATURATION & ACCESS METRICS

---

## 13. DSI — Demographic Saturation Index

### Definition  
Measures whether enrolment activity is proportionate to district/state context.

### Interpretation  
- DSI ≈ 1 → balanced
- DSI > 1 → over-saturation
- DSI < 1 → under-coverage

---

## 14. Saturation Index

### Definition  
Normalized measure of enrolment concentration relative to peers.

### Purpose  
Detects congestion vs under-utilisation of enrolment infrastructure.

---

## 15. Administrative Friction Hotspots

### Definition  
Districts exhibiting sustained enrolment inefficiencies despite demand signals.

### Purpose  
Highlights governance and access bottlenecks.

---

# VI. MIGRATION & DEMOGRAPHIC SIGNALS

---

## 16. Migration Hotspot Indicator

### Definition  
Identifies districts with abnormal adult enrolment surges linked to migration.

---

## 17. Seasonal Migration Signal

### Definition  
Detects cyclical enrolment spikes aligned with seasonal labour movement.

---

## 18. Persistent Friction Districts

### Definition  
Districts consistently underperforming across multiple time periods.

---

# VII. SILENT EXCLUSION & STRUCTURAL RISK METRICS

---

## 19. Silent Exclusion Risk Indicator

### Definition  
Composite signal capturing districts with:
- Low enrolment volume
- Low volatility
- Low child participation

### Purpose  
Detects exclusion without visible decline.

---

## 20. Administrative Friction Index

### Definition  
Measures enrolment inefficiency arising from systemic or governance constraints.

---

# VIII. COMPOSITE RISK & INTERVENTION METRICS

---

## 21. Future_Risk_Score

### Definition  
A composite, forward-looking score estimating probability of future enrolment stress or exclusion.

### Inputs Used
- ALHS
- BCI
- DSI
- Growth & volatility signals
- Structural risk flags

### Interpretation  
Higher score → higher future risk.

---

## 22. Lifecycle_Risk_Level

### Definition  
Categorical representation of the Future Risk Score.

### Levels
- Healthy
- Watchlist
- Critical

---

## 23. Intervention Priority

### Definition  
Operational classification translating risk into action urgency.

### Levels
- Immediate Intervention
- Monitor Closely
- Routine Monitoring

---

## 24. Primary Failure Domain

### Definition  
Identifies the dominant root cause contributing to district risk.

### Possible Domains
- Late Enrolment Dominance
- Silent Exclusion
- Biometric Coverage Failure
- Saturation Stress
- Growth Collapse
- Administrative Friction

---

# IX. DESIGN & GOVERNANCE PRINCIPLES

- No black-box machine learning
- Explainable, auditable logic
- District-first governance perspective
- Designed for proactive intervention
- Ethical, aggregated analysis only

---

End of Metric Definitions

