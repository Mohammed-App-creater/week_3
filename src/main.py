import os
import sys
import pandas as pd
import logging
from src.data.data_loader import load_data
from src.features.preprocessing import prepare_modeling_data, encode_categorical, split_data
from src.models.modeling_severity import SeverityModeler
from src.models.modeling_premium import PremiumModeler


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_PATH = r"C:\Users\yoga\code\10_Academy\week_3\data\raw\MachineLearningRating_v3.txt"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    try:
        # 1. Load Data
        logging.info("--- 1. Data Loading ---")
        df = load_data(DATA_PATH)
        
        # 2. Preprocessing
        logging.info("--- 2. Preprocessing ---")
        df_clean = prepare_modeling_data(df)
        
        # 3. Model 1: Claim Severity (Regression)
        logging.info("--- 3. Severity Model (Regression) ---")
        # Filter for claims > 0
        df_claims = df_clean[df_clean['TotalClaims'] > 0].copy()
        
        # Encoder needs to be consistent, but for simplicity we re-fit here for regression task
        # Ideally we persistence the encoder or use a pipeline
        df_claims_encoded, _ = encode_categorical(df_claims, target_col='TotalClaims')
        print("df_claims_encoded shape:", df_claims_encoded.shape)
        print(df_claims_encoded.head())
        X_train_s, X_test_s, y_train_s, y_test_s = split_data(df_claims_encoded, 'TotalClaims')
        
        severity_modeler = SeverityModeler(df_claims_encoded)
        severity_modeler.train_evaluate(X_train_s, X_test_s, y_train_s, y_test_s)
        best_severity_path = severity_modeler.save_best_model()

        # 4. Model 2: Premium Optimization (Classification)
        logging.info("--- 4. Premium Model (Classification) ---")
        # Use full dataset
        df_clean['HasClaim'] = (df_clean['TotalClaims'] > 0).astype(int)
        
        df_full_encoded, _ = encode_categorical(df_clean, target_col='HasClaim')
        # Drop TotalClaims and other leakages
        if 'TotalClaims' in df_full_encoded.columns:
            df_full_encoded = df_full_encoded.drop(columns=['TotalClaims'])
            
        X_train_p, X_test_p, y_train_p, y_test_p = split_data(df_full_encoded, 'HasClaim')
        
        premium_modeler = PremiumModeler(df_full_encoded)
        premium_modeler.train_evaluate(X_train_p, X_test_p, y_train_p, y_test_p)
        
        # 5. Interpretation
        logging.info("--- 5. Interpretation (SHAP) ---")
        from src.evaluation.interpretation import ModelInterpreter
        
        # Interpret Severity Model (Random Forest or XGBoost usually best for SHAP)
        # Using the trained XGBoost model from the dictionary if available
        if 'XGBoost' in severity_modeler.results:
            model_to_interpret = severity_modeler.results['XGBoost']['model']
            interpreter = ModelInterpreter(model_to_interpret, X_train_s, feature_names=X_train_s.columns)
            interpreter.plot_top_features(output_path=os.path.join(OUTPUT_DIR, 'shap_severity.png'))
            top_features = interpreter.get_top_features_df()
            print("\nTop 10 Features for Severity Model:")
            print(top_features)

        # 6. Save Results
        logging.info("Pipeline Completed Successfully.")
        
    except Exception as e:
        logging.error(f"Pipeline Failed: {e}")
        raise e

if __name__ == "__main__":
    main()
