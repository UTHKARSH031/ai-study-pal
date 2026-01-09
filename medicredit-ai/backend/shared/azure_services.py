"""Azure service clients for MediCredit AI"""
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from openai import AzureOpenAI
from shared.config import Config
import logging

logger = logging.getLogger(__name__)


class AzureServices:
    """Wrapper for Azure AI services"""
    
    def __init__(self):
        # Form Recognizer client
        self.form_recognizer_client = None
        if Config.FORM_RECOGNIZER_ENDPOINT and Config.FORM_RECOGNIZER_KEY:
            self.form_recognizer_client = DocumentAnalysisClient(
                endpoint=Config.FORM_RECOGNIZER_ENDPOINT,
                credential=AzureKeyCredential(Config.FORM_RECOGNIZER_KEY)
            )
        
        # Text Analytics client
        self.text_analytics_client = None
        if Config.TEXT_ANALYTICS_ENDPOINT and Config.TEXT_ANALYTICS_KEY:
            self.text_analytics_client = TextAnalyticsClient(
                endpoint=Config.TEXT_ANALYTICS_ENDPOINT,
                credential=AzureKeyCredential(Config.TEXT_ANALYTICS_KEY)
            )
        
        # AI Search client
        self.search_client = None
        if Config.SEARCH_ENDPOINT and Config.SEARCH_KEY:
            self.search_client = SearchClient(
                endpoint=Config.SEARCH_ENDPOINT,
                index_name="assistance-programs",
                credential=AzureKeyCredential(Config.SEARCH_KEY)
            )
        
        # Azure OpenAI client
        self.openai_client = None
        if Config.OPENAI_ENDPOINT and Config.OPENAI_KEY:
            self.openai_client = AzureOpenAI(
                api_key=Config.OPENAI_KEY,
                api_version="2024-02-15-preview",
                azure_endpoint=Config.OPENAI_ENDPOINT
            )
    
    def analyze_document(self, document_url: str) -> dict:
        """Analyze medical bill using Form Recognizer"""
        if not self.form_recognizer_client:
            raise ValueError("Form Recognizer client not initialized")
        
        try:
            poller = self.form_recognizer_client.begin_analyze_document(
                model_id="prebuilt-document",
                document=document_url
            )
            result = poller.result()
            
            # Extract structured data from document
            extracted_data = {
                "pages": len(result.pages),
                "tables": [],
                "key_value_pairs": {},
                "line_items": []
            }
            
            # Extract tables (bill line items)
            for table_idx, table in enumerate(result.tables):
                table_data = []
                for row in table.rows:
                    row_data = []
                    for cell in row.cells:
                        row_data.append(cell.content)
                    table_data.append(row_data)
                extracted_data["tables"].append(table_data)
            
            # Extract key-value pairs
            for kv_pair in result.key_value_pairs:
                if kv_pair.key and kv_pair.value:
                    extracted_data["key_value_pairs"][kv_pair.key.content] = kv_pair.value.content
            
            return extracted_data
        except Exception as e:
            logger.error(f"Form Recognizer error: {str(e)}")
            raise
    
    def search_assistance_programs(self, query: str, filters: dict = None) -> list:
        """Search for financial assistance programs"""
        if not self.search_client:
            raise ValueError("AI Search client not initialized")
        
        try:
            search_options = {
                "query_type": QueryType.SEMANTIC,
                "semantic_configuration_name": "default",
                "top": 10
            }
            
            if filters:
                filter_string = " AND ".join([f"{k} eq '{v}'" for k, v in filters.items()])
                search_options["filter"] = filter_string
            
            results = self.search_client.search(
                search_text=query,
                **search_options
            )
            
            programs = []
            for result in results:
                programs.append({
                    "program_name": result.get("program_name", ""),
                    "description": result.get("description", ""),
                    "eligibility": result.get("eligibility", ""),
                    "coverage": result.get("coverage", ""),
                    "contact": result.get("contact", ""),
                    "score": result.get("@search.score", 0)
                })
            
            return programs
        except Exception as e:
            logger.error(f"AI Search error: {str(e)}")
            raise
    
    def generate_explanation(self, context: str, bill_items: list, issues: list) -> str:
        """Generate patient-friendly bill explanation using Azure OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        try:
            prompt = f"""You are a healthcare financial advisor. Explain the following medical bill analysis to a patient in simple, clear language.

Bill Context: {context}

Bill Items:
{chr(10).join([f"- {item}" for item in bill_items])}

Issues Found:
{chr(10).join([f"- {issue}" for issue in issues])}

Provide a friendly, empathetic explanation that:
1. Explains what each issue means in plain language
2. Suggests what the patient should do next
3. Uses no medical jargon
4. Is encouraging and supportive

Explanation:"""
            
            response = self.openai_client.chat.completions.create(
                model=Config.OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful healthcare financial advisor who explains medical bills in simple terms."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI error: {str(e)}")
            raise


# Global Azure services instance
azure_services = AzureServices()

