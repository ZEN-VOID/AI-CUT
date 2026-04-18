"""Shared default-model selection helpers for video provider scripts.

This module is the script-level source of truth for the cross-provider
families documented in `../runbooks/default-model-policy.md`.
Provider scripts still own their local model sets, filters, and alias
fallback chains; they should not re-implement the generic "pick the highest
eligible model" scaffolding.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import TypeVar

ModelT = TypeVar("ModelT", bound=str)


def _materialize(
    models: Iterable[ModelT],
    *,
    predicate: Callable[[ModelT], bool] | None = None,
) -> list[ModelT]:
    values = list(models)
    if predicate is None:
        return values
    return [model for model in values if predicate(model)]


def select_highest_model(
    models: Iterable[ModelT],
    *,
    sort_key: Callable[[ModelT], tuple],
    predicate: Callable[[ModelT], bool] | None = None,
    error_message: str = "未找到可作为默认值的模型",
) -> ModelT:
    """Return the highest eligible model under a provider-specific sort key."""

    eligible = _materialize(models, predicate=predicate)
    if not eligible:
        raise ValueError(error_message)
    return max(eligible, key=sort_key)


def select_latest_by_version(
    models: Iterable[ModelT],
    *,
    version_key: Callable[[ModelT], tuple[int, ...]],
    preferred_order: Sequence[ModelT] = (),
    predicate: Callable[[ModelT], bool] | None = None,
    error_message: str = "未找到可作为默认值的模型",
) -> ModelT:
    """Pick the latest version, then break ties with provider-specific aliases."""

    eligible = _materialize(models, predicate=predicate)
    if not eligible:
        raise ValueError(error_message)

    latest_version = max((version_key(model) for model in eligible), default=(0,))
    latest_models = [model for model in eligible if version_key(model) == latest_version]

    for preferred in preferred_order:
        if preferred in latest_models:
            return preferred

    return sorted(latest_models)[0]
