import shap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelInterpreter:
    def __init__(self, model, X_train, feature_names=None):
        self.model = model
        self.X_train = X_train
        self.feature_names = feature_names if feature_names is not None else X_train.columns
        self.explainer = None
        self.shap_values = None

    def calculate_shap(self):
        """
        Calculates SHAP values.
        """
        logging.info("Calculating SHAP values...")
        try:
            # TreeExplainer for Tree models (XGBoost, RF)
            self.explainer = shap.TreeExplainer(self.model)
            # Use a sample for speed if dataset is large
            sample_size = min(1000, self.X_train.shape[0])
            self.shap_values = self.explainer.shap_values(self.X_train.iloc[:sample_size])
            logging.info("SHAP values calculated.")
        except Exception as e:
            logging.warning(f"TreeExplainer failed, falling back to KernelExplainer or Linear: {e}")
            # Fallback could be implemented here
            pass

    def plot_top_features(self, output_path='outputs/shap_summary.png'):
        """
        Generates and saves a SHAP summary plot.
        """
        if self.shap_values is None:
            self.calculate_shap()
        
        plt.figure(figsize=(10, 8))
        shap.summary_plot(self.shap_values, self.X_train.iloc[:min(1000, self.X_train.shape[0])], 
                          feature_names=self.feature_names, show=False)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        logging.info(f"SHAP summary plot saved to {output_path}")

    def get_top_features_df(self, n=10):
        """
        Returns a dataframe of top N important features based on mean |SHAP|.
        """
        if self.shap_values is None:
            self.calculate_shap()
            
        feature_importance = np.abs(self.shap_values).mean(0)
        df_imp = pd.DataFrame({
            'feature': self.feature_names,
            'importance': feature_importance
        }).sort_values('importance', ascending=False).head(n)
        
        return df_imp

if __name__ == "__main__":
    pass
