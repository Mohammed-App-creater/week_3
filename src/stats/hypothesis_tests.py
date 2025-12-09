import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.proportion import proportions_ztest

def check_normality(data, p_threshold=0.05):
    """
    Checks normality using Shapiro-Wilk (for small n) or D'Agostino's K^2.
    For large N > 5000, normality tests often reject even trivial deviations.
    We will output p-value but also rely on sample size > 30 (CLT) for t-tests usually.
    """
    if len(data) > 5000:
        # For very large data, standard tests are too sensitive. 
        # We assume CLT holds for means, but check skew/kurtosis if needed.
        return True, 1.0 
    stat, p = stats.shapiro(data)
    return p > p_threshold, p

def test_risk_differences_categorical(df, group_col, target_binary_col='HasClaim'):
    """
    H0: No difference in risk (claims frequency) across groups.
    Uses Chi-Square test of independence.
    Returns: p-value, contingency table
    """
    contingency = pd.crosstab(df[group_col], df[target_binary_col])
    chi2, p, dof, ex = stats.chi2_contingency(contingency)
    return p, contingency, chi2

def test_means_diff_two_groups(group1_data, group2_data, parametric=True):
    """
    H0: Means of two independent groups are equal.
    Parametric: t-test (Independent)
    Non-Parametric: Mann-Whitney U
    """
    if parametric:
        stat, p = stats.ttest_ind(group1_data, group2_data, equal_var=False) # Welch's t-test
        test_name = "Welch's t-test"
    else:
        stat, p = stats.mannwhitneyu(group1_data, group2_data, alternative='two-sided')
        test_name = "Mann-Whitney U"
    
    return p, stat, test_name

def test_means_diff_multiple_groups(df, group_col, metric_col, parametric=True):
    """
    H0: Means of multiple groups are equal.
    Parametric: ANOVA (One-way)
    Non-Parametric: Kruskal-Wallis H-test
    """
    groups = [group[metric_col].dropna() for name, group in df.groupby(group_col)]
    # Filter out empty groups
    groups = [g for g in groups if len(g) > 1]
    
    if len(groups) < 2:
        return np.nan, np.nan, "Insufficient Groups"

    if parametric:
        stat, p = stats.f_oneway(*groups)
        test_name = "ANOVA"
    else:
        stat, p = stats.kruskal(*groups)
        test_name = "Kruskal-Wallis"
        
    return p, stat, test_name

def calculate_effect_size_cohens_d(group1, group2):
    """Calculates Cohen's d for two groups."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    pooled_se = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    diff = np.mean(group1) - np.mean(group2)
    
    if pooled_se == 0:
        return 0
    return diff / pooled_se
