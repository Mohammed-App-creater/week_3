import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SeverityModeler:
    def __init__(self, data, target_col='TotalClaims'):
        self.data = data
        self.target_col = target_col
        self.models = {
            'LinearRegression': LinearRegression(),
            'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
            'XGBoost': XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42, n_jobs=-1)
        }
        self.results = {}
        self.best_model = None

    def train_evaluate(self, X_train, X_test, y_train, y_test):
        """
        Trains and evaluates all defined models.
        """
        logging.info("Starting Severity Model Training...")
        
        for name, model in self.models.items():
            logging.info(f"Training {name}...")
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.results[name] = {
                'RMSE': rmse,
                'MAE': mae,
                'R2': r2,
                'model': model
            }
            logging.info(f"{name} - RMSE: {rmse:.2f}, R2: {r2:.4f}")

    def save_best_model(self, output_dir='models'):
        """
        Saves the best model based on RMSE.
        """
        if not self.results:
            logging.warning("No models trained yet.")
            return

        best_name = min(self.results, key=lambda x: self.results[x]['RMSE'])
        self.best_model = self.results[best_name]['model']
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        path = os.path.join(output_dir, f'best_severity_model_{best_name}.joblib')
        joblib.dump(self.best_model, path)
        logging.info(f"Examples of {best_name} saved to {path}")
        return path

if __name__ == "__main__":
    # Test stub
    pass
