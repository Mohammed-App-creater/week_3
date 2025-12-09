import pandas as pd
import numpy as np
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_data(df):
    """
    Handles missing values and basic data cleaning.
    """
    logging.info("Starting data cleaning...")
    
    # Critical: Ensure target columns are numeric immediately
    # This prevents them from being treated as object/categorical and filled with strings
    for col in ['TotalClaims', 'CalculatedPremiumPerTerm', 'SumInsured']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing numeric values with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
        
    # Fill missing categorical values with 'Unknown' or mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
        
    # Drop duplicates
    df = df.drop_duplicates()
    
    logging.info("Data cleaning completed.")
    return df

def winsorize_data(df, columns, limits=(0.01, 0.01)):
    """
    Winsorizes specified columns to handle outliers.
    """
    logging.info(f"Winsorizing columns: {columns} with limits {limits}...")
    from scipy.stats import mstats
    for col in columns:
        if col in df.columns:
            df[col] = mstats.winsorize(df[col], limits=limits)
    return df

def feature_engineering(df):
    """
    Creates new features for modeling.
    """
    logging.info("Starting feature engineering...")
    
    # 1. Vehicle Age
    current_year = 2015 # Assuming dataset context is around 2014-2015 based on typical ACIS data, or use max year
    if 'RegistrationYear' in df.columns:
        # Clean RegistrationYear first to avoid noise
        df['RegistrationYear'] = pd.to_numeric(df['RegistrationYear'], errors='coerce')
        df['RegistrationYear'] = df['RegistrationYear'].fillna(df['RegistrationYear'].median())
        df['VehicleAge'] = current_year - df['RegistrationYear']
        df['VehicleAge'] = df['VehicleAge'].apply(lambda x: max(0, x)) # Ensure no negative age
    
    # 2. Power Ratio
    if 'Kilowatts' in df.columns and 'Cubiccapacity' in df.columns:
        df['PowerRatio'] = df['Kilowatts'] / df['Cubiccapacity']
        df['PowerRatio'] = df['PowerRatio'].replace([np.inf, -np.inf], 0).fillna(0)

    # 3. Target Columns Prep
    # Ensure TotalClaims and CalculatedPremiumPerTerm are numeric
    for col in ['TotalClaims', 'CalculatedPremiumPerTerm']:
        if col in df.columns:
             df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    logging.info("Feature engineering completed.")
    return df

def encode_categorical(df, target_col=None):
    """
    Encodes categorical variables using Label Encoding (simple baseline).
    """
    logging.info("Encoding categorical variables...")
    categorical_cols = df.select_dtypes(include=['object']).columns
    le_dict = {}
    
    for col in categorical_cols:
        if col != target_col:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            le_dict[col] = le
            
    return df, le_dict

def prepare_modeling_data(df):
    """
    Master pipeline to Clean -> Winsorize -> Feature Engineer -> Encode -> Split.
    """
    # 1. Clean
    df = clean_data(df)
    
    # 2. Winsorize Outliers
    # Capping TotalClaims and Premium at 1% and 99%
    df = winsorize_data(df, columns=['TotalClaims', 'CalculatedPremiumPerTerm', 'SumInsured'], limits=(0.0, 0.01)) # Only cap top end
    
    # 3. Feature Engineering
    df = feature_engineering(df)
    
    return df

def split_data(df, target_col, test_size=0.2):
    """
    Splits data into train and test sets.
    """
    logging.info(f"Splitting data with target: {target_col}")
    
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Test pipeline
    try:
        from src.data.data_loader import load_data
        DATA_PATH = r"C:\Users\yoga\code\10_Academy\week_3\data\raw\MachineLearningRating_v3.txt"
        
        df = load_data(DATA_PATH)
        df = prepare_modeling_data(df)
        
        # Example split for Severity Model
        df_claims = df[df['TotalClaims'] > 0].copy() # Filter for severity model
        df_encoded, _ = encode_categorical(df_claims)
        X_train, X_test, y_train, y_test = split_data(df_encoded, 'TotalClaims')
        
        print(f"Train Cleaned Shape: {X_train.shape}")
        print("Sample Features:", X_train.head())
    except Exception as e:
        print(f"Error: {e}")
