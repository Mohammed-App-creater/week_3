"""
Data Preprocessing Pipeline for ACIS Insurance Risk Analytics

This module provides a complete data transformation pipeline including:
- Data cleaning and missing value handling
- Feature engineering (loss ratio, claim metrics, vehicle age, etc.)
- Customer risk segmentation
- Categorical encoding
- Outlier detection and treatment
- Train/validation/test splitting
- Data export to parquet format

Author: Data Science Team - ACIS Risk Analytics Project
Date: December 2025
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings
warnings.filterwarnings('ignore')


class InsuranceDataPreprocessor:
    """Complete preprocessing pipeline for insurance data"""
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def clean_column_names(self, df):
        """Standardize column names to lowercase snake_case"""
        print("Cleaning column names...")
        df.columns = df.columns.str.strip()
        return df
    
    def handle_missing_values(self, df):
        """Handle missing values according to transformation plan"""
        print("Handling missing values...")
        
        # Drop columns with no value
        cols_to_drop = ['NumberOfVehiclesInFleet', 'CrossBorder']
        existing_cols_to_drop = [col for col in cols_to_drop if col in df.columns]
        df = df.drop(existing_cols_to_drop, axis=1)
        print(f"  Dropped {len(existing_cols_to_drop)} columns with excessive missing values")
        
        # Drop rows with missing critical vehicle info
        critical_cols = ['mmcode', 'VehicleType', 'make', 'Model']
        before_rows = len(df)
        df = df.dropna(subset=[col for col in critical_cols if col in df.columns])
        print(f"  Dropped {before_rows - len(df)} rows with missing critical vehicle info")
        
        # Impute vehicle condition fields
        for col in ['WrittenOff', 'Rebuilt', 'Converted']:
            if col in df.columns:
                df[col] = df[col].fillna('No')
        
        # Impute CustomValueEstimate with median by VehicleType
        if 'CustomValueEstimate' in df.columns and 'VehicleType' in df.columns:
            df['CustomValueEstimate'] = df.groupby('VehicleType')['CustomValueEstimate'].transform(
                lambda x: x.fillna(x.median())
            )
        
        # Create Unknown categories for demographic fields
        for col in ['Bank', 'AccountType', 'MaritalStatus', 'Gender']:
            if col in df.columns:
                df[col] = df[col].fillna('Unknown')
        
        # Impute CapitalOutstanding
        if 'CapitalOutstanding' in df.columns:
            df['CapitalOutstanding'] = df['CapitalOutstanding'].fillna('No')
        
        # Infer NewVehicle from RegistrationYear
        if 'NewVehicle' in df.columns and 'RegistrationYear' in df.columns:
            current_year = 2015  # Dataset end year
            df['NewVehicle'] = df.apply(
                lambda row: 'Yes' if pd.isna(row['NewVehicle']) and (current_year - row['RegistrationYear']) <= 1 
                else (row['NewVehicle'] if not pd.isna(row['NewVehicle']) else 'No'),
                axis=1
            )
        
        print(f"  Missing value handling complete. Remaining rows: {len(df)}")
        return df
    
    def optimize_data_types(self, df):
        """Optimize data types for memory efficiency"""
        print("Optimizing data types...")
        
        # Convert dates
        date_columns = ['TransactionMonth', 'VehicleIntroDate']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Optimize integers
        if 'PostalCode' in df.columns:
            df['PostalCode'] = df['PostalCode'].astype('int32')
        if 'RegistrationYear' in df.columns:
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
        
        print(f"  Data types optimized")
        return df
    
    def create_loss_ratio(self, df):
        """Calculate loss ratio with handling for zero premiums"""
        print("Creating loss ratio feature...")
        df['LossRatio'] = np.where(
            df['TotalPremium'] > 0,
            df['TotalClaims'] / df['TotalPremium'],
            0
        )
        # Cap extreme values
        df['LossRatio'] = df['LossRatio'].clip(upper=5.0)
        return df
    
    def create_claim_frequency(self, df):
        """Binary indicator for claim occurrence"""
        print("Creating claim frequency feature...")
        df['ClaimFrequency'] = (df['TotalClaims'] > 0).astype(int)
        return df
    
    def create_claim_severity(self, df):
        """Calculate average claim amount when claims occur"""
        print("Creating claim severity feature...")
        df['ClaimSeverity'] = np.where(
            df['ClaimFrequency'] == 1,
            df['TotalClaims'],
            0
        )
        return df
    
    def create_vehicle_age(self, df):
        """Calculate vehicle age in years"""
        print("Creating vehicle age feature...")
        if 'TransactionMonth' in df.columns and 'RegistrationYear' in df.columns:
            df['TransactionYear'] = df['TransactionMonth'].dt.year
            df['VehicleAge'] = df['TransactionYear'] - df['RegistrationYear']
            # Handle negative ages (data errors)
            df['VehicleAge'] = df['VehicleAge'].clip(lower=0, upper=50)
        return df
    
    def create_temporal_features(self, df):
        """Extract time-based features"""
        print("Creating temporal features...")
        if 'TransactionMonth' in df.columns:
            df['TransactionMonthNum'] = df['TransactionMonth'].dt.month
            df['TransactionQuarter'] = df['TransactionMonth'].dt.quarter
            
            # Create season
            df['Season'] = pd.cut(
                df['TransactionMonthNum'],
                bins=[0, 3, 6, 9, 12],
                labels=['Summer', 'Autumn', 'Winter', 'Spring']
            ).astype('category')
        return df
    
    def create_security_score(self, df):
        """Calculate security score (0-2)"""
        print("Creating security score feature...")
        df['SecurityScore'] = 0
        if 'AlarmImmobiliser' in df.columns:
            df.loc[df['AlarmImmobiliser'] == 'Yes', 'SecurityScore'] += 1
        if 'TrackingDevice' in df.columns:
            df.loc[df['TrackingDevice'] == 'Yes', 'SecurityScore'] += 1
        return df
    
    def create_premium_ratio(self, df):
        """Calculate annual premium as % of vehicle value"""
        print("Creating premium-to-value ratio feature...")
        if 'TotalPremium' in df.columns and 'SumInsured' in df.columns:
            df['PremiumToValueRatio'] = np.where(
                df['SumInsured'] > 0,
                (df['TotalPremium'] * 12) / df['SumInsured'],
                0
            )
        return df
    
    def create_geographic_features(self, df):
        """Create geographic risk indicators"""
        print("Creating geographic features...")
        if 'Province' in df.columns:
            high_risk_provinces = ['Limpopo', 'Mpumalanga', 'North West']
            low_risk_provinces = ['Western Cape', 'Gauteng']
            
            df['ProvinceRiskLevel'] = 'Medium'
            df.loc[df['Province'].isin(high_risk_provinces), 'ProvinceRiskLevel'] = 'High'
            df.loc[df['Province'].isin(low_risk_provinces), 'ProvinceRiskLevel'] = 'Low'
            df['ProvinceRiskLevel'] = df['ProvinceRiskLevel'].astype('category')
        return df
    
    def create_risk_segments(self, df):
        """Assign customers to risk segments based on segmentation framework"""
        print("Creating risk segments...")
        
        def assign_risk_segment(row):
            score = 0
            
            # Demographic (1 point)
            if row.get('MaritalStatus') == 'Married' or row.get('Gender') == 'Female':
                score += 1
            
            # Geographic (1 point)
            if row.get('Province') in ['Western Cape', 'Gauteng']:
                score += 1
            
            # Vehicle Type (1 point)
            if row.get('VehicleType') in ['Sedan', 'Light Commercial Vehicle']:
                score += 1
            
            # Vehicle Age (1 point)
            if 'VehicleAge' in row and 2 <= row['VehicleAge'] <= 5:
                score += 1
            
            # Security (1 point)
            if row.get('SecurityScore', 0) == 2:
                score += 1
            
            # Claims (1 point)
            if row.get('TotalClaims', 0) == 0:
                score += 1
            
            # Coverage (1 point) - simplified check
            if row.get('CoverType') == 'Comprehensive':
                score += 1
            
            # Vehicle Condition (1 point)
            if row.get('WrittenOff') == 'No' and row.get('Rebuilt') == 'No':
                score += 1
            
            # Apply exclusion rules
            if (row.get('TotalClaims', 0) > 0 and row.get('ClaimFrequency', 0) > 0) or \
               (row.get('LossRatio', 0) > 0.8) or \
               (row.get('WrittenOff') == 'Yes') or \
               (row.get('VehicleType') in ['Motorcycle', 'Taxi']) or \
               (row.get('VehicleAge', 0) > 15):
                return 'High-Risk'
            
            # Assign segment based on score
            if score >= 5:
                return 'Low-Risk'
            elif score >= 3:
                return 'Medium-Risk'
            else:
                return 'High-Risk'
        
        df['RiskSegment'] = df.apply(assign_risk_segment, axis=1)
        df['RiskSegment'] = df['RiskSegment'].astype('category')
        
        # Print segment distribution
        print("\n  Risk Segment Distribution:")
        segment_counts = df['RiskSegment'].value_counts()
        for segment, count in segment_counts.items():
            pct = (count / len(df)) * 100
            print(f"    {segment}: {count:,} ({pct:.1f}%)")
        
        return df
    
    def detect_outliers(self, df, column):
        """Detect outliers using IQR method"""
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
        return outliers
    
    def treat_outliers(self, df):
        """Cap outliers at percentile thresholds"""
        print("Treating outliers...")
        
        # Cap financial metrics at 99th percentile
        for col in ['TotalPremium', 'TotalClaims', 'SumInsured']:
            if col in df.columns:
                upper_limit = df[col].quantile(0.99)
                df[f'{col}_capped'] = df[col].clip(upper=upper_limit)
                outliers = (df[col] > upper_limit).sum()
                print(f"  Capped {outliers} outliers in {col}")
        
        # Flag extreme values for review
        df['has_outlier'] = 0
        if 'TotalPremium' in df.columns and 'TotalClaims' in df.columns:
            df['has_outlier'] = (
                (df['TotalPremium'] > df['TotalPremium'].quantile(0.99)) |
                (df['TotalClaims'] > df['TotalClaims'].quantile(0.99))
            ).astype(int)
        
        return df
    
    def encode_categorical(self, df, train_mode=True):
        """Encode categorical variables"""
        print("Encoding categorical variables...")
        
        # One-hot encode low-cardinality categoricals
        one_hot_cols = ['Gender', 'MaritalStatus', 'ProvinceRiskLevel', 'Season']
        existing_one_hot = [col for col in one_hot_cols if col in df.columns]
        
        if existing_one_hot:
            df = pd.get_dummies(df, columns=existing_one_hot, prefix=existing_one_hot, drop_first=True)
            print(f"  One-hot encoded {len(existing_one_hot)} columns")
        
        return df
    
    def split_data(self, df, test_size=0.15, val_size=0.15):
        """Split data into train/val/test with stratification"""
        print("\nSplitting data into train/val/test sets...")
        
        # Create stratification bins for loss ratio
        df['LossRatioBin'] = pd.qcut(df['LossRatio'], q=5, labels=False, duplicates='drop')
        
        # First split: train+val vs test
        train_val, test = train_test_split(
            df,
            test_size=test_size,
            stratify=df['LossRatioBin'],
            random_state=self.random_state
        )
        
        # Second split: train vs val
        val_size_adjusted = val_size / (1 - test_size)
        train, val = train_test_split(
            train_val,
            test_size=val_size_adjusted,
            stratify=train_val['LossRatioBin'],
            random_state=self.random_state
        )
        
        # Drop temporary stratification column
        train = train.drop('LossRatioBin', axis=1)
        val = val.drop('LossRatioBin', axis=1)
        test = test.drop('LossRatioBin', axis=1)
        
        print(f"  Train set: {len(train):,} rows ({len(train)/len(df)*100:.1f}%)")
        print(f"  Validation set: {len(val):,} rows ({len(val)/len(df)*100:.1f}%)")
        print(f"  Test set: {len(test):,} rows ({len(test)/len(df)*100:.1f}%)")
        
        return train, val, test
    
    def save_processed_data(self, train, val, test, output_dir='data/processed'):
        """Save processed datasets to parquet format"""
        print(f"\nSaving processed data to {output_dir}...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        train.to_parquet(f'{output_dir}/train.parquet', index=False, compression='snappy')
        val.to_parquet(f'{output_dir}/val.parquet', index=False, compression='snappy')
        test.to_parquet(f'{output_dir}/test.parquet', index=False, compression='snappy')
        
        print(f"  ✓ Saved train.parquet: {len(train):,} rows")
        print(f"  ✓ Saved val.parquet: {len(val):,} rows")
        print(f"  ✓ Saved test.parquet: {len(test):,} rows")
        
        # Save summary statistics
        summary = {
            'train_rows': len(train),
            'val_rows': len(val),
            'test_rows': len(test),
            'total_rows': len(train) + len(val) + len(test),
            'train_pct': len(train) / (len(train) + len(val) + len(test)) * 100,
            'val_pct': len(val) / (len(train) + len(val) + len(test)) * 100,
            'test_pct': len(test) / (len(train) + len(val) + len(test)) * 100,
        }
        
        summary_df = pd.DataFrame([summary])
        summary_df.to_csv(f'{output_dir}/split_summary.csv', index=False)
        print(f"  ✓ Saved split_summary.csv")
    
    def validate_processed_data(self, df):
        """Run quality checks on processed data"""
        print("\nValidating processed data...")
        
        checks = {
            'no_missing_target': df['LossRatio'].isna().sum() == 0,
            'no_negative_premium': (df['TotalPremium'] >= 0).all(),
            'no_negative_claims': (df['TotalClaims'] >= 0).all(),
            'valid_loss_ratio': (df['LossRatio'] >= 0).all() and (df['LossRatio'] <= 5).all(),
            'segments_assigned': df['RiskSegment'].isna().sum() == 0,
        }
        
        if 'VehicleAge' in df.columns:
            checks['valid_vehicle_age'] = (df['VehicleAge'] >= 0).all() and (df['VehicleAge'] <= 50).all()
        
        all_passed = True
        for check, passed in checks.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status}: {check}")
            if not passed:
                all_passed = False
        
        return all_passed
    
    def run_pipeline(self, input_file, output_dir='data/processed'):
        """Execute complete preprocessing pipeline"""
        print("="*80)
        print("ACIS INSURANCE DATA PREPROCESSING PIPELINE")
        print("="*80)
        
        # 1. Load data
        print(f"\nLoading data from {input_file}...")
        df = pd.read_csv(input_file, sep='|', low_memory=False)
        print(f"  Loaded {len(df):,} rows × {len(df.columns)} columns")
        
        # 2. Clean column names
        df = self.clean_column_names(df)
        
        # 3. Handle missing values
        df = self.handle_missing_values(df)
        
        # 4. Optimize data types
        df = self.optimize_data_types(df)
        
        # 5. Feature engineering
        print("\n" + "="*80)
        print("FEATURE ENGINEERING")
        print("="*80)
        df = self.create_loss_ratio(df)
        df = self.create_claim_frequency(df)
        df = self.create_claim_severity(df)
        df = self.create_vehicle_age(df)
        df = self.create_temporal_features(df)
        df = self.create_security_score(df)
        df = self.create_premium_ratio(df)
        df = self.create_geographic_features(df)
        
        # 6. Create risk segments
        print("\n" + "="*80)
        print("RISK SEGMENTATION")
        print("="*80)
        df = self.create_risk_segments(df)
        
        # 7. Outlier treatment
        print("\n" + "="*80)
        print("OUTLIER TREATMENT")
        print("="*80)
        df = self.treat_outliers(df)
        
        # 8. Validate data
        print("\n" + "="*80)
        print("DATA VALIDATION")
        print("="*80)
        validation_passed = self.validate_processed_data(df)
        
        if not validation_passed:
            print("\n⚠ WARNING: Some validation checks failed. Review data before proceeding.")
        
        # 9. Encode categoricals
        print("\n" + "="*80)
        print("CATEGORICAL ENCODING")
        print("="*80)
        df = self.encode_categorical(df)
        
        # 10. Split data
        print("\n" + "="*80)
        print("DATA SPLITTING")
        print("="*80)
        train, val, test = self.split_data(df)
        
        # 11. Save processed data
        print("\n" + "="*80)
        print("SAVING PROCESSED DATA")
        print("="*80)
        self.save_processed_data(train, val, test, output_dir)
        
        print("\n" + "="*80)
        print("PREPROCESSING PIPELINE COMPLETE")
        print("="*80)
        print(f"\n✓ Processed datasets saved to: {output_dir}/")
        print(f"✓ Train set: {len(train):,} rows")
        print(f"✓ Validation set: {len(val):,} rows")
        print(f"✓ Test set: {len(test):,} rows")
        print(f"✓ Total: {len(train) + len(val) + len(test):,} rows")
        
        return train, val, test


def main():
    """Main execution function"""
    # Configuration
    INPUT_FILE = 'C:/Users/yoga/code/10_Academy/week_3/data/raw/MachineLearningRating_v3.txt'
    OUTPUT_DIR = 'C:/Users/yoga/code/10_Academy/week_3/data/processed'
    
    # Initialize preprocessor
    preprocessor = InsuranceDataPreprocessor(random_state=42)
    
    # Run pipeline
    train, val, test = preprocessor.run_pipeline(INPUT_FILE, OUTPUT_DIR)
    
    print("\n" + "="*80)
    print("NEXT STEPS")
    print("="*80)
    print("1. Review processed datasets in data/processed/")
    print("2. Run segment_report.py to generate segment analysis")
    print("3. Proceed to Task 3 for statistical hypothesis testing")
    print("="*80)


if __name__ == "__main__":
    main()
