# Risk Scoring Framework  
UIDAI Aadhaar Lifecycle Risk Analytics

This document explains how district-level enrolment risks are quantified using a transparent and explainable scoring framework.

---

## Objective

To provide a **forward-looking early warning system** that identifies districts likely to experience enrolment stress, exclusion, or operational failure.

---

## Components Used

The Future Risk Score integrates multiple dimensions:

- Aadhaar Lifecycle Health Score (ALHS)
- Biometric Coverage Index (BCI)
- Demographic Saturation Index (DSI)
- Growth and volatility signals
- Structural exclusion indicators

Each component captures a different failure mode.

---

## Aggregation Logic

Conceptually, the score follows:

Future Risk Score =
- Lifecycle imbalance contribution  
- Biometric weakness contribution  
- Saturation deviation contribution  
- Trend instability contribution  
- Structural risk flags  

Higher values indicate higher risk.

---

## Weighting Philosophy

- Lifecycle imbalance has long-term impact
- Biometric gaps directly affect authentication
- Saturation reflects service accessibility
- Trends capture emerging risks

Weights are balanced to avoid dominance of any single metric.

---

## Risk Classification

Based on score thresholds, districts are classified as:

- **Healthy** – Stable enrolment ecosystem
- **Watchlist** – Early warning signals present
- **Critical** – High likelihood of exclusion or failure

---

## Primary Failure Domain Identification

The dominant contributor to the risk score is identified as the **Primary Failure Domain**, enabling targeted interventions rather than generic responses.

---

## Governance Alignment

This framework is:
- Explainable
- Auditable
- Scalable nationwide
- Suitable for operational and policy use

No black-box logic is used.

---

## Intended Use

- District prioritization
- Resource allocation
- Preventive planning
- Early-warning dashboards

---

End of Risk Scoring Framework

