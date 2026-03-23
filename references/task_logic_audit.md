# Task Logic Audit: Visual Search Task

## 1. Paradigm Intent

- Task: `visual_search`.
- Construct: selective-attention efficiency in feature search versus conjunction search.
- Manipulated factors:
  - search type (`feature`, `conjunction`)
  - target presence (`present`, `absent`)
  - set size sampled from configured pools.
- Primary dependent measures:
  - response key (`present` / `absent`)
  - response time (`search_array_rt`)
  - accuracy (`search_array_hit`)
  - timeout rate.
- Key citations:
  - `TreismanGelade1980`
  - `Wolfe1994`
  - `DuncanHumphreys1989`

## 2. Block/Trial Workflow

### Block Structure

- Human profile: `3` blocks x `48` trials.
- QA/sim profiles: `1` block x `16` trials.
- `BlockUnit.generate_conditions(...)` schedules label-level conditions from `task.conditions` (default PsyFlow path).
- `run_trial.py` realizes trial-level item layouts from each condition label and resolves global `trial_id` via PsyFlow `next_trial_id()`.

### Trial State Machine

1. `fixation`
- Stimuli: `fixation`, `search_goal`.
- Trigger: `fixation_onset`.
- Keys: none.
- Next: `search_array`.

2. `search_array`
- Stimuli: `array_boundary`, `fixation`, `search_goal`, plus dynamic item list from trial sampler helpers (`search_items`).
- Trigger: `search_onset`.
- Valid keys: `present_key`, `absent_key`.
- Response triggers: `response_present`, `response_absent`.
- Timeout trigger: `search_timeout`.
- Next: `iti`.

3. `iti`
- Stimulus: `fixation`.
- Trigger: `iti_onset`.
- Keys: none.
- Next: next trial or block end.

## 3. Condition Semantics

- `feature_present`:
  - target exists in a feature-search display.
  - realization: one red `T` among green `T` distractors.
  - correct response: `present_key`.

- `feature_absent`:
  - no target in a feature-search display.
  - realization: green `T` distractors only.
  - correct response: `absent_key`.

- `conjunction_present`:
  - target exists in a conjunction-search display.
  - realization: one red `T` among red `L` and green `T` distractors.
  - correct response: `present_key`.

- `conjunction_absent`:
  - no target in a conjunction-search display.
  - realization: red `L` and green `T` distractors without red `T`.
  - correct response: `absent_key`.

## 4. Response and Scoring Rules

- Key mapping (default):
  - `f` -> target present
  - `j` -> target absent.
- Timeout policy:
  - if no valid key before `response_deadline`, mark `timed_out=true` and emit `search_timeout`.
- Accuracy policy:
  - `search_array_hit=true` only when key matches target presence.
- Aggregation policy:
  - block and overall summaries report accuracy, mean correct RT (ms), and timeout counts.
- QA-required fields are produced in trial rows:
  - `condition`, `block_id`, `trial_index`, `search_type`, `target_present`, `set_size`, `search_array_response`, `search_array_rt`, `search_array_hit`.

## 5. Stimulus Layout Plan

- Display envelope: `1280 x 720`, unit `pix`.
- `search_goal`: top-center (`0, 305`) to keep objective visible.
- `fixation`: center (`0, 0`).
- `array_boundary`: centered circle radius around `285` px.
- Search items:
  - sampled positions around circular ring (`array_radius_px` with jitter)
  - item height configured by `timing.item_height`
  - item font configured by `timing.item_font`
  - orientation sampled from `condition_generation.orientation_pool` inside runtime helpers.
- Readability rationale:
  - set sizes are capped and positions are jittered from angular scaffolding to avoid dense overlap.

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | fixation phase onset |
| `search_onset` | 30 | search-array onset |
| `response_present` | 31 | present-key response |
| `response_absent` | 32 | absent-key response |
| `search_timeout` | 33 | no response before deadline |
| `iti_onset` | 40 | inter-trial interval onset |

## 7. Architecture Decisions (Auditability)

- `main.py` remains one mode-aware runtime (`human|qa|sim`) with shared trial loop and summary calculation.
- `src/run_trial.py` uses visual-search-native phases only (`fixation -> search_array -> iti`); MID template phases are removed.
- `set_trial_context(...)` on `search_array` includes sampler-critical factors: `target_present`, `present_key`, `absent_key`, `set_size`.
- Participant-facing wording is config-driven (`stimuli.*`) to support localization without code edits.
- Search-array generation is implemented as pure helper functions in `src/utils.py`; `run_trial.py` performs condition-to-stimulus realization on demand (no custom block-level condition generator).
- Duration ranges are passed directly to `StimUnit.show(...)` / `StimUnit.capture_response(...)`; no task-local `_sample_duration` layer is used.

## 8. Inference Log

- Letter-and-color instantiation (`T`/`L`, red/green) is an implementation inference consistent with feature/conjunction definitions in cited papers.
- Exact block/trial counts are implementation choices for operational practicality; QA/sim profiles intentionally reduce counts for gate speed.
- Circular array geometry and jitter values are inferred layout parameters chosen to preserve readable spacing while maintaining eccentricity-based search demands.
- No monetary reward/penalty feedback is implemented because this paradigm focuses on RT/accuracy search efficiency rather than value updates.
