"""ML model utilities for cost prediction and denial classification"""
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
import logging
import os

logger = logging.getLogger(__name__)


# Procedure code benchmarks (simplified - in production, use comprehensive database)
PROCEDURE_BENCHMARKS = {
    "99213": 150,  # Office visit, established patient
    "99214": 200,  # Office visit, detailed
    "36415": 25,   # Venipuncture
    "80053": 50,   # Comprehensive metabolic panel
    "85025": 30,   # Complete blood count
    "93000": 100,  # EKG
    "45378": 2000, # Colonoscopy
    "27447": 15000, # Total knee arthroplasty
    "27130": 20000, # Total hip arthroplasty
    "99221": 500,  # Initial hospital care
    "99232": 400,  # Subsequent hospital care
    "99284": 800,  # Emergency department visit
}

# Insurance plan adjustments (allowed amount multipliers)
PLAN_ADJUSTMENT = {
    "medicare": 0.8,
    "medicaid": 0.7,
    "blue_cross": 0.85,
    "aetna": 0.88,
    "united_healthcare": 0.87,
    "cigna": 0.86,
    "self_pay": 1.0,
}

# Insurance plan copay rates
PLAN_COPAY_RATES = {
    "medicare": 0.2,
    "medicaid": 0.05,
    "blue_cross": 0.15,
    "aetna": 0.18,
    "united_healthcare": 0.17,
    "cigna": 0.16,
    "self_pay": 1.0,
}


class CostPredictor:
    """Cost prediction model using rule-based calculation (MVP)"""
    
    def __init__(self):
        self.procedure_benchmarks = PROCEDURE_BENCHMARKS
        self.plan_adjustments = PLAN_ADJUSTMENT
        self.copay_rates = PLAN_COPAY_RATES
    
    def estimate_cost(
        self,
        procedure_code: str,
        insurance_plan: str,
        deductible_used: float,
        annual_income: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Estimate patient out-of-pocket cost
        
        Args:
            procedure_code: CPT code
            insurance_plan: Insurance plan identifier
            deductible_used: Amount of deductible already used this year
            annual_income: Patient annual income (optional, for risk assessment)
        
        Returns:
            Dictionary with cost estimate and risk level
        """
        # Get base cost for procedure
        base_cost = self.procedure_benchmarks.get(procedure_code, 1000)
        
        # Adjust by insurance plan (allowed amount)
        plan_multiplier = self.plan_adjustments.get(insurance_plan, 0.9)
        allowed_amount = base_cost * plan_multiplier
        
        # Calculate patient share
        remaining_deductible = max(0, 5000 - deductible_used)  # Assume $5000 deductible
        copay_rate = self.copay_rates.get(insurance_plan, 0.2)
        
        if remaining_deductible > 0:
            # Patient pays deductible portion
            deductible_payment = min(remaining_deductible, allowed_amount)
            copay_payment = max(0, (allowed_amount - deductible_payment) * copay_rate)
            patient_oop = deductible_payment + copay_payment
        else:
            # Deductible met, patient pays copay only
            patient_oop = allowed_amount * copay_rate
        
        # Calculate confidence interval (±15%)
        confidence_interval = allowed_amount * 0.15
        
        # Categorize risk level
        risk_level = self._categorize_risk(patient_oop, annual_income)
        
        return {
            "estimated_total": round(allowed_amount, 2),
            "patient_oop": round(patient_oop, 2),
            "insurance_pays": round(allowed_amount - patient_oop, 2),
            "confidence_interval": round(confidence_interval, 2),
            "risk_level": risk_level,
            "procedure_code": procedure_code,
            "insurance_plan": insurance_plan
        }
    
    def _categorize_risk(self, patient_oop: float, annual_income: Optional[float]) -> str:
        """Categorize financial risk level"""
        if annual_income:
            oop_percentage = (patient_oop / annual_income) * 100
            if oop_percentage > 40:
                return "CATASTROPHIC"
            elif oop_percentage > 20:
                return "HIGH"
            elif oop_percentage > 10:
                return "MODERATE"
            else:
                return "LOW"
        
        # Fallback to absolute thresholds
        if patient_oop > 50000:
            return "CATASTROPHIC"
        elif patient_oop > 20000:
            return "HIGH"
        elif patient_oop > 5000:
            return "MODERATE"
        else:
            return "LOW"


class DenialClassifier:
    """Denial risk classifier using Random Forest (MVP with synthetic model)"""
    
    def __init__(self):
        self.model = None
        self.feature_names = [
            'procedure_code_numeric',
            'diagnosis_code_numeric',
            'payer_id_numeric',
            'patient_age_band',
            'gender_numeric',
            'place_of_service_numeric',
            'prior_auth_obtained',
            'modifier_present',
            'days_since_last_claim',
            'payer_denial_rate'
        ]
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load trained model or create synthetic one for MVP"""
        model_path = os.path.join(os.path.dirname(__file__), "../models/denial_classifier.pkl")
        
        try:
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("Loaded trained denial classifier model")
            else:
                # Create synthetic model for MVP
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.datasets import make_classification
                
                # Generate synthetic training data
                X, y = make_classification(
                    n_samples=1000,
                    n_features=10,
                    n_informative=8,
                    n_redundant=2,
                    random_state=42
                )
                
                # Train model
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
                self.model.fit(X, y)
                
                # Save model
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                joblib.dump(self.model, model_path)
                logger.info("Created synthetic denial classifier model")
        except Exception as e:
            logger.error(f"Error loading/creating model: {str(e)}")
            self.model = None
    
    def predict_denial(
        self,
        procedure_code: str,
        diagnosis_code: str,
        payer_id: str,
        patient_age: int,
        gender: str,
        place_of_service: str,
        prior_auth_obtained: bool,
        modifier_present: bool,
        days_since_last_claim: int,
        payer_denial_rate: float = 0.3
    ) -> Dict[str, Any]:
        """
        Predict claim denial risk
        
        Returns:
            Dictionary with prediction probability and risk factors
        """
        if not self.model:
            # Fallback to rule-based prediction
            return self._rule_based_prediction(
                prior_auth_obtained, modifier_present, payer_denial_rate
            )
        
        # Encode features (simplified encoding for MVP)
        features = self._encode_features(
            procedure_code, diagnosis_code, payer_id, patient_age,
            gender, place_of_service, prior_auth_obtained,
            modifier_present, days_since_last_claim, payer_denial_rate
        )
        
        # Predict
        features_array = np.array([features])
        probability = self.model.predict_proba(features_array)[0][1]  # Probability of denial
        predicted_class = probability > 0.5
        
        # Identify risk factors
        risk_factors = self._identify_risk_factors(
            prior_auth_obtained, modifier_present, payer_denial_rate,
            days_since_last_claim
        )
        
        return {
            "denial_probability": round(float(probability), 4),
            "predicted_class": "DENIED" if predicted_class else "APPROVED",
            "risk_factors": risk_factors,
            "confidence": round(abs(probability - 0.5) * 2, 4)  # Distance from 0.5
        }
    
    def _encode_features(
        self, procedure_code: str, diagnosis_code: str, payer_id: str,
        patient_age: int, gender: str, place_of_service: str,
        prior_auth_obtained: bool, modifier_present: bool,
        days_since_last_claim: int, payer_denial_rate: float
    ) -> list:
        """Encode features for model input"""
        # Simplified encoding (in production, use proper encoders)
        return [
            hash(procedure_code) % 1000 / 1000.0,
            hash(diagnosis_code) % 1000 / 1000.0,
            hash(payer_id) % 1000 / 1000.0,
            min(patient_age // 20, 4) / 4.0,  # Age band
            1.0 if gender.lower() == 'male' else 0.0,
            hash(place_of_service) % 1000 / 1000.0,
            1.0 if prior_auth_obtained else 0.0,
            1.0 if modifier_present else 0.0,
            min(days_since_last_claim / 365.0, 1.0),
            payer_denial_rate
        ]
    
    def _rule_based_prediction(
        self, prior_auth_obtained: bool, modifier_present: bool, payer_denial_rate: float
    ) -> Dict[str, Any]:
        """Fallback rule-based prediction"""
        base_probability = payer_denial_rate
        
        if not prior_auth_obtained:
            base_probability += 0.25
        
        if not modifier_present:
            base_probability += 0.1
        
        base_probability = min(base_probability, 0.95)
        
        risk_factors = []
        if not prior_auth_obtained:
            risk_factors.append("Prior authorization missing")
        if payer_denial_rate > 0.4:
            risk_factors.append("High payer denial rate")
        
        return {
            "denial_probability": round(base_probability, 4),
            "predicted_class": "DENIED" if base_probability > 0.5 else "APPROVED",
            "risk_factors": risk_factors,
            "confidence": 0.7
        }
    
    def _identify_risk_factors(
        self, prior_auth_obtained: bool, modifier_present: bool,
        payer_denial_rate: float, days_since_last_claim: int
    ) -> list:
        """Identify specific risk factors"""
        factors = []
        
        if not prior_auth_obtained:
            factors.append("Prior authorization missing for this procedure")
        
        if payer_denial_rate > 0.4:
            factors.append(f"High denial rate for this payer ({payer_denial_rate:.1%})")
        
        if days_since_last_claim < 30:
            factors.append("Recent similar claim may trigger frequency limit")
        
        if not modifier_present and payer_denial_rate > 0.3:
            factors.append("Missing modifier may cause coding denial")
        
        return factors


# Global model instances
cost_predictor = CostPredictor()
denial_classifier = DenialClassifier()

