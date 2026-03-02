# CHANGELOG

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
