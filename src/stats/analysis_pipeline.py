import sys
import os
import pandas as pd
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.stats.metrics import load_and_clean_data, calculate_kpis, apply_winsorization, get_claimant_data
from src.stats.hypothesis_tests import test_risk_differences_categorical, test_means_diff_multiple_groups, test_means_diff_two_groups

def run_analysis():
    file_path = r"C:\Users\yoga\code\10_Academy\week_3\data\raw\MachineLearningRating_v3.txt"
    print(f"Loading data from {file_path}...")
    
    df = load_and_clean_data(file_path)
    df = calculate_kpis(df)
    df = apply_winsorization(df, cols=['TotalClaims', 'Margin'])
    
    print(f"Data Loaded. Policy Count: {len(df)}")
    print("-" * 50)

    results = []

    # 1. H0: No risk differences across provinces
    print("\n--- Testing H0: No risk differences across provinces ---")
    p_prov, cont_prov, chi2 = test_risk_differences_categorical(df, 'Province', 'HasClaim')
    print(f"Frequency (Chi-Square): p-value = {p_prov:.4e}")
    results.append({
        'Hypothesis': 'Risk vs Province',
        'Metric': 'Frequency',
        'Test': 'Chi-Square',
        'pValue': p_prov,
        'Reject': p_prov < 0.05
    })

    # Severity (Claims > 0)
    claimants = get_claimant_data(df)
    # Check normality for severity
    # For large datasets, Shapiro is meaningless, proceed with Kruskal-Wallis as Severity is typically skewed
    p_sev_prov, stat_sev_prov, test_name_sev = test_means_diff_multiple_groups(claimants, 'Province', 'TotalClaims', parametric=False)
    print(f"Severity (Kruskal-Wallis): p-value = {p_sev_prov:.4e}")
    results.append({
        'Hypothesis': 'Risk vs Province',
        'Metric': 'Severity',
        'Test': test_name_sev,
        'pValue': p_sev_prov,
        'Reject': p_sev_prov < 0.05
    })

    # 2. H0: No risk differences between zip codes (PostalCode)
    print("\n--- Testing H0: No risk differences between zip codes ---")
    # PostalCode has many levels, might be slow or sparse.
    # Grouping distinct counts
    print(f"Unique Zip Codes: {df['PostalCode'].nunique()}")
    p_zip, cont_zip, chi2_zip = test_risk_differences_categorical(df, 'PostalCode', 'HasClaim')
    print(f"Frequency (Chi-Square): p-value = {p_zip:.4e}")
    results.append({
        'Hypothesis': 'Risk vs ZipCode',
        'Metric': 'Frequency',
        'Test': 'Chi-Square',
        'pValue': p_zip,
        'Reject': p_zip < 0.05
    })

    # 3. H0: No significant margin difference between zip codes
    print("\n--- Testing H0: No significant margin difference between zip codes ---")
    # Margin is often skewed, use Kruskal-Wallis
    p_marg_zip, stat_marg_zip, test_name_marg = test_means_diff_multiple_groups(df, 'PostalCode', 'Margin', parametric=False)
    print(f"Margin (Kruskal-Wallis): p-value = {p_marg_zip:.4e}")
    results.append({
        'Hypothesis': 'Margin vs ZipCode',
        'Metric': 'Margin',
        'Test': test_name_marg,
        'pValue': p_marg_zip,
        'Reject': p_marg_zip < 0.05
    })

    # 4. H0: No significant risk difference between women and men
    print("\n--- Testing H0: No significant risk difference between women and men ---")
    # Clean Gender first (remove Not Specified if exists or include as category?)
    # Usually we compare only Male vs Female for this specific hypothesis
    gender_df = df[df['Gender'].isin(['Male', 'Female'])].copy()
    
    # Frequency
    p_gen, cont_gen, chi2_gen = test_risk_differences_categorical(gender_df, 'Gender', 'HasClaim')
    print(f"Frequency (Chi-Square): p-value = {p_gen:.4e}")
    results.append({
        'Hypothesis': 'Risk vs Gender',
        'Metric': 'Frequency',
        'Test': 'Chi-Square',
        'pValue': p_gen,
        'Reject': p_gen < 0.05
    })
    
    # Severity (among claimants)
    gender_claimants = get_claimant_data(gender_df)
    group_m = gender_claimants[gender_claimants['Gender'] == 'Male']['TotalClaims']
    group_f = gender_claimants[gender_claimants['Gender'] == 'Female']['TotalClaims']
    
    p_sev_gen, stat_sev_gen, test_name_gen = test_means_diff_two_groups(group_m, group_f, parametric=False)
    print(f"Severity ({test_name_gen}): p-value = {p_sev_gen:.4e}")
    
    results.append({
        'Hypothesis': 'Risk vs Gender',
        'Metric': 'Severity',
        'Test': test_name_gen,
        'pValue': p_sev_gen,
        'Reject': p_sev_gen < 0.05
    })

    # Print Summary Table
    print("\n\n--- SUMMARY TABLE ---")
    res_df = pd.DataFrame(results)
    print(res_df.to_string(index=False))
    
    # Save results to file for reading
    res_df.to_csv("outputs/stats_results.csv", index=False)
    print("\nResults saved to outputs/stats_results.csv")

if __name__ == "__main__":
    run_analysis()
