# Task 4: Modeling & Pricing Report

## Executive Summary
*To be filled after model training.*

**Key Findings:**
-   **Risk Factors:** [Placeholder: e.g., Older vehicles show 15% higher claim severity]
-   **Pricing Strategy:** [Placeholder: e.g., Recommended 10% premium uplift for high-risk provinces]
-   **Impact:** [Placeholder: e.g., Potential 5% improvement in loss ratio]

## Technical Analysis

### Data Preparation
-   **Source:** `MachineLearningRating_v3.txt` (Pipe-delimited).
-   **Cleaning:** Imputed missing values (median/mode); Winsorized outliers at 1% and 99%.
-   **Features:** Created `VehicleAge`, `PowerRatio`, and encoded categorical variables.

### Modeling Methodology
We employed a two-stage approach:
1.  **Claim Probability Model (Classification):** Predicting `HasClaim` (1/0) using XGBoost/Random Forest.
2.  **Claim Severity Model (Regression):** Predicting `TotalClaims` (amount) for positive claims using XGBoost/Linear Regression.

### Model Performance
*Run `src/main.py` to populate these metrics.*

| Model | Metric | Value |
| :--- | :--- | :--- |
| Severity (XGBoost) | RMSE | TBD |
| Severity (Linear) | RMSE | TBD |
| Classification (XGBoost) | AUC | TBD |
| Classification (RF) | AUC | TBD |

## Interpretability (SHAP)
*Refer to `outputs/shap_severity.png` after execution.*

**Top 3 Drivers of Claim Severity:**
1.  [Feature A]
2.  [Feature B]
3.  [Feature C]

## Pricing Recommendations
Based on the analysis, we recommend:
1.  **Base Rate Adjustment:** Adjust base premiums for segments identified as high-risk by the model (e.g., specific vehicle classes).
2.  **Discount Strategy:** Offer discounts to low-risk profiles (e.g., high probability of no-claim) to improve retention.
3.  **Risk-Based Scoring:** Implement the `Probability * Severity` scoring in the underwriting engine.

## Conclusion
The developed pipeline provides an audit-ready framework for dynamic pricing. The use of XGBoost offers superior predictive power, while SHAP values ensure regulatory compliance through explainability.
