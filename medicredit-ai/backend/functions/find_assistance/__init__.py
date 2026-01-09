"""Azure Function: Find Assistance Programs"""
import azure.functions as func
import json
import logging
from shared.azure_services import azure_services

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Find financial assistance programs for patient"""
    try:
        # Parse request
        req_body = req.get_json()
        
        query = req_body.get('query', '')  # Search query (e.g., "cancer financial assistance")
        condition = req_body.get('condition', '')  # Medical condition
        income_level = req_body.get('income_level', '')  # Income bracket
        location = req_body.get('location', '')  # Patient location
        patient_id = req_body.get('patient_id')
        
        # Build search query if not provided
        if not query:
            query_parts = []
            if condition:
                query_parts.append(condition)
            if income_level:
                query_parts.append(income_level)
            if location:
                query_parts.append(location)
            query = " ".join(query_parts) if query_parts else "financial assistance programs"
        
        # Build filters
        filters = {}
        if condition:
            filters['condition'] = condition
        if income_level:
            filters['income_level'] = income_level
        if location:
            filters['location'] = location
        
        # Search for assistance programs
        try:
            programs = azure_services.search_assistance_programs(query, filters if filters else None)
        except Exception as e:
            logger.warning(f"AI Search failed, returning mock data: {str(e)}")
            # Fallback to mock data for MVP
            programs = _get_mock_assistance_programs(condition, income_level)
        
        # Add metadata
        result = {
            "programs": programs,
            "total_programs": len(programs),
            "query": query,
            "filters": filters,
            "patient_id": patient_id
        }
        
        return func.HttpResponse(
            json.dumps(result, default=str),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logger.error(f"Error in find_assistance: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


def _get_mock_assistance_programs(condition: str = '', income_level: str = '') -> list:
    """Mock assistance programs for MVP when AI Search is not available"""
    return [
        {
            "program_name": "HealthWell Foundation",
            "description": "Provides financial assistance to eligible patients for copays, premiums, and deductibles",
            "eligibility": "Income up to 400% of Federal Poverty Level, diagnosed condition",
            "coverage": "Copays, deductibles, premiums",
            "contact": "1-800-675-8416",
            "score": 0.95
        },
        {
            "program_name": "Patient Access Network (PAN) Foundation",
            "description": "Helps underinsured people with life-threatening, chronic, and rare diseases",
            "eligibility": "Income up to 500% FPL, insurance coverage required",
            "coverage": "Out-of-pocket costs for medications",
            "contact": "1-866-316-7263",
            "score": 0.90
        },
        {
            "program_name": "NeedyMeds",
            "description": "Free information on programs that help people who cannot afford medications",
            "eligibility": "Varies by program",
            "coverage": "Prescription assistance, drug discount cards",
            "contact": "www.needymeds.org",
            "score": 0.85
        },
        {
            "program_name": "Medicare Extra Help",
            "description": "Helps pay for Medicare prescription drug costs",
            "eligibility": "Medicare Part D enrollees, income and resource limits apply",
            "coverage": "Prescription drug costs",
            "contact": "1-800-MEDICARE",
            "score": 0.80
        }
    ]

