# Visual Search Task

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Visual Search Task |
| Version | v0.1.1-dev |
| URL / Repository | https://github.com/TaskBeacon/T000033-visual-search |
| Short Description | Feature and conjunction search efficiency assessment. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-19 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (voice disabled by default) |

## 1. Task Overview

This task implements a visual search paradigm with `feature`, `conjunction`, and `absent` conditions. Trials include cueing, anticipation, target response capture, and feedback.

The implementation supports standardized human/QA/simulation execution with condition-resolved logs and trigger instrumentation for reproducibility.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Load block conditions | Condition schedule is prepared for each block. |
| 2. Run trial loop | `run_trial(...)` executes cue, anticipation, target, and feedback phases. |
| 3. Block summary | Block-level accuracy and score are displayed. |
| 4. Final summary | End-of-task score summary is displayed. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Cue | Search-condition cue is displayed. |
| Anticipation | Fixation interval before target onset. |
| Target | Search target appears and response is captured. |
| Pre-feedback fixation | Brief fixation transition stage. |
| Feedback | Hit/miss feedback is shown with score delta. |

### Controller Logic

| Component | Description |
|---|---|
| Adaptive timing | Target duration adapts around configured accuracy target. |
| Condition tracking | Trial outcomes are tracked by condition. |
| Score update | Hit/miss response updates cumulative score. |

### Runtime Context Phases

| Phase Label | Meaning |
|---|---|
| `anticipation` | Pre-target monitoring stage. |
| `target` | Main target response stage. |

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
| `feature_cue`, `conjunction_cue`, `absent_cue` | text | Condition-specific cue stimuli. |
| `feature_target`, `conjunction_target`, `absent_target` | text | Target stimuli for search decisions. |
| `*_hit_feedback`, `*_miss_feedback` | text | Condition-specific feedback text. |
| `fixation`, `block_break`, `good_bye` | text | Shared fixation and summary displays. |

### d. Timing

| Phase | Duration |
|---|---|
| cue | 0.5 s |
| anticipation | 1.0 s |
| prefeedback | 0.4 s |
| feedback | 0.8 s |
| target | adaptive via controller (`0.08`-`0.40` s bounds) |

## 4. Methods (for academic publication)

Participants completed feature, conjunction, and target-absent visual search trials. Each trial provided a condition cue, a pre-target interval, a target response window, and immediate performance feedback.

Task timing was adaptively adjusted by controller logic to maintain target performance levels. Trial records included condition labels, response outcomes, timing measures, and score changes.

Trigger events were emitted at major trial transitions to support synchronized recording and reproducible QA checks.
