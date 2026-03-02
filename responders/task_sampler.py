from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import random as _py_random

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for visual-search present/absent decisions."""

    hit_rate: float = 0.8
    error_rate: float = 0.1
    rt_mean_s: float = 0.42
    rt_sd_s: float = 0.08
    rt_min_s: float = 0.15

    def __post_init__(self) -> None:
        self._rng: Any = None
        self.hit_rate = max(0.0, min(1.0, float(self.hit_rate)))
        self.error_rate = max(0.0, min(1.0, float(self.error_rate)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _sample_normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _sample_random(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    @staticmethod
    def _truthy(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"1", "true", "yes", "y"}

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        rng = self._rng
        if rng is None:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "rng_missing"})

        phase = str(obs.phase or "")
        if phase != "search_array":
            chosen_key = "space" if "space" in valid_keys else valid_keys[0]
            rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))
            return Action(
                key=chosen_key,
                rt_s=rt,
                meta={"source": "task_sampler", "phase": phase, "outcome": "continue"},
            )

        if self._sample_random() > self.hit_rate:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "outcome": "miss"})

        factors = dict(obs.task_factors or {})
        present_key = str(factors.get("present_key", "f")).strip().lower()
        absent_key = str(factors.get("absent_key", "j")).strip().lower()
        if present_key not in valid_keys:
            present_key = valid_keys[0]
        if absent_key not in valid_keys:
            absent_key = valid_keys[-1]

        target_present = self._truthy(factors.get("target_present", True))
        correct_key = present_key if target_present else absent_key
        if self._sample_random() < self.error_rate:
            wrong = [k for k in valid_keys if k != correct_key]
            chosen_key = wrong[0] if wrong else correct_key
            outcome = "error"
        else:
            chosen_key = correct_key
            outcome = "hit"

        rt = max(self.rt_min_s, self._sample_normal(self.rt_mean_s, self.rt_sd_s))
        return Action(key=chosen_key, rt_s=rt, meta={"source": "task_sampler", "outcome": outcome})
