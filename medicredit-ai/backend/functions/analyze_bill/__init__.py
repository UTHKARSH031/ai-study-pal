"""Azure Function: Analyze Bill"""
import azure.functions as func
import json
import logging
from shared.azure_services import azure_services
from shared.bill_analyzer import bill_analyzer
from shared.database import db

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Analyze medical bill for errors and anomalies"""
    try:
        # Parse request
        req_body = req.get_json()
        
        bill_id = req_body.get('bill_id')
        patient_id = req_body.get('patient_id')
        document_url = req_body.get('document_url')  # Blob storage URL
        line_items = req_body.get('line_items')  # Optional: pre-extracted items
        
        if not document_url and not line_items:
            return func.HttpResponse(
                json.dumps({"error": "Missing required field: document_url or line_items"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Extract bill data using Form Recognizer if document_url provided
        extracted_data = None
        if document_url:
            try:
                extracted_data = azure_services.analyze_document(document_url)
                # Convert extracted data to line items format
                line_items = _extract_line_items_from_document(extracted_data)
            except Exception as e:
                logger.warning(f"Form Recognizer failed, using provided line_items: {str(e)}")
                if not line_items:
                    raise
        
        # Analyze bill for anomalies
        analysis = bill_analyzer.analyze_bill(line_items)
        
        # Add metadata
        analysis['bill_id'] = bill_id
        analysis['patient_id'] = patient_id
        analysis['analysis_timestamp'] = str(func.datetime.datetime.now())
        
        # Save to database
        if patient_id and bill_id:
            try:
                analysis_data = {
                    'patient_id': patient_id,
                    'bill_id': bill_id,
                    'issues': analysis['issues'],
                    'total_savings': analysis['total_savings']
                }
                db.save_bill_analysis(analysis_data)
            except Exception as e:
                logger.warning(f"Failed to save analysis to database: {str(e)}")
        
        return func.HttpResponse(
            json.dumps(analysis, default=str),
            status_code=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        logger.error(f"Error in analyze_bill: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


def _extract_line_items_from_document(extracted_data: dict) -> list:
    """Convert Form Recognizer output to line items format"""
    line_items = []
    
    # Extract from tables (most bills have line items in tables)
    for table in extracted_data.get('tables', []):
        # Assume first row is header, rest are data
        if len(table) > 1:
            headers = table[0]
            for row in table[1:]:
                item = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        header_lower = header.lower()
                        if 'code' in header_lower or 'cpt' in header_lower:
                            item['code'] = row[i]
                        elif 'date' in header_lower:
                            item['date'] = row[i]
                        elif 'price' in header_lower or 'amount' in header_lower or 'charge' in header_lower:
                            try:
                                # Remove $ and commas, convert to float
                                price_str = str(row[i]).replace('$', '').replace(',', '')
                                item['price'] = float(price_str)
                            except:
                                item['price'] = 0
                        elif 'description' in header_lower or 'service' in header_lower:
                            item['description'] = row[i]
                
                if 'code' in item:  # Only add if we have a code
                    line_items.append(item)
    
    # If no tables, try key-value pairs
    if not line_items:
        kv_pairs = extracted_data.get('key_value_pairs', {})
        # Simplified extraction - in production, use more sophisticated parsing
        for key, value in kv_pairs.items():
            if 'code' in key.lower() or 'cpt' in key.lower():
                line_items.append({
                    'code': value,
                    'description': key,
                    'price': 0,
                    'date': ''
                })
    
    return line_items

