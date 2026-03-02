# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.conditions` | `['feature_present', 'feature_absent', 'conjunction_present', 'conjunction_absent']` | `TreismanGelade1980` | `inferred` | Explicit factorial condition tokens are needed to operationalize search type x target presence. |
| `task.key_list` | `['f', 'j', 'space']` | `DuncanHumphreys1989` | `inferred` | Binary present/absent decision requires two response keys plus instruction-advance key. |
| `timing.response_deadline` | `2.0 s` (human), `1.2 s` (QA/sim) | `Wolfe1994` | `inferred` | Deadline enforces speeded search decisions while keeping enough time for conjunction trials. |
| `timing.fixation_duration` | `[0.5, 0.8] s` (human) | `Wolfe1994` | `inferred` | Jittered fixation minimizes rhythmic anticipation and stabilizes pre-search baseline. |
| `timing.iti_duration` | `0.4 s` (human) | `DuncanHumphreys1989` | `inferred` | Brief ITI separates trials without heavy temporal overhead. |
| `controller.feature_set_sizes` | `[8, 12, 16]` | `TreismanGelade1980` | `inferred` | Multiple set sizes enable search-efficiency comparisons across load levels. |
| `controller.conjunction_set_sizes` | `[8, 12, 16]` | `Wolfe1994` | `inferred` | Matching set-size grid supports direct comparison with feature search. |
| `controller.target_glyph` | `T` | `TreismanGelade1980` | `inferred` | Letter-based target is a practical psycho-visual instantiation of feature conjunction manipulation. |
| `controller.conjunction_alt_glyph` | `L` | `Wolfe1994` | `inferred` | Alternate distractor letter supports conjunction competition while maintaining recognizability. |
| `controller.target_color` / `distractor_color` | `red` / `green` | `TreismanGelade1980` | `inferred` | Color-channel contrast creates clear feature vs conjunction conditions. |
| `controller.array_radius_px` | `245` | `DuncanHumphreys1989` | `inferred` | Ring layout controls eccentricity and reduces item overlap at tested set sizes. |
| `triggers.map.search_onset` | `30` | `Wolfe1994` | `implemented` | Marks onset of the decision-critical search display. |
| `triggers.map.response_present` | `31` | `DuncanHumphreys1989` | `implemented` | Distinguishes present responses for synchronization and analysis. |
| `triggers.map.response_absent` | `32` | `DuncanHumphreys1989` | `implemented` | Distinguishes absent responses for synchronization and analysis. |
| `triggers.map.search_timeout` | `33` | `DuncanHumphreys1989` | `implemented` | Marks missed responses under speeded deadline constraints. |
