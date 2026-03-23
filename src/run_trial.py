from __future__ import annotations

from functools import partial

from psychopy.visual import TextStim

from psyflow import StimUnit, next_trial_id, resolve_deadline, set_trial_context
from .utils import build_visual_search_trial_spec


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
    block_seed=None,
    condition_generation_config=None,
):
    """Run one feature/conjunction visual-search trial."""
    trial_id = int(next_trial_id())
    condition_label = (
        str(condition).strip().lower()
        if not isinstance(condition, dict)
        else str(condition.get("condition", "feature_present")).strip().lower()
    )
    spec = build_visual_search_trial_spec(
        condition=condition_label,
        trial_id=trial_id,
        block_seed=block_seed,
        generation_config=condition_generation_config,
    )
    condition_label = str(spec.get("condition", condition_label)).strip().lower()
    search_type = str(spec.get("search_type", "feature")).strip().lower()
    target_present = bool(spec.get("target_present", True))
    set_size = int(spec.get("set_size", 0))
    target_index = spec.get("target_index", None)
    condition_id = str(spec.get("condition_id", f"{condition_label}_trial_{trial_id:03d}"))
    items_payload = list(spec.get("items", [])) if isinstance(spec.get("items", []), list) else []
    fixation_duration = getattr(settings, "fixation_duration", 0.6)
    iti_duration = getattr(settings, "iti_duration", 0.4)

    block_label = str(block_id) if block_id is not None else "block_0"
    block_index = int(block_idx) if block_idx is not None else 0

    present_key = str(getattr(settings, "present_key", "f")).strip().lower()
    absent_key = str(getattr(settings, "absent_key", "j")).strip().lower()
    response_keys = [present_key, absent_key]
    correct_key = present_key if target_present else absent_key

    response_deadline = getattr(settings, "response_deadline", 2.0)

    trial_data = {
        "condition": condition_label,
        "trial_id": trial_id,
        "trial_index": trial_id,
        "block_id": block_label,
        "block_idx": block_index,
        "search_type": search_type,
        "target_present": target_present,
        "set_size": set_size,
        "target_index": target_index,
        "condition_id": condition_id,
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
        deadline_s=resolve_deadline(fixation_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=condition_id,
        task_factors={
            "condition": condition_label,
            "search_type": search_type,
            "target_present": target_present,
            "set_size": set_size,
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
    for item in items_payload:
        if not isinstance(item, dict):
            continue
        pos = item.get("pos", [0.0, 0.0])
        if not isinstance(pos, (list, tuple)) or len(pos) < 2:
            pos = [0.0, 0.0]
        search_items.append(
            TextStim(
                win=win,
                text=str(item.get("glyph", "T")),
                pos=(float(pos[0]), float(pos[1])),
                color=str(item.get("color", "white")),
                ori=float(item.get("ori", 0.0)),
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
        deadline_s=resolve_deadline(response_deadline),
        valid_keys=response_keys,
        block_id=block_label,
        condition_id=condition_id,
        task_factors={
            "condition": condition_label,
            "search_type": search_type,
            "target_present": target_present,
            "set_size": set_size,
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
        deadline_s=resolve_deadline(iti_duration),
        valid_keys=[],
        block_id=block_label,
        condition_id=condition_id,
        task_factors={
            "condition": condition_label,
            "search_type": search_type,
            "target_present": target_present,
            "set_size": set_size,
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
    return trial_data
