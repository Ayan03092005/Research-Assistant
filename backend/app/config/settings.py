from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    ENV: str = "dev"
    PORT: int = 8000

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_EXP_MINUTES: int = 120

    OPENAI_API_KEY: str
    GEMINI_API_KEY: str | None = None

    CROSSREF_MAILTO: str = "you@example.com"
    UNPAYWALL_EMAIL: str = "you@example.com"
    SEMANTIC_SCHOLAR_API_KEY: str | None = None

    FEATURE_TRANSLATION: bool = True
    FEATURE_CONTRADICTION: bool = True
    FEATURE_REPLICATOR: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
