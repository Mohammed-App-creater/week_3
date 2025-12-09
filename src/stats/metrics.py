import pandas as pd
import numpy as np
from scipy.stats import mstats

def load_and_clean_data(file_path):
    """
    Loads insurance data, aggregates by PolicyID to create a policy-level dataset,
    and performs basic cleaning.
    """
    # Load with correct delimiter
    df = pd.read_csv(file_path, sep='|')
    
    # 1. Standardize text columns
    text_cols = ['Gender', 'Province', 'PostalCode', 'StatutoryRiskType']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title().str.strip()

    # 2. Key Numeric Conversions
    num_cols = ['TotalPremium', 'TotalClaims']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    # 3. Aggregation by PolicyID
    # We take the first value for categorical info (assuming constant per policy)
    # and sum statistical financial info.
    agg_rules = {
        'TotalPremium': 'sum',
        'TotalClaims': 'sum',
        'Gender': 'first',
        'Province': 'first',
        'PostalCode': 'first',
        'StatutoryRiskType': 'first'
    }
    
    # Keep only columns we need for efficiency if dataset is huge, 
    # but for now let's stick to the core ones + agg
    policy_df = df.groupby('PolicyID').agg(agg_rules).reset_index()

    return policy_df

def calculate_kpis(df):
    """
    Adds KPI columns to the dataframe:
    - ClaimFrequency (Binary: 1 if TotalClaims > 0)
    - Margin (Premium - Claims)
    - LossRatio (Claims / Premium)
    """
    df = df.copy()
    df['HasClaim'] = (df['TotalClaims'] > 0).astype(int)
    df['Margin'] = df['TotalPremium'] - df['TotalClaims']
    # Avoid zero division
    df['LossRatio'] = df.apply(
        lambda x: x['TotalClaims'] / x['TotalPremium'] if x['TotalPremium'] > 0 else 0, 
        axis=1
    )
    return df

def apply_winsorization(df, cols=['TotalClaims', 'Margin'], limits=(0.01, 0.01)):
    """
    Applies winsorization to robustify against extreme outliers.
    """
    df_out = df.copy()
    for col in cols:
        if col in df_out.columns:
            # Winsorize returns a masked array, convert back to numpy
            df_out[f'{col}_Winsorized'] = mstats.winsorize(df_out[col], limits=limits)
    return df_out

def get_claimant_data(df):
    """Returns subset of policies that had at least one claim (for Severity analysis)"""
    return df[df['TotalClaims'] > 0].copy()
