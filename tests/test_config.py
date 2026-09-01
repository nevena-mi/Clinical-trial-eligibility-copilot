import importlib
import sys
from unittest.mock import Mock

import dotenv
import pytest


def _load_config_without_dotenv(monkeypatch):
    monkeypatch.setattr(dotenv, "load_dotenv", lambda *_args, **_kwargs: None)
    sys.modules.pop("src.config", None)
    return importlib.import_module("src.config")


def test_config_imports_without_api_key_and_does_not_create_client(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    config = _load_config_without_dotenv(monkeypatch)

    assert config.OPENAI_API_KEY is None


def test_missing_api_key_fails_only_when_client_is_requested(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    config = _load_config_without_dotenv(monkeypatch)
    config.get_openai_client.cache_clear()

    with pytest.raises(config.ConfigurationError, match="OPENAI_API_KEY is required"):
        config.get_openai_client()


def test_client_creation_preserves_wrapping_and_metadata(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    config = _load_config_without_dotenv(monkeypatch)
    config.get_openai_client.cache_clear()
    raw_client = object()
    wrapped_client = object()
    openai_constructor = Mock(return_value=raw_client)
    wrapper = Mock(return_value=wrapped_client)
    monkeypatch.setattr(config, "OpenAI", openai_constructor)
    monkeypatch.setattr(config, "wrap_openai", wrapper)

    assert config.get_openai_client() is wrapped_client
    assert config.get_openai_client() is wrapped_client
    openai_constructor.assert_called_once_with(api_key="test-key")
    wrapper.assert_called_once_with(
        raw_client,
        tracing_extra={
            "metadata": {
                "application": "clinical-trial-eligibility-copilot",
                "environment": "capstone-poc",
                "data_classification": "public-synthetic",
                "decision_mode": "human-review-required",
            }
        },
    )


def test_missing_key_failure_is_not_cached(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    config = _load_config_without_dotenv(monkeypatch)
    config.get_openai_client.cache_clear()

    with pytest.raises(config.ConfigurationError):
        config.get_openai_client()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(config, "OpenAI", Mock(return_value=object()))
    monkeypatch.setattr(config, "wrap_openai", Mock(return_value=object()))
    assert config.get_openai_client() is not None
