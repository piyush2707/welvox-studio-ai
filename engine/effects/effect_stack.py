"""Welvox Studio AI - Multi-effect stack builder."""

from engine.effects.vfx_engine import build_vfx_filters


def build_effect_stack(effects):
    """Build one FFmpeg filter chain from an ordered effect list.

    Each item must contain:
        operation: registered VFX operation
        parameters: optional effect parameters

    Effects are applied in list order.
    """
    if not isinstance(effects, list):
        raise ValueError("Effects must be provided as a list.")

    if not effects:
        raise ValueError("At least one effect is required.")

    filters = []

    for index, effect in enumerate(effects):
        if not isinstance(effect, dict):
            raise ValueError(
                f"Effect at position {index} must be an object."
            )

        operation = effect.get("operation")

        if not isinstance(operation, str) or not operation:
            raise ValueError(
                f"Effect at position {index} needs an operation."
            )

        parameters = effect.get("parameters", {})

        filters.append(
            build_vfx_filters(operation, parameters)
        )

    return ",".join(filters)
  
