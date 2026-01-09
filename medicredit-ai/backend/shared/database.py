"""Database utilities for MediCredit AI"""
import pyodbc
from typing import Optional, List, Dict, Any
from shared.config import Config
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database connection and query utilities"""
    
    def __init__(self):
        self.connection_string = Config.get_sql_connection_string()
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = pyodbc.connect(self.connection_string)
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
        except Exception as e:
            logger.error(f"Query execution error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """Execute INSERT/UPDATE/DELETE query"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            logger.error(f"Update execution error: {str(e)}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def get_patient_by_id(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get patient information"""
        query = "SELECT * FROM Patients WHERE patient_id = ?"
        results = self.execute_query(query, (patient_id,))
        return results[0] if results else None
    
    def get_claim_by_id(self, claim_id: str) -> Optional[Dict[str, Any]]:
        """Get claim information"""
        query = "SELECT * FROM Claims WHERE claim_id = ?"
        results = self.execute_query(query, (claim_id,))
        return results[0] if results else None
    
    def save_cost_estimate(self, estimate_data: Dict[str, Any]) -> str:
        """Save cost estimate to database"""
        query = """
            INSERT INTO CostEstimates 
            (patient_id, procedure_code, insurance_plan, estimated_total, patient_oop, risk_level, confidence_interval)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            estimate_data.get('patient_id'),
            estimate_data.get('procedure_code'),
            estimate_data.get('insurance_plan'),
            estimate_data.get('estimated_total'),
            estimate_data.get('patient_oop'),
            estimate_data.get('risk_level'),
            estimate_data.get('confidence_interval')
        )
        self.execute_update(query, params)
        return "estimate_saved"
    
    def save_denial_prediction(self, prediction_data: Dict[str, Any]) -> str:
        """Save denial prediction to database"""
        query = """
            INSERT INTO DenialPredictions 
            (claim_id, denial_probability, predicted_class, risk_factors, timestamp)
            VALUES (?, ?, ?, ?, GETDATE())
        """
        params = (
            prediction_data.get('claim_id'),
            prediction_data.get('denial_probability'),
            prediction_data.get('predicted_class'),
            str(prediction_data.get('risk_factors', []))
        )
        self.execute_update(query, params)
        return "prediction_saved"
    
    def save_bill_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Save bill analysis results"""
        query = """
            INSERT INTO BillAnalyses 
            (patient_id, bill_id, issues_found, total_savings, analysis_timestamp)
            VALUES (?, ?, ?, ?, GETDATE())
        """
        params = (
            analysis_data.get('patient_id'),
            analysis_data.get('bill_id'),
            str(analysis_data.get('issues', [])),
            analysis_data.get('total_savings', 0)
        )
        self.execute_update(query, params)
        return "analysis_saved"


# Global database instance
db = Database()

