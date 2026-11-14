"""Welvox VFX Engine.

First functional version: cinematic color treatments.
Compositing, particles, tracking and animated effects
will be implemented in later versions.
"""


def build_vfx_filters(operation, parameters=None):
    """Build a validated FFmpeg filter chain."""
    parameters = parameters or {}

    if not isinstance(parameters, dict):
        raise ValueError("VFX parameters must be an object.")

    if operation == "cinematic_grade":
        return (
            "eq=contrast=1.12:saturation=1.12:brightness=-0.015,"
            "colorbalance=rs=0.025:gs=0.005:bs=-0.025,"
            "vignette=PI/5"
        )

    if operation == "tech_neon_grade":
        return (
            "eq=contrast=1.18:saturation=1.45:brightness=-0.02,"
            "colorbalance=rs=0.025:gs=0.005:bs=0.12:"
            "rm=0.015:gm=0.005:bm=0.08,"
            "vignette=PI/6"
        )

    if operation == "vignette":
        angle = parameters.get("angle", 0.65)

        if (
            not isinstance(angle, (int, float))
            or isinstance(angle, bool)
            or not 0.1 <= angle <= 1.5
        ):
            raise ValueError(
                "Vignette angle must be between 0.1 and 1.5."
            )

        return f"vignette=PI/{3.141592653589793 / angle:.4f}"

    raise ValueError(
        f"Unsupported VFX operation: {operation}"
    )
