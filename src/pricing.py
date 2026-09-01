"""Model-aware token pricing for evaluation reporting."""

from dataclasses import dataclass
from numbers import Integral


class PricingError(ValueError):
    """Raised when model pricing is unavailable or token values are invalid."""


@dataclass(frozen=True)
class ModelPricing:
    model: str
    input_usd_per_million: float
    output_usd_per_million: float
    source: str
    checked_date: str


PRICING = {
    "gpt-4.1": ModelPricing(
        model="gpt-4.1",
        input_usd_per_million=2.00,
        output_usd_per_million=8.00,
        source="https://developers.openai.com/api/docs/models/gpt-4.1",
        checked_date="2026-09-01",
    ),
    "gpt-5.6-sol": ModelPricing(
        model="gpt-5.6-sol",
        input_usd_per_million=4.00,
        output_usd_per_million=20.00,
        source="https://developers.openai.com/api/docs/models/gpt-5.6-sol",
        checked_date="2026-09-01",
    ),
}


def get_model_pricing(model: str) -> ModelPricing:
    if not isinstance(model, str) or not model.strip():
        raise PricingError("A non-empty model is required for pricing.")
    try:
        return PRICING[model]
    except KeyError as error:
        raise PricingError(f"No pricing is registered for model {model!r}.") from error


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = get_model_pricing(model)
    if not isinstance(input_tokens, Integral) or not isinstance(output_tokens, Integral):
        raise PricingError("Token counts must be integers for cost estimation.")
    if input_tokens < 0 or output_tokens < 0:
        raise PricingError("Token counts cannot be negative.")
    return (
        int(input_tokens) * pricing.input_usd_per_million
        + int(output_tokens) * pricing.output_usd_per_million
    ) / 1_000_000
