"""Configuration management for MediCredit AI backend"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # Azure Storage
    STORAGE_CONNECTION_STRING: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    
    # Form Recognizer
    FORM_RECOGNIZER_ENDPOINT: str = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT", "")
    FORM_RECOGNIZER_KEY: str = os.getenv("AZURE_FORM_RECOGNIZER_KEY", "")
    
    # Text Analytics
    TEXT_ANALYTICS_ENDPOINT: str = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT", "")
    TEXT_ANALYTICS_KEY: str = os.getenv("AZURE_TEXT_ANALYTICS_KEY", "")
    
    # AI Search
    SEARCH_ENDPOINT: str = os.getenv("AZURE_SEARCH_ENDPOINT", "")
    SEARCH_KEY: str = os.getenv("AZURE_SEARCH_KEY", "")
    
    # Azure OpenAI
    OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    OPENAI_KEY: str = os.getenv("AZURE_OPENAI_KEY", "")
    OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    
    # Azure SQL Database
    SQL_SERVER: str = os.getenv("AZURE_SQL_SERVER", "")
    SQL_DATABASE: str = os.getenv("AZURE_SQL_DATABASE", "")
    SQL_USERNAME: str = os.getenv("AZURE_SQL_USERNAME", "")
    SQL_PASSWORD: str = os.getenv("AZURE_SQL_PASSWORD", "")
    
    # Azure ML
    ML_ENDPOINT_COST_PREDICTOR: str = os.getenv("AZURE_ML_ENDPOINT_COST_PREDICTOR", "")
    ML_ENDPOINT_DENIAL_CLASSIFIER: str = os.getenv("AZURE_ML_ENDPOINT_DENIAL_CLASSIFIER", "")
    ML_KEY: str = os.getenv("AZURE_ML_KEY", "")
    
    # Application
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def get_sql_connection_string(cls) -> str:
        """Get SQL Server connection string"""
        return (
            f"Driver={{ODBC Driver 18 for SQL Server}};"
            f"Server={cls.SQL_SERVER};"
            f"Database={cls.SQL_DATABASE};"
            f"Uid={cls.SQL_USERNAME};"
            f"Pwd={cls.SQL_PASSWORD};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )

