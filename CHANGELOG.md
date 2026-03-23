# CHANGELOG

## [v0.1.5-dev] - 2026-03-18

### Changed
- Switched block condition scheduling back to native `BlockUnit.generate_conditions(...)` (label-level), with optional `task.condition_weights` resolved through `TaskSettings.resolve_condition_weights()`.
- Refactored `src/run_trial.py` to realize search-item layout and timing directly from condition labels plus seed context (no custom block-level condition payload generator).
- Updated `src/utils.py` to provide lightweight runtime helpers (`build_visual_search_trial_spec`) instead of custom condition-sequence APIs.
- Synced skill/docs text to the default policy: built-in condition generator first, custom generators only for cross-trial/global constraints.
- Removed task-local duration sampling for fixation/ITI; duration ranges are now passed directly to `StimUnit.show(...)` and sampled by PsyFlow runtime.
- Added `task_flow.png` embed under README `## 2. Task Flow` for direct visual preview.

### Fixed
- Removed the incompatible custom generator call signature path that expected keyword-only arguments and could fail under `BlockUnit.generate_conditions(func=...)` positional callback invocation.

## [v0.1.4-dev] - 2026-03-18

### Changed
- Removed the `Controller` class and replaced it with pure generation helpers in `src/utils.py` (`generate_visual_search_conditions`).
- Refactored `src/run_trial.py` to consume pre-generated condition payloads and use PsyFlow `next_trial_id()` / `resolve_deadline()`.
- Simplified `main.py` to pre-generate trial conditions via `BlockUnit.generate_conditions(func=generate_visual_search_conditions, ...)` and removed runtime sampler/counter plumbing.
- Updated `README.md` and `references/task_logic_audit.md` to match the no-controller-class architecture and current trial-flow semantics.

## [v0.1.3-dev] - 2026-03-02

### Changed
- Repaired `src/run_trial.py` to a visual-search-native trial flow (`fixation -> search_array -> iti`) and removed residual MID-style stages.
- Implemented controller-driven search-array rendering in runtime (feature/conjunction, present/absent, set size, item orientation/position) using PsychoPy text stimuli.
- Aligned trial context and outputs to QA/sampler contracts (`phase=search_array`, key mapping factors, `search_array_response`, `search_array_rt`, `search_array_hit`, `timed_out`).
- Rebuilt all reference artifacts to the current schema contract (`references.yaml`, `references.md`, `parameter_mapping.md`, `stimulus_mapping.md`, `task_logic_audit.md` with sections `## 1` to `## 8`).

## [v0.1.1-dev] - 2026-02-19

### Changed
- Replaced MID-style cue/anticipation/target/feedback flow with a zero-base visual-search implementation: fixation -> search array -> ITI.
- Rebuilt `src/utils.py` as a visual-search controller that generates feature/conjunction arrays, target-present/absent conditions, and circular item layouts.
- Rewrote `src/run_trial.py` to draw real search stimuli (`T`/`L` letter arrays) and capture present/absent responses with timeout handling.
- Updated all configs to explicit visual-search conditions (`feature_present`, `feature_absent`, `conjunction_present`, `conjunction_absent`) and coherent trigger maps.
- Replaced poisoned reference artifacts with literature-first mappings (`task_logic_audit.md`, `stimulus_mapping.md`, `parameter_mapping.md`, `references.yaml`).
- Updated `README.md` and simulation responder logic to match the repaired paradigm.

## [0.1.0] - 2026-02-17

### Added
- Added initial PsyFlow/TAPS task scaffold for Visual Search Task.
- Added mode-aware runtime (`human|qa|sim`) in `main.py`.
- Added split configs (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`).
- Added responder trial-context plumbing via `set_trial_context(...)` in `src/run_trial.py`.
- Added generated cue/target image stimuli under `assets/generated/`.

### Verified
- `python -m psyflow.validate <task_path>`
- `psyflow-qa <task_path> --config config/config_qa.yaml --no-maturity-update`
- `python main.py sim --config config/config_scripted_sim.yaml`
- `python main.py sim --config config/config_sampler_sim.yaml`
