import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PremiumModeler:
    def __init__(self, data, target_col='HasClaim'):
        self.data = data
        self.target_col = target_col
        # Ensure target is present or created
        if target_col not in data.columns and 'TotalClaims' in data.columns:
            self.data[target_col] = (self.data['TotalClaims'] > 0).astype(int)
            
        self.models = {
            'LogisticRegression': LogisticRegression(max_iter=1000),
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, class_weight='balanced'),
            'XGBoost': XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42, n_jobs=-1, scale_pos_weight=10) # Adjust scale_pos_weight
        }
        self.results = {}

    def train_evaluate(self, X_train, X_test, y_train, y_test):
        """
        Trains and evaluates classification models.
        """
        logging.info("Starting Probability Model Training...")
        
        for name, model in self.models.items():
            logging.info(f"Training {name}...")
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]
            
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_prob)
            
            self.results[name] = {
                'Accuracy': acc,
                'Precision': prec,
                'Recall': rec,
                'F1': f1,
                'AUC': auc,
                'model': model
            }
            logging.info(f"{name} - AUC: {auc:.4f}, F1: {f1:.4f}")

    def calculate_risk_premium(self, X_data, severity_model, probability_model, base_premium=0):
        """
        Calculates Risk Premium = P(Claim) * E(Severity)
        """
        prob_claim = probability_model.predict_proba(X_data)[:, 1]
        exp_severity = severity_model.predict(X_data)
        
        risk_premium = prob_claim * exp_severity
        return risk_premium

if __name__ == "__main__":
    pass
