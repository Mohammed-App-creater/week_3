# Statistical Testing Plan for Task 3

## Executive Summary

This document outlines the comprehensive statistical testing framework for Task 3 of the ACIS Risk Analytics project. The plan defines hypotheses, statistical tests, assumptions, and interpretation guidelines to validate segment differences and inform business decisions.

**Primary Objective**: Test whether risk profiles (loss ratios, claim frequencies) differ significantly across customer segments, geographic regions, and demographic groups.

---

## 1. Hypotheses Framework

### Hypothesis 1: Provincial Risk Differences

**Research Question**: Do loss ratios differ significantly across South African provinces?

**Null Hypothesis (H₀)**: There is no significant difference in mean loss ratios across provinces.  
**Alternative Hypothesis (H₁)**: At least one province has a significantly different mean loss ratio.

**Business Implication**: If H₀ is rejected, ACIS should implement province-specific pricing strategies.

**Variables**:
- Independent: `Province` (categorical, 9 levels)
- Dependent: `LossRatio` (continuous)

**Statistical Test**: One-way ANOVA  
**Post-hoc Test**: Tukey HSD (if ANOVA significant)  
**Significance Level**: α = 0.05

---

### Hypothesis 2: Zip Code Risk Differences

**Research Question**: Do loss ratios vary significantly between different postal codes within the same province?

**Null Hypothesis (H₀)**: Postal codes within a province have equal mean loss ratios.  
**Alternative Hypothesis (H₁)**: Postal codes within a province have different mean loss ratios.

**Business Implication**: Fine-grained geographic pricing based on postal codes.

**Variables**:
- Independent: `PostalCode` (categorical, high cardinality)
- Dependent: `LossRatio` (continuous)
- Control: `Province` (stratify analysis by province)

**Statistical Test**: Kruskal-Wallis H test (non-parametric alternative to ANOVA due to high cardinality)  
**Post-hoc Test**: Dunn's test with Bonferroni correction  
**Significance Level**: α = 0.05

---

### Hypothesis 3: Gender Risk Differences

**Research Question**: Do male and female drivers have different risk profiles?

**Null Hypothesis (H₀)**: Mean loss ratio for males equals mean loss ratio for females.  
**Alternative Hypothesis (H₁)**: Mean loss ratio for males differs from mean loss ratio for females.

**Business Implication**: Gender-based pricing adjustments (subject to regulatory constraints).

**Variables**:
- Independent: `Gender` (categorical, 2 levels: Male, Female)
- Dependent: `LossRatio` (continuous)

**Statistical Test**: Independent samples t-test  
**Alternative Test**: Mann-Whitney U test (if normality violated)  
**Significance Level**: α = 0.05

---

### Hypothesis 4: Margin Differences Between Zip Codes

**Research Question**: Do profit margins (premium - claims) differ significantly across postal codes?

**Null Hypothesis (H₀)**: Mean profit margin is equal across postal codes.  
**Alternative Hypothesis (H₁)**: Mean profit margin differs across postal codes.

**Business Implication**: Identify high-margin and low-margin areas for resource allocation.

**Variables**:
- Independent: `PostalCode` (categorical)
- Dependent: `ProfitMargin = TotalPremium - TotalClaims` (continuous)

**Statistical Test**: Kruskal-Wallis H test  
**Post-hoc Test**: Pairwise Mann-Whitney U tests  
**Significance Level**: α = 0.05

---

### Hypothesis 5: Vehicle Type Risk Differences

**Research Question**: Do different vehicle types have significantly different claim frequencies?

**Null Hypothesis (H₀)**: Claim frequency is independent of vehicle type.  
**Alternative Hypothesis (H₁)**: Claim frequency depends on vehicle type.

**Business Implication**: Vehicle-type-specific pricing and coverage options.

**Variables**:
- Independent: `VehicleType` (categorical, ~15 levels)
- Dependent: `ClaimFrequency` (binary: 0 or 1)

**Statistical Test**: Chi-square test of independence  
**Alternative Test**: Fisher's exact test (if expected frequencies < 5)  
**Significance Level**: α = 0.05

---

### Hypothesis 6: Marital Status and Risk

**Research Question**: Does marital status affect loss ratios?

**Null Hypothesis (H₀)**: Mean loss ratio is equal across marital status groups.  
**Alternative Hypothesis (H₁)**: Mean loss ratio differs across marital status groups.

**Business Implication**: Marital status as a pricing factor.

**Variables**:
- Independent: `MaritalStatus` (categorical, 5 levels)
- Dependent: `LossRatio` (continuous)

**Statistical Test**: One-way ANOVA  
**Post-hoc Test**: Tukey HSD  
**Significance Level**: α = 0.05

---

### Hypothesis 7: Cover Type and Profitability

**Research Question**: Do different cover types have different profitability (loss ratios)?

**Null Hypothesis (H₀)**: Mean loss ratio is equal across cover types.  
**Alternative Hypothesis (H₁)**: Mean loss ratio differs across cover types.

**Business Implication**: Optimize product mix and pricing by cover type.

**Variables**:
- Independent: `CoverType` (categorical, 3 levels: Third Party, Third Party Fire & Theft, Comprehensive)
- Dependent: `LossRatio` (continuous)

**Statistical Test**: One-way ANOVA  
**Post-hoc Test**: Tukey HSD  
**Significance Level**: α = 0.05

---

### Hypothesis 8: Security Features and Risk Reduction

**Research Question**: Do vehicles with security features (alarm, tracking) have lower claim frequencies?

**Null Hypothesis (H₀)**: Claim frequency is independent of security features.  
**Alternative Hypothesis (H₁)**: Vehicles with security features have lower claim frequencies.

**Business Implication**: Incentivize security feature adoption through discounts.

**Variables**:
- Independent: `SecurityScore` (ordinal, 0-2)
- Dependent: `ClaimFrequency` (binary)

**Statistical Test**: Chi-square test for trend  
**Alternative Test**: Logistic regression (more sophisticated)  
**Significance Level**: α = 0.05

---

## 2. Statistical Tests Specification

### 2.1 One-Way ANOVA

**Purpose**: Compare means across 3+ independent groups

**Assumptions**:
1. **Independence**: Observations are independent
2. **Normality**: Dependent variable is approximately normally distributed within each group
3. **Homogeneity of Variance**: Variances are equal across groups (Levene's test)

**Python Implementation**:
```python
from scipy import stats

def perform_anova(df, group_col, value_col):
    """Perform one-way ANOVA"""
    groups = [group[value_col].values for name, group in df.groupby(group_col)]
    
    # Perform ANOVA
    f_stat, p_value = stats.f_oneway(*groups)
    
    # Check assumptions
    # 1. Normality (Shapiro-Wilk test for each group)
    normality_tests = {}
    for name, group in df.groupby(group_col):
        if len(group) >= 3:
            stat, p = stats.shapiro(group[value_col])
            normality_tests[name] = {'statistic': stat, 'p_value': p}
    
    # 2. Homogeneity of variance (Levene's test)
    levene_stat, levene_p = stats.levene(*groups)
    
    results = {
        'f_statistic': f_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'levene_statistic': levene_stat,
        'levene_p_value': levene_p,
        'homogeneity_met': levene_p > 0.05,
        'normality_tests': normality_tests
    }
    
    return results
```

**Post-hoc Test (Tukey HSD)**:
```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def tukey_post_hoc(df, group_col, value_col):
    """Perform Tukey HSD post-hoc test"""
    tukey = pairwise_tukeyhsd(
        endog=df[value_col],
        groups=df[group_col],
        alpha=0.05
    )
    return tukey
```

---

### 2.2 Independent Samples t-test

**Purpose**: Compare means between 2 independent groups

**Assumptions**:
1. **Independence**: Observations are independent
2. **Normality**: Dependent variable is approximately normally distributed in both groups
3. **Homogeneity of Variance**: Variances are equal (Levene's test)

**Python Implementation**:
```python
def perform_t_test(df, group_col, value_col, group1, group2):
    """Perform independent samples t-test"""
    data1 = df[df[group_col] == group1][value_col]
    data2 = df[df[group_col] == group2][value_col]
    
    # Levene's test for equal variances
    levene_stat, levene_p = stats.levene(data1, data2)
    equal_var = levene_p > 0.05
    
    # t-test
    t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=equal_var)
    
    # Effect size (Cohen's d)
    cohens_d = (data1.mean() - data2.mean()) / np.sqrt(
        ((len(data1) - 1) * data1.std()**2 + (len(data2) - 1) * data2.std()**2) / 
        (len(data1) + len(data2) - 2)
    )
    
    results = {
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'cohens_d': cohens_d,
        'equal_variances': equal_var,
        'mean_diff': data1.mean() - data2.mean()
    }
    
    return results
```

---

### 2.3 Chi-Square Test of Independence

**Purpose**: Test association between two categorical variables

**Assumptions**:
1. **Independence**: Observations are independent
2. **Expected Frequencies**: Expected frequency ≥ 5 in at least 80% of cells

**Python Implementation**:
```python
def perform_chi_square(df, var1, var2):
    """Perform chi-square test of independence"""
    # Create contingency table
    contingency_table = pd.crosstab(df[var1], df[var2])
    
    # Chi-square test
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    # Check expected frequencies assumption
    min_expected = expected.min()
    pct_above_5 = (expected >= 5).sum() / expected.size
    
    # Cramér's V (effect size)
    n = contingency_table.sum().sum()
    min_dim = min(contingency_table.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim))
    
    results = {
        'chi2_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': dof,
        'significant': p_value < 0.05,
        'cramers_v': cramers_v,
        'min_expected_freq': min_expected,
        'assumption_met': min_expected >= 5 and pct_above_5 >= 0.8
    }
    
    return results
```

---

### 2.4 Mann-Whitney U Test (Non-parametric)

**Purpose**: Compare distributions between 2 independent groups (alternative to t-test)

**Use When**: Normality assumption violated or ordinal data

**Python Implementation**:
```python
def perform_mann_whitney(df, group_col, value_col, group1, group2):
    """Perform Mann-Whitney U test"""
    data1 = df[df[group_col] == group1][value_col]
    data2 = df[df[group_col] == group2][value_col]
    
    u_stat, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
    
    # Effect size (rank-biserial correlation)
    n1, n2 = len(data1), len(data2)
    r = 1 - (2 * u_stat) / (n1 * n2)
    
    results = {
        'u_statistic': u_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'rank_biserial_r': r,
        'median_diff': data1.median() - data2.median()
    }
    
    return results
```

---

### 2.5 Kruskal-Wallis H Test (Non-parametric)

**Purpose**: Compare distributions across 3+ independent groups (alternative to ANOVA)

**Use When**: Normality or homogeneity of variance violated

**Python Implementation**:
```python
def perform_kruskal_wallis(df, group_col, value_col):
    """Perform Kruskal-Wallis H test"""
    groups = [group[value_col].values for name, group in df.groupby(group_col)]
    
    h_stat, p_value = stats.kruskal(*groups)
    
    # Effect size (epsilon squared)
    n = len(df)
    k = len(groups)
    epsilon_squared = (h_stat - k + 1) / (n - k)
    
    results = {
        'h_statistic': h_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'epsilon_squared': epsilon_squared
    }
    
    return results
```

---

## 3. Multiple Testing Correction

### 3.1 Bonferroni Correction

**Purpose**: Control family-wise error rate when conducting multiple tests

**Formula**: `α_adjusted = α / number_of_tests`

**Application**: With 8 hypotheses and α = 0.05:
- Adjusted α = 0.05 / 8 = 0.00625

**Python Implementation**:
```python
def bonferroni_correction(p_values, alpha=0.05):
    """Apply Bonferroni correction to p-values"""
    n_tests = len(p_values)
    adjusted_alpha = alpha / n_tests
    
    significant = [p < adjusted_alpha for p in p_values]
    
    return {
        'adjusted_alpha': adjusted_alpha,
        'significant_tests': significant,
        'n_significant': sum(significant)
    }
```

---

### 3.2 False Discovery Rate (FDR) - Benjamini-Hochberg

**Purpose**: Control expected proportion of false discoveries (less conservative than Bonferroni)

**Python Implementation**:
```python
from statsmodels.stats.multitest import multipletests

def fdr_correction(p_values, alpha=0.05):
    """Apply Benjamini-Hochberg FDR correction"""
    reject, p_adjusted, _, _ = multipletests(p_values, alpha=alpha, method='fdr_bh')
    
    return {
        'adjusted_p_values': p_adjusted,
        'significant_tests': reject,
        'n_significant': sum(reject)
    }
```

---

## 4. Effect Size Interpretation

### 4.1 Cohen's d (for t-tests)
- Small: d = 0.2
- Medium: d = 0.5
- Large: d = 0.8

### 4.2 Eta-squared (for ANOVA)
- Small: η² = 0.01
- Medium: η² = 0.06
- Large: η² = 0.14

### 4.3 Cramér's V (for Chi-square)
- Small: V = 0.1
- Medium: V = 0.3
- Large: V = 0.5

---

## 5. Data Requirements

### 5.1 Sample Size Requirements

**Minimum Sample Sizes**:
- t-test: n ≥ 30 per group (for CLT to apply)
- ANOVA: n ≥ 20 per group
- Chi-square: Expected frequency ≥ 5 in 80% of cells

**Power Analysis**:
```python
from statsmodels.stats.power import tt_ind_solve_power

def calculate_required_sample_size(effect_size=0.5, alpha=0.05, power=0.8):
    """Calculate required sample size for t-test"""
    n = tt_ind_solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        alternative='two-sided'
    )
    return int(np.ceil(n))
```

---

### 5.2 Data Quality Requirements

1. **No Missing Values**: Complete data for test variables
2. **Valid Range**: Loss ratios between 0 and 5
3. **Sufficient Variation**: At least 2 unique values per group
4. **Balanced Groups**: Ideally, group sizes within 2:1 ratio

---

## 6. Assumption Checking Procedures

### 6.1 Normality Tests

**Shapiro-Wilk Test** (for n < 5000):
```python
def check_normality(data):
    """Check normality using Shapiro-Wilk test"""
    stat, p_value = stats.shapiro(data)
    return {
        'statistic': stat,
        'p_value': p_value,
        'is_normal': p_value > 0.05
    }
```

**Kolmogorov-Smirnov Test** (for n ≥ 5000):
```python
def check_normality_ks(data):
    """Check normality using K-S test"""
    stat, p_value = stats.kstest(data, 'norm')
    return {
        'statistic': stat,
        'p_value': p_value,
        'is_normal': p_value > 0.05
    }
```

**Visual Check**: Q-Q plot
```python
import matplotlib.pyplot as plt
from scipy import stats

def qq_plot(data, title='Q-Q Plot'):
    """Create Q-Q plot for normality assessment"""
    stats.probplot(data, dist="norm", plot=plt)
    plt.title(title)
    plt.show()
```

---

### 6.2 Homogeneity of Variance

**Levene's Test**:
```python
def check_homogeneity(df, group_col, value_col):
    """Check homogeneity of variance using Levene's test"""
    groups = [group[value_col].values for name, group in df.groupby(group_col)]
    stat, p_value = stats.levene(*groups)
    
    return {
        'statistic': stat,
        'p_value': p_value,
        'homogeneous': p_value > 0.05
    }
```

---

## 7. Results Interpretation Framework

### 7.1 Significance Interpretation

| p-value | Interpretation | Action |
|---------|---------------|--------|
| p < 0.001 | Highly significant | Strong evidence to reject H₀ |
| 0.001 ≤ p < 0.01 | Very significant | Reject H₀ |
| 0.01 ≤ p < 0.05 | Significant | Reject H₀ |
| 0.05 ≤ p < 0.10 | Marginally significant | Weak evidence, investigate further |
| p ≥ 0.10 | Not significant | Fail to reject H₀ |

---

### 7.2 Business Decision Framework

**If Hypothesis is Supported (p < 0.05)**:
1. Calculate effect size to assess practical significance
2. Identify which groups differ (post-hoc tests)
3. Quantify business impact (e.g., loss ratio difference)
4. Develop targeted strategies for each group

**If Hypothesis is Not Supported (p ≥ 0.05)**:
1. Check statistical power (was sample size sufficient?)
2. Consider alternative explanations
3. Investigate potential confounding variables
4. Maintain current pricing/strategy for that factor

---

## 8. Reporting Template

### 8.1 Hypothesis Test Report Structure

```markdown
## Hypothesis X: [Title]

**Research Question**: [Question]

**Test Used**: [Test name]

**Results**:
- Test Statistic: [value]
- p-value: [value]
- Significance: [Yes/No at α = 0.05]
- Effect Size: [value and interpretation]

**Assumptions**:
- Normality: [Met/Not Met]
- Homogeneity: [Met/Not Met]
- Independence: [Met/Not Met]

**Conclusion**:
[Interpretation in plain language]

**Business Recommendation**:
[Actionable recommendation based on results]
```

---

## 9. Implementation Checklist

- [ ] Load processed data from Task 2
- [ ] Check data quality and completeness
- [ ] Perform assumption checks for each test
- [ ] Run primary statistical tests
- [ ] Apply multiple testing correction
- [ ] Calculate effect sizes
- [ ] Conduct post-hoc tests where needed
- [ ] Create visualizations for each hypothesis
- [ ] Document results in standardized format
- [ ] Translate findings to business recommendations

---

## 10. Expected Outcomes

Based on EDA from Task 1, we expect:

1. **H1 (Province)**: REJECT H₀ - Significant differences exist
2. **H2 (Zip Code)**: REJECT H₀ - Postal code matters
3. **H3 (Gender)**: REJECT H₀ - Gender affects risk
4. **H4 (Margin)**: REJECT H₀ - Margins vary by location
5. **H5 (Vehicle Type)**: REJECT H₀ - Vehicle type matters
6. **H6 (Marital Status)**: REJECT H₀ - Marital status affects risk
7. **H7 (Cover Type)**: REJECT H₀ - Cover type affects profitability
8. **H8 (Security)**: REJECT H₀ - Security reduces claims

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Owner**: Data Science Team - ACIS Risk Analytics Project
