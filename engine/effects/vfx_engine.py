
"""Welvox Studio AI - FFmpeg VFX engine.

Provides named, validated video effects using FFmpeg filters.
No user-supplied raw filter expressions are accepted.
"""

import math


_EFFECTS = {
    "cinematic_grade": (
        "eq=contrast=1.12:saturation=1.12:brightness=-0.015,"
        "colorbalance=rs=0.025:gs=0.005:bs=-0.025,vignette=PI/5"
    ),
    "tech_neon_grade": (
        "eq=contrast=1.18:saturation=1.45:brightness=-0.02,"
        "colorbalance=rs=0.025:gs=0.005:bs=0.12:"
        "rm=0.015:gm=0.005:bm=0.08,vignette=PI/6"
    ),
    "vignette": None,
    "film_grain": None,
    "warm_glow": (
        "eq=brightness=0.025:saturation=1.18,"
        "colorbalance=rs=0.08:gs=0.025:bs=-0.06,"
        "gblur=sigma=0.35"
    ),
    "cold_steel": (
        "eq=contrast=1.12:saturation=0.82,"
        "colorbalance=rs=-0.04:gs=0.015:bs=0.09"
    ),
    "sunset_tone": (
        "eq=saturation=1.28:contrast=1.08,"
        "colorbalance=rs=0.12:gs=0.025:bs=-0.10"
    ),
    "teal_orange": (
        "colorbalance=rs=0.08:gs=0.015:bs=-0.08:"
        "rm=-0.025:gm=0.025:bm=0.08"
    ),
    "monochrome": "hue=s=0",
    "sepia": (
        "colorchannelmixer="
        ".393:.769:.189:0:.349:.686:.168:0:.272:.534:.131"
    ),
    "vintage_film": "curves=preset=vintage,eq=saturation=0.82:contrast=0.94",
    "high_contrast": "eq=contrast=1.45:brightness=-0.025",
    "soft_contrast": "eq=contrast=0.86:brightness=0.015",
    "vivid_color": "eq=saturation=1.55:contrast=1.08",
    "muted_color": "eq=saturation=0.62:contrast=0.96",
    "bleach_bypass": "eq=contrast=1.35:saturation=0.48:brightness=-0.015",
    "dream_soft": "gblur=sigma=1.1,eq=brightness=0.025:saturation=1.12",
    "soft_focus": "gblur=sigma=0.7",
    "sharpen": "unsharp=5:5:1.0:5:5:0.0",
    "edge_detect": "edgedetect=low=0.08:high=0.22",
    "emboss": "convolution=-2 -1 0 -1 1 1 0 1 2",
    "negative": "negate",
    "mirror_horizontal": "hflip",
    "flip_vertical": "vflip",
    "rotate_clockwise": "transpose=clock",
    "rotate_counterclockwise": "transpose=cclock",
    "pixelate": (
        "scale=iw/12:ih/12:flags=neighbor,"
        "scale=iw*12:ih*12:flags=neighbor"
    ),
    "gaussian_blur": "gblur=sigma=2.2",
    "box_blur": "boxblur=8:2",
    "motion_blend": "tblend=all_mode=average",
    "frame_ghost": "tmix=frames=3:weights='1 0.55 0.25'",
    "rgb_glitch": "rgbashift=rh=8:rv=-3:bh=-8:bv=3",
    "hue_shift": "hue=h=45",
    "cool_blue": "colorbalance=rs=-0.05:bs=0.12",
    "golden_hour": (
        "colorbalance=rs=0.10:gs=0.04:bs=-0.09,"
        "eq=saturation=1.16"
    ),
    "crushed_blacks": (
        "colorlevels=romin=0.08:gomin=0.08:bomin=0.08"
    ),
    "lifted_blacks": (
        "colorlevels=romin=0.04:gomin=0.04:bomin=0.04"
    ),
    "fade_wash": "eq=contrast=0.82:brightness=0.06:saturation=0.78",
    "noir": "hue=s=0,eq=contrast=1.55:brightness=-0.04,vignette=PI/4",
    "vhs_tape": (
        "eq=saturation=1.25:contrast=1.08,"
        "rgbashift=rh=3:bh=-3,noise=alls=8:allf=t"
    ),
    "scanlines": (
        "drawgrid=width=iw:height=4:thickness=1:color=black@0.28"
    ),
    "grid_overlay": (
        "drawgrid=width=80:height=80:thickness=1:color=white@0.18"
    ),
    "crosshair": (
        "drawbox=x=iw/2-1:y=0:w=2:h=ih:color=white@0.35:t=fill,"
        "drawbox=x=0:y=ih/2-1:w=iw:h=2:color=white@0.35:t=fill"
    ),
    "letterbox": "crop=iw:ih*0.82:0:ih*0.09,scale=iw:ih",
    "fisheye": "lenscorrection=cx=0.5:cy=0.5:k1=-0.18:k2=-0.02",
    "poster_tone": (
        "eq=contrast=1.25:saturation=1.35,"
        "unsharp=5:5:0.5:5:5:0.0"
    ),
    "neon_edges": (
        "edgedetect=mode=colormix:high=0.12,"
        "eq=saturation=2.0:contrast=1.3"
    ),
    "tv_static": "noise=alls=24:allf=t+u",
    "film_fade": "curves=preset=lighter,eq=saturation=0.88:contrast=0.92",
    "clarity": (
        "unsharp=7:7:0.65:5:5:0.0,eq=contrast=1.06"
    ),
    "dark_cinema": (
        "eq=brightness=-0.055:contrast=1.22:saturation=0.92,"
        "vignette=PI/5"
    ),
    "bright_pop": "eq=brightness=0.045:contrast=1.12:saturation=1.32",
    "soft_vignette": "vignette=PI/3",
    "strong_vignette": "vignette=PI/7",
    "warm_monochrome": (
        "hue=s=0,"
        "colorbalance=rs=0.12:gs=0.04:bs=-0.10"
    ),
    "cool_monochrome": (
        "hue=s=0,"
        "colorbalance=rs=-0.08:gs=0.02:bs=0.12"
    ),
    "color_pop": "eq=saturation=1.8:contrast=1.12",
    "subtle_grain": "noise=alls=5:allf=t",
    "heavy_grain": "noise=alls=35:allf=t",
}


def available_effects():
    """Return all supported effect identifiers."""
    return sorted(_EFFECTS.keys())


def build_vfx_filters(operation, parameters=None):
    """Build a validated FFmpeg filter chain."""
    if parameters is None:
        parameters = {}

    if not isinstance(parameters, dict):
        raise ValueError("VFX parameters must be an object.")

    if operation not in _EFFECTS:
        raise ValueError(
            f"Unsupported VFX operation: {operation}"
        )

    if operation == "vignette":
        angle = parameters.get("angle", 0.65)

        if (
            not isinstance(angle, (int, float))
            or isinstance(angle, bool)
            or not math.isfinite(angle)
            or not 0.1 <= angle <= 1.5
        ):
            raise ValueError(
                "Vignette angle must be between 0.1 and 1.5."
            )

        return f"vignette=PI/{math.pi / angle:.4f}"

    if operation == "film_grain":
        strength = parameters.get("strength", 12)

        if (
            not isinstance(strength, int)
            or isinstance(strength, bool)
            or not 1 <= strength <= 100
        ):
            raise ValueError(
                "Film grain strength must be an integer "
                "between 1 and 100."
            )

        return f"noise=alls={strength}:allf=t"

    if parameters:
        raise ValueError(
            f"Effect '{operation}' does not accept parameters: "
            + ", ".join(sorted(parameters))
        )

    return _EFFECTS[operation]
    
