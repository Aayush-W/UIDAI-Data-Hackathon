# Aadhaar Lifecycle Risk & Intervention Dashboard
### UIDAI Data Hackathon 2026

A **Lifecycle-Based Early-Warning and Decision Intelligence Framework** for the
Unique Identification Authority of India (UIDAI).



 📌 Project Overview

Aadhaar has evolved from a one-time enrolment exercise into a **long-term national identity system** that must remain accurate, inclusive, and reliable across an individual’s entire lifecycle.

While enrolment has achieved near-universal coverage, **systemic risk now emerges from delayed enrolment, demographic instability, migration-driven updates, and biometric compliance stress**.

This project introduces a **district-level lifecycle risk intelligence framework** that integrates:

- Enrolment behaviour  
- Demographic update dynamics  
- Biometric compliance patterns  

into a **single, decision-ready analytical system**.

The result is an **Early-Warning Risk & Intervention Dashboard** that enables UIDAI to move from **reactive monitoring** to **predictive, preventive governance**.

---

 🎯 Core Problem Addressed

Current UIDAI monitoring practices analyse enrolment, demographic updates, and biometric updates **in silos**.  
This fragmented view prevents early detection of:

- Silent and delayed exclusion  
- Structural administrative failure  
- Predictable biometric overload  

**Key Insight:**  
Failures in Aadhaar are **lifecycle-propagated**. Weaknesses at enrolment compound and re-emerge later as demographic churn and biometric stress.

---

🧠 Conceptual Framework

The Aadhaar system is modelled as a **three-stage lifecycle**:

| Lifecycle Stage | Analytical Focus | Risk Captured |
|----------------|----------------|---------------|
| Enrolment | Timing & completeness | Late onboarding, access gaps |
| Demographic Stability | Identity corrections | Migration stress, admin friction |
| Biometric Compliance | Mandatory updates | Authentication failure, overload |

Risk flows **forward through the lifecycle**, amplifying downstream impact.

---

📊 Datasets Used

All datasets are **UIDAI-provided, aggregated, and privacy-preserving**.

- **Enrolment Data** – Age-wise onboarding patterns  
- **Demographic Update Data** – Identity corrections & migration signals  
- **Biometric Update Data** – Compliance behaviour & infrastructure load  

**Granularity:** District × Month

---

 🧮 Key Metrics & Indices

This project deliberately de-emphasises raw volumes and focuses on **second-order, interaction-driven metrics**.

### Core Advanced Metrics
- **ALHS** – Aadhaar Lifecycle Health Score  
- **ELCD** – Early-Life Capture Deficit  
- **IVC** – Identity Volatility Coefficient  
- **PFD** – Persistent Friction Density  
- **CBCG** – Child Biometric Compliance Gap  
- **CSI** – Catch-Up Shock Indicator  
- **DRM** – Downstream Risk Multiplier  
- **Future Risk Score** – Predictive composite risk indicator  

### Policy Classifications
- **Lifecycle Risk Level**: Healthy / Stable / Stressed / Critical  
- **Primary Failure Domain**: Enrolment / Demographic / Biometric  
- **Intervention Priority**: Routine / Monitor / Immediate  

📘 *Detailed metric definitions, legends, and dashboard tooltips are documented in the project documentation.*

---

🗺️ Dashboard & Outputs

The analytical pipeline produces **district-level, decision-ready outputs** suitable for:

- Heatmaps and spatial risk analysis  
- District ranking tables  
- Early-warning watchlists  
- Intervention prioritisation dashboards  

The system is **auditable, reproducible, and scalable**.

---

## 📂 Repository Structure

UIDAI-Data-Hackathon/
│
├── README.md                      
│
├── Datasets/
│   │
│   ├── Raw Data/
│   │   ├── api_data_aadhar_enrolment.zip
│   │   ├── api_data_aadhar_biometric.zip
│   │   ├── api_data_aadhar_demographic.zip
│   │   ├── data.zip
│   │   └── README.md               
│   │
│   └── Processed Data/
│       │
│       ├── Enrollment/
│       │   ├── enrolment_0_5.xlsx
│       │   ├── enrolment_5_10.xlsx
│       │   ├── enrolment_10_plus.xlsx
│       │   ├── Aadhaar_Analysis_Final_Report_merged.zip
│       │   └── README.md
│       │
│       ├── Biometric/
│       │   ├── uidai_biometric_flagged.csv
│       │   ├── uidai_biometric_monthly_aggregated.csv
│       │   ├── uidai_monthly_master_9_columns.csv
│       │   └── README.md
│       │
│       ├── Demographic/
│       │   ├── Administrative_Friction_Hotspots.csv
│       │   ├── Persistent_Friction_Districts.csv
│       │   ├── Migration_Hotspots.csv
│       │   ├── Seasonal_Migration_Signal.csv
│       │   ├── Early_Warning_Youth_Instability.csv
│       │   └── README.md
│       │
│       └── README.md              
│
├── Documentation/
│   ├── Biometrics_Methodology_Documentation.docx
│   ├── Demographics_Methodology_Documentation.docx
│   ├── Enrollment_Methodology_Documentation.docx
│   └── UIDAI_Aadhaar_Lifecycle_Risk_Dashboard_with_Metric_Appendix.pdf
│
├── Visuals/
│   │
│   ├── Heatmaps/
│   │   ├── future_risk_score.jpeg
│   │   ├── lifecycle_risk_level.jpeg
│   │   ├── intervention_priority.jpeg
│   │   ├── primary_failure_domain.jpeg
│   │   └── README.md
│   │
│   ├── PowerBI/
│   │   ├── dashboards/
│   │   │   ├── UIDAI_Enrollments.pbix
│   │   │   ├── UIDAI_Demographics.pbix
│   │   │   ├── UIDAI_Biometrics.pbix
│   │   │   └── UIDAI_Final_Dashboard.pbix
│   │   │
│   │   ├── screenshots/
│   │   │   ├── district_enrollment_profile.jpeg
│   │   │   ├── monthly_biometric_profile.jpeg
│   │   │   └── state_demographic_profile.jpeg
│   │   │
│   │   └── README.md
│   │
│   └── Tableau/
│       ├── UIDAI_Dashboard.twb
│       └── README.md
│
└── docs/
    ├── metric_definitions.md
    ├── methodology.md
    └── risk_scoring_framework.md

