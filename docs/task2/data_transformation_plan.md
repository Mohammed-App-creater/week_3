# Data Transformation Plan

## Executive Summary

This document outlines the complete data transformation strategy for the AlphaCare Insurance Solutions dataset. The transformation pipeline will convert raw insurance data into analysis-ready datasets suitable for statistical testing (Task 3) and predictive modeling (Task 4).

**Key Objectives**:
1. Clean and standardize data quality
2. Engineer features for risk analysis
3. Create customer risk segments
4. Prepare data for statistical hypothesis testing
5. Optimize data for machine learning models

---

## 1. Data Cleaning

### 1.1 Column Name Standardization

**Issue**: Column names have inconsistent casing and formatting  
**Solution**: Standardize to snake_case for Python compatibility

```python
def clean_column_names(df):
    """Convert column names to lowercase snake_case"""
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    return df
```

**Affected Columns**: All 52 columns

---

### 1.2 Missing Value Analysis & Treatment

Based on Task 1 EDA, the following columns have missing values:

#### High Missing Rate (> 50%)
| Column | Missing % | Treatment Strategy |
|--------|-----------|-------------------|
| `NumberOfVehiclesInFleet` | 100% | **DROP** - No information value |
| `CrossBorder` | 99.9% | **DROP** - Insufficient data |
| `WrittenOff` | 64.2% | **IMPUTE** - Fill with "No" (assume not written off) |
| `Rebuilt` | 64.2% | **IMPUTE** - Fill with "No" |
| `Converted` | 64.2% | **IMPUTE** - Fill with "No" |
| `CustomValueEstimate` | 78.0% | **IMPUTE** - Fill with median by VehicleType |

#### Moderate Missing Rate (10-50%)
| Column | Missing % | Treatment Strategy |
|--------|-----------|-------------------|
| `NewVehicle` | 15.3% | **IMPUTE** - Infer from RegistrationYear (< 1 year = Yes) |
| `Bank` | 14.6% | **CATEGORY** - Create "Unknown" category |
| `AccountType` | 4.0% | **CATEGORY** - Create "Unknown" category |
| `MaritalStatus` | 0.8% | **CATEGORY** - Create "Unknown" category |
| `Gender` | 0.9% | **CATEGORY** - Create "Unknown" category |

#### Low Missing Rate (< 1%)
| Column | Missing % | Treatment Strategy |
|--------|-----------|-------------------|
| `mmcode` | 0.06% | **DROP ROWS** - Critical vehicle identifier |
| `VehicleType` | 0.06% | **DROP ROWS** - Essential for segmentation |
| `make` | 0.06% | **DROP ROWS** - Linked to mmcode |
| `Model` | 0.06% | **DROP ROWS** - Linked to mmcode |
| `CapitalOutstanding` | 0.0002% | **IMPUTE** - Fill with "No" |

**Implementation**:
```python
def handle_missing_values(df):
    # Drop columns with no value
    df = df.drop(['NumberOfVehiclesInFleet', 'CrossBorder'], axis=1)
    
    # Drop rows with missing critical vehicle info
    df = df.dropna(subset=['mmcode', 'VehicleType', 'make', 'Model'])
    
    # Impute vehicle condition fields
    for col in ['WrittenOff', 'Rebuilt', 'Converted']:
        df[col] = df[col].fillna('No')
    
    # Impute CustomValueEstimate with median by VehicleType
    df['CustomValueEstimate'] = df.groupby('VehicleType')['CustomValueEstimate'].transform(
        lambda x: x.fillna(x.median())
    )
    
    # Create Unknown categories
    for col in ['Bank', 'AccountType', 'MaritalStatus', 'Gender']:
        df[col] = df[col].fillna('Unknown')
    
    # Infer NewVehicle from RegistrationYear
    current_year = 2015  # Dataset end year
    df['NewVehicle'] = df.apply(
        lambda row: 'Yes' if pd.isna(row['NewVehicle']) and (current_year - row['RegistrationYear']) <= 1 else row['NewVehicle'],
        axis=1
    )
    
    return df
```

---

### 1.3 Duplicate Detection & Removal

**Issue**: Multiple rows per policy (monthly transactions)  
**Strategy**: Aggregate to policy-level for cross-sectional analysis

```python
def aggregate_policy_level(df):
    """Aggregate monthly transactions to policy level"""
    agg_dict = {
        # Sum financial metrics
        'TotalPremium': 'sum',
        'TotalClaims': 'sum',
        'CalculatedPremiumPerTerm': 'mean',
        
        # Take most recent values
        'TransactionMonth': 'max',
        'Province': 'last',
        'VehicleType': 'last',
        
        # Keep constant attributes
        'Gender': 'first',
        'MaritalStatus': 'first',
        'make': 'first',
        'Model': 'first',
        # ... (all other non-changing fields)
    }
    
    df_policy = df.groupby('PolicyID').agg(agg_dict).reset_index()
    return df_policy
```

**Note**: For time-series analysis (Task 3), keep monthly granularity. For modeling (Task 4), use policy-level aggregation.

---

### 1.4 Data Type Optimization

**Current Memory Usage**: ~2,124 MB  
**Target Memory Usage**: < 1,000 MB

| Column | Current Type | Optimized Type | Rationale |
|--------|-------------|----------------|-----------|
| `TransactionMonth` | object | datetime64 | Enable temporal operations |
| `VehicleIntroDate` | object | datetime64 | Calculate vehicle age |
| Categorical columns (36) | object | category | Reduce memory by 50-70% |
| `PostalCode` | int64 | int32 | Sufficient range |
| `RegistrationYear` | int64 | int16 | Range: 1900-2015 |
| Boolean flags | object | bool | Memory efficient |

```python
def optimize_data_types(df):
    # Convert dates
    df['TransactionMonth'] = pd.to_datetime(df['TransactionMonth'])
    df['VehicleIntroDate'] = pd.to_datetime(df['VehicleIntroDate'])
    
    # Optimize integers
    df['PostalCode'] = df['PostalCode'].astype('int32')
    df['RegistrationYear'] = df['RegistrationYear'].astype('int16')
    
    # Convert to category
    categorical_cols = [
        'Citizenship', 'LegalType', 'Title', 'Language', 'Bank', 'AccountType',
        'MaritalStatus', 'Gender', 'Country', 'Province', 'MainCrestaZone',
        'SubCrestaZone', 'ItemType', 'VehicleType', 'make', 'Model', 'bodytype',
        'AlarmImmobiliser', 'TrackingDevice', 'CapitalOutstanding', 'NewVehicle',
        'WrittenOff', 'Rebuilt', 'Converted', 'TermFrequency', 'ExcessSelected',
        'CoverCategory', 'CoverType', 'CoverGroup', 'Section', 'Product',
        'StatutoryClass', 'StatutoryRiskType'
    ]
    
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype('category')
    
    return df
```

---

## 2. Feature Engineering

### 2.1 Target Variable: Loss Ratio

**Definition**: Ratio of claims paid to premiums collected  
**Formula**: `LossRatio = TotalClaims / TotalPremium`

```python
def create_loss_ratio(df):
    """Calculate loss ratio with handling for zero premiums"""
    df['LossRatio'] = np.where(
        df['TotalPremium'] > 0,
        df['TotalClaims'] / df['TotalPremium'],
        0  # If no premium, loss ratio is 0
    )
    
    # Cap extreme values
    df['LossRatio'] = df['LossRatio'].clip(upper=5.0)  # Cap at 500%
    
    return df
```

**Business Interpretation**:
- LossRatio < 0.4: Profitable (low-risk)
- LossRatio 0.4-0.7: Break-even (medium-risk)
- LossRatio > 0.7: Unprofitable (high-risk)

---

### 2.2 Claim Frequency

**Definition**: Binary indicator of whether a claim occurred  
**Formula**: `ClaimFrequency = 1 if TotalClaims > 0 else 0`

```python
def create_claim_frequency(df):
    """Binary indicator for claim occurrence"""
    df['ClaimFrequency'] = (df['TotalClaims'] > 0).astype(int)
    return df
```

**Use Case**: Classification models for claim prediction

---

### 2.3 Claim Severity

**Definition**: Average claim amount when claims occur  
**Formula**: `ClaimSeverity = TotalClaims / NumberOfClaims`

```python
def create_claim_severity(df):
    """Calculate average claim amount"""
    # For policy-level data, severity equals total claims when claim occurred
    df['ClaimSeverity'] = np.where(
        df['ClaimFrequency'] == 1,
        df['TotalClaims'],
        0
    )
    return df
```

**Use Case**: Regression models for claim amount prediction

---

### 2.4 Vehicle Age

**Definition**: Age of vehicle at transaction time  
**Formula**: `VehicleAge = TransactionYear - RegistrationYear`

```python
def create_vehicle_age(df):
    """Calculate vehicle age in years"""
    df['TransactionYear'] = df['TransactionMonth'].dt.year
    df['VehicleAge'] = df['TransactionYear'] - df['RegistrationYear']
    
    # Handle negative ages (data errors)
    df['VehicleAge'] = df['VehicleAge'].clip(lower=0, upper=50)
    
    return df
```

**Risk Relationship**: U-shaped - very new and very old vehicles have higher risk

---

### 2.5 Temporal Features

**Purpose**: Capture seasonality and trends

```python
def create_temporal_features(df):
    """Extract time-based features"""
    df['TransactionYear'] = df['TransactionMonth'].dt.year
    df['TransactionMonthNum'] = df['TransactionMonth'].dt.month
    df['TransactionQuarter'] = df['TransactionMonth'].dt.quarter
    df['TransactionDayOfYear'] = df['TransactionMonth'].dt.dayofyear
    
    # Create season
    df['Season'] = pd.cut(
        df['TransactionMonthNum'],
        bins=[0, 3, 6, 9, 12],
        labels=['Summer', 'Autumn', 'Winter', 'Spring']
    )
    
    return df
```

---

### 2.6 Security Score

**Purpose**: Quantify vehicle security level

```python
def create_security_score(df):
    """Calculate security score (0-2)"""
    df['SecurityScore'] = 0
    df.loc[df['AlarmImmobiliser'] == 'Yes', 'SecurityScore'] += 1
    df.loc[df['TrackingDevice'] == 'Yes', 'SecurityScore'] += 1
    
    return df
```

**Interpretation**: 0 = No security, 1 = Partial security, 2 = Full security

---

### 2.7 Premium-to-Value Ratio

**Purpose**: Assess pricing relative to vehicle value

```python
def create_premium_ratio(df):
    """Calculate annual premium as % of vehicle value"""
    df['PremiumToValueRatio'] = np.where(
        df['SumInsured'] > 0,
        (df['TotalPremium'] * 12) / df['SumInsured'],  # Annualize premium
        0
    )
    
    return df
```

**Typical Range**: 3-8% for comprehensive cover

---

### 2.8 Geographic Risk Features

**Purpose**: Encode geographic risk levels

```python
def create_geographic_features(df):
    """Create geographic risk indicators"""
    # Province risk (based on EDA loss ratios)
    high_risk_provinces = ['Limpopo', 'Mpumalanga', 'North West']
    low_risk_provinces = ['Western Cape', 'Gauteng']
    
    df['ProvinceRiskLevel'] = 'Medium'
    df.loc[df['Province'].isin(high_risk_provinces), 'ProvinceRiskLevel'] = 'High'
    df.loc[df['Province'].isin(low_risk_provinces), 'ProvinceRiskLevel'] = 'Low'
    
    return df
```

---

## 3. Categorical Encoding

### 3.1 One-Hot Encoding

**Use Case**: Tree-based models, neural networks  
**Columns**: Low-cardinality categoricals (< 10 unique values)

```python
def one_hot_encode(df, columns):
    """One-hot encode categorical variables"""
    df_encoded = pd.get_dummies(
        df,
        columns=columns,
        prefix=columns,
        drop_first=True  # Avoid multicollinearity
    )
    return df_encoded
```

**Recommended Columns**:
- `Gender` (3 values)
- `MaritalStatus` (5 values)
- `ProvinceRiskLevel` (3 values)
- `SecurityScore` (3 values)
- `Season` (4 values)

---

### 3.2 Label Encoding

**Use Case**: Ordinal relationships, tree-based models  
**Columns**: Ordinal categoricals

```python
from sklearn.preprocessing import LabelEncoder

def label_encode(df, columns):
    """Label encode ordinal variables"""
    le_dict = {}
    
    for col in columns:
        le = LabelEncoder()
        df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
        le_dict[col] = le
    
    return df, le_dict
```

**Recommended Columns**:
- `ExcessSelected` (ordinal: No excess < Low < Medium < High)
- `CoverType` (ordinal: Third Party < Third Party Fire & Theft < Comprehensive)

---

### 3.3 Target Encoding

**Use Case**: High-cardinality categoricals  
**Columns**: Province, PostalCode, make, Model

```python
def target_encode(df, column, target='LossRatio'):
    """Target encode using mean loss ratio"""
    target_means = df.groupby(column)[target].mean()
    df[f'{column}_target_encoded'] = df[column].map(target_means)
    
    # Fill missing with global mean
    df[f'{column}_target_encoded'].fillna(df[target].mean(), inplace=True)
    
    return df
```

**Note**: Apply only on training data, then map to validation/test to avoid leakage

---

## 4. Outlier Detection & Treatment

### 4.1 Outlier Detection Methods

#### IQR Method (Interquartile Range)
```python
def detect_outliers_iqr(df, column):
    """Detect outliers using IQR method"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    return outliers
```

#### Z-Score Method
```python
def detect_outliers_zscore(df, column, threshold=3):
    """Detect outliers using Z-score method"""
    z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
    outliers = z_scores > threshold
    return outliers
```

---

### 4.2 Outlier Treatment Strategy

| Column | Detection Method | Treatment | Rationale |
|--------|-----------------|-----------|-----------|
| `TotalPremium` | Percentile (99th) | **CAP** at 99th percentile | Preserve high-value policies |
| `TotalClaims` | Percentile (99th) | **CAP** at 99th percentile | Large claims are legitimate |
| `SumInsured` | Percentile (99th) | **CAP** at 99th percentile | Luxury vehicles exist |
| `LossRatio` | Cap at 5.0 | **CAP** | Ratios > 500% are data errors |
| `VehicleAge` | Cap at 50 | **CAP** | Age > 50 years is rare |
| `kilowatts` | IQR | **FLAG** | Keep for analysis, flag for review |

```python
def treat_outliers(df):
    """Cap outliers at percentile thresholds"""
    # Cap financial metrics at 99th percentile
    for col in ['TotalPremium', 'TotalClaims', 'SumInsured']:
        upper_limit = df[col].quantile(0.99)
        df[f'{col}_capped'] = df[col].clip(upper=upper_limit)
    
    # Cap loss ratio
    df['LossRatio'] = df['LossRatio'].clip(upper=5.0)
    
    # Cap vehicle age
    df['VehicleAge'] = df['VehicleAge'].clip(upper=50)
    
    # Flag extreme values for review
    df['has_outlier'] = (
        (df['TotalPremium'] > df['TotalPremium'].quantile(0.99)) |
        (df['TotalClaims'] > df['TotalClaims'].quantile(0.99))
    ).astype(int)
    
    return df
```

---

## 5. Feature Scaling

### 5.1 Standardization (Z-Score Normalization)

**Use Case**: Linear models, neural networks, distance-based algorithms  
**Formula**: `z = (x - μ) / σ`

```python
from sklearn.preprocessing import StandardScaler

def standardize_features(df, columns):
    """Standardize numerical features"""
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df, scaler
```

**Recommended Columns**:
- `TotalPremium`, `TotalClaims`, `SumInsured`
- `VehicleAge`, `kilowatts`, `cubiccapacity`
- `LossRatio`, `PremiumToValueRatio`

---

### 5.2 Min-Max Normalization

**Use Case**: Neural networks, algorithms sensitive to scale  
**Formula**: `x_norm = (x - x_min) / (x_max - x_min)`

```python
from sklearn.preprocessing import MinMaxScaler

def normalize_features(df, columns):
    """Normalize features to [0, 1] range"""
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df, scaler
```

---

### 5.3 Robust Scaling

**Use Case**: Data with outliers  
**Formula**: `x_scaled = (x - median) / IQR`

```python
from sklearn.preprocessing import RobustScaler

def robust_scale(df, columns):
    """Scale using median and IQR (robust to outliers)"""
    scaler = RobustScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df, scaler
```

**Recommended for**: Financial metrics with outliers

---

## 6. Transformations for Statistical Testing (Task 3)

### 6.1 Normality Transformations

**Purpose**: Meet ANOVA and t-test assumptions

```python
def apply_log_transform(df, columns):
    """Log transform for right-skewed data"""
    for col in columns:
        df[f'{col}_log'] = np.log1p(df[col])  # log(1 + x) to handle zeros
    return df

def apply_sqrt_transform(df, columns):
    """Square root transform for moderate skewness"""
    for col in columns:
        df[f'{col}_sqrt'] = np.sqrt(df[col])
    return df
```

**Apply to**:
- `TotalPremium_log`, `TotalClaims_log` (right-skewed)
- `LossRatio_sqrt` (moderate skewness)

---

### 6.2 Variance Stabilization

**Purpose**: Homogeneity of variance for ANOVA

```python
def variance_stabilize(df, column):
    """Box-Cox transformation for variance stabilization"""
    from scipy.stats import boxcox
    
    df[f'{column}_boxcox'], lambda_param = boxcox(df[column] + 1)
    return df, lambda_param
```

---

## 7. Transformations for Modeling (Task 4)

### 7.1 Polynomial Features

**Purpose**: Capture non-linear relationships

```python
from sklearn.preprocessing import PolynomialFeatures

def create_polynomial_features(df, columns, degree=2):
    """Create polynomial and interaction features"""
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    poly_features = poly.fit_transform(df[columns])
    
    feature_names = poly.get_feature_names_out(columns)
    df_poly = pd.DataFrame(poly_features, columns=feature_names, index=df.index)
    
    return pd.concat([df, df_poly], axis=1)
```

**Recommended Interactions**:
- `VehicleAge × SecurityScore`
- `TotalPremium × CoverType`
- `Province × VehicleType`

---

### 7.2 Binning for Tree Models

**Purpose**: Create categorical features from continuous variables

```python
def bin_continuous_features(df):
    """Bin continuous features into categories"""
    # Age bins
    df['VehicleAgeGroup'] = pd.cut(
        df['VehicleAge'],
        bins=[0, 2, 5, 10, 50],
        labels=['New', 'Recent', 'Mature', 'Old']
    )
    
    # Premium bins
    df['PremiumGroup'] = pd.qcut(
        df['TotalPremium'],
        q=4,
        labels=['Low', 'Medium', 'High', 'Very High']
    )
    
    return df
```

---

## 8. Train/Validation/Test Split

### 8.1 Stratified Split

**Purpose**: Maintain class distribution across splits

```python
from sklearn.model_selection import train_test_split

def split_data(df, target='LossRatio', test_size=0.15, val_size=0.15):
    """Split data into train/val/test with stratification"""
    # Create stratification bins for continuous target
    df['LossRatioBin'] = pd.qcut(df[target], q=5, labels=False, duplicates='drop')
    
    # First split: train+val vs test
    train_val, test = train_test_split(
        df,
        test_size=test_size,
        stratify=df['LossRatioBin'],
        random_state=42
    )
    
    # Second split: train vs val
    val_size_adjusted = val_size / (1 - test_size)
    train, val = train_test_split(
        train_val,
        test_size=val_size_adjusted,
        stratify=train_val['LossRatioBin'],
        random_state=42
    )
    
    # Drop temporary stratification column
    train = train.drop('LossRatioBin', axis=1)
    val = val.drop('LossRatioBin', axis=1)
    test = test.drop('LossRatioBin', axis=1)
    
    return train, val, test
```

**Split Ratios**: 70% train, 15% validation, 15% test

---

### 8.2 Temporal Split (Alternative)

**Purpose**: Respect temporal ordering for time-series analysis

```python
def temporal_split(df, train_end='2015-03-31', val_end='2015-06-30'):
    """Split data by time periods"""
    train = df[df['TransactionMonth'] <= train_end]
    val = df[(df['TransactionMonth'] > train_end) & (df['TransactionMonth'] <= val_end)]
    test = df[df['TransactionMonth'] > val_end]
    
    return train, val, test
```

---

## 9. Data Export

### 9.1 Parquet Format

**Advantages**: Compressed, columnar storage, preserves data types

```python
def save_processed_data(train, val, test, output_dir='data/processed'):
    """Save processed datasets to parquet format"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    train.to_parquet(f'{output_dir}/train.parquet', index=False, compression='snappy')
    val.to_parquet(f'{output_dir}/val.parquet', index=False, compression='snappy')
    test.to_parquet(f'{output_dir}/test.parquet', index=False, compression='snappy')
    
    print(f"Saved train: {len(train)} rows")
    print(f"Saved val: {len(val)} rows")
    print(f"Saved test: {len(test)} rows")
```

---

## 10. Pipeline Orchestration

### 10.1 Complete Pipeline

```python
def run_preprocessing_pipeline(input_file, output_dir='data/processed'):
    """Execute complete preprocessing pipeline"""
    # 1. Load data
    df = pd.read_csv(input_file, sep='|', low_memory=False)
    print(f"Loaded {len(df)} rows")
    
    # 2. Clean column names
    df = clean_column_names(df)
    
    # 3. Handle missing values
    df = handle_missing_values(df)
    
    # 4. Optimize data types
    df = optimize_data_types(df)
    
    # 5. Feature engineering
    df = create_loss_ratio(df)
    df = create_claim_frequency(df)
    df = create_claim_severity(df)
    df = create_vehicle_age(df)
    df = create_temporal_features(df)
    df = create_security_score(df)
    df = create_premium_ratio(df)
    df = create_geographic_features(df)
    
    # 6. Create risk segments
    df = create_risk_segments(df)  # From segmentation framework
    
    # 7. Outlier treatment
    df = treat_outliers(df)
    
    # 8. Split data
    train, val, test = split_data(df)
    
    # 9. Encode categoricals (on train, apply to val/test)
    # ... (encoding logic)
    
    # 10. Scale features (fit on train, transform val/test)
    # ... (scaling logic)
    
    # 11. Save processed data
    save_processed_data(train, val, test, output_dir)
    
    return train, val, test
```

---

## 11. Validation & Quality Checks

### 11.1 Data Quality Checks

```python
def validate_processed_data(df):
    """Run quality checks on processed data"""
    checks = {
        'no_missing_target': df['LossRatio'].isna().sum() == 0,
        'no_negative_premium': (df['TotalPremium'] >= 0).all(),
        'no_negative_claims': (df['TotalClaims'] >= 0).all(),
        'valid_loss_ratio': (df['LossRatio'] >= 0).all() and (df['LossRatio'] <= 5).all(),
        'valid_vehicle_age': (df['VehicleAge'] >= 0).all() and (df['VehicleAge'] <= 50).all(),
        'segments_assigned': df['RiskSegment'].isna().sum() == 0,
    }
    
    for check, passed in checks.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check}")
    
    return all(checks.values())
```

---

## Summary

This transformation plan provides a comprehensive, production-ready approach to preparing the insurance dataset for analysis and modeling. The pipeline is modular, allowing for easy updates and customization based on model performance and business requirements.

**Next Steps**:
1. Implement `preprocess.py` with all functions
2. Test pipeline on sample data
3. Validate output quality
4. Generate segment reports
5. Proceed to statistical testing (Task 3)

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Owner**: Data Science Team - ACIS Risk Analytics Project
