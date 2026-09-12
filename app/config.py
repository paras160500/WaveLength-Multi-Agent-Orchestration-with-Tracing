# =========================================================================================
#                                     Import/Init Statements
# =========================================================================================

from functools import lru_cache
from typing import List 
from pydantic_settings import BaseSettings, SettingsConfigDict

# =========================================================================================
#                                        Class Statements
# =========================================================================================

class Settings(BaseSettings):
    # LLM Provider
    openai_api_key : str = ""
    openai_model : str = "gpt-4o-mini"

    # Langsmith tracking
    langsmith_api_key : str = ""
    langsmith_tracing : bool = False 
    langsmith_project : str = "multi-agent-ai-system"

    # Sample Database
    chinook_sql_url : str = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"

    # API/CORS
    frontend_origins: str = "http://localhost:5173,http://localhost:3000,https://wavelength-multi-agent-orchestration.onrender.com"

    model_config = SettingsConfigDict(env_file=".env" , extra="ignore")

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.frontend_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
