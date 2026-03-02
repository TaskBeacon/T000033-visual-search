# Stimulus Mapping

Task: `Visual Search Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `feature_present` | `array_boundary`, `fixation`, `search_goal`, dynamic item set (`red T` target + `green T` distractors) | `TreismanGelade1980` | Feature search: target differs by a single feature dimension from distractors. | `psychopy_builtin` | Implemented with PsychoPy text stimuli sampled on a circular layout. |
| `feature_absent` | `array_boundary`, `fixation`, `search_goal`, dynamic item set (`green T` distractors only) | `TreismanGelade1980` | Target-absent trials in feature search contain only non-target feature items. | `psychopy_builtin` | No target instance is inserted. |
| `conjunction_present` | `array_boundary`, `fixation`, `search_goal`, dynamic item set (`red T` target among `red L` and `green T`) | `Wolfe1994` | Conjunction search requires combining feature channels to identify the target. | `psychopy_builtin` | Distractors carry one but not both target-defining features. |
| `conjunction_absent` | `array_boundary`, `fixation`, `search_goal`, dynamic item set (`red L` and `green T` only) | `Wolfe1994` | Target-absent conjunction displays remove the target conjunction while preserving distractor mixture. | `psychopy_builtin` | Balanced with present trials at block generation level. |
| `all_conditions` | `instruction_text`, `block_break`, `good_bye` | `DuncanHumphreys1989` | Shared instructions and summaries support consistent response policy and quality control. | `psychopy_builtin` | Participant-facing text avoids exposing internal condition IDs. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config/code.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
