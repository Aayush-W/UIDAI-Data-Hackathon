# 🌍 Geographic Heatmaps – UIDAI Lifecycle Risk Analysis

This repository contains **district-level geographic heatmaps of India** that visualize Aadhaar enrolment lifecycle risks, infrastructure stress, and intervention priorities.

These dashboards form the **strategic intelligence layer** for detecting systemic failure zones, identifying root causes, and enabling data-driven policy interventions.

---

## 📁 Repository Contents

### 🔴 `future_risk_score.jpeg`

**Future Risk Score Heatmap**
🔗 [https://public.tableau.com/app/profile/aayush.w8472/viz/UIDAIDashboard/FutureRiskScore?publish=yes](https://public.tableau.com/app/profile/aayush.w8472/viz/UIDAIDashboard/FutureRiskScore?publish=yes)

* District-wise **composite future enrolment risk**
* Higher intensity = higher probability of future exclusion or system collapse
* Derived from lifecycle imbalance, biometric failure, saturation stress, maintenance overload, and trend collapse

**Use Case:** Early-warning system & geographic prioritization

---

### 🚨 `intervention_priority.jpeg`

**Intervention Priority Heatmap**
🔗 [https://public.tableau.com/app/profile/aayush.w8472/viz/UIDAIDashboard/InterventionPriority?publish=yes](https://public.tableau.com/app/profile/aayush.w8472/viz/UIDAIDashboard/InterventionPriority?publish=yes)

* Categorizes districts into:

  * Immediate Intervention
  * Monitor Closely
  * Routine Monitoring
* Converts analytics into **field-ready decision signals**

**Use Case:** Resource deployment & corrective action planning

---

### ⚠️ `lifecycle_risk_level.jpeg`

**Lifecycle Risk Level Heatmap**
🔗 [https://public.tableau.com/app/profile/aayush.w8472/viz/UIDAIDashboard/LifecycleRiskLevel?publish=yes](https://public.tableau.com/app/profile/aayush.w8472/viz/UIDAIDashboard/LifecycleRiskLevel?publish=yes)

* Executive categories:

  * Healthy
  * Watchlist
  * Critical
* Separates *slow systems* from *structurally broken systems*

**Use Case:** Leadership review & governance reporting

---

### 🧩 `primary_failure_domain.jpeg`

**Primary Failure Domain Heatmap**
🔗 [https://public.tableau.com/app/profile/aayush.w8472/viz/UIDAIDashboard/PrimaryFailureDomain?publish=yes](https://public.tableau.com/app/profile/aayush.w8472/viz/UIDAIDashboard/PrimaryFailureDomain?publish=yes)

* Dominant root cause per district:

  * Late Enrolment
  * Silent Exclusion
  * Biometric Stress
  * Saturation Stress
  * Growth Collapse
  * **Black Hole Friction** – instant backend rejection
  * **Maintenance Debt Collapse** – update traffic choking infrastructure

**Use Case:** Precision policy & infrastructure correction

---

## 🧨 Emerging System Failure Patterns

| Failure Class                 | Meaning                                                                                 | Example Regions            |
| ----------------------------- | --------------------------------------------------------------------------------------- | -------------------------- |
| **Black Hole Friction**       | Near-zero processing delay but extremely high rejection — system rejects at entry point | Delhi (Child Aadhaar)      |
| **Maintenance Debt Collapse** | Update volume overwhelms shared infrastructure, blocking enrollments & authentication   | Maharashtra – Nanded, Beed |

These failures indicate **protocol & architecture breakdowns**, not manpower shortages.

---

## 🧮 Core Metrics Used

| Metric                                      | Formula                                    | Insight                                           |
| ------------------------------------------- | ------------------------------------------ | ------------------------------------------------- |
| **Friction Intensity Score (FIS)**          | Composite backend failure score            | Detects districts where system is fighting itself |
| **Lifecycle Delay Index (LDI)**             | Avg processing time                        | Differentiates backlog from fast-failure          |
| **Efficiency Ratio (ER)**                   | Enrollments ÷ Friction                     | Measures operational productivity                 |
| **Maintenance Ratio (MR)**                  | (Demo Updates + Bio Updates) ÷ Enrollments | Quantifies infrastructure overload                |
| **Black Hole Index (BHI)**                  | High FIS + Near-Zero LDI                   | Flags silent mass-rejection zones                 |
| **Rural Bandwidth Stress Indicator (RBSI)** | District FIS ÷ Update Volume               | Identifies low-capacity rural collapse risk       |

---

## 🎯 Project Objective

To transform Aadhaar monitoring from **descriptive reporting** into a **diagnostic control system** that answers:

* Where is the system failing?
* Why is it failing?
* What intervention will actually fix it?

---

## 🧠 Design Principles

* District-level granularity
* Red–Amber–Green executive logic
* Root-cause driven analytics
* Built strictly on UIDAI-provided datasets
* No individual-level or sensitive data used

---
