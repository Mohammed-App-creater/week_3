# ACIS Task 3: Statistical Analysis Report

## A. Executive Summary

We have performed a rigorous A/B hypothesis testing analysis on the auto-insurance dataset to determine the key drivers of risk and profitability. Our findings indicate:

1.  **Geography is the primary risk driver**: There are statistically significant differences in both claim frequency and claim severity across **Provinces**. Similarly, **Zip Codes** show significant variation in claim frequency.
2.  **Gender is neutral**: We found **no statistically significant evidence** that gender correlates with risk (frequency or severity). This suggests that gender-based pricing may be unnecessary or redundant if other factors are used.
3.  **Margins are stable across Zip Codes**: While claim *counts* vary by zip code, the overall *margin* (profit) does not differ significantly. This implies effective cross-subsidization or that current pricing mechanisms already account for location-based risk adequately.

**Recommendation**: Focus segmentation efforts on Geography (Province/Zip) rather than Gender.

---

## B. Technical Results

### 1. Test Summary Table

| Hypothesis | Metric | Test Used | p-value | Reject $H_0$? | Interpretation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Risk vs Province** | Frequency | Chi-Square | $< 0.001$ | **Yes** | Strong evidence that claim rates vary by Province. |
| **Risk vs Province** | Severity | Kruskal-Wallis | $< 0.001$ | **Yes** | Meaningful difference in claim cost/severity across Provinces. |
| **Risk vs ZipCode** | Frequency | Chi-Square | $0.003$ | **Yes** | Zip codes show significant variation in accident likelihood. |
| **Margin vs ZipCode** | Margin | Kruskal-Wallis | $0.097$ | No | No significant profit margin difference detected across Zip Codes. |
| **Risk vs Gender** | Frequency | Chi-Square | $0.440$ | No | Gender does not significantly affect the likelihood of making a claim. |
| **Risk vs Gender** | Severity | Mann-Whitney U | $0.984$ | No | Male/Female policyholders have statistically identical claim severities. |

### 2. Detailed Interpretation

#### 2.1 Geography (Province & Zip Code)
- **Result**: We rejected the null hypothesis for both risk frequency and severity across provinces. The p-values are extremely small ($< 10^{-5}$), indicating this is not due to random chance.
- **Implication**: Location is a critical determinant of risk. Some provinces are inherently riskier (higher frequency) or more expensive (higher severity) than others. Zip codes also show frequency differences, but interestingly, the profit **Margin** is consistent (p=0.097). This suggests that while accidents happen more often in some areas, the premiums collected there might already be higher, or the severity lower, balancing the books.

#### 2.2 Gender
- **Result**: We failed to reject the null hypothesis for both frequency (p=0.44) and severity (p=0.98).
- **Implication**: There is no statistical justification in this dataset to charge different rates based on gender alone. Any perceived difference might be confounded by other variables (e.g., Vehicle Type, Age) which should be investigated instead.

### 3. Business Recommendations

1.  **Dynamic Pricing by Location**: Implement granular pricing models at the **Province** level. Consider surcharges for high-risk provinces identified in the descriptive stats.
2.  **Marketing Efficiency**: Since Margin is stable across Zip Codes, high-frequency zip codes are not necessarily "unprofitable"—they just have more churn/activity. Focus retention efforts there. Low-frequency zip codes are "easy wins" for marketing.
3.  **Ethical & Simplified Pricing**: **Remove Gender** from the risk rating model for the "Standard" product line. It adds complexity and potential regulatory friction without providing statistical predictive power.

---

## C. Python Code Appendix

The analysis was performed using the following production-ready scripts:
- `src/stats/metrics.py`: Data loading, cleaning, and metric calculation.
- `src/stats/hypothesis_tests.py`: Statistical test functions.
- `src/stats/analysis_pipeline.py`: Orchestration script generating the results.

(See attached files for full source code).
