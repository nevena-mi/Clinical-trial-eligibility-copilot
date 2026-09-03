"""Reproducible model configurations for screening runs."""

from dataclasses import dataclass


class ModelConfigurationError(ValueError):
    """Raised when a requested model configuration is unavailable."""


@dataclass(frozen=True)
class ModelConfiguration:
    configuration_id: str
    model: str
    prompt_version: str
    reasoning_effort: str | None
    temperature: float | None


GPT41_V2 = ModelConfiguration(
    configuration_id="gpt41-v2",
    model="gpt-4.1",
    prompt_version="v2_abstention_rules",
    reasoning_effort=None,
    temperature=0,
)

GPT41_V3 = ModelConfiguration(
    configuration_id="gpt41-v3",
    model="gpt-4.1",
    prompt_version="v3_safety_and_label_rules",
    reasoning_effort=None,
    temperature=0,
)

GPT56SOL_MEDIUM_V2 = ModelConfiguration(
    configuration_id="gpt56sol-medium-v2",
    model="gpt-5.6-sol",
    prompt_version="v2_abstention_rules",
    reasoning_effort="medium",
    temperature=None,
)

GPT56TERRA_MEDIUM_V2 = ModelConfiguration(
    configuration_id="gpt56terra-medium-v2",
    model="gpt-5.6-terra",
    prompt_version="v2_abstention_rules",
    reasoning_effort="medium",
    temperature=None,
)

MODEL_CONFIGURATIONS = {
    GPT41_V2.configuration_id: GPT41_V2,
    GPT41_V3.configuration_id: GPT41_V3,
    GPT56SOL_MEDIUM_V2.configuration_id: GPT56SOL_MEDIUM_V2,
    GPT56TERRA_MEDIUM_V2.configuration_id: GPT56TERRA_MEDIUM_V2,
}


def get_model_configuration(configuration_id: str) -> ModelConfiguration:
    try:
        return MODEL_CONFIGURATIONS[configuration_id]
    except KeyError as error:
        raise ModelConfigurationError(
            f"Unknown model configuration: {configuration_id}."
        ) from error
