"""Azure Function: Explain Bill"""
import azure.functions as func
import json
import logging
from shared.azure_services import azure_services

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Generate patient-friendly bill explanation using Azure OpenAI"""
    try:
        # Parse request
        req_body = req.get_json()
        
        bill_context = req_body.get('bill_context', '')
        bill_items = req_body.get('bill_items', [])
        issues = req_body.get('issues', [])
        patient_id = req_body.get('patient_id')
        
        if not bill_items and not issues:
            return func.HttpResponse(
                json.dumps({"error": "Missing required field: bill_items or issues"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Format bill items for explanation
        formatted_items = []
        for item in bill_items:
            if isinstance(item, dict):
                item_str = f"{item.get('code', 'N/A')}: {item.get('description', 'N/A')} - ${item.get('price', 0):.2f}"
            else:
                item_str = str(item)
            formatted_items.append(item_str)
        
        # Format issues for explanation
        formatted_issues = []
        for issue in issues:
            if isinstance(issue, dict):
                issue_str = issue.get('description', str(issue))
            else:
                issue_str = str(issue)
            formatted_issues.append(issue_str)
        
        # Generate explanation using Azure OpenAI
        try:
            explanation = azure_services.generate_explanation(
                context=bill_context or "Medical bill analysis",
                bill_items=formatted_items,
                issues=formatted_issues
            )
        except Exception as e:
            logger.warning(f"OpenAI failed, returning template explanation: {str(e)}")
            # Fallback explanation
            explanation = _generate_fallback_explanation(formatted_items, formatted_issues)
        
        result = {
            "explanation": explanation,
            "bill_items_count": len(bill_items),
            "issues_count": len(issues),
            "patient_id": patient_id,
            "generated_at": str(func.datetime.datetime.now())
        }
        
        return func.HttpResponse(
            json.dumps(result, default=str),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logger.error(f"Error in explain_bill: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


def _generate_fallback_explanation(bill_items: list, issues: list) -> str:
    """Generate fallback explanation when OpenAI is unavailable"""
    explanation = "We've analyzed your medical bill and found the following:\n\n"
    
    if issues:
        explanation += "Issues Found:\n"
        for i, issue in enumerate(issues, 1):
            explanation += f"{i}. {issue}\n"
        explanation += "\n"
    else:
        explanation += "No major issues were found in your bill.\n\n"
    
    explanation += "Next Steps:\n"
    explanation += "1. Review the flagged items with your healthcare provider\n"
    explanation += "2. Contact your insurance company if you have questions\n"
    explanation += "3. Consider requesting an itemized bill for detailed review\n"
    explanation += "4. If you believe there are errors, file an appeal with your insurance\n\n"
    explanation += "If you need help understanding any charges, please contact our support team."
    
    return explanation

