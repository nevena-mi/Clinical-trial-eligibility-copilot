import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from langsmith.wrappers import wrap_openai

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"

load_dotenv(PROJECT_ROOT / ".env")

def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} is missing from the project-root .env file.")
    return value

def _as_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes"}

OPENAI_API_KEY = _required_env("OPENAI_API_KEY")
DEFAULT_SCREENING_MODEL = os.getenv("SCREENING_MODEL", "gpt-4o-mini")
SCREENING_TEMPERATURE = float(os.getenv("SCREENING_TEMPERATURE", "0"))
PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v2_abstention_rules")
STORE_OPENAI_RESPONSES = _as_bool(os.getenv("STORE_OPENAI_RESPONSES", "false"))
EXPECTED_EVALUATION_ROWS = int(os.getenv("EXPECTED_EVALUATION_ROWS", "120"))

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_TRACING = _as_bool(os.getenv("LANGSMITH_TRACING", "false"))
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")

openai_client = wrap_openai(
    OpenAI(api_key=OPENAI_API_KEY),
    tracing_extra={
        "metadata": {
            "application": "clinical-trial-eligibility-copilot",
            "environment": "capstone-poc",
            "data_classification": "public-synthetic",
            "decision_mode": "human-review-required",
        }
    },
)