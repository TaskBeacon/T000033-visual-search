# Visual Search Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Visual Search Task |
| Version | v0.1.5-dev |
| URL / Repository | https://github.com/TaskBeacon/T000033-visual-search |
| Short Description | Feature vs conjunction visual search with present/absent decisions. |
| Created By | TaskBeacon |
| Date Updated | 2026-03-18 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | English |
| Voice Name | en-US-AriaNeural (voice disabled by default) |

## 1. Task Overview

This task implements a classical visual-search paradigm grounded in feature-integration and guided-search literature. Participants search for a red `T` and report whether it is present (`F`) or absent (`J`).

The implementation explicitly separates feature-search and conjunction-search displays, with both target-present and target-absent trials, and logs trial-level RT/accuracy under PsyFlow `human|qa|sim` modes.

## 2. Task Flow

![Task Flow](task_flow.png)

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Block setup | `BlockUnit.generate_conditions(...)` creates label-level condition sequence from `task.conditions`. |
| 2. Trial execution | `run_trial(...)` runs fixation -> search array -> ITI per trial. |
| 3. Block summary | Accuracy, mean correct RT, and timeout count are shown between blocks. |
| 4. Final summary | Session-level accuracy/RT/timeout metrics are displayed. |

### Trial-Level Flow

| Step | Description |
|---|---|
| `fixation` | Fixation cross (jittered duration) with target reminder text. |
| `search_array` | Circular array of letters appears; participant responds present/absent. |
| `iti` | Brief fixation-only inter-trial interval before next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Condition parser | Maps condition tokens to `(search_type, target_present)` factors. |
| Runtime realization | `run_trial(...)` resolves set size/positions/distractor composition from condition label plus seed context; duration ranges are passed to `StimUnit.show()/capture_response()` for framework-level sampling. |
| Trial ID resolver | Uses PsyFlow `next_trial_id()` at runtime for global trial IDs (no task-local `Controller` class). |

### Other Logic

| Component | Description |
|---|---|
| Dynamic stimuli | Search items are generated per trial in `src/run_trial.py` via PsychoPy text primitives. |
| Trigger alignment | Phase/response/timeout triggers are emitted at fixation/search/ITI and key events. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | 3-digit participant identifier. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `fixation` | text | Central fixation cross used in fixation/ITI/search display. |
| `search_goal` | text | Constant top reminder: `Find red T`. |
| `array_boundary` | circle | Visual boundary for ring-based search layout. |
| dynamic search items | text | Trial-generated letters (`T`/`L`) with color/orientation/position factors. |
| `instruction_text`, `block_break`, `good_bye` | text | Instruction and summary screens. |

### d. Timing

| Phase | Duration |
|---|---|
| fixation | sampled from `fixation_duration` range |
| search array response window | `response_deadline` |
| ITI | `iti_duration` |

### e. Triggers

| Trigger | Code | Meaning |
|---|---:|---|
| `fixation_onset` | 20 | fixation phase onset |
| `search_onset` | 30 | search display onset |
| `response_present` | 31 | present-key response |
| `response_absent` | 32 | absent-key response |
| `search_timeout` | 33 | no response before deadline |
| `iti_onset` | 40 | inter-trial interval onset |

### f. Adaptive Controller

| Parameter Group | Purpose |
|---|---|
| `feature_set_sizes`, `conjunction_set_sizes` | Set-size pools for feature/conjunction trials. |
| `array_radius_px`, `array_radius_jitter_px` | Circular layout geometry. |
| `target_glyph`, `conjunction_alt_glyph`, color fields | Defines target and distractor identities. |
| Notes | No separate controller class; these parameters are consumed directly inside `run_trial(...)`. |

## 4. Methods (for academic publication)

Participants performed speeded present/absent judgments in a visual-search paradigm where the target was a red `T`. Trials manipulated search difficulty via feature versus conjunction distractor structure and target presence.

Each trial began with fixation, followed by a response-bounded search display with item positions sampled on a circular layout. Responses were logged with RT, correctness, and timeout flags. Session outcomes were summarized by accuracy, mean correct RT, and timeout frequency.

The implementation follows a literature-first mapping to feature-integration and guided-search frameworks and avoids MID-style cue/anticipation/feedback state templates.
