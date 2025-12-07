"""
Data Loading Utilities for AlphaCare Insurance Solutions
"""

import pandas as pd
import numpy as np
from typing import Optional, List


def load_insurance_data(
    filepath: str,
    parse_dates: Optional[List[str]] = None,
    low_memory: bool = False
) -> pd.DataFrame:
    """
    Load insurance dataset from CSV file.
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
    parse_dates : list, optional
        List of column names to parse as dates
    low_memory : bool, default False
        Whether to use low memory mode
        
    Returns:
    --------
    pd.DataFrame
        Loaded dataset
    """
    if parse_dates is None:
        parse_dates = ['TransactionMonth', 'VehicleIntroDate']
    
    df = pd.read_csv(filepath, parse_dates=parse_dates, low_memory=low_memory)
    
    print(f"Dataset loaded successfully!")
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    
    return df


def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize data types for memory efficiency.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with optimized dtypes
    """
    # Categorical columns
    categorical_columns = [
        'Province', 'Gender', 'VehicleType', 'MaritalStatus', 'Title', 'Language',
        'CoverType', 'CoverCategory', 'Product', 'CoverGroup', 'Section',
        'make', 'Model', 'bodytype', 'Citizenship', 'LegalType', 'Bank', 'AccountType'
    ]
    
    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].astype('category')
    
    print(f"Optimized {len([c for c in categorical_columns if c in df.columns])} columns to category dtype")
    
    return df


def extract_temporal_features(df: pd.DataFrame, date_column: str = 'TransactionMonth') -> pd.DataFrame:
    """
    Extract temporal features from date column.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    date_column : str, default 'TransactionMonth'
        Name of the date column
        
    Returns:
    --------
    pd.DataFrame
        Dataframe with additional temporal features
    """
    if date_column in df.columns:
        df[f'{date_column}_Year'] = df[date_column].dt.year
        df[f'{date_column}_Month'] = df[date_column].dt.month
        df[f'{date_column}_Quarter'] = df[date_column].dt.quarter
        df[f'{date_column}_DayOfWeek'] = df[date_column].dt.dayofweek
        
        print(f"Extracted temporal features from {date_column}")
    
    return df


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Get comprehensive data summary.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    Returns:
    --------
    dict
        Dictionary containing summary statistics
    """
    summary = {
        'n_rows': len(df),
        'n_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'n_duplicates': df.duplicated().sum(),
        'n_missing_values': df.isnull().sum().sum(),
        'columns_with_missing': df.columns[df.isnull().any()].tolist(),
        'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist(),
        'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
        'datetime_columns': df.select_dtypes(include=['datetime64']).columns.tolist()
    }
    
    return summary


def print_data_summary(df: pd.DataFrame) -> None:
    """
    Print comprehensive data summary.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
    """
    summary = get_data_summary(df)
    
    print("=" * 80)
    print("DATA SUMMARY")
    print("=" * 80)
    print(f"Rows: {summary['n_rows']:,}")
    print(f"Columns: {summary['n_columns']}")
    print(f"Memory Usage: {summary['memory_usage_mb']:.2f} MB")
    print(f"Duplicates: {summary['n_duplicates']:,}")
    print(f"Missing Values: {summary['n_missing_values']:,}")
    print(f"Columns with Missing: {len(summary['columns_with_missing'])}")
    print(f"\nNumeric Columns: {len(summary['numeric_columns'])}")
    print(f"Categorical Columns: {len(summary['categorical_columns'])}")
    print(f"Datetime Columns: {len(summary['datetime_columns'])}")
    print("=" * 80)
