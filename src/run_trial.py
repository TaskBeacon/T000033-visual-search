from __future__ import annotations

from functools import partial
from typing import Any

from psychopy.visual import TextStim

from psyflow import StimUnit, set_trial_context


def _deadline_s(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return None
    return None


def _sample_duration(controller, value: Any, default_value: float) -> float:
    if hasattr(controller, "sample_duration"):
        return float(controller.sample_duration(value, default_value))
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)) and value:
        try:
            return float(max(value))
        except Exception:
            return float(default_value)
    return float(default_value)


def _trial_id(controller) -> int:
    if hasattr(controller, "next_trial_id"):
        return int(controller.next_trial_id())
    return 1


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one feature/conjunction visual-search trial."""
    trial_id = _trial_id(controller)
    trial_spec = controller.build_trial(condition)

    block_label = str(block_id) if block_id is not None else "block_0"
    block_index = int(block_idx) if block_idx is not None else 0
    trial_index = int(getattr(controller, "trial_count_block", 0)) + 1

    present_key = str(getattr(settings, "present_key", "f")).strip().lower()
    absent_key = str(getattr(settings, "absent_key", "j")).strip().lower()
    response_keys = [present_key, absent_key]
    correct_key = present_key if bool(trial_spec.target_present) else absent_key

    fixation_duration = _sample_duration(controller, settings.fixation_duration, 0.6)
    response_deadline = float(getattr(settings, "response_deadline", 2.0))
    iti_duration = _sample_duration(controller, settings.iti_duration, 0.4)

    trial_data = {
        "condition": str(trial_spec.condition),
        "trial_id": trial_id,
        "trial_index": trial_index,
        "block_id": block_label,
        "block_idx": block_index,
        "search_type": str(trial_spec.search_type),
        "target_present": bool(trial_spec.target_present),
        "set_size": int(trial_spec.set_size),
        "target_index": trial_spec.target_index,
        "correct_key": correct_key,
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    fixation = make_unit(unit_label="fixation")
    fixation.add_stim(stim_bank.get("fixation"))
    fixation.add_stim(stim_bank.get("search_goal"))
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="fixation",
        deadline_s=_deadline_s(fixation_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=str(trial_spec.condition),
        task_factors={
            "condition": str(trial_spec.condition),
            "search_type": str(trial_spec.search_type),
            "target_present": bool(trial_spec.target_present),
            "set_size": int(trial_spec.set_size),
            "stage": "fixation",
            "block_idx": block_index,
        },
        stim_id="fixation+search_goal",
    )
    fixation.show(
        duration=fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    item_height = float(getattr(settings, "item_height", 44))
    item_font = str(getattr(settings, "item_font", "Arial"))
    search_items = []
    for item in trial_spec.items:
        search_items.append(
            TextStim(
                win=win,
                text=str(item.glyph),
                pos=(float(item.pos[0]), float(item.pos[1])),
                color=item.color,
                ori=float(item.ori),
                height=item_height,
                font=item_font,
            )
        )

    search_array = make_unit(unit_label="search_array")
    search_array.add_stim(stim_bank.get("array_boundary"))
    search_array.add_stim(stim_bank.get("fixation"))
    search_array.add_stim(stim_bank.get("search_goal"))
    search_array.add_stim(search_items)
    set_trial_context(
        search_array,
        trial_id=trial_id,
        phase="search_array",
        deadline_s=_deadline_s(response_deadline),
        valid_keys=response_keys,
        block_id=block_label,
        condition_id=str(trial_spec.condition),
        task_factors={
            "condition": str(trial_spec.condition),
            "search_type": str(trial_spec.search_type),
            "target_present": bool(trial_spec.target_present),
            "set_size": int(trial_spec.set_size),
            "present_key": present_key,
            "absent_key": absent_key,
            "block_idx": block_index,
        },
        stim_id="array_boundary+fixation+search_goal+search_items",
    )
    search_array.capture_response(
        keys=response_keys,
        correct_keys=[correct_key],
        duration=response_deadline,
        onset_trigger=settings.triggers.get("search_onset"),
        response_trigger={
            present_key: settings.triggers.get("response_present"),
            absent_key: settings.triggers.get("response_absent"),
        },
        timeout_trigger=settings.triggers.get("search_timeout"),
    )
    search_array.to_dict(trial_data)

    response_key = str(search_array.get_state("response", "")).strip().lower()
    responded = response_key in response_keys
    rt = search_array.get_state("rt", None)
    rt_s = float(rt) if isinstance(rt, (int, float)) else None
    hit = bool(responded and response_key == correct_key)

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="iti",
        deadline_s=_deadline_s(iti_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=str(trial_spec.condition),
        task_factors={
            "condition": str(trial_spec.condition),
            "search_type": str(trial_spec.search_type),
            "target_present": bool(trial_spec.target_present),
            "set_size": int(trial_spec.set_size),
            "stage": "iti",
            "block_idx": block_index,
        },
        stim_id="fixation",
    )
    iti.show(
        duration=iti_duration,
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    trial_data.update(
        {
            "search_array_response": response_key if responded else "",
            "search_array_rt": rt_s,
            "search_array_hit": hit,
            "timed_out": not responded,
            "responded": responded,
        }
    )

    controller.record_trial(
        hit=hit,
        rt_s=rt_s,
        responded=responded,
        condition=str(trial_spec.condition),
    )
    return trial_data
