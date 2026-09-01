import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from langsmith.wrappers import wrap_openai

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"

load_dotenv(PROJECT_ROOT / ".env")

def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes"}

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_SCREENING_MODEL = os.getenv("SCREENING_MODEL", "gpt-4.1")
SCREENING_TEMPERATURE = float(os.getenv("SCREENING_TEMPERATURE", "0"))
PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v2_abstention_rules")
STORE_OPENAI_RESPONSES = _as_bool(os.getenv("STORE_OPENAI_RESPONSES", "false"))
EXPECTED_EVALUATION_ROWS = int(os.getenv("EXPECTED_EVALUATION_ROWS", "120"))

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_TRACING = _as_bool(os.getenv("LANGSMITH_TRACING", "false"))
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")

class ConfigurationError(RuntimeError):
    """Raised when model-call configuration is unavailable."""


@lru_cache(maxsize=1)
def get_openai_client():
    """Create and cache the wrapped OpenAI client on the first model call."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ConfigurationError(
            "OPENAI_API_KEY is required to make a model call. "
            "Set it in the project-root .env file or the process environment."
        )

    return wrap_openai(
        OpenAI(api_key=api_key),
        tracing_extra={
            "metadata": {
                "application": "clinical-trial-eligibility-copilot",
                "environment": "capstone-poc",
                "data_classification": "public-synthetic",
                "decision_mode": "human-review-required",
            }
        },
    )
