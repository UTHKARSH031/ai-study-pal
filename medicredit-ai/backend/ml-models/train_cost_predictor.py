"""Train cost prediction model using XGBoost"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_synthetic_data(n_samples=1000):
    """Generate synthetic training data for cost prediction"""
    np.random.seed(42)
    
    # Procedure codes
    procedure_codes = ["99213", "99214", "36415", "80053", "85025", "93000", 
                       "45378", "27447", "27130", "99221", "99232", "99284"]
    
    # Base costs for procedures
    base_costs = {
        "99213": 150, "99214": 200, "36415": 25, "80053": 50, "85025": 30,
        "93000": 100, "45378": 2000, "27447": 15000, "27130": 20000,
        "99221": 500, "99232": 400, "99284": 800
    }
    
    # Insurance plans
    insurance_plans = ["medicare", "medicaid", "blue_cross", "aetna", 
                       "united_healthcare", "cigna", "self_pay"]
    
    data = []
    
    for _ in range(n_samples):
        procedure_code = np.random.choice(procedure_codes)
        base_cost = base_costs[procedure_code]
        
        # Add variation to base cost
        cost_variation = np.random.normal(1.0, 0.2)
        adjusted_base = base_cost * cost_variation
        
        # Insurance plan adjustment
        insurance_plan = np.random.choice(insurance_plans)
        plan_multipliers = {
            "medicare": 0.8, "medicaid": 0.7, "blue_cross": 0.85,
            "aetna": 0.88, "united_healthcare": 0.87, "cigna": 0.86, "self_pay": 1.0
        }
        allowed_amount = adjusted_base * plan_multipliers[insurance_plan]
        
        # Deductible and copay
        deductible_used = np.random.uniform(0, 5000)
        remaining_deductible = max(0, 5000 - deductible_used)
        copay_rates = {
            "medicare": 0.2, "medicaid": 0.05, "blue_cross": 0.15,
            "aetna": 0.18, "united_healthcare": 0.17, "cigna": 0.16, "self_pay": 1.0
        }
        copay_rate = copay_rates[insurance_plan]
        
        if remaining_deductible > 0:
            deductible_payment = min(remaining_deductible, allowed_amount)
            copay_payment = max(0, (allowed_amount - deductible_payment) * copay_rate)
            patient_oop = deductible_payment + copay_payment
        else:
            patient_oop = allowed_amount * copay_rate
        
        # Encode features
        procedure_encoded = hash(procedure_code) % 1000
        insurance_encoded = hash(insurance_plan) % 100
        
        data.append({
            'procedure_code_encoded': procedure_encoded,
            'insurance_plan_encoded': insurance_encoded,
            'base_cost': adjusted_base,
            'deductible_used': deductible_used,
            'remaining_deductible': remaining_deductible,
            'allowed_amount': allowed_amount,
            'patient_oop': patient_oop
        })
    
    return pd.DataFrame(data)


def train_model():
    """Train XGBoost model for cost prediction"""
    logger.info("Generating synthetic training data...")
    df = generate_synthetic_data(n_samples=1000)
    
    # Features
    feature_columns = [
        'procedure_code_encoded',
        'insurance_plan_encoded',
        'base_cost',
        'deductible_used',
        'remaining_deductible'
    ]
    
    X = df[feature_columns]
    y = df['patient_oop']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    logger.info("Training XGBoost model...")
    model = xgb.XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    logger.info(f"Model Performance:")
    logger.info(f"  MAE: ${mae:.2f}")
    logger.info(f"  MSE: ${mse:.2f}")
    logger.info(f"  R²: {r2:.4f}")
    
    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "cost_predictor.pkl")
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")
    
    # Save feature names
    feature_names_path = os.path.join(model_dir, "cost_predictor_features.txt")
    with open(feature_names_path, 'w') as f:
        f.write('\n'.join(feature_columns))
    
    return model


if __name__ == "__main__":
    train_model()

