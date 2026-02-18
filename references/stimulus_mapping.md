# Stimulus Mapping

Task: `Visual Search Task`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `feature` | `feature_cue`, `feature_target` | `W2101334128` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for FEATURE; target token for condition-specific response context. |
| `conjunction` | `conjunction_cue`, `conjunction_target` | `W2101334128` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for CONJUNCTION; target token for condition-specific response context. |
| `absent` | `absent_cue`, `absent_target` | `W2101334128` | Methods section describes condition-specific cue-target structure and response phase. | `psychopy_builtin` | Cue label text for ABSENT; target token for condition-specific response context. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
