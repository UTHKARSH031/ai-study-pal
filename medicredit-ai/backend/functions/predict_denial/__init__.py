"""Azure Function: Predict Denial Risk"""
import azure.functions as func
import json
import logging
from shared.ml_models import denial_classifier
from shared.database import db

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Predict claim denial risk"""
    try:
        # Parse request
        req_body = req.get_json()
        
        claim_id = req_body.get('claim_id')
        procedure_code = req_body.get('procedure_code')
        diagnosis_code = req_body.get('diagnosis_code')
        payer_id = req_body.get('payer_id')
        patient_age = int(req_body.get('patient_age', 40))
        gender = req_body.get('gender', 'unknown')
        place_of_service = req_body.get('place_of_service', 'office')
        prior_auth_obtained = req_body.get('prior_auth_obtained', False)
        modifier_present = req_body.get('modifier_present', False)
        days_since_last_claim = int(req_body.get('days_since_last_claim', 365))
        payer_denial_rate = float(req_body.get('payer_denial_rate', 0.3))
        
        if not procedure_code or not diagnosis_code or not payer_id:
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: procedure_code, diagnosis_code, payer_id"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Get denial prediction
        prediction = denial_classifier.predict_denial(
            procedure_code=procedure_code,
            diagnosis_code=diagnosis_code,
            payer_id=payer_id,
            patient_age=patient_age,
            gender=gender,
            place_of_service=place_of_service,
            prior_auth_obtained=prior_auth_obtained,
            modifier_present=modifier_present,
            days_since_last_claim=days_since_last_claim,
            payer_denial_rate=payer_denial_rate
        )
        
        # Add claim metadata
        prediction['claim_id'] = claim_id
        prediction['procedure_code'] = procedure_code
        prediction['diagnosis_code'] = diagnosis_code
        prediction['payer_id'] = payer_id
        
        # Save to database if claim_id provided
        if claim_id:
            try:
                prediction_data = {
                    'claim_id': claim_id,
                    'denial_probability': prediction['denial_probability'],
                    'predicted_class': prediction['predicted_class'],
                    'risk_factors': prediction['risk_factors']
                }
                db.save_denial_prediction(prediction_data)
            except Exception as e:
                logger.warning(f"Failed to save prediction to database: {str(e)}")
        
        return func.HttpResponse(
            json.dumps(prediction, default=str),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logger.error(f"Error in predict_denial: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

