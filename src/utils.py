
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any

from psychopy import logging

SEARCH_FEATURE = "feature"
SEARCH_CONJUNCTION = "conjunction"


@dataclass(frozen=True)
class SearchItem:
    glyph: str
    color: str
    ori: float
    pos: tuple[float, float]
    is_target: bool


@dataclass(frozen=True)
class TrialSpec:
    condition: str
    search_type: str
    target_present: bool
    set_size: int
    items: list[SearchItem]
    target_index: int | None


class Controller:
    """Trial generator and summary tracker for the visual search paradigm."""

    def __init__(
        self,
        feature_set_sizes: list[int] | tuple[int, ...] = (8, 12, 16),
        conjunction_set_sizes: list[int] | tuple[int, ...] = (8, 12, 16),
        array_radius_px: float = 250.0,
        array_radius_jitter_px: float = 30.0,
        orientation_pool: list[float] | tuple[float, ...] = (0.0, 90.0, 180.0, 270.0),
        target_glyph: str = "T",
        conjunction_alt_glyph: str = "L",
        target_color: str = "red",
        distractor_color: str = "green",
        random_seed: int | None = None,
        enable_logging: bool = True,
    ):
        self.feature_set_sizes = self._clean_int_list(feature_set_sizes, default=(8, 12, 16))
        self.conjunction_set_sizes = self._clean_int_list(conjunction_set_sizes, default=(8, 12, 16))
        self.array_radius_px = max(80.0, float(array_radius_px))
        self.array_radius_jitter_px = max(0.0, float(array_radius_jitter_px))
        self.orientation_pool = self._clean_float_list(orientation_pool, default=(0.0, 90.0, 180.0, 270.0))
        self.target_glyph = str(target_glyph or "T")
        self.conjunction_alt_glyph = str(conjunction_alt_glyph or "L")
        self.target_color = str(target_color or "red")
        self.distractor_color = str(distractor_color or "green")
        self.enable_logging = bool(enable_logging)
        self.rng = random.Random(random_seed)

        self.block_idx = -1
        self.trial_count_total = 0
        self.trial_count_block = 0
        self.correct_total = 0
        self.correct_block = 0
        self.timeout_total = 0
        self.timeout_block = 0
        self.correct_rt_sum_total = 0.0
        self.correct_rt_sum_block = 0.0
        self.correct_rt_n_total = 0
        self.correct_rt_n_block = 0

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "Controller":
        cfg = dict(config or {})
        return cls(
            feature_set_sizes=cfg.get("feature_set_sizes", (8, 12, 16)),
            conjunction_set_sizes=cfg.get("conjunction_set_sizes", (8, 12, 16)),
            array_radius_px=cfg.get("array_radius_px", 250.0),
            array_radius_jitter_px=cfg.get("array_radius_jitter_px", 30.0),
            orientation_pool=cfg.get("orientation_pool", (0.0, 90.0, 180.0, 270.0)),
            target_glyph=cfg.get("target_glyph", "T"),
            conjunction_alt_glyph=cfg.get("conjunction_alt_glyph", "L"),
            target_color=cfg.get("target_color", "red"),
            distractor_color=cfg.get("distractor_color", "green"),
            random_seed=cfg.get("random_seed", None),
            enable_logging=bool(cfg.get("enable_logging", True)),
        )

    @staticmethod
    def _clean_int_list(values: Any, default: tuple[int, ...]) -> list[int]:
        if isinstance(values, (list, tuple)):
            out = []
            for v in values:
                try:
                    x = int(v)
                except Exception:
                    continue
                if x > 0:
                    out.append(x)
            if out:
                return out
        return list(default)

    @staticmethod
    def _clean_float_list(values: Any, default: tuple[float, ...]) -> list[float]:
        if isinstance(values, (list, tuple)):
            out = []
            for v in values:
                try:
                    out.append(float(v))
                except Exception:
                    continue
            if out:
                return out
        return [float(v) for v in default]

    @staticmethod
    def _truthy(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"1", "true", "yes", "y"}

    def start_block(self, block_idx: int) -> None:
        self.block_idx = int(block_idx)
        self.trial_count_block = 0
        self.correct_block = 0
        self.timeout_block = 0
        self.correct_rt_sum_block = 0.0
        self.correct_rt_n_block = 0

    def next_trial_id(self) -> int:
        return int(self.trial_count_total) + 1

    def sample_duration(self, value: Any, default: float) -> float:
        if isinstance(value, (int, float)):
            return max(0.0, float(value))
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            try:
                low = float(value[0])
                high = float(value[1])
            except Exception:
                return max(0.0, float(default))
            if high < low:
                low, high = high, low
            return max(0.0, float(self.rng.uniform(low, high)))
        return max(0.0, float(default))

    def parse_condition(self, condition: str) -> tuple[str, bool]:
        token = str(condition).strip().lower()
        mapping = {
            "feature_present": (SEARCH_FEATURE, True),
            "feature_absent": (SEARCH_FEATURE, False),
            "conjunction_present": (SEARCH_CONJUNCTION, True),
            "conjunction_absent": (SEARCH_CONJUNCTION, False),
            # Legacy compatibility
            "feature": (SEARCH_FEATURE, True),
            "conjunction": (SEARCH_CONJUNCTION, True),
            "absent": (SEARCH_CONJUNCTION, False),
        }
        if token not in mapping:
            raise ValueError(f"Unsupported visual-search condition: {condition!r}")
        return mapping[token]

    def _sample_set_size(self, search_type: str) -> int:
        pool = self.feature_set_sizes if search_type == SEARCH_FEATURE else self.conjunction_set_sizes
        return int(self.rng.choice(pool))

    def _sample_positions(self, n_items: int) -> list[tuple[float, float]]:
        # Even angular scaffolding with jitter keeps readable spacing.
        step = 360.0 / max(1, n_items)
        positions: list[tuple[float, float]] = []
        for i in range(n_items):
            angle_deg = (i * step) + self.rng.uniform(-0.25 * step, 0.25 * step)
            radius = self.array_radius_px + self.rng.uniform(-self.array_radius_jitter_px, self.array_radius_jitter_px)
            radius = max(80.0, radius)
            theta = math.radians(angle_deg)
            positions.append((radius * math.cos(theta), radius * math.sin(theta)))
        self.rng.shuffle(positions)
        return positions

    def build_trial(self, condition: str) -> TrialSpec:
        search_type, target_present = self.parse_condition(condition)
        set_size = self._sample_set_size(search_type)
        positions = self._sample_positions(set_size)
        target_index = self.rng.randrange(set_size) if target_present else None

        items: list[SearchItem] = []
        for idx, pos in enumerate(positions):
            is_target = target_index is not None and idx == target_index
            if is_target:
                glyph = self.target_glyph
                color = self.target_color
            elif search_type == SEARCH_FEATURE:
                glyph = self.target_glyph
                color = self.distractor_color
            else:
                if self.rng.random() < 0.5:
                    glyph = self.target_glyph
                    color = self.distractor_color
                else:
                    glyph = self.conjunction_alt_glyph
                    color = self.target_color

            items.append(
                SearchItem(
                    glyph=glyph,
                    color=color,
                    ori=float(self.rng.choice(self.orientation_pool)),
                    pos=(float(pos[0]), float(pos[1])),
                    is_target=is_target,
                )
            )

        return TrialSpec(
            condition=str(condition),
            search_type=search_type,
            target_present=bool(target_present),
            set_size=int(set_size),
            items=items,
            target_index=target_index,
        )

    def evaluate_response(self, response_key: str | None, *, present_key: str, absent_key: str, target_present: bool) -> bool:
        key = str(response_key or "").strip().lower()
        if key not in {present_key, absent_key}:
            return False
        if target_present:
            return key == present_key
        return key == absent_key

    def record_trial(self, *, hit: bool, rt_s: float | None, responded: bool, condition: str) -> None:
        self.trial_count_total += 1
        self.trial_count_block += 1
        if bool(hit):
            self.correct_total += 1
            self.correct_block += 1
            if rt_s is not None:
                rt = max(0.0, float(rt_s))
                self.correct_rt_sum_total += rt
                self.correct_rt_sum_block += rt
                self.correct_rt_n_total += 1
                self.correct_rt_n_block += 1
        if not responded:
            self.timeout_total += 1
            self.timeout_block += 1

        if self.enable_logging:
            logging.data(
                f"[VisualSearch] block={self.block_idx} trial_block={self.trial_count_block} "
                f"trial_total={self.trial_count_total} cond={condition} hit={bool(hit)} responded={responded} rt={rt_s}"
            )
