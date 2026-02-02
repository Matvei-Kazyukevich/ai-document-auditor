from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Application
    app_name: str = Field('AI-Document-Auditor')
    env: str = Field('dev')

    # Database
    database_url: str = Field(default='postgresql+psycopg2://postgres:postgres:3003@localhost:5432/ai_document_auditor_db')

    # Storage
    storage_backend: str = Field(default='local')
    storage_dir: str = Field(default='storage')

    # AI
    ollama_base_url: str = Field(default='http://localhost:11434')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()