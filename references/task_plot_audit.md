# Task Plot Audit

- generated_at: 2026-03-18T17:32:07
- mode: existing
- task_path: E:\xhmhc\TaskBeacon\T000033-visual-search

## 1. Inputs and provenance

- E:\xhmhc\TaskBeacon\T000033-visual-search\README.md
- E:\xhmhc\TaskBeacon\T000033-visual-search\config\config.yaml
- E:\xhmhc\TaskBeacon\T000033-visual-search\src\run_trial.py

## 2. Evidence extracted from README

- | Step | Description |
- |---|---|
- | `fixation` | Fixation cross (jittered duration) with target reminder text. |
- | `search_array` | Circular array of letters appears; participant responds present/absent. |
- | `iti` | Brief fixation-only inter-trial interval before next trial. |

## 3. Evidence extracted from config/source

- feature_present: phase=fixation, deadline_expr=resolve_deadline(fixation_duration), response_expr=n/a, stim_expr='fixation+search_goal'
- feature_present: phase=search array, deadline_expr=resolve_deadline(response_deadline), response_expr=response_deadline, stim_expr='array_boundary+fixation+search_goal+search_items'
- feature_present: phase=iti, deadline_expr=resolve_deadline(iti_duration), response_expr=n/a, stim_expr='fixation'
- feature_absent: phase=fixation, deadline_expr=resolve_deadline(fixation_duration), response_expr=n/a, stim_expr='fixation+search_goal'
- feature_absent: phase=search array, deadline_expr=resolve_deadline(response_deadline), response_expr=response_deadline, stim_expr='array_boundary+fixation+search_goal+search_items'
- feature_absent: phase=iti, deadline_expr=resolve_deadline(iti_duration), response_expr=n/a, stim_expr='fixation'
- conjunction_present: phase=fixation, deadline_expr=resolve_deadline(fixation_duration), response_expr=n/a, stim_expr='fixation+search_goal'
- conjunction_present: phase=search array, deadline_expr=resolve_deadline(response_deadline), response_expr=response_deadline, stim_expr='array_boundary+fixation+search_goal+search_items'
- conjunction_present: phase=iti, deadline_expr=resolve_deadline(iti_duration), response_expr=n/a, stim_expr='fixation'
- conjunction_absent: phase=fixation, deadline_expr=resolve_deadline(fixation_duration), response_expr=n/a, stim_expr='fixation+search_goal'
- conjunction_absent: phase=search array, deadline_expr=resolve_deadline(response_deadline), response_expr=response_deadline, stim_expr='array_boundary+fixation+search_goal+search_items'
- conjunction_absent: phase=iti, deadline_expr=resolve_deadline(iti_duration), response_expr=n/a, stim_expr='fixation'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 2
- screens_per_timeline: 4
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.008, right=0.032, blank=0.114
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0082, 'right_ratio': 0.0323, 'blank_ratio': 0.1141}
- validator_warnings:
  - timelines[0].phases[0] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[1] missing duration_ms; renderer will annotate as n/a.
  - timelines[0].phases[2] missing duration_ms; renderer will annotate as n/a.

## 7. Output files and checksums

- E:\xhmhc\TaskBeacon\T000033-visual-search\references\task_plot_spec.yaml: sha256=057e0d881a778240bc353e5dd58945645ab123b27276c1204c5c85b2b5141ff4
- E:\xhmhc\TaskBeacon\T000033-visual-search\references\task_plot_spec.json: sha256=75af8b3cb5603ebb9e1e2eb39875d00e28a4c7656270c4c113c80c42db9b186d
- E:\xhmhc\TaskBeacon\T000033-visual-search\references\task_plot_source_excerpt.md: sha256=92e7565fba3f5eabacf026038e225e60168274dc25612564d8518c836d30ab38
- E:\xhmhc\TaskBeacon\T000033-visual-search\task_flow.png: sha256=93f60dc7f133c4a44a96dbb4e446f5c54e811e1a91a2a0b4584d9ff7ee35b793

## 8. Inferred/uncertain items

- feature_present:fixation:unable to resolve duration from 'resolve_deadline(fixation_duration)'
- feature_present:search array:unable to resolve duration from 'resolve_deadline(response_deadline)'
- feature_present:search array:heuristic numeric parse from 'getattr(settings, 'response_deadline', 2.0)'
- feature_present:iti:unable to resolve duration from 'resolve_deadline(iti_duration)'
- feature_absent:fixation:unable to resolve duration from 'resolve_deadline(fixation_duration)'
- feature_absent:search array:unable to resolve duration from 'resolve_deadline(response_deadline)'
- feature_absent:search array:heuristic numeric parse from 'getattr(settings, 'response_deadline', 2.0)'
- feature_absent:iti:unable to resolve duration from 'resolve_deadline(iti_duration)'
- conjunction_present:fixation:unable to resolve duration from 'resolve_deadline(fixation_duration)'
- conjunction_present:search array:unable to resolve duration from 'resolve_deadline(response_deadline)'
- conjunction_present:search array:heuristic numeric parse from 'getattr(settings, 'response_deadline', 2.0)'
- conjunction_present:iti:unable to resolve duration from 'resolve_deadline(iti_duration)'
- conjunction_absent:fixation:unable to resolve duration from 'resolve_deadline(fixation_duration)'
- conjunction_absent:search array:unable to resolve duration from 'resolve_deadline(response_deadline)'
- conjunction_absent:search array:heuristic numeric parse from 'getattr(settings, 'response_deadline', 2.0)'
- conjunction_absent:iti:unable to resolve duration from 'resolve_deadline(iti_duration)'
- collapsed equivalent condition logic into representative timeline: feature_present, feature_absent, conjunction_present, conjunction_absent
- unparsed if-tests defaulted to condition-agnostic applicability: not isinstance(item, dict); not isinstance(pos, (list, tuple)); len(pos) < 2
