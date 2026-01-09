"""Azure Function: Health Check"""
import azure.functions as func
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "MediCredit AI Backend",
            "version": "1.0.0",
            "endpoints": {
                "estimate_cost": "/api/estimate-cost",
                "predict_denial": "/api/predict-denial",
                "analyze_bill": "/api/analyze-bill",
                "find_assistance": "/api/find-assistance",
                "explain_bill": "/api/explain-bill"
            }
        }
        
        return func.HttpResponse(
            json.dumps(health_status, default=str),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logger.error(f"Error in health_check: {str(e)}")
        return func.HttpResponse(
            json.dumps({"status": "error", "error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

