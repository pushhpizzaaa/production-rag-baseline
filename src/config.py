"""
Configuration Management for Baseline RAG Pipeline.
Uses Pydantic Settings to load settings from environment variables or .env file.
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # App Settings
    app_name: str = Field(default="RAG Baseline Pipeline", description="Service application name")
    app_env: str = Field(default="development", description="Environment: development, staging, production")
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    log_level: str = Field(default="INFO", description="Log level")

    # Storage Paths
    base_dir: Path = BASE_DIR
    data_dir: Path = BASE_DIR / "data"
    raw_data_dir: Path = BASE_DIR / "data" / "raw"
    eval_data_dir: Path = BASE_DIR / "data" / "eval"
    results_dir: Path = BASE_DIR / "eval" / "results"

    # Qdrant Vector Store
    # Empty QDRANT_URL defaults to local embedded storage in QDRANT_STORAGE_PATH
    qdrant_url: str = Field(default="", description="Remote Qdrant URL (e.g. http://localhost:6333)")
    qdrant_api_key: str = Field(default="", description="Qdrant Cloud API Key if using remote instance")
    qdrant_storage_path: str = Field(
        default=str(BASE_DIR / ".qdrant_data"),
        description="Local directory for embedded on-disk Qdrant storage"
    )
    collection_name: str = Field(default="rag_baseline_corpus", description="Qdrant collection name")

    # Embeddings Configuration
    embedding_provider: str = Field(default="fastembed", description="Provider: fastembed, mock")
    embedding_model: str = Field(default="BAAI/bge-small-en-v1.5", description="Embedding model name")
    embedding_dim: int = Field(default=384, description="Vector dimension of embedding model")

    # Chunker Configuration
    chunk_size_tokens: int = Field(default=500, description="Target chunk size in tokens (~350 words)")
    chunk_overlap_tokens: int = Field(default=50, description="Token overlap between consecutive chunks")

    # Retrieval Configuration
    top_k: int = Field(default=5, description="Number of top context chunks to retrieve")
    score_threshold: float = Field(default=0.25, description="Minimum cosine similarity score threshold")

    # LLM Generation Configuration (LiteLLM)
    llm_model: str = Field(default="gpt-4o-mini", description="LiteLLM model identifier")
    openai_api_key: str = Field(default="", description="OpenAI API Key")
    gemini_api_key: str = Field(default="", description="Google Gemini API Key")
    anthropic_api_key: str = Field(default="", description="Anthropic API Key")
    groq_api_key: str = Field(default="", description="Groq API Key")

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
