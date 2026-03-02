# Task Logic Audit: Visual Search Task (Feature vs Conjunction)

## 1. Paradigm Intent

- Task: `visual_search`
- Primary construct: search efficiency differences between single-feature search and conjunction search.
- Manipulated factors:
  - search type (`feature`, `conjunction`)
  - target presence (`present`, `absent`)
  - set size (sampled from configured lists)
- Dependent measures: response key, RT, correctness, timeout rate, and condition-wise accuracy/RT summaries.
- Key citations:
  - Treisman, A., & Gelade, G. (1980). *A feature-integration theory of attention.*
  - Wolfe, J. M. (1994). *Guided Search 2.0.*
  - Duncan, J., & Humphreys, G. W. (1989). *Visual search and stimulus similarity.*

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 3 (human), 1 (QA/sim profiles).
- Trials per block: fixed by config (`trial_per_block`).
- Randomization/counterbalancing: conditions are sampled by `BlockUnit.generate_conditions()` with balanced counts; each trial independently samples set size and item positions.

### Trial State Machine

1. `fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown: central fixation cross plus top reminder text (`Target: red T`)
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after sampled fixation duration
   - Next state: `search_array`

2. `search_array`
   - Onset trigger: `search_onset`
   - Stimuli shown: circular search layout with item set (letters with color/orientation), fixation, and goal label
   - Valid keys: `[present_key, absent_key]` (default `f`, `j`)
   - Timeout behavior: if no response before `response_deadline`, emit `search_timeout` and mark timeout
   - Next state: `iti`

3. `iti`
   - Onset trigger: `iti_onset`
   - Stimuli shown: fixation
   - Valid keys: `[]`
   - Timeout behavior: auto-advance after ITI duration
   - Next state: next trial or block end

## 3. Condition Semantics

- Condition ID: `feature_present`
  - Participant-facing meaning: target exists in a feature-search display.
  - Concrete stimulus realization: one red `T` target among green `T` distractors.
  - Outcome rules: correct response is `present_key`.

- Condition ID: `feature_absent`
  - Participant-facing meaning: no target in a feature-search display.
  - Concrete stimulus realization: all items are green `T` distractors (no red `T`).
  - Outcome rules: correct response is `absent_key`.

- Condition ID: `conjunction_present`
  - Participant-facing meaning: target exists in a conjunction-search display.
  - Concrete stimulus realization: one red `T` target among mixed red `L` and green `T` distractors.
  - Outcome rules: correct response is `present_key`.

- Condition ID: `conjunction_absent`
  - Participant-facing meaning: no target in a conjunction-search display.
  - Concrete stimulus realization: mixed red `L` and green `T` distractors, with no red `T` target.
  - Outcome rules: correct response is `absent_key`.

## 4. Response and Scoring Rules

- Response mapping: `F = target present`, `J = target absent`.
- Missing-response policy: timeout after `response_deadline`; timeout count is tracked per block/session.
- Correctness logic: `hit=True` only when response matches target presence (present key on target-present trial, absent key on target-absent trial).
- Reward/penalty updates: none (no point-based scoring); performance summarized by accuracy and RT.
- Running metrics: per block and overall, report accuracy, mean correct RT (ms), and timeout counts.

## 5. Stimulus Layout Plan

- Screen: `search_array`
  - Stimulus IDs shown together: `array_boundary`, `fixation`, `search_goal`, dynamic item letters.
  - Layout anchors (`pos`):
    - fixation at center `(0, 0)`
    - goal text near top `(0, 305)`
    - items placed around a circular ring (`array_radius_px` with jitter)
  - Size/spacing:
    - item letter height (`item_height`, default 42-44 px)
    - ring radius around 240-245 px with limited jitter
  - Readability checks: bounded set sizes (8-16) and angular spacing prevent overlap and preserve visual crowding manipulation.
  - Rationale: circular distribution provides standard visual-search geometry with controlled eccentricity.

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | fixation phase onset |
| `search_onset` | 30 | search array onset |
| `response_present` | 31 | present-key response |
| `response_absent` | 32 | absent-key response |
| `search_timeout` | 33 | no response before deadline |
| `iti_onset` | 40 | ITI onset |

## 7. Inference Log

- Decision: use letter stimuli (`T`, `L`) with color conjunction manipulation instead of image assets.
- Why inference was required: cited theories define search constraints (feature vs conjunction) but not a single mandatory graphic asset set.
- Citation-supported rationale: feature-integration and guided-search frameworks are operationalized with color/shape conjunction displays.

- Decision: include four explicit conditions (`feature/conjunction` x `present/absent`) as config tokens.
- Why inference was required: literature describes factors, while implementation needs explicit trial labels.
- Citation-supported rationale: explicit factorized condition tokens preserve direct mapping from theory to runtime state.

- Decision: no per-trial reward scoring or evaluative feedback text.
- Why inference was required: canonical visual-search protocols primarily analyze RT/accuracy rather than point rewards.
- Citation-supported rationale: dependent measures in the cited literature center on search efficiency (accuracy and RT trends).
