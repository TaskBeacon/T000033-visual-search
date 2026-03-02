# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| task.conditions | `task.conditions` | `['feature_present','feature_absent','conjunction_present','conjunction_absent']` | TreismanGelade1980 | Feature and conjunction search are treated as distinct condition families with present/absent outcomes. | inferred | Runtime parses condition token to search type and target presence. |
| task.blocks_trials | `task.total_blocks`, `task.trial_per_block` | Human `3 x 48`; QA/sim `1 x 16` | Wolfe1994 | Repeated trials across loads are needed for stable RT/accuracy contrasts. | inferred | QA/sim reduced for operational validation speed. |
| task.key_mapping | `task.present_key`, `task.absent_key`, `task.key_list` | present=`f`, absent=`j`, continue=`space` | DuncanHumphreys1989 | Speeded present/absent decisions require a fixed two-key mapping. | inferred | Key mapping is fully config-defined for localization portability. |
| timing.fixation | `timing.fixation_duration` | Human `[0.5,0.8]`; QA/sim `[0.3,0.4]` | Wolfe1994 | Brief pre-array fixation separates trial epochs and stabilizes attention. | inferred | Jitter sampled via controller `sample_duration`. |
| timing.response_deadline | `timing.response_deadline` | Human `2.0s`; QA/sim `1.2s` | Wolfe1994 | Visual-search tasks emphasize RT under bounded decision windows. | inferred | Timeout trigger emitted at missed deadline. |
| timing.iti | `timing.iti_duration` | Human `0.4s`; QA/sim `0.2s` | DuncanHumphreys1989 | Inter-trial separation avoids immediate carryover between arrays. | inferred | Applied as post-response fixation interval. |
| controller.feature_set_sizes | `controller.feature_set_sizes` | Human `[8,12,16]`; QA/sim `[8,12]` | TreismanGelade1980 | Feature search efficiency is evaluated across set-size levels. | inferred | Sampled each trial for feature conditions. |
| controller.conjunction_set_sizes | `controller.conjunction_set_sizes` | Human `[8,12,16]`; QA/sim `[8,12]` | Wolfe1994 | Conjunction search cost is expected to scale with set size. | inferred | Sampled each trial for conjunction conditions. |
| controller.item_semantics | `controller.target_glyph`, `controller.conjunction_alt_glyph`, `controller.target_color`, `controller.distractor_color` | target=`T`, alt=`L`, target_color=`red`, distractor_color=`green` | TreismanGelade1980 | Feature channels are instantiated by color and letter conjunction contrasts. | inferred | Participant wording stays config-driven; runtime builds arrays from these params. |
| controller.layout | `controller.array_radius_px`, `controller.array_radius_jitter_px`, `timing.item_height`, `timing.item_font` | radius `245`, jitter `25`, item height `44`, font `Arial` | DuncanHumphreys1989 | Controlled eccentricity and readable item spacing are required for search tasks. | inferred | Circular layout with jitter keeps spacing legible. |
| trigger.search | `triggers.map.search_onset` | `30` | Wolfe1994 | Search-array onset is the core event for RT-aligned analyses. | inferred | Emitted at `search_array` phase onset. |
| trigger.response | `triggers.map.response_present`, `triggers.map.response_absent`, `triggers.map.search_timeout` | `31`, `32`, `33` | DuncanHumphreys1989 | Present/absent responses and omissions are behaviorally distinct outcomes. | inferred | Response triggers are key-mapped in `capture_response(...)`. |
| trigger.fix_iti | `triggers.map.fixation_onset`, `triggers.map.iti_onset` | `20`, `40` | Wolfe1994 | Epoch boundaries support clean trial segmentation. | inferred | Fixation and ITI are both explicit phases in runtime. |
