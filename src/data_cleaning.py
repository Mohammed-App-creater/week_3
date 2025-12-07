"""
Data Cleaning Utilities for AlphaCare Insurance Solutions
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Optional


def detect_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect and summarize missing values.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Summary of missing values
    """
    missing_data = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum(),
        'Missing_Percentage': (df.isnull().sum() / len(df)) * 100
    })
    
    missing_data = missing_data[missing_data['Missing_Count'] > 0].sort_values(
        'Missing_Percentage', ascending=False
    ).reset_index(drop=True)
    
    return missing_data


def detect_outliers_iqr(df: pd.DataFrame, column: str) -> Tuple[pd.DataFrame, float, float]:
    """
    Detect outliers using the IQR method.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column name to check for outliers
        
    Returns:
    --------
    tuple
        (outliers_df, lower_bound, upper_bound)
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    return outliers, lower_bound, upper_bound


def detect_outliers_zscore(df: pd.DataFrame, column: str, threshold: float = 3.0) -> pd.DataFrame:
    """
    Detect outliers using Z-score method.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    column : str
        Column name to check for outliers
    threshold : float, default 3.0
        Z-score threshold
        
    Returns:
    --------
    pd.DataFrame
        Dataframe containing outliers
    """
    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
    outliers = df[z_scores > threshold]
    
    return outliers


def calculate_loss_ratio(df: pd.DataFrame, 
                         premium_col: str = 'TotalPremium',
                         claims_col: str = 'TotalClaims') -> pd.Series:
    """
    Calculate loss ratio.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    premium_col : str, default 'TotalPremium'
        Column name for premiums
    claims_col : str, default 'TotalClaims'
        Column name for claims
        
    Returns:
    --------
    pd.Series
        Loss ratio values
    """
    loss_ratio = (df[claims_col] / df[premium_col]) * 100
    loss_ratio = loss_ratio.replace([np.inf, -np.inf], np.nan)
    
    return loss_ratio


def calculate_loss_ratio_by_group(df: pd.DataFrame,
                                   group_col: str,
                                   premium_col: str = 'TotalPremium',
                                   claims_col: str = 'TotalClaims',
                                   count_col: str = 'PolicyID') -> pd.DataFrame:
    """
    Calculate loss ratio by group.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    group_col : str
        Column to group by
    premium_col : str, default 'TotalPremium'
        Column name for premiums
    claims_col : str, default 'TotalClaims'
        Column name for claims
    count_col : str, default 'PolicyID'
        Column to count
        
    Returns:
    --------
    pd.DataFrame
        Grouped loss ratio analysis
    """
    analysis = df.groupby(group_col).agg({
        premium_col: 'sum',
        claims_col: 'sum',
        count_col: 'count'
    }).reset_index()
    
    analysis.columns = [group_col, 'TotalPremium', 'TotalClaims', 'PolicyCount']
    analysis['LossRatio'] = (analysis['TotalClaims'] / analysis['TotalPremium']) * 100
    analysis = analysis.sort_values('LossRatio', ascending=True)
    
    return analysis


def calculate_claim_frequency(df: pd.DataFrame,
                              group_col: Optional[str] = None,
                              claims_col: str = 'TotalClaims') -> pd.Series:
    """
    Calculate claim frequency.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    group_col : str, optional
        Column to group by
    claims_col : str, default 'TotalClaims'
        Column name for claims
        
    Returns:
    --------
    pd.Series
        Claim frequency values
    """
    if group_col:
        frequency = df.groupby(group_col).apply(
            lambda x: ((x[claims_col] > 0).sum() / len(x)) * 100
        )
    else:
        frequency = ((df[claims_col] > 0).sum() / len(df)) * 100
    
    return frequency


def calculate_claim_severity(df: pd.DataFrame,
                             group_col: Optional[str] = None,
                             claims_col: str = 'TotalClaims') -> pd.Series:
    """
    Calculate claim severity (average claim amount for policies with claims).
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    group_col : str, optional
        Column to group by
    claims_col : str, default 'TotalClaims'
        Column name for claims
        
    Returns:
    --------
    pd.Series
        Claim severity values
    """
    df_with_claims = df[df[claims_col] > 0]
    
    if group_col:
        severity = df_with_claims.groupby(group_col)[claims_col].mean()
    else:
        severity = df_with_claims[claims_col].mean()
    
    return severity


def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Remove duplicate records.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    subset : list, optional
        Columns to consider for identifying duplicates
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with duplicates removed
    """
    n_before = len(df)
    df_clean = df.drop_duplicates(subset=subset)
    n_after = len(df_clean)
    
    print(f"Removed {n_before - n_after:,} duplicate records")
    
    return df_clean


def handle_missing_values(df: pd.DataFrame,
                         strategy: str = 'drop',
                         columns: Optional[List[str]] = None,
                         fill_value: Optional[any] = None) -> pd.DataFrame:
    """
    Handle missing values.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    strategy : str, default 'drop'
        Strategy: 'drop', 'fill', 'forward_fill', 'backward_fill'
    columns : list, optional
        Columns to apply strategy to
    fill_value : any, optional
        Value to fill missing values with
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with missing values handled
    """
    df_clean = df.copy()
    
    if columns is None:
        columns = df.columns
    
    if strategy == 'drop':
        df_clean = df_clean.dropna(subset=columns)
    elif strategy == 'fill':
        df_clean[columns] = df_clean[columns].fillna(fill_value)
    elif strategy == 'forward_fill':
        df_clean[columns] = df_clean[columns].fillna(method='ffill')
    elif strategy == 'backward_fill':
        df_clean[columns] = df_clean[columns].fillna(method='bfill')
    
    return df_clean


def validate_data_quality(df: pd.DataFrame) -> dict:
    """
    Validate data quality and return issues.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    dict
        Dictionary of data quality issues
    """
    issues = {}
    
    # Check for negative values in financial columns
    financial_cols = ['TotalPremium', 'TotalClaims', 'SumInsured']
    for col in financial_cols:
        if col in df.columns:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                issues[f'{col}_negative'] = negative_count
    
    # Check for claims exceeding sum insured
    if 'TotalClaims' in df.columns and 'SumInsured' in df.columns:
        exceeding = (df['TotalClaims'] > df['SumInsured']).sum()
        if exceeding > 0:
            issues['claims_exceed_sum_insured'] = exceeding
    
    # Check for zero premiums with claims
    if 'TotalPremium' in df.columns and 'TotalClaims' in df.columns:
        zero_premium_with_claims = ((df['TotalPremium'] == 0) & (df['TotalClaims'] > 0)).sum()
        if zero_premium_with_claims > 0:
            issues['zero_premium_with_claims'] = zero_premium_with_claims
    
    return issues
