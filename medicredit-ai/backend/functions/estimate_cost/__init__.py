"""Azure Function: Estimate Cost"""
import azure.functions as func
import json
import logging
from shared.ml_models import cost_predictor
from shared.database import db

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Estimate patient out-of-pocket cost"""
    try:
        # Parse request
        req_body = req.get_json()
        
        procedure_code = req_body.get('procedure_code')
        insurance_plan = req_body.get('insurance_plan')
        deductible_used = float(req_body.get('deductible_used', 0))
        annual_income = req_body.get('annual_income')
        patient_id = req_body.get('patient_id')
        
        if not procedure_code or not insurance_plan:
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: procedure_code, insurance_plan"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Get cost estimate
        estimate = cost_predictor.estimate_cost(
            procedure_code=procedure_code,
            insurance_plan=insurance_plan,
            deductible_used=deductible_used,
            annual_income=annual_income
        )
        
        # Save to database if patient_id provided
        if patient_id:
            try:
                estimate_data = {
                    'patient_id': patient_id,
                    'procedure_code': procedure_code,
                    'insurance_plan': insurance_plan,
                    'estimated_total': estimate['estimated_total'],
                    'patient_oop': estimate['patient_oop'],
                    'risk_level': estimate['risk_level'],
                    'confidence_interval': estimate['confidence_interval']
                }
                db.save_cost_estimate(estimate_data)
            except Exception as e:
                logger.warning(f"Failed to save estimate to database: {str(e)}")
        
        return func.HttpResponse(
            json.dumps(estimate, default=str),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logger.error(f"Error in estimate_cost: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

