from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any

from psychopy import logging

SEARCH_FEATURE = "feature"
SEARCH_CONJUNCTION = "conjunction"
DEFAULT_CONDITIONS = (
    "feature_present",
    "feature_absent",
    "conjunction_present",
    "conjunction_absent",
)


@dataclass(frozen=True)
class SearchItem:
    glyph: str
    color: str
    ori: float
    pos: tuple[float, float]
    is_target: bool


def parse_condition(condition: str) -> tuple[str, bool]:
    token = str(condition).strip().lower()
    mapping = {
        "feature_present": (SEARCH_FEATURE, True),
        "feature_absent": (SEARCH_FEATURE, False),
        "conjunction_present": (SEARCH_CONJUNCTION, True),
        "conjunction_absent": (SEARCH_CONJUNCTION, False),
        "feature": (SEARCH_FEATURE, True),
        "conjunction": (SEARCH_CONJUNCTION, True),
        "absent": (SEARCH_CONJUNCTION, False),
    }
    if token not in mapping:
        raise ValueError(f"Unsupported visual-search condition: {condition!r}")
    return mapping[token]


def _clean_int_list(values: Any, default: tuple[int, ...]) -> list[int]:
    if isinstance(values, (list, tuple)):
        out = []
        for value in values:
            try:
                parsed = int(value)
            except Exception:
                continue
            if parsed > 0:
                out.append(parsed)
        if out:
            return out
    return list(default)


def _clean_float_list(values: Any, default: tuple[float, ...]) -> list[float]:
    if isinstance(values, (list, tuple)):
        out = []
        for value in values:
            try:
                out.append(float(value))
            except Exception:
                continue
        if out:
            return out
    return [float(value) for value in default]


def _sample_positions(
    *,
    rng: random.Random,
    n_items: int,
    array_radius_px: float,
    array_radius_jitter_px: float,
) -> list[tuple[float, float]]:
    step = 360.0 / max(1, n_items)
    positions: list[tuple[float, float]] = []
    for idx in range(n_items):
        angle_deg = (idx * step) + rng.uniform(-0.25 * step, 0.25 * step)
        radius = array_radius_px + rng.uniform(-array_radius_jitter_px, array_radius_jitter_px)
        radius = max(80.0, radius)
        theta = math.radians(angle_deg)
        positions.append((radius * math.cos(theta), radius * math.sin(theta)))
    rng.shuffle(positions)
    return positions


def _build_search_items(
    *,
    rng: random.Random,
    search_type: str,
    target_present: bool,
    set_size: int,
    positions: list[tuple[float, float]],
    target_glyph: str,
    conjunction_alt_glyph: str,
    target_color: str,
    distractor_color: str,
    orientation_pool: list[float],
) -> tuple[list[SearchItem], int | None]:
    target_index = rng.randrange(set_size) if target_present else None
    items: list[SearchItem] = []
    for idx, pos in enumerate(positions):
        is_target = target_index is not None and idx == target_index
        if is_target:
            glyph = target_glyph
            color = target_color
        elif search_type == SEARCH_FEATURE:
            glyph = target_glyph
            color = distractor_color
        else:
            if rng.random() < 0.5:
                glyph = target_glyph
                color = distractor_color
            else:
                glyph = conjunction_alt_glyph
                color = target_color
        items.append(
            SearchItem(
                glyph=str(glyph),
                color=str(color),
                ori=float(rng.choice(orientation_pool)),
                pos=(float(pos[0]), float(pos[1])),
                is_target=is_target,
            )
        )
    return items, target_index


def _trial_rng(*, block_seed: int | None, trial_id: int, condition: str, random_seed: int | None) -> random.Random:
    if random_seed is not None:
        base = int(random_seed)
    elif block_seed is not None:
        base = int(block_seed)
    else:
        base = 0

    condition_norm = str(condition).strip().lower()
    if condition_norm == "feature_present":
        cond_offset = 11
    elif condition_norm == "feature_absent":
        cond_offset = 12
    elif condition_norm == "conjunction_present":
        cond_offset = 21
    elif condition_norm == "conjunction_absent":
        cond_offset = 22
    else:
        cond_offset = 99
    mixed_seed = (base * 1000003 + int(trial_id) * 97 + cond_offset) % (2**32)
    return random.Random(mixed_seed)


def build_visual_search_trial_spec(
    *,
    condition: str,
    trial_id: int,
    block_seed: int | None = None,
    generation_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = dict(generation_config or {})
    token = str(condition).strip().lower()
    if not token:
        token = "feature_present"
    if token not in DEFAULT_CONDITIONS:
        token = "feature_present"

    random_seed = cfg.get("random_seed", None)
    rng = _trial_rng(block_seed=block_seed, trial_id=int(trial_id), condition=token, random_seed=random_seed)
    search_type, target_present = parse_condition(token)

    feature_sizes = _clean_int_list(cfg.get("feature_set_sizes"), default=(8, 12, 16))
    conjunction_sizes = _clean_int_list(cfg.get("conjunction_set_sizes"), default=(8, 12, 16))
    set_size_pool = feature_sizes if search_type == SEARCH_FEATURE else conjunction_sizes
    set_size = int(rng.choice(set_size_pool))

    radius_px = max(80.0, float(cfg.get("array_radius_px", 245.0)))
    radius_jitter = max(0.0, float(cfg.get("array_radius_jitter_px", 25.0)))
    positions = _sample_positions(
        rng=rng,
        n_items=set_size,
        array_radius_px=radius_px,
        array_radius_jitter_px=radius_jitter,
    )

    orientation_pool = _clean_float_list(cfg.get("orientation_pool"), default=(0.0, 90.0, 180.0, 270.0))
    target_glyph = str(cfg.get("target_glyph", "T"))
    conjunction_alt_glyph = str(cfg.get("conjunction_alt_glyph", "L"))
    target_color = str(cfg.get("target_color", "red"))
    distractor_color = str(cfg.get("distractor_color", "green"))
    items, target_index = _build_search_items(
        rng=rng,
        search_type=search_type,
        target_present=bool(target_present),
        set_size=set_size,
        positions=positions,
        target_glyph=target_glyph,
        conjunction_alt_glyph=conjunction_alt_glyph,
        target_color=target_color,
        distractor_color=distractor_color,
        orientation_pool=orientation_pool,
    )

    if bool(cfg.get("enable_logging", True)):
        logging.data(
            f"[VisualSearch] condition={token} trial_id={trial_id} "
            f"set_size={set_size} target_present={target_present}"
        )

    return {
        "condition": token,
        "condition_id": f"{token}_trial_{int(trial_id):03d}",
        "search_type": search_type,
        "target_present": bool(target_present),
        "set_size": int(set_size),
        "target_index": target_index,
        "items": [
            {
                "glyph": item.glyph,
                "color": item.color,
                "ori": float(item.ori),
                "pos": [float(item.pos[0]), float(item.pos[1])],
                "is_target": bool(item.is_target),
            }
            for item in items
        ],
    }
