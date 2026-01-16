# Methodology  
UIDAI Aadhaar Lifecycle Risk Analytics

This document outlines the end-to-end analytical methodology used to convert Aadhaar enrolment data into dashboards, risk scores, and geographic intelligence.

---

## 1. Data Sources

All analysis is based strictly on **UIDAI-provided datasets**, including:
- Enrolment data
- Demographic data
- Biometric data

No external datasets or personal identifiers were used.

---

## 2. Data Preparation

Key preparation steps:
- Standardisation of state and district names
- Aggregation at **district × month** level
- Segmentation by age groups
- Validation of temporal consistency

This ensured comparability across datasets.

---

## 3. Feature Engineering

Advanced indicators were derived to capture non-obvious risks:
- Lifecycle imbalance metrics
- Growth decline and stagnation signals
- Saturation and concentration indicators
- Silent exclusion proxies

This moved the analysis beyond descriptive statistics.

---

## 4. Metric Construction

Core metrics (ALHS, BCI, DSI) were constructed using:
- Proportional relationships
- State-level normalization
- Temporal trend checks

All metrics were designed to be interpretable and reproducible.

---

## 5. Risk Modelling Approach

A **rule-based composite risk framework** was used instead of black-box machine learning to ensure:
- Transparency
- Auditability
- Policy trust

This aligns with public-sector decision-making standards.

---

## 6. Visualization Strategy

Different tools were used based on analytical purpose:
- **Power BI** – Operational and diagnostic dashboards
- **Tableau** – Geographic and spatial storytelling
- **Static Heatmaps** – Executive-level summaries

---

## 7. Insight Validation

Insights were validated using:
- Cross-metric consistency
- Temporal persistence checks
- Geographic clustering patterns

Only structurally consistent patterns were surfaced.

---

## 8. Limitations

- Population baselines are inferred indirectly
- District name resolution limits map granularity
- Risk scores indicate probability, not certainty

---

## 9. Ethical Considerations

- No individual-level analysis
- Only aggregated trends used
- Designed for inclusion and governance support

---

End of Methodology

