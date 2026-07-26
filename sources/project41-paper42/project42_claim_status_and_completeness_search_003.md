# Project 42 Claim Status and Completeness Search 003

Project: `/Users/scottcave/dev/cori/research/mathematics/thalean-graph-theory/41-order-4-dodecahedral-residue`

## Claim ledger

### Aut(X) has order 720

- Status: `locked`
- Source: `028N, 028O, 028M, 028Q`

### natural quotient stabilizer is S5 x C2 of order 240

- Status: `locked`
- Source: `028N, 028O, 028M, 028Q`

### natural partition orbit has size 3

- Status: `locked`
- Source: `028N, 028O, 028M, 028Q`

### natural pair orbit contains 45 distinct pairs

- Status: `locked`
- Source: `028N, 028M`

### Aut(X) is S5 x S3

- Status: `locked`
- Source: `028O`

### vertex action is S5/V4_even

- Status: `locked`
- Source: `028P`

### X is unique connected triangle-free quartic orbital

- Status: `locked`
- Source: `028P`

### there exist no admissible L(P)-quotient systems outside the natural orbit

- Status: `not yet demonstrated by current packet`
- Source: `requires exhaustive involution or partition census`

### the three orbit partitions are pairwise block-disjoint

- Status: `locked`
- Source: `028N forty-five-pair orbit`

## Core artifact boundaries

### `artifacts/json/all_one_full_automorphism_census_audit_028n.json`

Verdict: `the_all_one_bipartite_cover_has_full_automorphism_order720_and_its_natural_G15_partition_has_order240_stabilizer_and_orbit_size3`

Boundary:

```json
{"group_structure_identified_here": false, "historical_replay_used": false, "natural_G15_partition_characteristic": false, "networkx_full_enumeration_used": true}
```

Important fields:

- `$.boundary`: `{"group_structure_identified_here": false, "historical_replay_used": false, "natural_G15_partition_characteristic": false, "networkx_full_enumeration_used": true}`
- `$.boundary.group_structure_identified_here`: `false`
- `$.boundary.historical_replay_used`: `false`
- `$.boundary.natural_G15_partition_characteristic`: `false`
- `$.boundary.networkx_full_enumeration_used`: `true`
- `$.measurements.expected_240_partition_stabilizer_pass`: `true`
- `$.measurements.natural_pair_orbit`: `[[0, 1], [0, 11], [0, 29], [1, 10], [1, 28], [2, 3], [2, 13], [2, 25], [3, 12], [3, 24], [4, 5], [4, 19], [4, 27], [5, 18], [5, 26], [6, 7], [6, 15], [6, 23], [7, 14], [7, 22], [8, 9], [8, 17], [8, 21], [9, 16], [9, 20], [10, 11], [10, 29], [11, 28], [12, 13], [12, 25], [13, 24], [14, 15], [14, 23], [15, 22], [16, 17], [16, 21], [17, 20], [18, 19], [18, 27], [19, 26], [20, 21], [22, 23], [24, 25], [26, 27], [28, 29]]`
- `$.measurements.natural_pair_orbit[0]`: `[0, 1]`
- `$.measurements.natural_pair_orbit[0][0]`: `0`
- `$.measurements.natural_pair_orbit[0][1]`: `1`
- `$.measurements.natural_pair_orbit[1]`: `[0, 11]`
- `$.measurements.natural_pair_orbit[1][0]`: `0`
- `$.measurements.natural_pair_orbit[1][1]`: `11`
- `$.measurements.natural_pair_orbit[2]`: `[0, 29]`
- `$.measurements.natural_pair_orbit[2][0]`: `0`
- `$.measurements.natural_pair_orbit[2][1]`: `29`
- `$.measurements.natural_pair_orbit[3]`: `[1, 10]`
- `$.measurements.natural_pair_orbit[3][0]`: `1`
- `$.measurements.natural_pair_orbit[3][1]`: `10`
- `$.measurements.natural_pair_orbit[4]`: `[1, 28]`
- `$.measurements.natural_pair_orbit[4][0]`: `1`
- `$.measurements.natural_pair_orbit[4][1]`: `28`
- `$.measurements.natural_pair_orbit[5]`: `[2, 3]`
- `$.measurements.natural_pair_orbit[5][0]`: `2`
- `$.measurements.natural_pair_orbit[5][1]`: `3`
- `$.measurements.natural_pair_orbit[6]`: `[2, 13]`
- `$.measurements.natural_pair_orbit[6][0]`: `2`
- `$.measurements.natural_pair_orbit[6][1]`: `13`
- `$.measurements.natural_pair_orbit[7]`: `[2, 25]`
- `$.measurements.natural_pair_orbit[7][0]`: `2`
- `$.measurements.natural_pair_orbit[7][1]`: `25`
- `$.measurements.natural_pair_orbit[8]`: `[3, 12]`
- `$.measurements.natural_pair_orbit[8][0]`: `3`
- `$.measurements.natural_pair_orbit[8][1]`: `12`
- `$.measurements.natural_pair_orbit[9]`: `[3, 24]`
- `$.measurements.natural_pair_orbit[9][0]`: `3`
- `$.measurements.natural_pair_orbit[9][1]`: `24`
- `$.measurements.natural_pair_orbit[10]`: `[4, 5]`
- `$.measurements.natural_pair_orbit[10][0]`: `4`
- `$.measurements.natural_pair_orbit[10][1]`: `5`
- `$.measurements.natural_pair_orbit[11]`: `[4, 19]`
- `$.measurements.natural_pair_orbit[11][0]`: `4`
- `$.measurements.natural_pair_orbit[11][1]`: `19`
- `$.measurements.natural_pair_orbit[12]`: `[4, 27]`
- `$.measurements.natural_pair_orbit[12][0]`: `4`
- `$.measurements.natural_pair_orbit[12][1]`: `27`
- `$.measurements.natural_pair_orbit[13]`: `[5, 18]`
- `$.measurements.natural_pair_orbit[13][0]`: `5`
- `$.measurements.natural_pair_orbit[13][1]`: `18`
- `$.measurements.natural_pair_orbit[14]`: `[5, 26]`
- `$.measurements.natural_pair_orbit[14][0]`: `5`
- `$.measurements.natural_pair_orbit[14][1]`: `26`
- `$.measurements.natural_pair_orbit[15]`: `[6, 7]`
- `$.measurements.natural_pair_orbit[15][0]`: `6`
- `$.measurements.natural_pair_orbit[15][1]`: `7`
- `$.measurements.natural_pair_orbit[16]`: `[6, 15]`
- `$.measurements.natural_pair_orbit[16][0]`: `6`
- `$.measurements.natural_pair_orbit[16][1]`: `15`
- `$.measurements.natural_pair_orbit[17]`: `[6, 23]`
- `$.measurements.natural_pair_orbit[17][0]`: `6`
- `$.measurements.natural_pair_orbit[17][1]`: `23`
- `$.measurements.natural_pair_orbit[18]`: `[7, 14]`
- `$.measurements.natural_pair_orbit[18][0]`: `7`
- `$.measurements.natural_pair_orbit[18][1]`: `14`
- `$.measurements.natural_pair_orbit[19]`: `[7, 22]`
- `$.measurements.natural_pair_orbit[19][0]`: `7`
- `$.measurements.natural_pair_orbit[19][1]`: `22`
- `$.measurements.natural_pair_orbit[20]`: `[8, 9]`
- `$.measurements.natural_pair_orbit[20][0]`: `8`
- `$.measurements.natural_pair_orbit[20][1]`: `9`
- `$.measurements.natural_pair_orbit[21]`: `[8, 17]`
- `$.measurements.natural_pair_orbit[21][0]`: `8`
- `$.measurements.natural_pair_orbit[21][1]`: `17`
- `$.measurements.natural_pair_orbit[22]`: `[8, 21]`
- `$.measurements.natural_pair_orbit[22][0]`: `8`
- `$.measurements.natural_pair_orbit[22][1]`: `21`
- `$.measurements.natural_pair_orbit[23]`: `[9, 16]`
- `$.measurements.natural_pair_orbit[23][0]`: `9`
- `$.measurements.natural_pair_orbit[23][1]`: `16`
- `$.measurements.natural_pair_orbit[24]`: `[9, 20]`
- `$.measurements.natural_pair_orbit[24][0]`: `9`
- `$.measurements.natural_pair_orbit[24][1]`: `20`
- `$.measurements.natural_pair_orbit[25]`: `[10, 11]`
- `$.measurements.natural_pair_orbit[25][0]`: `10`
- `$.measurements.natural_pair_orbit[25][1]`: `11`
- `$.measurements.natural_pair_orbit[26]`: `[10, 29]`
- `$.measurements.natural_pair_orbit[26][0]`: `10`
- `$.measurements.natural_pair_orbit[26][1]`: `29`
- `$.measurements.natural_pair_orbit[27]`: `[11, 28]`
- `$.measurements.natural_pair_orbit[27][0]`: `11`
- `$.measurements.natural_pair_orbit[27][1]`: `28`
- `$.measurements.natural_pair_orbit[28]`: `[12, 13]`
- `$.measurements.natural_pair_orbit[28][0]`: `12`
- `$.measurements.natural_pair_orbit[28][1]`: `13`
- `$.measurements.natural_pair_orbit[29]`: `[12, 25]`
- `$.measurements.natural_pair_orbit[29][0]`: `12`
- `$.measurements.natural_pair_orbit[29][1]`: `25`
- `$.measurements.natural_pair_orbit[30]`: `[13, 24]`
- `$.measurements.natural_pair_orbit[30][0]`: `13`
- `$.measurements.natural_pair_orbit[30][1]`: `24`
- `$.measurements.natural_pair_orbit[31]`: `[14, 15]`
- `$.measurements.natural_pair_orbit[31][0]`: `14`
- `$.measurements.natural_pair_orbit[31][1]`: `15`
- `$.measurements.natural_pair_orbit[32]`: `[14, 23]`
- `$.measurements.natural_pair_orbit[32][0]`: `14`
- `$.measurements.natural_pair_orbit[32][1]`: `23`
- `$.measurements.natural_pair_orbit[33]`: `[15, 22]`
- `$.measurements.natural_pair_orbit[33][0]`: `15`
- `$.measurements.natural_pair_orbit[33][1]`: `22`
- `$.measurements.natural_pair_orbit[34]`: `[16, 17]`
- `$.measurements.natural_pair_orbit[34][0]`: `16`
- `$.measurements.natural_pair_orbit[34][1]`: `17`
- `$.measurements.natural_pair_orbit[35]`: `[16, 21]`
- `$.measurements.natural_pair_orbit[35][0]`: `16`
- `$.measurements.natural_pair_orbit[35][1]`: `21`
- `$.measurements.natural_pair_orbit[36]`: `[17, 20]`
- `$.measurements.natural_pair_orbit[36][0]`: `17`
- `$.measurements.natural_pair_orbit[36][1]`: `20`
- `$.measurements.natural_pair_orbit[37]`: `[18, 19]`
- `$.measurements.natural_pair_orbit[37][0]`: `18`
- `$.measurements.natural_pair_orbit[37][1]`: `19`
- `$.measurements.natural_pair_orbit[38]`: `[18, 27]`
- `$.measurements.natural_pair_orbit[38][0]`: `18`
- `$.measurements.natural_pair_orbit[38][1]`: `27`
- `$.measurements.natural_pair_orbit[39]`: `[19, 26]`
- `$.measurements.natural_pair_orbit[39][0]`: `19`
- `$.measurements.natural_pair_orbit[39][1]`: `26`
- `$.measurements.natural_pair_orbit[40]`: `[20, 21]`
- `$.measurements.natural_pair_orbit[40][0]`: `20`
- `$.measurements.natural_pair_orbit[40][1]`: `21`
- `$.measurements.natural_pair_orbit[41]`: `[22, 23]`
- `$.measurements.natural_pair_orbit[41][0]`: `22`
- `$.measurements.natural_pair_orbit[41][1]`: `23`
- `$.measurements.natural_pair_orbit[42]`: `[24, 25]`
- `$.measurements.natural_pair_orbit[42][0]`: `24`
- `$.measurements.natural_pair_orbit[42][1]`: `25`
- `$.measurements.natural_pair_orbit[43]`: `[26, 27]`
- `$.measurements.natural_pair_orbit[43][0]`: `26`
- `$.measurements.natural_pair_orbit[43][1]`: `27`
- `$.measurements.natural_pair_orbit[44]`: `[28, 29]`
- `$.measurements.natural_pair_orbit[44][0]`: `28`
- `$.measurements.natural_pair_orbit[44][1]`: `29`
- `$.measurements.natural_pair_orbit_size`: `45`
- `$.measurements.natural_partition_orbit_size`: `3`
- `$.measurements.natural_partition_stabilizer_count`: `240`
- `$.measurements.orbit_stabilizer_pass`: `true`
- `$.verdict`: `"the_all_one_bipartite_cover_has_full_automorphism_order720_and_its_natural_G15_partition_has_order240_stabilizer_and_orbit_size3"`

### `artifacts/json/all_one_group_anatomy_audit_028o.json`

Verdict: `the_all_one_cover_automorphism_group_is_exactly_S5_times_S3_with_trivial_center_derived_subgroup_A5_times_C3_and_natural_partition_stabilizer_S5_times_C2`

Boundary:

```json
{"graph_identification_claimed_here": false, "historical_replay_used": false, "isomorphism_is_exact_permutation_group_certificate": true}
```

Important fields:

- `$.boundary`: `{"graph_identification_claimed_here": false, "historical_replay_used": false, "isomorphism_is_exact_permutation_group_certificate": true}`
- `$.boundary.graph_identification_claimed_here`: `false`
- `$.boundary.historical_replay_used`: `false`
- `$.boundary.isomorphism_is_exact_permutation_group_certificate`: `true`
- `$.measurements.centralizer_element_order_distribution`: `{"1": 1, "2": 3, "3": 2}`
- `$.measurements.centralizer_element_order_distribution.1`: `1`
- `$.measurements.centralizer_element_order_distribution.2`: `3`
- `$.measurements.centralizer_element_order_distribution.3`: `2`
- `$.measurements.centralizer_is_S3_pass`: `true`
- `$.measurements.kernel_centralizer_intersection_order`: `1`
- `$.measurements.kernel_centralizer_order`: `6`
- `$.measurements.kernel_element_order_distribution`: `{"1": 1, "2": 25, "3": 20, "4": 30, "5": 24, "6": 20}`
- `$.measurements.kernel_element_order_distribution.1`: `1`
- `$.measurements.kernel_element_order_distribution.2`: `25`
- `$.measurements.kernel_element_order_distribution.3`: `20`
- `$.measurements.kernel_element_order_distribution.4`: `30`
- `$.measurements.kernel_element_order_distribution.5`: `24`
- `$.measurements.kernel_element_order_distribution.6`: `20`
- `$.measurements.kernel_is_S5_pass`: `true`
- `$.measurements.kernel_times_centralizer_order`: `720`
- `$.measurements.natural_partition_stabilizer_order`: `240`
- `$.measurements.natural_partition_stabilizer_structure`: `"S5_x_C2"`
- `$.measurements.natural_stabilizer_element_order_distribution`: `{"1": 1, "10": 24, "2": 51, "3": 20, "4": 60, "5": 24, "6": 60}`
- `$.measurements.natural_stabilizer_element_order_distribution.1`: `1`
- `$.measurements.natural_stabilizer_element_order_distribution.10`: `24`
- `$.measurements.natural_stabilizer_element_order_distribution.2`: `51`
- `$.measurements.natural_stabilizer_element_order_distribution.3`: `20`
- `$.measurements.natural_stabilizer_element_order_distribution.4`: `60`
- `$.measurements.natural_stabilizer_element_order_distribution.5`: `24`
- `$.measurements.natural_stabilizer_element_order_distribution.6`: `60`
- `$.measurements.partition_action_image_order`: `6`
- `$.measurements.partition_action_image_order_profile`: `{"1": 1, "2": 3, "3": 2}`
- `$.measurements.partition_action_image_order_profile.1`: `1`
- `$.measurements.partition_action_image_order_profile.2`: `3`
- `$.measurements.partition_action_image_order_profile.3`: `2`
- `$.measurements.partition_action_kernel_order`: `120`
- `$.measurements.partition_orbit_size`: `3`
- `$.verdict`: `"the_all_one_cover_automorphism_group_is_exactly_S5_times_S3_with_trivial_center_derived_subgroup_A5_times_C3_and_natural_partition_stabilizer_S5_times_C2"`

### `artifacts/json/all_one_oriented_frame_identification_audit_028p.json`

Verdict: `the_all_one_cover_is_the_unique_connected_triangle_free_degree4_S5_orbital_graph_on_the_oriented_frame_coset_geometry_S5_over_even_V4`

Boundary:

```json
{"historical_replay_used": false, "native_mixed_V4_quotient_identified_as_same_graph": false, "standard_external_graph_name_claimed": false}
```

Important fields:

- `$.boundary`: `{"historical_replay_used": false, "native_mixed_V4_quotient_identified_as_same_graph": false, "standard_external_graph_name_claimed": false}`
- `$.boundary.historical_replay_used`: `false`
- `$.boundary.native_mixed_V4_quotient_identified_as_same_graph`: `false`
- `$.boundary.standard_external_graph_name_claimed`: `false`
- `$.measurements.S5_kernel_order`: `120`
- `$.measurements.S5_vertex_orbit_size`: `30`
- `$.measurements.all_one_is_unique_connected_triangle_free_degree4_orbital`: `true`
- `$.measurements.degree4_orbital_candidate_count`: `4`
- `$.measurements.degree4_orbital_candidates`: `[{"bipartite": false, "component_sizes": [15, 15], "degree_set": [4], "edge_count": 60, "equals_all_one": false, "orbit_index": 1, "orbit_size": 60, "seed_pair": [0, 2], "triangle_count": 20}, {"bipartite": true, "component_sizes": [30], "degree_set": [4], "edge_count": 60, "equals_all_one": true, "orbit_index": 2, "orbit_size": 60, "seed_pair": [0, 3], "triangle_count": 0}, {"bipartite": false, "component_sizes": [15, 15], "degree_set": [4], "edge_count": 60, "equals_all_one": false, "orbit_index": 3, "orbit_size": 60, "seed_pair": [0, 4], "triangle_count": 20}, {"bipartite": false, "component_sizes": [15, 15], "degree_set": [4], "edge_count": 60, "equals_all_one": false, "orbit_index": 7, "orbit_size": 60, "seed_pair": [0, 14], "triangle_count": 20}]`
- `$.measurements.degree4_orbital_candidates[0]`: `{"bipartite": false, "component_sizes": [15, 15], "degree_set": [4], "edge_count": 60, "equals_all_one": false, "orbit_index": 1, "orbit_size": 60, "seed_pair": [0, 2], "triangle_count": 20}`
- `$.measurements.degree4_orbital_candidates[0].bipartite`: `false`
- `$.measurements.degree4_orbital_candidates[0].component_sizes`: `[15, 15]`
- `$.measurements.degree4_orbital_candidates[0].component_sizes[0]`: `15`
- `$.measurements.degree4_orbital_candidates[0].component_sizes[1]`: `15`
- `$.measurements.degree4_orbital_candidates[0].degree_set`: `[4]`
- `$.measurements.degree4_orbital_candidates[0].degree_set[0]`: `4`
- `$.measurements.degree4_orbital_candidates[0].edge_count`: `60`
- `$.measurements.degree4_orbital_candidates[0].equals_all_one`: `false`
- `$.measurements.degree4_orbital_candidates[0].orbit_index`: `1`
- `$.measurements.degree4_orbital_candidates[0].orbit_size`: `60`
- `$.measurements.degree4_orbital_candidates[0].seed_pair`: `[0, 2]`
- `$.measurements.degree4_orbital_candidates[0].seed_pair[0]`: `0`
- `$.measurements.degree4_orbital_candidates[0].seed_pair[1]`: `2`
- `$.measurements.degree4_orbital_candidates[0].triangle_count`: `20`
- `$.measurements.degree4_orbital_candidates[1]`: `{"bipartite": true, "component_sizes": [30], "degree_set": [4], "edge_count": 60, "equals_all_one": true, "orbit_index": 2, "orbit_size": 60, "seed_pair": [0, 3], "triangle_count": 0}`
- `$.measurements.degree4_orbital_candidates[1].bipartite`: `true`
- `$.measurements.degree4_orbital_candidates[1].component_sizes`: `[30]`
- `$.measurements.degree4_orbital_candidates[1].component_sizes[0]`: `30`
- `$.measurements.degree4_orbital_candidates[1].degree_set`: `[4]`
- `$.measurements.degree4_orbital_candidates[1].degree_set[0]`: `4`
- `$.measurements.degree4_orbital_candidates[1].edge_count`: `60`
- `$.measurements.degree4_orbital_candidates[1].equals_all_one`: `true`
- `$.measurements.degree4_orbital_candidates[1].orbit_index`: `2`
- `$.measurements.degree4_orbital_candidates[1].orbit_size`: `60`
- `$.measurements.degree4_orbital_candidates[1].seed_pair`: `[0, 3]`
- `$.measurements.degree4_orbital_candidates[1].seed_pair[0]`: `0`
- `$.measurements.degree4_orbital_candidates[1].seed_pair[1]`: `3`
- `$.measurements.degree4_orbital_candidates[1].triangle_count`: `0`
- `$.measurements.degree4_orbital_candidates[2]`: `{"bipartite": false, "component_sizes": [15, 15], "degree_set": [4], "edge_count": 60, "equals_all_one": false, "orbit_index": 3, "orbit_size": 60, "seed_pair": [0, 4], "triangle_count": 20}`
- `$.measurements.degree4_orbital_candidates[2].bipartite`: `false`
- `$.measurements.degree4_orbital_candidates[2].component_sizes`: `[15, 15]`
- `$.measurements.degree4_orbital_candidates[2].component_sizes[0]`: `15`
- `$.measurements.degree4_orbital_candidates[2].component_sizes[1]`: `15`
- `$.measurements.degree4_orbital_candidates[2].degree_set`: `[4]`
- `$.measurements.degree4_orbital_candidates[2].degree_set[0]`: `4`
- `$.measurements.degree4_orbital_candidates[2].edge_count`: `60`
- `$.measurements.degree4_orbital_candidates[2].equals_all_one`: `false`
- `$.measurements.degree4_orbital_candidates[2].orbit_index`: `3`
- `$.measurements.degree4_orbital_candidates[2].orbit_size`: `60`
- `$.measurements.degree4_orbital_candidates[2].seed_pair`: `[0, 4]`
- `$.measurements.degree4_orbital_candidates[2].seed_pair[0]`: `0`
- `$.measurements.degree4_orbital_candidates[2].seed_pair[1]`: `4`
- `$.measurements.degree4_orbital_candidates[2].triangle_count`: `20`
- `$.measurements.degree4_orbital_candidates[3]`: `{"bipartite": false, "component_sizes": [15, 15], "degree_set": [4], "edge_count": 60, "equals_all_one": false, "orbit_index": 7, "orbit_size": 60, "seed_pair": [0, 14], "triangle_count": 20}`
- `$.measurements.degree4_orbital_candidates[3].bipartite`: `false`
- `$.measurements.degree4_orbital_candidates[3].component_sizes`: `[15, 15]`
- `$.measurements.degree4_orbital_candidates[3].component_sizes[0]`: `15`
- `$.measurements.degree4_orbital_candidates[3].component_sizes[1]`: `15`
- `$.measurements.degree4_orbital_candidates[3].degree_set`: `[4]`
- `$.measurements.degree4_orbital_candidates[3].degree_set[0]`: `4`
- `$.measurements.degree4_orbital_candidates[3].edge_count`: `60`
- `$.measurements.degree4_orbital_candidates[3].equals_all_one`: `false`
- `$.measurements.degree4_orbital_candidates[3].orbit_index`: `7`
- `$.measurements.degree4_orbital_candidates[3].orbit_size`: `60`
- `$.measurements.degree4_orbital_candidates[3].seed_pair`: `[0, 14]`
- `$.measurements.degree4_orbital_candidates[3].seed_pair[0]`: `0`
- `$.measurements.degree4_orbital_candidates[3].seed_pair[1]`: `14`
- `$.measurements.degree4_orbital_candidates[3].triangle_count`: `20`
- `$.measurements.partition_orbit_size`: `3`
- `$.measurements.unordered_pair_orbit_count`: `9`
- `$.measurements.vertex_stabilizer_all_even`: `true`
- `$.measurements.vertex_stabilizer_element_order_profile`: `{"1": 1, "2": 3}`
- `$.measurements.vertex_stabilizer_element_order_profile.1`: `1`
- `$.measurements.vertex_stabilizer_element_order_profile.2`: `3`
- `$.measurements.vertex_stabilizer_identification`: `"V4_even"`
- `$.measurements.vertex_stabilizer_order`: `4`
- `$.measurements.vertex_stabilizer_petersen_parities`: `[0, 0, 0, 0]`
- `$.measurements.vertex_stabilizer_petersen_parities[0]`: `0`
- `$.measurements.vertex_stabilizer_petersen_parities[1]`: `0`
- `$.measurements.vertex_stabilizer_petersen_parities[2]`: `0`
- `$.measurements.vertex_stabilizer_petersen_parities[3]`: `0`
- `$.verdict`: `"the_all_one_cover_is_the_unique_connected_triangle_free_degree4_S5_orbital_graph_on_the_oriented_frame_coset_geometry_S5_over_even_V4"`

### `artifacts/json/invariant_cover_square_automorphism_orders_audit_028m.json`

Verdict: `the_four_S5_fixed_C2_cover_classes_have_exact_full_automorphism_orders_28800_240_240_720_for_zero_native_alternative_all_one`

Boundary:

```json
{"all_one_order_uses_independent_full_enumeration": true, "connected_extension_splitting_tested": false, "historical_replay_used": false, "named_graph_identification_claimed": false, "project_mutation_during_computation": false}
```

Important fields:

- `$.boundary`: `{"all_one_order_uses_independent_full_enumeration": true, "connected_extension_splitting_tested": false, "historical_replay_used": false, "named_graph_identification_claimed": false, "project_mutation_during_computation": false}`
- `$.boundary.all_one_order_uses_independent_full_enumeration`: `true`
- `$.boundary.connected_extension_splitting_tested`: `false`
- `$.boundary.historical_replay_used`: `false`
- `$.boundary.named_graph_identification_claimed`: `false`
- `$.boundary.project_mutation_during_computation`: `false`
- `$.checks.all_one_orbit_stabilizer`: `true`
- `$.checks.all_one_partition_orbit_3`: `true`
- `$.checks.all_one_partition_stabilizer_240`: `true`
- `$.checks.all_one_worker_constructs_240_stabilizer`: `true`
- `$.checks.oriented_frame_unique_orbital`: `true`
- `$.measurements.all_one_full_census.natural_pair_orbit_size`: `45`
- `$.measurements.all_one_full_census.partition_orbit_size`: `3`
- `$.measurements.all_one_full_census.partition_stabilizer_order`: `240`
- `$.measurements.all_one_initial_worker.kernel_order`: `2`
- `$.measurements.all_one_initial_worker.rounds[0].unordered_pair_class_count`: `2`
- `$.measurements.all_one_initial_worker.rounds[1].unordered_pair_class_count`: `3`
- `$.measurements.all_one_initial_worker.rounds[2].unordered_pair_class_count`: `5`
- `$.measurements.all_one_initial_worker.rounds[3].unordered_pair_class_count`: `5`
- `$.measurements.all_one_initial_worker.rounds[4].unordered_pair_class_count`: `5`
- `$.measurements.all_one_initial_worker.rounds[5].unordered_pair_class_count`: `5`
- `$.measurements.all_one_initial_worker.rounds[6].unordered_pair_class_count`: `5`
- `$.measurements.alternative.kernel_order`: `2`
- `$.measurements.alternative.rounds[0].unordered_pair_class_count`: `2`
- `$.measurements.alternative.rounds[1].unordered_pair_class_count`: `3`
- `$.measurements.alternative.rounds[2].unordered_pair_class_count`: `6`
- `$.measurements.native.kernel_order`: `2`
- `$.measurements.native.rounds[0].unordered_pair_class_count`: `2`
- `$.measurements.native.rounds[1].unordered_pair_class_count`: `3`
- `$.measurements.native.rounds[2].unordered_pair_class_count`: `6`
- `$.verdict`: `"the_four_S5_fixed_C2_cover_classes_have_exact_full_automorphism_orders_28800_240_240_720_for_zero_native_alternative_all_one"`

### `artifacts/json/invariant_cover_square_closure_audit_028q.json`

Verdict: `the_invariant_cover_square_is_closed_at_full_automorphism_order_and_the_all_one_class_is_exactly_the_unique_connected_triangle_free_degree4_orbital_on_S5_over_even_V4_with_full_group_S5_times_S3`

Boundary:

```json
{"archived_G30_identified": false, "connected_extension_splitting_for_native_and_alternative": false, "external_standard_graph_name_for_all_one": false, "historical_replay_used": false, "physics_claim": false}
```

Important fields:

- `$.boundary`: `{"archived_G30_identified": false, "connected_extension_splitting_for_native_and_alternative": false, "external_standard_graph_name_for_all_one": false, "historical_replay_used": false, "physics_claim": false}`
- `$.boundary.archived_G30_identified`: `false`
- `$.boundary.connected_extension_splitting_for_native_and_alternative`: `false`
- `$.boundary.external_standard_graph_name_for_all_one`: `false`
- `$.boundary.historical_replay_used`: `false`
- `$.boundary.physics_claim`: `false`
- `$.checks.all_one_orbit_stabilizer`: `true`
- `$.checks.all_one_partition_orbit_3`: `true`
- `$.checks.all_one_partition_stabilizer_240`: `true`
- `$.checks.all_one_worker_constructs_240_stabilizer`: `true`
- `$.checks.oriented_frame_unique_orbital`: `true`
- `$.closed_results.all_one_partition_action`: `"S3"`
- `$.closed_results.all_one_partition_count`: `3`
- `$.closed_results.all_one_partition_stabilizer`: `"S5_x_C2"`
- `$.verdict`: `"the_invariant_cover_square_is_closed_at_full_automorphism_order_and_the_all_one_class_is_exactly_the_unique_connected_triangle_free_degree4_orbital_on_S5_over_even_V4_with_full_group_S5_times_S3"`

## Completeness search hits

No candidate completeness artifact found.
