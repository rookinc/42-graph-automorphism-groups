# Project 42 Certificate Source Inventory

Repository: `/Users/scottcave/dev/cori/research/mathematics/thalean-graph-theory/41-order-4-dodecahedral-residue`

Matching files: 59

## `artifacts/json/all_one_full_automorphism_census_audit_028n.json`

Matched terms: all_one

- `$.measurements.status`: `project41_all_one_full_aut_census_complete`
- `$.verdict`: `the_all_one_bipartite_cover_has_full_automorphism_order720_and_its_natural_G15_partition_has_order240_stabilizer_and_orbit_size3`

## `artifacts/json/all_one_group_anatomy_audit_028o.json`

Matched terms: centralizer, kernel, all_one

- `$.measurements.centralizer_element_order_distribution.1`: `1`
- `$.measurements.centralizer_element_order_distribution.2`: `3`
- `$.measurements.centralizer_element_order_distribution.3`: `2`
- `$.measurements.centralizer_is_S3_pass`: `True`
- `$.measurements.kernel_centralizer_intersection_order`: `1`
- `$.measurements.kernel_centralizer_order`: `6`
- `$.measurements.kernel_element_order_distribution.1`: `1`
- `$.measurements.kernel_element_order_distribution.2`: `25`
- `$.measurements.kernel_element_order_distribution.3`: `20`
- `$.measurements.kernel_element_order_distribution.4`: `30`
- `$.measurements.kernel_element_order_distribution.5`: `24`
- `$.measurements.kernel_element_order_distribution.6`: `20`
- `$.measurements.kernel_is_S5_pass`: `True`
- `$.measurements.kernel_times_centralizer_order`: `720`
- `$.measurements.partition_action_kernel_order`: `120`
- `$.measurements.status`: `project41_all_one_group_anatomy_complete`
- `$.verdict`: `the_all_one_cover_automorphism_group_is_exactly_S5_times_S3_with_trivial_center_derived_subgroup_A5_times_C3_and_natural_partition_stabilizer_S5_times_C2`

## `artifacts/json/all_one_oriented_frame_identification_audit_028p.json`

Matched terms: kernel, V4_even, even_v4, all_one

- `$.measurements.S5_kernel_order`: `120`
- `$.measurements.all_one_is_unique_connected_triangle_free_degree4_orbital`: `True`
- `$.measurements.coset_geometry`: `S5_over_V4_even`
- `$.measurements.degree4_orbital_candidates[0].equals_all_one`: `False`
- `$.measurements.degree4_orbital_candidates[1].equals_all_one`: `True`
- `$.measurements.degree4_orbital_candidates[2].equals_all_one`: `False`
- `$.measurements.degree4_orbital_candidates[3].equals_all_one`: `False`
- `$.measurements.status`: `project41_all_one_oriented_frame_identification_complete`
- `$.measurements.vertex_stabilizer_identification`: `V4_even`
- `$.verdict`: `the_all_one_cover_is_the_unique_connected_triangle_free_degree4_S5_orbital_graph_on_the_oriented_frame_coset_geometry_S5_over_even_V4`

## `artifacts/json/character_phase_compensation_audit_027e.json`

Matched terms: kernel

- `$.sources.audit027d.verdict`: `the_global_interface_obstruction_characters_are_exactly_diagonal_native_v4_axis_characters_G0_uses_both_ordered_pentagon_stabilizer_axes_G1_uses_the_right_stabilizer_axis_G2_uses_the_left_stabilizer_axis_and_G3_uses_their_product_sign_kernel_axis`

## `artifacts/json/dual_icosahedral_distance_decomposition_audit_028f.json`

Matched terms: kernel

- `$.sources.audit025.verdict`: `the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab`

## `artifacts/json/explicit_standard_a5_identification_audit_016.json`

Matched terms: kernel

- `$.checks.five_point_action_kernel_is_trivial`: `True`
- `$.interpretation`: `The order-60 regular group acts by conjugation on its five V4 subgroups. This action is defined on every group element, is a homomorphism, has trivial kernel, and has an image of order 60. Every image permutation is even, and the image is exactly the full standard alternating group on five points. Therefore the native G60 Cayley group is explicitly isomorphic to standard A5.`
- `$.measurements.five_point_action_kernel_size`: `1`

## `artifacts/json/index5_refinement_action_audit_028k.json`

Matched terms: kernel

- `$.boundary.action_kernel_order`: `2`
- `$.checks.action_kernel_order2`: `True`
- `$.interpretation`: `The five conjugate rank-8 refinements are the coset geometry of the self-normalizing order-24 color subgroup inside the full order-120 icosahedral graph automorphism group. Conjugation gives a faithful quotient after removing a central kernel of order two. The image is A5 in its standard 2-transitive degree-five action. Thus the five refinements form an intrinsic K5 object, and the original rank-8 refinement is one distinguished K5 vertex whose stabilizer is C2 times A4.`
- `$.measurements.action_kernel_order`: `2`
- `$.verdict`: `the_five_conjugate_rank8_refinements_carry_the_exact_degree5_quotient_action_of_the_full_icosahedral_group_with_kernel_C2_and_image_A5_the_action_is_2_transitive_the_original_C2_times_A4_color_group_is_one_point_stabilizer_and_the_five_refinements_therefore_form_an_intrinsic_K5_set`

## `artifacts/json/invariant_cover_square_automorphism_orders_audit_028m.json`

Matched terms: kernel, all_one, 28800

- `$.boundary.all_one_order_uses_independent_full_enumeration`: `True`
- `$.checks.all_one_center_trivial`: `True`
- `$.checks.all_one_derived_order_180`: `True`
- `$.checks.all_one_exact_structure`: `True`
- `$.checks.all_one_full_order_720`: `True`
- `$.checks.all_one_orbit_stabilizer`: `True`
- `$.checks.all_one_partition_orbit_3`: `True`
- `$.checks.all_one_partition_stabilizer_240`: `True`
- `$.checks.all_one_structure_S5_x_S3`: `True`
- `$.checks.all_one_worker_constructs_240_stabilizer`: `True`
- `$.checks.all_one_worker_does_not_claim_full_order`: `True`
- `$.checks.zero_order_28800`: `True`
- `$.measurements.all_one_full_census.automorphism_count`: `720`
- `$.measurements.all_one_full_census.natural_pair_orbit_size`: `45`
- `$.measurements.all_one_full_census.partition_orbit_size`: `3`
- `$.measurements.all_one_full_census.partition_stabilizer_order`: `240`
- `$.measurements.all_one_initial_worker.constructed_lift_count`: `240`
- `$.measurements.all_one_initial_worker.exact_order_certificate`: `False`
- `$.measurements.all_one_initial_worker.graph_summary.bipartite`: `True`
- `$.measurements.all_one_initial_worker.graph_summary.component_sizes[0]`: `30`
- `$.measurements.all_one_initial_worker.graph_summary.degree_profile.4`: `30`
- `$.measurements.all_one_initial_worker.graph_summary.edge_count`: `60`
- `$.measurements.all_one_initial_worker.graph_summary.triangle_count`: `0`
- `$.measurements.all_one_initial_worker.intrinsic_projection`: `False`
- `$.measurements.all_one_initial_worker.kernel_order`: `2`
- `$.measurements.all_one_initial_worker.label`: `all_one`
- `$.measurements.all_one_initial_worker.lift_count_profile.2`: `120`
- `$.measurements.all_one_initial_worker.rounds[0].largest_mixed_classes[0][0][0]`: `2`
- `$.measurements.all_one_initial_worker.rounds[0].largest_mixed_classes[0][0][1]`: `2`
- `$.measurements.all_one_initial_worker.rounds[0].largest_mixed_classes[0][1]`: `15`
- `$.measurements.all_one_initial_worker.rounds[0].largest_mixed_classes[0][2]`: `360`
- `$.measurements.all_one_initial_worker.rounds[0].mixed_class_count`: `1`
- `$.measurements.all_one_initial_worker.rounds[0].ordered_color_count`: `3`
- `$.measurements.all_one_initial_worker.rounds[0].recovered_exact`: `False`
- `$.measurements.all_one_initial_worker.rounds[0].relation_separated`: `False`
- `$.measurements.all_one_initial_worker.rounds[0].round`: `0`
- `$.measurements.all_one_initial_worker.rounds[0].unordered_pair_class_count`: `2`
- `$.measurements.all_one_initial_worker.rounds[1].largest_mixed_classes[0][0][0]`: `3`
- `$.measurements.all_one_initial_worker.rounds[1].largest_mixed_classes[0][0][1]`: `3`
- `$.measurements.all_one_initial_worker.rounds[1].largest_mixed_classes[0][1]`: `15`
- `$.measurements.all_one_initial_worker.rounds[1].largest_mixed_classes[0][2]`: `180`
- `$.measurements.all_one_initial_worker.rounds[1].mixed_class_count`: `1`
- `$.measurements.all_one_initial_worker.rounds[1].ordered_color_count`: `4`
- `$.measurements.all_one_initial_worker.rounds[1].recovered_exact`: `False`
- `$.measurements.all_one_initial_worker.rounds[1].relation_separated`: `False`
- `$.measurements.all_one_initial_worker.rounds[1].round`: `1`
- `$.measurements.all_one_initial_worker.rounds[1].unordered_pair_class_count`: `3`
- `$.measurements.all_one_initial_worker.rounds[2].largest_mixed_classes[0][0][0]`: `4`
- `$.measurements.all_one_initial_worker.rounds[2].largest_mixed_classes[0][0][1]`: `4`
- `$.measurements.all_one_initial_worker.rounds[2].largest_mixed_classes[0][1]`: `15`
- `$.measurements.all_one_initial_worker.rounds[2].largest_mixed_classes[0][2]`: `30`
- `$.measurements.all_one_initial_worker.rounds[2].mixed_class_count`: `1`
- `$.measurements.all_one_initial_worker.rounds[2].ordered_color_count`: `6`
- `$.measurements.all_one_initial_worker.rounds[2].recovered_exact`: `False`
- `$.measurements.all_one_initial_worker.rounds[2].relation_separated`: `False`
- `$.measurements.all_one_initial_worker.rounds[2].round`: `2`
- `$.measurements.all_one_initial_worker.rounds[2].unordered_pair_class_count`: `5`
- `$.measurements.all_one_initial_worker.rounds[3].largest_mixed_classes[0][0][0]`: `4`
- `$.measurements.all_one_initial_worker.rounds[3].largest_mixed_classes[0][0][1]`: `4`
- `$.measurements.all_one_initial_worker.rounds[3].largest_mixed_classes[0][1]`: `15`
- `$.measurements.all_one_initial_worker.rounds[3].largest_mixed_classes[0][2]`: `30`
- `$.measurements.all_one_initial_worker.rounds[3].mixed_class_count`: `1`
- `$.measurements.all_one_initial_worker.rounds[3].ordered_color_count`: `6`
- `$.measurements.all_one_initial_worker.rounds[3].recovered_exact`: `False`
- `$.measurements.all_one_initial_worker.rounds[3].relation_separated`: `False`
- `$.measurements.all_one_initial_worker.rounds[3].round`: `3`
- `$.measurements.all_one_initial_worker.rounds[3].unordered_pair_class_count`: `5`
- `$.measurements.all_one_initial_worker.rounds[4].largest_mixed_classes[0][0][0]`: `4`
- `$.measurements.all_one_initial_worker.rounds[4].largest_mixed_classes[0][0][1]`: `4`
- `$.measurements.all_one_initial_worker.rounds[4].largest_mixed_classes[0][1]`: `15`
- `$.measurements.all_one_initial_worker.rounds[4].largest_mixed_classes[0][2]`: `30`
- `$.measurements.all_one_initial_worker.rounds[4].mixed_class_count`: `1`
- `$.measurements.all_one_initial_worker.rounds[4].ordered_color_count`: `6`
- `$.measurements.all_one_initial_worker.rounds[4].recovered_exact`: `False`
- `$.measurements.all_one_initial_worker.rounds[4].relation_separated`: `False`
- `$.measurements.all_one_initial_worker.rounds[4].round`: `4`
- `$.measurements.all_one_initial_worker.rounds[4].unordered_pair_class_count`: `5`
- `$.measurements.all_one_initial_worker.rounds[5].largest_mixed_classes[0][0][0]`: `4`
- `$.measurements.all_one_initial_worker.rounds[5].largest_mixed_classes[0][0][1]`: `4`
- `$.measurements.all_one_initial_worker.rounds[5].largest_mixed_classes[0][1]`: `15`
- `$.measurements.all_one_initial_worker.rounds[5].largest_mixed_classes[0][2]`: `30`
- `$.measurements.all_one_initial_worker.rounds[5].mixed_class_count`: `1`
- `$.measurements.all_one_initial_worker.rounds[5].ordered_color_count`: `6`
- `$.measurements.all_one_initial_worker.rounds[5].recovered_exact`: `False`
- `$.measurements.all_one_initial_worker.rounds[5].relation_separated`: `False`
- `$.measurements.all_one_initial_worker.rounds[5].round`: `5`
- `$.measurements.all_one_initial_worker.rounds[5].unordered_pair_class_count`: `5`
- `$.measurements.all_one_initial_worker.rounds[6].largest_mixed_classes[0][0][0]`: `4`
- `$.measurements.all_one_initial_worker.rounds[6].largest_mixed_classes[0][0][1]`: `4`
- `$.measurements.all_one_initial_worker.rounds[6].largest_mixed_classes[0][1]`: `15`
- `$.measurements.all_one_initial_worker.rounds[6].largest_mixed_classes[0][2]`: `30`
- `$.measurements.all_one_initial_worker.rounds[6].mixed_class_count`: `1`
- `$.measurements.all_one_initial_worker.rounds[6].ordered_color_count`: `6`
- `$.measurements.all_one_initial_worker.rounds[6].recovered_exact`: `False`
- `$.measurements.all_one_initial_worker.rounds[6].relation_separated`: `False`
- `$.measurements.all_one_initial_worker.rounds[6].round`: `6`
- `$.measurements.all_one_initial_worker.rounds[6].unordered_pair_class_count`: `5`
- `$.measurements.alternative.kernel_order`: `2`
- `$.measurements.automorphism_orders.all_one`: `720`
- `$.measurements.automorphism_orders.zero`: `28800`

## `artifacts/json/invariant_cover_square_closure_audit_028q.json`

Matched terms: V4_even, even_v4, all_one, 28800

- `$.boundary.external_standard_graph_name_for_all_one`: `False`
- `$.checks.all_one_center_trivial`: `True`
- `$.checks.all_one_derived_order_180`: `True`
- `$.checks.all_one_exact_structure`: `True`
- `$.checks.all_one_full_order_720`: `True`
- `$.checks.all_one_orbit_stabilizer`: `True`
- `$.checks.all_one_partition_orbit_3`: `True`
- `$.checks.all_one_partition_stabilizer_240`: `True`
- `$.checks.all_one_structure_S5_x_S3`: `True`
- `$.checks.all_one_worker_constructs_240_stabilizer`: `True`
- `$.checks.all_one_worker_does_not_claim_full_order`: `True`
- `$.checks.zero_order_28800`: `True`
- `$.closed_results.all_one_group`: `S5_x_S3`
- `$.closed_results.all_one_partition_action`: `S3`
- `$.closed_results.all_one_partition_count`: `3`
- `$.closed_results.all_one_partition_stabilizer`: `S5_x_C2`
- `$.closed_results.all_one_vertex_set`: `S5_over_V4_even`
- `$.closed_results.automorphism_orders.all_one`: `720`
- `$.closed_results.automorphism_orders.zero`: `28800`
- `$.verdict`: `the_invariant_cover_square_is_closed_at_full_automorphism_order_and_the_all_one_class_is_exactly_the_unique_connected_triangle_free_degree4_orbital_on_S5_over_even_V4_with_full_group_S5_times_S3`

## `artifacts/json/local_shift_pair_admissibility_classification_audit_026b.json`

Matched terms: kernel

- `$.checks.character_has_two_kernel_elements`: `True`
- `$.checks.stabilizer_generator_product_is_kernel_axis`: `True`
- `$.interpretation`: `The failed first 026B run exposed a genuine omitted invariant, not a global obstruction. The actual signed V4 orbit carries ordered left and right order-two pentagon stabilizers. Their nonidentity generators are distinct togglers, and their product is the sign-kernel axis. A left sheet shift equal to the left stabilizer generator collapses left face-copy incidence; the analogous statement holds on the right. Therefore exactly four of the nine gauge-reduced shift pairs are locally admissible. The five rejected pairs are explained exactly by two left-only, two right-only, and one simultaneous stabilizer collision. Once the ordered side stabilizers are retained, the remaining automorphism group is trivial and the four survivors are four distinct ordered local grammar types.`
- `$.native_v4.kernel_axis`: `a`
- `$.sources.audit025.verdict`: `the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab`

## `artifacts/json/native_affine_compensation_audit_027f.json`

Matched terms: kernel

- `$.sources.audit027d.verdict`: `the_global_interface_obstruction_characters_are_exactly_diagonal_native_v4_axis_characters_G0_uses_both_ordered_pentagon_stabilizer_axes_G1_uses_the_right_stabilizer_axis_G2_uses_the_left_stabilizer_axis_and_G3_uses_their_product_sign_kernel_axis`

## `artifacts/json/native_character_axis_interpretation_audit_027d.json`

Matched terms: kernel

- `$.checks.every_certificate_has_native_kernel_axis`: `True`
- `$.checks.ordered_stabilizer_product_is_kernel_axis`: `True`
- `$.interpretation`: `The Audit 027C mask IDs are not arbitrary binary labels. Every certificate has equal left and right masks, so it is a diagonal character chi_r(u,v)=phi_r(u) xor phi_r(v). The one-factor character phi_r has kernel {identity,r}, giving each certificate a native V4 axis. In the ordered local frame, G0 is certified by both pentagon-stabilizer axes, G1 by the right stabilizer axis, G2 by the left stabilizer axis, and G3 by their product, which is the signed-face character kernel axis. Every certificate vanishes on common left-right gauge motion and on the grammar's own sheet-shift pair, but reads every admissible inter-orbit interface as odd.`
- `$.measurements.character_rows[0].kernel_axis`: `b`
- `$.measurements.character_rows[1].kernel_axis`: `ab`
- `$.measurements.character_rows[2].kernel_axis`: `b`
- `$.measurements.character_rows[3].kernel_axis`: `ab`
- `$.measurements.character_rows[4].kernel_axis`: `a`
- `$.native_frame.kernel_axis`: `a`
- `$.sources.audit025.verdict`: `the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab`
- `$.verdict`: `the_global_interface_obstruction_characters_are_exactly_diagonal_native_v4_axis_characters_G0_uses_both_ordered_pentagon_stabilizer_axes_G1_uses_the_right_stabilizer_axis_G2_uses_the_left_stabilizer_axis_and_G3_uses_their_product_sign_kernel_axis`

## `artifacts/json/nested_dodecahedral_registration_audit_028c.json`

Matched terms: kernel

- `$.sources.audit025.verdict`: `the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab`

## `artifacts/json/rank8_schurian_automorphism_group_audit_028j.json`

Matched terms: kernel

- `$.checks.kernel_exact_C2_cubed_shift_law`: `True`
- `$.checks.kernel_order8`: `True`
- `$.checks.rotation_action_fixed_kernel_size2`: `True`
- `$.measurements.even_parity_kernel[0][0]`: `0`
- `$.measurements.even_parity_kernel[0][1]`: `0`
- `$.measurements.even_parity_kernel[0][2]`: `0`
- `$.measurements.even_parity_kernel[1][0]`: `0`
- `$.measurements.even_parity_kernel[1][1]`: `1`
- `$.measurements.even_parity_kernel[1][2]`: `1`
- `$.measurements.even_parity_kernel[2][0]`: `1`
- `$.measurements.even_parity_kernel[2][1]`: `0`
- `$.measurements.even_parity_kernel[2][2]`: `1`
- `$.measurements.even_parity_kernel[3][0]`: `1`
- `$.measurements.even_parity_kernel[3][1]`: `1`
- `$.measurements.even_parity_kernel[3][2]`: `0`
- `$.measurements.fixed_kernel_elements[0][0]`: `0`
- `$.measurements.fixed_kernel_elements[0][1]`: `0`
- `$.measurements.fixed_kernel_elements[0][2]`: `0`
- `$.measurements.fixed_kernel_elements[1][0]`: `1`
- `$.measurements.fixed_kernel_elements[1][1]`: `1`
- `$.measurements.fixed_kernel_elements[1][2]`: `1`
- `$.measurements.kernel_order`: `8`
- `$.measurements.kernel_shift_rows[0].b[0]`: `0`
- `$.measurements.kernel_shift_rows[0].b[1]`: `0`
- `$.measurements.kernel_shift_rows[0].b[2]`: `0`
- `$.measurements.kernel_shift_rows[0].exact_kernel_law`: `True`
- `$.measurements.kernel_shift_rows[0].expected_shifts[0][0]`: `0`
- `$.measurements.kernel_shift_rows[0].expected_shifts[0][1]`: `0`
- `$.measurements.kernel_shift_rows[0].expected_shifts[1][0]`: `0`
- `$.measurements.kernel_shift_rows[0].expected_shifts[1][1]`: `0`
- `$.measurements.kernel_shift_rows[0].expected_shifts[2][0]`: `0`
- `$.measurements.kernel_shift_rows[0].expected_shifts[2][1]`: `0`
- `$.measurements.kernel_shift_rows[0].parity`: `0`
- `$.measurements.kernel_shift_rows[0].shifts[0][0]`: `0`
- `$.measurements.kernel_shift_rows[0].shifts[0][1]`: `0`
- `$.measurements.kernel_shift_rows[0].shifts[1][0]`: `0`
- `$.measurements.kernel_shift_rows[0].shifts[1][1]`: `0`
- `$.measurements.kernel_shift_rows[0].shifts[2][0]`: `0`
- `$.measurements.kernel_shift_rows[0].shifts[2][1]`: `0`
- `$.measurements.kernel_shift_rows[1].b[0]`: `0`
- `$.measurements.kernel_shift_rows[1].b[1]`: `0`
- `$.measurements.kernel_shift_rows[1].b[2]`: `1`
- `$.measurements.kernel_shift_rows[1].exact_kernel_law`: `True`
- `$.measurements.kernel_shift_rows[1].expected_shifts[0][0]`: `0`
- `$.measurements.kernel_shift_rows[1].expected_shifts[0][1]`: `0`
- `$.measurements.kernel_shift_rows[1].expected_shifts[1][0]`: `1`
- `$.measurements.kernel_shift_rows[1].expected_shifts[1][1]`: `0`
- `$.measurements.kernel_shift_rows[1].expected_shifts[2][0]`: `0`
- `$.measurements.kernel_shift_rows[1].expected_shifts[2][1]`: `1`
- `$.measurements.kernel_shift_rows[1].parity`: `1`
- `$.measurements.kernel_shift_rows[1].shifts[0][0]`: `0`
- `$.measurements.kernel_shift_rows[1].shifts[0][1]`: `0`
- `$.measurements.kernel_shift_rows[1].shifts[1][0]`: `1`
- `$.measurements.kernel_shift_rows[1].shifts[1][1]`: `0`
- `$.measurements.kernel_shift_rows[1].shifts[2][0]`: `0`
- `$.measurements.kernel_shift_rows[1].shifts[2][1]`: `1`
- `$.measurements.kernel_shift_rows[2].b[0]`: `0`
- `$.measurements.kernel_shift_rows[2].b[1]`: `1`
- `$.measurements.kernel_shift_rows[2].b[2]`: `0`
- `$.measurements.kernel_shift_rows[2].exact_kernel_law`: `True`
- `$.measurements.kernel_shift_rows[2].expected_shifts[0][0]`: `1`
- `$.measurements.kernel_shift_rows[2].expected_shifts[0][1]`: `0`
- `$.measurements.kernel_shift_rows[2].expected_shifts[1][0]`: `0`
- `$.measurements.kernel_shift_rows[2].expected_shifts[1][1]`: `1`
- `$.measurements.kernel_shift_rows[2].expected_shifts[2][0]`: `0`
- `$.measurements.kernel_shift_rows[2].expected_shifts[2][1]`: `0`
- `$.measurements.kernel_shift_rows[2].parity`: `1`
- `$.measurements.kernel_shift_rows[2].shifts[0][0]`: `1`
- `$.measurements.kernel_shift_rows[2].shifts[0][1]`: `0`
- `$.measurements.kernel_shift_rows[2].shifts[1][0]`: `0`
- `$.measurements.kernel_shift_rows[2].shifts[1][1]`: `1`
- `$.measurements.kernel_shift_rows[2].shifts[2][0]`: `0`
- `$.measurements.kernel_shift_rows[2].shifts[2][1]`: `0`
- `$.measurements.kernel_shift_rows[3].b[0]`: `0`
- `$.measurements.kernel_shift_rows[3].b[1]`: `1`
- `$.measurements.kernel_shift_rows[3].b[2]`: `1`
- `$.measurements.kernel_shift_rows[3].exact_kernel_law`: `True`
- `$.measurements.kernel_shift_rows[3].expected_shifts[0][0]`: `1`
- `$.measurements.kernel_shift_rows[3].expected_shifts[0][1]`: `0`
- `$.measurements.kernel_shift_rows[3].expected_shifts[1][0]`: `1`
- `$.measurements.kernel_shift_rows[3].expected_shifts[1][1]`: `1`
- `$.measurements.kernel_shift_rows[3].expected_shifts[2][0]`: `0`
- `$.measurements.kernel_shift_rows[3].expected_shifts[2][1]`: `1`
- `$.measurements.kernel_shift_rows[3].parity`: `0`
- `$.measurements.kernel_shift_rows[3].shifts[0][0]`: `1`
- `$.measurements.kernel_shift_rows[3].shifts[0][1]`: `0`
- `$.measurements.kernel_shift_rows[3].shifts[1][0]`: `1`
- `$.measurements.kernel_shift_rows[3].shifts[1][1]`: `1`
- `$.measurements.kernel_shift_rows[3].shifts[2][0]`: `0`
- `$.measurements.kernel_shift_rows[3].shifts[2][1]`: `1`
- `$.measurements.kernel_shift_rows[4].b[0]`: `1`
- `$.measurements.kernel_shift_rows[4].b[1]`: `0`
- `$.measurements.kernel_shift_rows[4].b[2]`: `0`
- `$.measurements.kernel_shift_rows[4].exact_kernel_law`: `True`
- `$.measurements.kernel_shift_rows[4].expected_shifts[0][0]`: `0`
- `$.measurements.kernel_shift_rows[4].expected_shifts[0][1]`: `1`
- `$.measurements.kernel_shift_rows[4].expected_shifts[1][0]`: `0`
- `$.measurements.kernel_shift_rows[4].expected_shifts[1][1]`: `0`
- `$.measurements.kernel_shift_rows[4].expected_shifts[2][0]`: `1`
- `$.measurements.kernel_shift_rows[4].expected_shifts[2][1]`: `0`

## `artifacts/json/refinement_native_k5_equivariant_join_audit_028l.json`

Matched terms: kernel

- `$.sources.audit028k.verdict`: `the_five_conjugate_rank8_refinements_carry_the_exact_degree5_quotient_action_of_the_full_icosahedral_group_with_kernel_C2_and_image_A5_the_action_is_2_transitive_the_original_C2_times_A4_color_group_is_one_point_stabilizer_and_the_five_refinements_therefore_form_an_intrinsic_K5_set`

## `artifacts/json/s3_sign_v4_d8_local_system_audit_021.json`

Matched terms: kernel

- `$.checks.sign_kernel_is_a3`: `True`
- `$.interpretation`: `The exact three-sheeted G15-to-K5 cover has full S3 monodromy. After correcting by the cyclic role frames inside each selected syntheme, every oriented K5 edge induces the same nontrivial automorphism of the native V4 axis set: the carrier axis is fixed while the b and ab axes are exchanged. The individual edge actions therefore generate the sign quotient C2 of S3, with kernel A3. Every K5 triangle has nontrivial C2 holonomy, so the b and ab axes cannot be globally separated, although the carrier axis is globally fixed. In native binary coordinates the holonomy swaps the two coordinates. Combining this C2 action with the native V4 translations gives V4 semidirect C2, a nonabelian order-eight group with D8 element-order profile. It is exactly the full automorphism group of the local four-state square.`
- `$.measurements.sign_kernel[0][0]`: `0`
- `$.measurements.sign_kernel[0][1]`: `1`
- `$.measurements.sign_kernel[0][2]`: `2`
- `$.measurements.sign_kernel[1][0]`: `1`
- `$.measurements.sign_kernel[1][1]`: `2`
- `$.measurements.sign_kernel[1][2]`: `0`
- `$.measurements.sign_kernel[2][0]`: `2`
- `$.measurements.sign_kernel[2][1]`: `0`
- `$.measurements.sign_kernel[2][2]`: `1`
- `$.measurements.sign_kernel_order`: `3`

## `artifacts/json/signed_24_face_block_closure_audit_025.json`

Matched terms: kernel

- `$.boundary.face_sign_character_kernel[0]`: `a`
- `$.boundary.face_sign_character_kernel[1]`: `identity`
- `$.checks.negative_kernel_orbits_are_six_pairs`: `True`
- `$.checks.positive_kernel_orbits_are_six_pairs`: `True`
- `$.interpretation`: `The twelve positive five-state face blocks obtained from the exact H40 pentagram pairings are one signed section, not a full V4-invariant face set. Closing this section under the native V4 action produces exactly twenty-four five-state blocks: twelve positive and twelve negative. Each sign section separately partitions all sixty native G60 states, while the combined system contains every state twice. The full V4 action has six free orbits of size four, each containing two positive and two negative blocks. The sign is governed by the homomorphism V4->C2 with kernel {identity,a}; b and ab exchange the positive and negative sections. This is the exact signed face-level closure compatible with the previously derived S3-sign/V4/D8 local system.`
- `$.keeper`: `The quotient face set is a positive section of a unique V4-equivariant signed double closure: twelve positive and twelve negative five-state face blocks, related by the character with kernel {identity,a}.`
- `$.measurements.character_kernel[0]`: `a`
- `$.measurements.character_kernel[1]`: `identity`
- `$.measurements.kernel_orbit_profiles.negative.2`: `6`
- `$.measurements.kernel_orbit_profiles.positive.2`: `6`
- `$.measurements.kernel_orbits_by_sign.negative[0][0][0].face_index`: `0`
- `$.measurements.kernel_orbits_by_sign.negative[0][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[0][0][1].face_index`: `8`
- `$.measurements.kernel_orbits_by_sign.negative[0][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[0][1][0].face_index`: `7`
- `$.measurements.kernel_orbits_by_sign.negative[0][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[0][1][1].face_index`: `11`
- `$.measurements.kernel_orbits_by_sign.negative[0][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[1][0][0].face_index`: `1`
- `$.measurements.kernel_orbits_by_sign.negative[1][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[1][0][1].face_index`: `9`
- `$.measurements.kernel_orbits_by_sign.negative[1][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[1][1][0].face_index`: `4`
- `$.measurements.kernel_orbits_by_sign.negative[1][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[1][1][1].face_index`: `10`
- `$.measurements.kernel_orbits_by_sign.negative[1][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[2][0][0].face_index`: `2`
- `$.measurements.kernel_orbits_by_sign.negative[2][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[2][0][1].face_index`: `3`
- `$.measurements.kernel_orbits_by_sign.negative[2][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[2][1][0].face_index`: `11`
- `$.measurements.kernel_orbits_by_sign.negative[2][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[2][1][1].face_index`: `6`
- `$.measurements.kernel_orbits_by_sign.negative[2][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[3][0][0].face_index`: `3`
- `$.measurements.kernel_orbits_by_sign.negative[3][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[3][0][1].face_index`: `2`
- `$.measurements.kernel_orbits_by_sign.negative[3][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[3][1][0].face_index`: `10`
- `$.measurements.kernel_orbits_by_sign.negative[3][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[3][1][1].face_index`: `7`
- `$.measurements.kernel_orbits_by_sign.negative[3][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[4][0][0].face_index`: `5`
- `$.measurements.kernel_orbits_by_sign.negative[4][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[4][0][1].face_index`: `0`
- `$.measurements.kernel_orbits_by_sign.negative[4][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[4][1][0].face_index`: `8`
- `$.measurements.kernel_orbits_by_sign.negative[4][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[4][1][1].face_index`: `5`
- `$.measurements.kernel_orbits_by_sign.negative[4][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[5][0][0].face_index`: `6`
- `$.measurements.kernel_orbits_by_sign.negative[5][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[5][0][1].face_index`: `4`
- `$.measurements.kernel_orbits_by_sign.negative[5][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.negative[5][1][0].face_index`: `9`
- `$.measurements.kernel_orbits_by_sign.negative[5][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.negative[5][1][1].face_index`: `1`
- `$.measurements.kernel_orbits_by_sign.negative[5][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[0][0][0].face_index`: `0`
- `$.measurements.kernel_orbits_by_sign.positive[0][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[0][0][1].face_index`: `11`
- `$.measurements.kernel_orbits_by_sign.positive[0][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[0][1][0].face_index`: `7`
- `$.measurements.kernel_orbits_by_sign.positive[0][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[0][1][1].face_index`: `8`
- `$.measurements.kernel_orbits_by_sign.positive[0][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[1][0][0].face_index`: `1`
- `$.measurements.kernel_orbits_by_sign.positive[1][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[1][0][1].face_index`: `10`
- `$.measurements.kernel_orbits_by_sign.positive[1][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[1][1][0].face_index`: `4`
- `$.measurements.kernel_orbits_by_sign.positive[1][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[1][1][1].face_index`: `9`
- `$.measurements.kernel_orbits_by_sign.positive[1][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[2][0][0].face_index`: `2`
- `$.measurements.kernel_orbits_by_sign.positive[2][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[2][0][1].face_index`: `6`
- `$.measurements.kernel_orbits_by_sign.positive[2][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[2][1][0].face_index`: `11`
- `$.measurements.kernel_orbits_by_sign.positive[2][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[2][1][1].face_index`: `3`
- `$.measurements.kernel_orbits_by_sign.positive[2][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[3][0][0].face_index`: `3`
- `$.measurements.kernel_orbits_by_sign.positive[3][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[3][0][1].face_index`: `7`
- `$.measurements.kernel_orbits_by_sign.positive[3][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[3][1][0].face_index`: `10`
- `$.measurements.kernel_orbits_by_sign.positive[3][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[3][1][1].face_index`: `2`
- `$.measurements.kernel_orbits_by_sign.positive[3][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[4][0][0].face_index`: `5`
- `$.measurements.kernel_orbits_by_sign.positive[4][0][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[4][0][1].face_index`: `5`
- `$.measurements.kernel_orbits_by_sign.positive[4][0][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[4][1][0].face_index`: `8`
- `$.measurements.kernel_orbits_by_sign.positive[4][1][0].side`: `left`
- `$.measurements.kernel_orbits_by_sign.positive[4][1][1].face_index`: `0`
- `$.measurements.kernel_orbits_by_sign.positive[4][1][1].side`: `right`
- `$.measurements.kernel_orbits_by_sign.positive[5][0][0].face_index`: `6`
- `$.measurements.kernel_orbits_by_sign.positive[5][0][0].side`: `left`

## `artifacts/json/signed_block_doubling_obstruction_audit_028b.json`

Matched terms: kernel

- `$.sources.audit025.verdict`: `the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab`

## `artifacts/json/six_orbit_pairwise_grammar_compatibility_audit_026c.json`

Matched terms: kernel

- `$.checks.character_has_two_kernel_elements`: `True`
- `$.measurements.orbit_rows[0].checks.side_generator_product_is_kernel_axis`: `True`
- `$.measurements.orbit_rows[1].checks.side_generator_product_is_kernel_axis`: `True`
- `$.measurements.orbit_rows[2].checks.side_generator_product_is_kernel_axis`: `True`
- `$.measurements.orbit_rows[3].checks.side_generator_product_is_kernel_axis`: `True`
- `$.measurements.orbit_rows[4].checks.side_generator_product_is_kernel_axis`: `True`
- `$.measurements.orbit_rows[5].checks.side_generator_product_is_kernel_axis`: `True`
- `$.native_v4.kernel_axis`: `a`
- `$.sources.audit025.verdict`: `the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab`

## `artifacts/json/synthematic_total_534_transport_tower_audit_020.json`

Matched terms: triangle holonomy

- `$.next_target`: `Compare the full S3 monodromy of the three-cover with the natural automorphism group Aut(V4) acting on the three nonidentity native deck transformations a, b, and ab. Test whether triangle holonomy permutes these three V4 axes exactly as it permutes the carrier, b, and ab roles. A positive result would replace the remaining local face-bit gauge by a canonical S3-twisted V4 incidence local system.`

## `artifacts/json/three_k4_cell_state_lift_audit_028g.json`

Matched terms: kernel

- `$.sources.audit025.verdict`: `the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab`

## `artifacts/json/v4_affine_character_cell_grammar_audit_028h.json`

Matched terms: all-one, all_one

- `$.checks.all_one_gauge_count2`: `True`
- `$.interpretation`: `The measured 3-by-3 array of four-state incidence blocks is not merely a count pattern. After coordinatizing each four-face cell as the same V4 torsor, every block is cut out by one exact low-complexity law. Internal flow is translation by the first seam generator u. Forward cross-cell flow equates the u-character on the source with the v-character on the target. Reverse flow uses the transposed character relation. The constants are cell-origin gauge data: two relative gauges produce the all-zero normal form and two produce the all-one normal form.`
- `$.measurements.all_one_gauge_count`: `2`
- `$.measurements.gauge_rows[0].all_one`: `False`
- `$.measurements.gauge_rows[1].all_one`: `False`
- `$.measurements.gauge_rows[2].all_one`: `False`
- `$.measurements.gauge_rows[3].all_one`: `False`
- `$.measurements.gauge_rows[4].all_one`: `False`
- `$.measurements.gauge_rows[5].all_one`: `False`
- `$.measurements.gauge_rows[6].all_one`: `False`
- `$.measurements.gauge_rows[7].all_one`: `False`
- `$.measurements.gauge_rows[8].all_one`: `True`
- `$.measurements.gauge_rows[9].all_one`: `False`
- `$.measurements.gauge_rows[10].all_one`: `False`
- `$.measurements.gauge_rows[11].all_one`: `False`
- `$.measurements.gauge_rows[12].all_one`: `False`
- `$.measurements.gauge_rows[13].all_one`: `False`
- `$.measurements.gauge_rows[14].all_one`: `True`
- `$.measurements.gauge_rows[15].all_one`: `False`
- `$.measurements.uniform_gauges[0].all_one`: `False`
- `$.measurements.uniform_gauges[1].all_one`: `False`
- `$.measurements.uniform_gauges[2].all_one`: `True`
- `$.measurements.uniform_gauges[3].all_one`: `True`

## `artifacts/json/v4xv4_gauge_orbit_theorem_audit_026a.json`

Matched terms: kernel

- `$.sources.audit025.verdict`: `the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab`

## `notes/all_one_full_automorphism_census_audit_028n.md`

Matched terms: all-one


Line 1:

```text
1: # All-One Full Automorphism Census Audit 028N
2: 
3: ## Result
```

Line 5:

```text
3: ## Result
4: 
5: The all-one bipartite cover has exactly 720 automorphisms.
6: 
7: A chosen G15 fiber partition has stabilizer order 240. Its orbit has
```

Line 17:

```text
15: ## Interpretation
16: 
17: The all-one graph does not carry one characteristic G15 quotient. It
18: carries three equivalent quotient presentations.
19: 
```

## `notes/all_one_group_anatomy_audit_028o.md`

Matched terms: quotient system, quotient systems, centralizer, kernel, S5 x S3, all-one, all_one


Line 1:

```text
1: # All-One Group Anatomy Audit 028O
2: 
3: ## Result
```

Line 7:

```text
5: The full automorphism group is
6: 
7:     Aut(X_all_one) = S5 x S3.
8: 
9: The action on the three G15 partitions has image S3 and kernel S5.
```

Line 9:

```text
7:     Aut(X_all_one) = S5 x S3.
8: 
9: The action on the three G15 partitions has image S3 and kernel S5.
10: 
11: The centralizer of the kernel has order six, is S3, intersects the
```

Line 11:

```text
9: The action on the three G15 partitions has image S3 and kernel S5.
10: 
11: The centralizer of the kernel has order six, is S3, intersects the
12: kernel trivially, and the two factors generate all 720 automorphisms.
13: 
```

Line 12:

```text
10: 
11: The centralizer of the kernel has order six, is S3, intersects the
12: kernel trivially, and the two factors generate all 720 automorphisms.
13: 
14: Further invariants are
```

Line 30:

```text
28: ## Keeper
29: 
30: The extra S3 permutes the three equivalent G15 quotient systems.
```

## `notes/all_one_oriented_frame_identification_audit_028p.md`

Matched terms: kernel, V4_even, orbital graph, all-one, all_one


Line 1:

```text
1: # All-One Oriented Frame Identification Audit 028P
2: 
3: ## Result
```

Line 5:

```text
3: ## Result
4: 
5: The order-120 S5 kernel acts transitively on the 30 vertices. A vertex
6: stabilizer is an even V4 in the Petersen S5 action. Therefore the
7: vertex set is
```

Line 9:

```text
7: vertex set is
8: 
9:     Omega30 = S5 / V4_even.
10: 
11: There are four degree-four S5 orbital graphs on this set. Three split
```

Line 11:

```text
9:     Omega30 = S5 / V4_even.
10: 
11: There are four degree-four S5 orbital graphs on this set. Three split
12: as 15 plus 15 and contain triangles. Exactly one is connected and
13: triangle-free, and it is the all-one bipartite cover.
```

Line 13:

```text
11: There are four degree-four S5 orbital graphs on this set. Three split
12: as 15 plus 15 and contain triangles. Exactly one is connected and
13: triangle-free, and it is the all-one bipartite cover.
14: 
15: Thus
```

Line 17:

```text
15: Thus
16: 
17:     X_all_one
18: 
19: is the unique connected triangle-free degree-four S5 orbital graph on
```

Line 19:

```text
17:     X_all_one
18: 
19: is the unique connected triangle-free degree-four S5 orbital graph on
20: the oriented-frame geometry S5 / V4_even.
21: 
```

Line 20:

```text
18: 
19: is the unique connected triangle-free degree-four S5 orbital graph on
20: the oriented-frame geometry S5 / V4_even.
21: 
22: ## Boundary
```

Line 29:

```text
27: ## Keeper
28: 
29: All-one belongs to the even-V4 oriented-frame geometry.
```

## `notes/index5_refinement_action_audit_028k.md`

Matched terms: kernel


Line 5:

```text
3: Audit pass: true
4: 
5: Verdict: `the_five_conjugate_rank8_refinements_carry_the_exact_degree5_quotient_action_of_the_full_icosahedral_group_with_kernel_C2_and_image_A5_the_action_is_2_transitive_the_original_C2_times_A4_color_group_is_one_point_stabilizer_and_the_five_refinements_therefore_form_an_intrinsic_K5_set`
6: 
7: ## Result
```

Line 14:

```text
12: The action has:
13: 
14: - kernel order 2
15: - image order 60
16: - image element-order profile of A5
```

## `notes/invariant_cover_square_automorphism_orders_audit_028m.md`

Matched terms: all-one, all_one, 28800


Line 8:

```text
6: orders
7: 
8:     zero         28800
9:     native         240
10:     alternative    240
```

Line 11:

```text
9:     native         240
10:     alternative    240
11:     all_one        720
12: 
13: The zero class is two disjoint G15 copies and has automorphism group
```

Line 20:

```text
18: automorphisms lifts exactly twice, so the full order is 240.
19: 
20: The all-one cover also has 240 automorphisms preserving one chosen
21: fiber partition, but that partition is not characteristic. Independent
22: full enumeration gives order 720.
```

Line 31:

```text
29: ## Keeper
30: 
31: The automorphism-order square is 28800, 240, 240, 720.
```

## `notes/invariant_cover_square_closure_audit_028q.md`

Matched terms: S5 x S3, V4_even, all-one, all_one, 28800


Line 10:

```text
8:     native        triangle 0  pentagon 1
9:     alternative   triangle 1  pentagon 0
10:     all_one       triangle 1  pentagon 1
11: 
12: Their full automorphism orders are
```

Line 14:

```text
12: Their full automorphism orders are
13: 
14:     28800, 240, 240, 720.
15: 
16: The all-one class has full group S5 x S3. Its three equivalent G15
```

Line 16:

```text
14:     28800, 240, 240, 720.
15: 
16: The all-one class has full group S5 x S3. Its three equivalent G15
17: fiber partitions form the natural three-point S3 action. Each
18: partition stabilizer is S5 x C2.
```

Line 20:

```text
18: partition stabilizer is S5 x C2.
19: 
20: The all-one vertex geometry is S5 / V4_even. The native central
21: quotient lies on S5 / V4_mixed.
22: 
```

Line 26:

```text
24: 
25: This closes the invariant cover square at automorphism order, group
26: anatomy for all-one, and homogeneous-space identification.
27: 
28: It does not identify the archived G30, prove splitting types for both
```

Line 30:

```text
28: It does not identify the archived G30, prove splitting types for both
29: order-240 connected extensions, or assign an external standard graph
30: name to the all-one graph.
31: 
32: ## Keeper
```

Line 34:

```text
32: ## Keeper
33: 
34: The two degree-30 geometries are distinct: even V4 carries all-one,
35: while mixed V4 carries the native central quotient.
```

## `notes/local_shift_pair_admissibility_classification_audit_026b.md`

Matched terms: kernel


Line 22:

```text
20: - Right generator: `b`
21: - Generator product: `a`
22: - Sign-kernel axis: `a`
23: 
24: ## Admissibility theorem
```

Line 64:

```text
62: ## Interpretation
63: 
64: The failed first 026B run exposed a genuine omitted invariant, not a global obstruction. The actual signed V4 orbit carries ordered left and right order-two pentagon stabilizers. Their nonidentity generators are distinct togglers, and their product is the sign-kernel axis. A left sheet shift equal to the left stabilizer generator collapses left face-copy incidence; the analogous statement holds on the right. Therefore exactly four of the nine gauge-reduced shift pairs are locally admissible. The five rejected pairs are explained exactly by two left-only, two right-only, and one simultaneous stabilizer collision. Once the ordered side stabilizers are retained, the remaining automorphism group is trivial and the four survivors are four distinct ordered local grammar types.
65: 
66: ## Boundary
```

## `notes/native_character_axis_interpretation_audit_027d.md`

Matched terms: kernel


Line 5:

```text
3: Audit pass: true
4: 
5: Verdict: `the_global_interface_obstruction_characters_are_exactly_diagonal_native_v4_axis_characters_G0_uses_both_ordered_pentagon_stabilizer_axes_G1_uses_the_right_stabilizer_axis_G2_uses_the_left_stabilizer_axis_and_G3_uses_their_product_sign_kernel_axis`
6: 
7: ## Native frame
```

Line 11:

```text
9: - Left pentagon stabilizer axis: `ab`
10: - Right pentagon stabilizer axis: `b`
11: - Product / sign-kernel axis: `a`
12: 
13: ## Character interpretation
```

## `notes/signed_24_face_block_closure_audit_025.md`

Matched terms: kernel


Line 5:

```text
3: Audit pass: true
4: 
5: Verdict: the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab
6: 
7: The twelve exact five-state face carriers form a positive
```

## `notes/v4_affine_character_cell_grammar_audit_028h.md`

Matched terms: all-one


Line 17:

```text
15: 
16: With cell 0 fixed, the 16 relative origin gauges contain four
17: uniform-constant gauges: two all-zero and two all-one. The
18: canonical all-zero gauge shifts the cells by
19: 
```

## `scripts/audit_all_one_full_automorphism_census_028n.py`

Matched terms: all_one


Line 26:

```text
24:     HOME
25:     / "tmp/project41-028m30j2/results"
26:     / "all_one_networkx_aut_census_028m30j3.json"
27: )
28: 
```

Line 101:

```text
99: 
100:     edges = module.build_cover_edges(
101:         source["voltages"]["all_one"],
102:         source["g15_edges"],
103:     )
```

Line 210:

```text
208:             ),
209:         "status":
210:             "project41_all_one_full_aut_census_complete",
211:     })
212: 
```

Line 226:

```text
224:             repr(exc),
225:         "status":
226:             "project41_all_one_full_aut_census_timed_out",
227:     })
228: 
```

Line 240:

```text
238:             traceback.format_exc(),
239:         "status":
240:             "project41_all_one_full_aut_census_failed",
241:     })
242: 
```

## `scripts/audit_all_one_group_anatomy_028o.py`

Matched terms: centralizer, kernel, all_one


Line 25:

```text
23:     HOME
24:     / "tmp/project41-028m30j2/results"
25:     / "all_one_group_anatomy_028m30j4.json"
26: )
27: 
```

Line 173:

```text
171: 
172:     edges = module.build_cover_edges(
173:         source["voltages"]["all_one"],
174:         source["g15_edges"],
175:     )
```

Line 257:

```text
255:     )
256: 
257:     action_kernel = frozenset(
258:         automorphism
259:         for automorphism
```

Line 286:

```text
284:     )
285: 
286:     kernel_centralizer = frozenset(
287:         element
288:         for element in automorphisms
```

Line 290:

```text
288:         for element in automorphisms
289:         if all(
290:             compose(element, kernel_element)
291:             == compose(kernel_element, element)
292:             for kernel_element in action_kernel
```

Line 291:

```text
289:         if all(
290:             compose(element, kernel_element)
291:             == compose(kernel_element, element)
292:             for kernel_element in action_kernel
293:         )
```

Line 292:

```text
290:             compose(element, kernel_element)
291:             == compose(kernel_element, element)
292:             for kernel_element in action_kernel
293:         )
294:     )
```

Line 296:

```text
294:     )
295: 
296:     kernel_centralizer_intersection = (
297:         action_kernel
298:         & kernel_centralizer
```

Line 297:

```text
295: 
296:     kernel_centralizer_intersection = (
297:         action_kernel
298:         & kernel_centralizer
299:     )
```

Line 298:

```text
296:     kernel_centralizer_intersection = (
297:         action_kernel
298:         & kernel_centralizer
299:     )
300: 
```

Line 302:

```text
300: 
301:     product_set = {
302:         compose(kernel_element, centralizer_element)
303:         for kernel_element in action_kernel
304:         for centralizer_element in kernel_centralizer
```

Line 303:

```text
301:     product_set = {
302:         compose(kernel_element, centralizer_element)
303:         for kernel_element in action_kernel
304:         for centralizer_element in kernel_centralizer
305:     }
```

Line 304:

```text
302:         compose(kernel_element, centralizer_element)
303:         for kernel_element in action_kernel
304:         for centralizer_element in kernel_centralizer
305:     }
306: 
```

Line 312:

```text
310:     )
311: 
312:     kernel_orders = Counter(
313:         element_order(element)
314:         for element in action_kernel
```

Line 314:

```text
312:     kernel_orders = Counter(
313:         element_order(element)
314:         for element in action_kernel
315:     )
316: 
```

Line 317:

```text
315:     )
316: 
317:     centralizer_orders = Counter(
318:         element_order(element)
319:         for element in kernel_centralizer
```

Line 319:

```text
317:     centralizer_orders = Counter(
318:         element_order(element)
319:         for element in kernel_centralizer
320:     )
321: 
```

Line 338:

```text
336:     )
337: 
338:     kernel_quotient_action_count = len({
339:         tuple(
340:             sorted(
```

Line 350:

```text
348:             )
349:         )
350:         for automorphism in action_kernel
351:     })
352: 
```

Line 354:

```text
352: 
353:     direct_product_pass = (
354:         len(action_kernel) == 120
355:         and len(kernel_centralizer) == 6
356:         and len(
```

Line 355:

```text
353:     direct_product_pass = (
354:         len(action_kernel) == 120
355:         and len(kernel_centralizer) == 6
356:         and len(
357:             kernel_centralizer_intersection
```

Line 357:

```text
355:         and len(kernel_centralizer) == 6
356:         and len(
357:             kernel_centralizer_intersection
358:         ) == 1
359:         and len(product_set) == 720
```

Line 364:

```text
362:     )
363: 
364:     kernel_is_S5_pass = (
365:         len(action_kernel) == 120
366:         and kernel_orders == Counter({
```

Line 365:

```text
363: 
364:     kernel_is_S5_pass = (
365:         len(action_kernel) == 120
366:         and kernel_orders == Counter({
367:             1: 1,
```

Line 366:

```text
364:     kernel_is_S5_pass = (
365:         len(action_kernel) == 120
366:         and kernel_orders == Counter({
367:             1: 1,
368:             2: 25,
```

Line 376:

```text
374:     )
375: 
376:     centralizer_is_S3_pass = (
377:         len(kernel_centralizer) == 6
378:         and centralizer_orders == Counter({
```

Line 377:

```text
375: 
376:     centralizer_is_S3_pass = (
377:         len(kernel_centralizer) == 6
378:         and centralizer_orders == Counter({
379:             1: 1,
```

Line 378:

```text
376:     centralizer_is_S3_pass = (
377:         len(kernel_centralizer) == 6
378:         and centralizer_orders == Counter({
379:             1: 1,
380:             2: 3,
```

Line 385:

```text
383:         and {
384:             partition_actions[element]
385:             for element in kernel_centralizer
386:         } == action_image
387:     )
```

Line 391:

```text
389:     exact_structure_pass = (
390:         direct_product_pass
391:         and kernel_is_S5_pass
392:         and centralizer_is_S3_pass
393:         and len(center) == 1
```

Line 392:

```text
390:         direct_product_pass
391:         and kernel_is_S5_pass
392:         and centralizer_is_S3_pass
393:         and len(center) == 1
394:         and len(derived_subgroup) == 180
```

Line 413:

```text
411:                 )
412:             ),
413:         "partition_action_kernel_order":
414:             len(action_kernel),
415:         "natural_partition_stabilizer_order":
```

Line 414:

```text
412:             ),
413:         "partition_action_kernel_order":
414:             len(action_kernel),
415:         "natural_partition_stabilizer_order":
416:             len(natural_stabilizer),
```

Line 424:

```text
422:             len(automorphisms)
423:             // len(derived_subgroup),
424:         "kernel_centralizer_order":
425:             len(kernel_centralizer),
426:         "kernel_centralizer_intersection_order":
```

Line 425:

```text
423:             // len(derived_subgroup),
424:         "kernel_centralizer_order":
425:             len(kernel_centralizer),
426:         "kernel_centralizer_intersection_order":
427:             len(
```

Line 426:

```text
424:         "kernel_centralizer_order":
425:             len(kernel_centralizer),
426:         "kernel_centralizer_intersection_order":
427:             len(
428:                 kernel_centralizer_intersection
```

Line 428:

```text
426:         "kernel_centralizer_intersection_order":
427:             len(
428:                 kernel_centralizer_intersection
429:             ),
430:         "kernel_times_centralizer_order":
```

Line 430:

```text
428:                 kernel_centralizer_intersection
429:             ),
430:         "kernel_times_centralizer_order":
431:             len(product_set),
432:         "full_element_order_distribution":
```

Line 434:

```text
432:         "full_element_order_distribution":
433:             dict(sorted(all_orders.items())),
434:         "kernel_element_order_distribution":
435:             dict(sorted(kernel_orders.items())),
436:         "centralizer_element_order_distribution":
```

Line 435:

```text
433:             dict(sorted(all_orders.items())),
434:         "kernel_element_order_distribution":
435:             dict(sorted(kernel_orders.items())),
436:         "centralizer_element_order_distribution":
437:             dict(
```

Line 436:

```text
434:         "kernel_element_order_distribution":
435:             dict(sorted(kernel_orders.items())),
436:         "centralizer_element_order_distribution":
437:             dict(
438:                 sorted(
```

Line 439:

```text
437:             dict(
438:                 sorted(
439:                     centralizer_orders.items()
440:                 )
441:             ),
```

Line 450:

```text
448:         "direct_product_pass":
449:             direct_product_pass,
450:         "kernel_is_S5_pass":
451:             kernel_is_S5_pass,
452:         "centralizer_is_S3_pass":
```

Line 451:

```text
449:             direct_product_pass,
450:         "kernel_is_S5_pass":
451:             kernel_is_S5_pass,
452:         "centralizer_is_S3_pass":
453:             centralizer_is_S3_pass,
```

Line 452:

```text
450:         "kernel_is_S5_pass":
451:             kernel_is_S5_pass,
452:         "centralizer_is_S3_pass":
453:             centralizer_is_S3_pass,
454:         "exact_structure_pass":
```

Line 453:

```text
451:             kernel_is_S5_pass,
452:         "centralizer_is_S3_pass":
453:             centralizer_is_S3_pass,
454:         "exact_structure_pass":
455:             exact_structure_pass,
```

Line 470:

```text
468:         "status":
469:             (
470:                 "project41_all_one_group_anatomy_complete"
471:                 if exact_structure_pass
472:                 else
```

Line 473:

```text
471:                 if exact_structure_pass
472:                 else
473:                 "project41_all_one_group_anatomy_inconclusive"
474:             ),
475:     })
```

Line 486:

```text
484:             False,
485:         "status":
486:             "project41_all_one_group_anatomy_failed",
487:     })
488: 
```

## `scripts/audit_all_one_oriented_frame_identification_028p.py`

Matched terms: kernel, V4_even, all_one


Line 26:

```text
24:     HOME
25:     / "tmp/project41-028m30j2/results"
26:     / "all_one_oriented_frame_identification_028m30j5.json"
27: )
28: 
```

Line 175:

```text
173:     source = module.reconstruct_source()
174: 
175:     all_one_edges = frozenset(
176:         module.build_cover_edges(
177:             source["voltages"]["all_one"],
```

Line 177:

```text
175:     all_one_edges = frozenset(
176:         module.build_cover_edges(
177:             source["voltages"]["all_one"],
178:             source["g15_edges"],
179:         )
```

Line 184:

```text
182:     graph = nx.Graph()
183:     graph.add_nodes_from(range(30))
184:     graph.add_edges_from(all_one_edges)
185: 
186:     full_automorphisms = tuple(
```

Line 223:

```text
221:     )
222: 
223:     kernel = tuple(
224:         automorphism
225:         for automorphism
```

Line 239:

```text
237:     )
238: 
239:     if len(kernel) != 120:
240:         raise RuntimeError(
241:             "partition-action kernel is not order 120"
```

Line 241:

```text
239:     if len(kernel) != 120:
240:         raise RuntimeError(
241:             "partition-action kernel is not order 120"
242:         )
243: 
```

Line 247:

```text
245:         automorphism[0]
246:         for automorphism
247:         in kernel
248:     }
249: 
```

Line 253:

```text
251:         automorphism
252:         for automorphism
253:         in kernel
254:         if automorphism[0] == 0
255:     )
```

Line 262:

```text
260:     ):
261:         raise RuntimeError(
262:             "kernel is not transitive with V4 stabilizer"
263:         )
264: 
```

Line 409:

```text
407:         orbit = pair_orbit(
408:             seed,
409:             kernel,
410:         )
411: 
```

Line 443:

```text
441:                     len(orbit),
442:                 **summary,
443:                 "equals_all_one":
444:                     orbit == all_one_edges,
445:             })
```

Line 444:

```text
442:                 **summary,
443:                 "equals_all_one":
444:                     orbit == all_one_edges,
445:             })
446: 
```

Line 464:

```text
462:         len(full_automorphisms) == 720
463:         and len(partition_orbit) == 3
464:         and len(kernel) == 120
465:         and len(vertex_orbit) == 30
466:         and len(vertex_stabilizer) == 4
```

Line 480:

```text
478:             0
479:         ][
480:             "equals_all_one"
481:         ]
482:     )
```

Line 489:

```text
487:         "partition_orbit_size":
488:             len(partition_orbit),
489:         "S5_kernel_order":
490:             len(kernel),
491:         "S5_vertex_orbit_size":
```

Line 490:

```text
488:             len(partition_orbit),
489:         "S5_kernel_order":
490:             len(kernel),
491:         "S5_vertex_orbit_size":
492:             len(vertex_orbit),
```

Line 510:

```text
508:             ),
509:         "vertex_stabilizer_identification":
510:             "V4_even",
511:         "coset_geometry":
512:             "S5_over_V4_even",
```

Line 512:

```text
510:             "V4_even",
511:         "coset_geometry":
512:             "S5_over_V4_even",
513:         "unordered_pair_orbit_count":
514:             len(
```

Line 527:

```text
525:                 connected_triangle_free
526:             ),
527:         "all_one_is_unique_connected_triangle_free_degree4_orbital":
528:             exact_identification,
529:         "identified_vertex_set":
```

Line 535:

```text
533:         "status":
534:             (
535:                 "project41_all_one_oriented_frame_identification_complete"
536:                 if exact_identification
537:                 else
```

Line 538:

```text
536:                 if exact_identification
537:                 else
538:                 "project41_all_one_oriented_frame_identification_inconclusive"
539:             ),
540:     })
```

Line 551:

```text
549:             False,
550:         "status":
551:             "project41_all_one_oriented_frame_identification_failed",
552:     })
553: 
```

## `scripts/audit_connection_stabilizer_native_deck_action_014.py`

Matched terms: kernel


Line 32:

```text
30:     HOME
31:     / "dev/cori/research/mathematics/thalean-graph-theory"
32:     / "18-g900-kernel-admission/artifacts/json"
33:     / "g60_native_generator_input_bundle_001.v1.json",
34: )
```

## `scripts/audit_desargues_signed_axis_gluing_007.py`

Matched terms: quotient involution


Line 153:

```text
151:         if len(set(orbit)) != 2:
152:             raise RuntimeError(
153:                 "quotient involution has a fixed point"
154:             )
155: 
```

## `scripts/audit_explicit_standard_a5_identification_016.py`

Matched terms: kernel


Line 259:

```text
257: image = set(action.values()) if action_defined else set()
258: 
259: kernel = [
260:     element
261:     for element, image_perm in action.items()
```

Line 366:

```text
364:     "five_point_action_image_size_60":
365:         len(image) == 60,
366:     "five_point_action_kernel_is_trivial":
367:         kernel == [identity60],
368:     "all_image_permutations_are_even":
```

Line 367:

```text
365:         len(image) == 60,
366:     "five_point_action_kernel_is_trivial":
367:         kernel == [identity60],
368:     "all_image_permutations_are_even":
369:         all(is_even(element) for element in image),
```

Line 420:

```text
418: print("action_defined:", str(action_defined).lower())
419: print("image_size:", len(image))
420: print("kernel_size:", len(kernel))
421: print(
422:     "homomorphism_failure_count:",
```

Line 602:

```text
600:         "five_point_action_image_size":
601:             len(image),
602:         "five_point_action_kernel_size":
603:             len(kernel),
604:         "homomorphism_failure_count":
```

Line 603:

```text
601:             len(image),
602:         "five_point_action_kernel_size":
603:             len(kernel),
604:         "homomorphism_failure_count":
605:             homomorphism_failure_count,
```

Line 632:

```text
630:         "The order-60 regular group acts by conjugation on its "
631:         "five V4 subgroups. This action is defined on every group "
632:         "element, is a homomorphism, has trivial kernel, and has "
633:         "an image of order 60. Every image permutation is even, "
634:         "and the image is exactly the full standard alternating "
```

Line 733:

```text
731: )
732: print("five_point_action_image_size:", len(image))
733: print("five_point_action_kernel_size:", len(kernel))
734: print(
735:     "homomorphism_failure_count:",
```

## `scripts/audit_index5_refinement_action_028k.py`

Matched terms: kernel


Line 25:

```text
23: 
24:    hence is the standard degree-5 action of A5.
25: 3. The action kernel has order 2.
26: 4. The action is 2-transitive.
27: 5. One-point stabilizers have:
```

Line 729:

```text
727: )
728: 
729: action_kernel = tuple(
730:     group_element
731:     for group_element in full_group
```

Line 871:

```text
869:             action_image
870:         ) == 60,
871:     "action_kernel_order2":
872:         len(
873:             action_kernel
```

Line 873:

```text
871:     "action_kernel_order2":
872:         len(
873:             action_kernel
874:         ) == 2,
875:     "image_element_order_profile_A5":
```

Line 945:

```text
943: )
944: print(
945:     "action_kernel_order:",
946:     len(
947:         action_kernel
```

Line 947:

```text
945:     "action_kernel_order:",
946:     len(
947:         action_kernel
948:     ),
949: )
```

Line 1051:

```text
1049: verdict = (
1050:     "the_five_conjugate_rank8_refinements_carry_the_exact_degree5_"
1051:     "quotient_action_of_the_full_icosahedral_group_with_kernel_C2_"
1052:     "and_image_A5_the_action_is_2_transitive_the_original_C2_times_"
1053:     "A4_color_group_is_one_point_stabilizer_and_the_five_refinements_"
```

Line 1165:

```text
1163:                 action_image
1164:             ),
1165:         "action_kernel_order":
1166:             len(
1167:                 action_kernel
```

Line 1167:

```text
1165:         "action_kernel_order":
1166:             len(
1167:                 action_kernel
1168:             ),
1169:         "action_image_element_order_profile":
```

Line 1213:

```text
1211:         "of the self-normalizing order-24 color subgroup inside the full "
1212:         "order-120 icosahedral graph automorphism group. Conjugation gives "
1213:         "a faithful quotient after removing a central kernel of order two. "
1214:         "The image is A5 in its standard 2-transitive degree-five action. "
1215:         "Thus the five refinements form an intrinsic K5 object, and the "
```

Line 1222:

```text
1220:         "five_refinement_A5_action_proved":
1221:             audit_pass,
1222:         "action_kernel_order":
1223:             2
1224:             if audit_pass
```

Line 1266:

```text
1264:     "The action has:",
1265:     "",
1266:     "- kernel order 2",
1267:     "- image order 60",
1268:     "- image element-order profile of A5",
```

Line 1346:

```text
1344: )
1345: print(
1346:     "action_kernel_order:",
1347:     len(
1348:         action_kernel
```

Line 1348:

```text
1346:     "action_kernel_order:",
1347:     len(
1348:         action_kernel
1349:     ),
1350: )
```

## `scripts/audit_invariant_cover_square_automorphism_orders_028m.py`

Matched terms: kernel, all_one, 28800


Line 735:

```text
733:             for edge in g15_edges
734:         },
735:         "all_one": {
736:             edge: 1
737:             for edge in g15_edges
```

Line 920:

```text
918:     )
919: 
920:     kernel_order = lift_count_by_base[
921:         tuple(range(15))
922:     ]
```

Line 927:

```text
925: 
926:     upper_bound = (
927:         120 * kernel_order
928:         if intrinsic_projection
929:         else None
```

Line 942:

```text
940:         and lift_count_profile
941:         == Counter({2: 120})
942:         and kernel_order == 2
943:         and lower_bound == 240
944:         and upper_bound == 240
```

Line 964:

```text
962:                 )
963:             ),
964:         "kernel_order":
965:             kernel_order,
966:         "constructed_lift_count":
```

Line 965:

```text
963:             ),
964:         "kernel_order":
965:             kernel_order,
966:         "constructed_lift_count":
967:             lower_bound,
```

Line 1008:

```text
1006:             len(components),
1007:         "full_aut_order":
1008:             28800 if exact else None,
1009:         "Aut_structure":
1010:             "S5_wreath_C2"
```

Line 1028:

```text
1026:             "native",
1027:             "alternative",
1028:             "all_one",
1029:         ],
1030:     )
```

## `scripts/audit_local_shift_pair_admissibility_classification_026b.py`

Matched terms: kernel


Line 413:

```text
411:     "character_identity_zero":
412:         character.get(identity_name) == 0,
413:     "character_has_two_kernel_elements":
414:         Counter(character.values()) == {0: 2, 1: 2},
415:     "character_is_homomorphism":
```

Line 437:

```text
435:     raise SystemExit(1)
436: 
437: kernel_axis_candidates = tuple(
438:     name
439:     for name in nonidentity_names
```

Line 449:

```text
447: )
448: 
449: if len(kernel_axis_candidates) != 1 or len(togglers) != 2:
450:     raise SystemExit(
451:         "unexpected sign-character partition of nonidentity elements"
```

Line 454:

```text
452:     )
453: 
454: kernel_axis = kernel_axis_candidates[0]
455: 
456: # ------------------------------------------------------------------
```

Line 620:

```text
618:             right_stabilizer_generator
619:         ] == 1,
620:     "stabilizer_generator_product_is_kernel_axis":
621:         multiply(
622:             left_stabilizer_generator,
```

Line 624:

```text
622:             left_stabilizer_generator,
623:             right_stabilizer_generator,
624:         ) == kernel_axis,
625: }
626: 
```

Line 1347:

```text
1345:     right_stabilizer_generator,
1346: )
1347: print("kernel_axis:", kernel_axis)
1348: print("togglers:", togglers)
1349: print(
```

Line 1539:

```text
1537:         "sign_character":
1538:             character,
1539:         "kernel_axis":
1540:             kernel_axis,
1541:         "togglers":
```

Line 1540:

```text
1538:             character,
1539:         "kernel_axis":
1540:             kernel_axis,
1541:         "togglers":
1542:             list(togglers),
```

Line 1692:

```text
1690:         "ordered left and right order-two pentagon stabilizers. Their "
1691:         "nonidentity generators are distinct togglers, and their product "
1692:         "is the sign-kernel axis. A left sheet shift equal to the left "
1693:         "stabilizer generator collapses left face-copy incidence; the "
1694:         "analogous statement holds on the right. Therefore exactly four "
```

Line 1761:

```text
1759:     f"- Right generator: `{right_stabilizer_generator}`",
1760:     f"- Generator product: `{multiply(left_stabilizer_generator, right_stabilizer_generator)}`",
1761:     f"- Sign-kernel axis: `{kernel_axis}`",
1762:     "",
1763:     "## Admissibility theorem",
```

## `scripts/audit_local_shift_pair_grammar_classification_026b.py`

Matched terms: kernel


Line 24:

```text
22: Because the Audit 025 sign character distinguishes
23: 
24:     kernel nonidentity: a
25:     togglers: b, ab,
26: 
```

Line 420:

```text
418:     "character_identity_zero":
419:         character.get(identity_name) == 0,
420:     "character_has_two_kernel_elements":
421:         Counter(character.values()) == {0: 2, 1: 2},
422:     "character_is_homomorphism":
```

Line 444:

```text
442:     raise SystemExit(1)
443: 
444: kernel_nonidentity = tuple(
445:     name
446:     for name in nonidentity_names
```

Line 456:

```text
454: )
455: 
456: if len(kernel_nonidentity) != 1 or len(togglers) != 2:
457:     raise SystemExit(
458:         "unexpected sign-character partition of nonidentity elements"
```

Line 461:

```text
459:     )
460: 
461: kernel_axis = kernel_nonidentity[0]
462: 
463: # ------------------------------------------------------------------
```

Line 622:

```text
620:     "character_preserving_aut_group_order2":
621:         len(character_preserving_automorphisms) == 2,
622:     "character_preserving_automorphisms_fix_kernel_axis":
623:         all(
624:             mapping[kernel_axis] == kernel_axis
```

Line 624:

```text
622:     "character_preserving_automorphisms_fix_kernel_axis":
623:         all(
624:             mapping[kernel_axis] == kernel_axis
625:             for mapping in character_preserving_automorphisms
626:         ),
```

Line 831:

```text
829: 
830:     # The sign-aware fingerprint deliberately forgets the names b and ab
831:     # while retaining the character distinction between the kernel axis
832:     # and the toggler coset. Left and right remain ordered.
833:     fingerprint_payload = {
```

Line 1195:

```text
1193:     "left_right_order_remains_distinguished":
1194:         shift_pair_to_aut_orbit[
1195:             (kernel_axis, togglers[0])
1196:         ]
1197:         != shift_pair_to_aut_orbit[
```

Line 1198:

```text
1196:         ]
1197:         != shift_pair_to_aut_orbit[
1198:             (togglers[0], kernel_axis)
1199:         ],
1200:     "same_and_distinct_toggler_pairs_are_distinguished":
```

Line 1240:

```text
1238:     )),
1239: )
1240: print("kernel_axis:", kernel_axis)
1241: print("togglers:", togglers)
1242: print(
```

Line 1382:

```text
1380:         "sign_character":
1381:             character,
1382:         "kernel_axis":
1383:             kernel_axis,
1384:         "togglers":
```

Line 1383:

```text
1381:             character,
1382:         "kernel_axis":
1383:             kernel_axis,
1384:         "togglers":
1385:             list(togglers),
```

Line 1552:

```text
1550:         "shift pairs do not collapse to one unlabeled type because "
1551:         "the Audit 025 sign character distinguishes the unique "
1552:         "nonidentity kernel axis from the two togglers. Under the "
1553:         "order-two character-preserving automorphism group of V4, "
1554:         "which fixes the kernel axis and exchanges the togglers, "
```

Line 1554:

```text
1552:         "nonidentity kernel axis from the two togglers. Under the "
1553:         "order-two character-preserving automorphism group of V4, "
1554:         "which fixes the kernel axis and exchanges the togglers, "
1555:         "the nine shift pairs form exactly five local grammar types. "
1556:         "A separately computed sign-aware incidence fingerprint gives "
```

Line 1590:

```text
1588:         "After seed gauge is removed, the signed V4 character leaves "
1589:         "five intrinsic ordered local lift grammars, not nine and not "
1590:         "one: kernel/kernel, kernel/toggler, toggler/kernel, equal "
1591:         "toggler/toggler, and distinct toggler/toggler."
1592:     ),
```

## `scripts/audit_native_character_axis_interpretation_027d.py`

Matched terms: kernel


Line 28:

```text
26:     chi_r(u,v) = phi_r(u) xor phi_r(v),
27: 
28: where phi_r is the unique nonzero V4 character with kernel {1,r}.
29: 
30: It then identifies the native kernel axis r for every grammar:
```

Line 30:

```text
28: where phi_r is the unique nonzero V4 character with kernel {1,r}.
29: 
30: It then identifies the native kernel axis r for every grammar:
31: - G0: both ordered pentagon-stabilizer axes,
32: - G1: the right pentagon-stabilizer axis,
```

Line 34:

```text
32: - G1: the right pentagon-stabilizer axis,
33: - G2: the left pentagon-stabilizer axis,
34: - G3: their product, the sign-kernel axis.
35: 
36: The audit also verifies:
```

Line 378:

```text
376: }
377: 
378: # Nonzero characters on one V4 factor, keyed by their kernel axis.
379: factor_character_by_kernel_axis: Dict[
380:     str,
```

Line 379:

```text
377: 
378: # Nonzero characters on one V4 factor, keyed by their kernel axis.
379: factor_character_by_kernel_axis: Dict[
380:     str,
381:     Dict[str, int],
```

Line 410:

```text
408:     if len(zero_nonidentity) != 1:
409:         raise SystemExit(
410:             f"factor character {mask} does not have one kernel axis"
411:         )
412: 
```

Line 413:

```text
411:         )
412: 
413:     factor_character_by_kernel_axis[
414:         zero_nonidentity[0]
415:     ] = values
```

Line 418:

```text
416: 
417: if set(
418:     factor_character_by_kernel_axis
419: ) != set(nonidentity_names):
420:     raise SystemExit("factor characters do not recover all native axes")
```

Line 494:

```text
492: )
493: 
494: kernel_axis = str(
495:     payload026b[
496:         "native_v4"
```

Line 498:

```text
496:         "native_v4"
497:     ][
498:         "kernel_axis"
499:     ]
500: )
```

Line 505:

```text
503:     left_stabilizer_generator,
504:     right_stabilizer_generator,
505: ) != kernel_axis:
506:     raise SystemExit(
507:         "ordered stabilizer generators do not multiply to kernel axis"
```

Line 507:

```text
505: ) != kernel_axis:
506:     raise SystemExit(
507:         "ordered stabilizer generators do not multiply to kernel axis"
508:     )
509: 
```

Line 588:

```text
586:         ]
587: 
588:         kernel_axis_for_character = (
589:             zero_nonidentity[0]
590:             if len(zero_nonidentity) == 1
```

Line 650:

```text
648:             "homomorphism":
649:                 homomorphism,
650:             "kernel_axis":
651:                 kernel_axis_for_character,
652:             "left_factor_values":
```

Line 651:

```text
649:                 homomorphism,
650:             "kernel_axis":
651:                 kernel_axis_for_character,
652:             "left_factor_values":
653:                 left_factor_values,
```

Line 688:

```text
686:         tuple(sorted(
687:             (
688:                 row["kernel_axis"]
689:                 for row
690:                 in rows_by_grammar[
```

Line 716:

```text
714:     ),
715:     "G3": (
716:         kernel_axis,
717:     ),
718: }
```

Line 758:

```text
756:             for row in character_rows
757:         ),
758:     "every_certificate_has_native_kernel_axis":
759:         all(
760:             row["kernel_axis"]
```

Line 760:

```text
758:     "every_certificate_has_native_kernel_axis":
759:         all(
760:             row["kernel_axis"]
761:             in nonidentity_names
762:             for row in character_rows
```

Line 788:

```text
786:         certificate_axis_sets
787:         == expected_certificate_axis_sets,
788:     "ordered_stabilizer_product_is_kernel_axis":
789:         multiply(
790:             left_stabilizer_generator,
```

Line 792:

```text
790:             left_stabilizer_generator,
791:             right_stabilizer_generator,
792:         ) == kernel_axis,
793: }
794: 
```

Line 806:

```text
804:     right_stabilizer_generator,
805: )
806: print("kernel_axis:", kernel_axis)
807: print(
808:     "stabilizer_generator_product:",
```

Line 842:

```text
840:         "character_id="
841:         + row["character_id"],
842:         "kernel_axis="
843:         + str(row["kernel_axis"]),
844:         "diagonal="
```

Line 843:

```text
841:         + row["character_id"],
842:         "kernel_axis="
843:         + str(row["kernel_axis"]),
844:         "diagonal="
845:         + str(row["diagonal"]).lower(),
```

Line 871:

```text
869:     "pentagon_stabilizer_axes_G1_uses_the_right_stabilizer_axis_"
870:     "G2_uses_the_left_stabilizer_axis_and_G3_uses_their_product_"
871:     "sign_kernel_axis"
872:     if audit_pass
873:     else
```

Line 875:

```text
873:     else
874:     "the_candidate_native_character_axis_interpretation_has_"
875:     "unresolved_basis_diagonal_kernel_shift_or_interface_checks"
876: )
877: 
```

Line 934:

```text
932:         "right_stabilizer_generator":
933:             right_stabilizer_generator,
934:         "kernel_axis":
935:             kernel_axis,
936:         "stabilizer_generator_product":
```

Line 935:

```text
933:             right_stabilizer_generator,
934:         "kernel_axis":
935:             kernel_axis,
936:         "stabilizer_generator_product":
937:             multiply(
```

Line 971:

```text
969:                 "diagonal":
970:                     row["diagonal"],
971:                 "kernel_axis":
972:                     row["kernel_axis"],
973:                 "left_factor_values":
```

Line 972:

```text
970:                     row["diagonal"],
971:                 "kernel_axis":
972:                     row["kernel_axis"],
973:                 "left_factor_values":
974:                     row["left_factor_values"],
```

Line 1013:

```text
1011:         "Every certificate has equal left and right masks, so it is a "
1012:         "diagonal character chi_r(u,v)=phi_r(u) xor phi_r(v). The "
1013:         "one-factor character phi_r has kernel {identity,r}, giving "
1014:         "each certificate a native V4 axis. In the ordered local frame, "
1015:         "G0 is certified by both pentagon-stabilizer axes, G1 by the "
```

Line 1017:

```text
1015:         "G0 is certified by both pentagon-stabilizer axes, G1 by the "
1016:         "right stabilizer axis, G2 by the left stabilizer axis, and G3 "
1017:         "by their product, which is the signed-face character kernel "
1018:         "axis. Every certificate vanishes on common left-right gauge "
1019:         "motion and on the grammar's own sheet-shift pair, but reads "
```

Line 1067:

```text
1065:     f"- Left pentagon stabilizer axis: `{left_stabilizer_generator}`",
1066:     f"- Right pentagon stabilizer axis: `{right_stabilizer_generator}`",
1067:     f"- Product / sign-kernel axis: `{kernel_axis}`",
1068:     "",
1069:     "## Character interpretation",
```

## `scripts/audit_rank8_schurian_automorphism_group_028j.py`

Matched terms: kernel


Line 866:

```text
864: )
865: 
866: kernel = tuple(
867:     permutation
868:     for permutation
```

Line 875:

```text
873: )
874: 
875: kernel_shift_rows = []
876: 
877: for permutation in kernel:
```

Line 877:

```text
875: kernel_shift_rows = []
876: 
877: for permutation in kernel:
878:     shifts = accepted_metadata[
879:         permutation
```

Line 903:

```text
901:     )
902: 
903:     kernel_shift_rows.append({
904:         "b":
905:             list(b),
```

Line 914:

```text
912:             for shift in expected_shifts
913:         ],
914:         "exact_kernel_law":
915:             shifts
916:             == expected_shifts,
```

Line 927:

```text
925:     })
926: 
927: kernel_shift_rows = sorted(
928:     kernel_shift_rows,
929:     key=lambda row: row["_b_tuple"],
```

Line 928:

```text
926: 
927: kernel_shift_rows = sorted(
928:     kernel_shift_rows,
929:     key=lambda row: row["_b_tuple"],
930: )
```

Line 952:

```text
950: )
951: 
952: kernel_conjugation_rows = []
953: 
954: for row in kernel_shift_rows:
```

Line 954:

```text
952: kernel_conjugation_rows = []
953: 
954: for row in kernel_shift_rows:
955:     permutation = next(
956:         permutation
```

Line 958:

```text
956:         permutation
957:         for permutation
958:         in kernel
959:         if accepted_metadata[
960:             permutation
```

Line 982:

```text
980:     )
981: 
982:     kernel_conjugation_rows.append({
983:         "b":
984:             list(
```

Line 997:

```text
995:     })
996: 
997: fixed_kernel_elements = tuple(
998:     row["_b_tuple"]
999:     for row
```

Line 1000:

```text
998:     row["_b_tuple"]
999:     for row
1000:     in kernel_conjugation_rows
1001:     if row["_b_tuple"]
1002:     == row["_conjugate_b_tuple"]
```

Line 1005:

```text
1003: )
1004: 
1005: even_parity_kernel = tuple(
1006:     row["_b_tuple"]
1007:     for row
```

Line 1008:

```text
1006:     row["_b_tuple"]
1007:     for row
1008:     in kernel_shift_rows
1009:     if row["parity"] == 0
1010: )
```

Line 1015:

```text
1013:     b
1014:     for b
1015:     in even_parity_kernel
1016:     if b != (
1017:         0,
```

Line 1036:

```text
1034:             row["_conjugate_b_tuple"]
1035:             for row
1036:             in kernel_conjugation_rows
1037:             if row["_b_tuple"] == current
1038:         )
```

Line 1284:

```text
1282:             "2": 8,
1283:         },
1284:     "kernel_order8":
1285:         len(kernel) == 8,
1286:     "kernel_exact_C2_cubed_shift_law":
```

Line 1285:

```text
1283:         },
1284:     "kernel_order8":
1285:         len(kernel) == 8,
1286:     "kernel_exact_C2_cubed_shift_law":
1287:         all(
```

Line 1286:

```text
1284:     "kernel_order8":
1285:         len(kernel) == 8,
1286:     "kernel_exact_C2_cubed_shift_law":
1287:         all(
1288:             row[
```

Line 1289:

```text
1287:         all(
1288:             row[
1289:                 "exact_kernel_law"
1290:             ]
1291:             for row
```

Line 1292:

```text
1290:             ]
1291:             for row
1292:             in kernel_shift_rows
1293:         )
1294:         and {
```

Line 1297:

```text
1295:             row["_b_tuple"]
1296:             for row
1297:             in kernel_shift_rows
1298:         }
1299:         == set(
```

Line 1308:

```text
1306:             )
1307:         ),
1308:     "rotation_action_fixed_kernel_size2":
1309:         len(
1310:             fixed_kernel_elements
```

Line 1310:

```text
1308:     "rotation_action_fixed_kernel_size2":
1309:         len(
1310:             fixed_kernel_elements
1311:         ) == 2,
1312:     "even_parity_plane_size4":
```

Line 1314:

```text
1312:     "even_parity_plane_size4":
1313:         len(
1314:             even_parity_kernel
1315:         ) == 4,
1316:     "rotation_cycles_three_nonzero_even_vectors":
```

Line 1422:

```text
1420: print()
1421: 
1422: print("== kernel and abstract group structure ==")
1423: print(
1424:     "kernel_order:",
```

Line 1424:

```text
1422: print("== kernel and abstract group structure ==")
1423: print(
1424:     "kernel_order:",
1425:     len(kernel),
1426: )
```

Line 1425:

```text
1423: print(
1424:     "kernel_order:",
1425:     len(kernel),
1426: )
1427: print(
```

Line 1428:

```text
1426: )
1427: print(
1428:     "kernel_shift_rows:",
1429:     [
1430:         {
```

Line 1436:

```text
1434:             if not key.startswith("_")
1435:         }
1436:         for row in kernel_shift_rows
1437:     ],
1438: )
```

Line 1449:

```text
1447:         }
1448:         for row
1449:         in kernel_conjugation_rows
1450:     ],
1451: )
```

Line 1453:

```text
1451: )
1452: print(
1453:     "fixed_kernel_elements:",
1454:     fixed_kernel_elements,
1455: )
```

Line 1454:

```text
1452: print(
1453:     "fixed_kernel_elements:",
1454:     fixed_kernel_elements,
1455: )
1456: print(
```

Line 1457:

```text
1455: )
1456: print(
1457:     "even_parity_kernel:",
1458:     even_parity_kernel,
1459: )
```

Line 1458:

```text
1456: print(
1457:     "even_parity_kernel:",
1458:     even_parity_kernel,
1459: )
1460: print(
```

Line 1483:

```text
1481:     if (
1482:         checks[
1483:             "kernel_exact_C2_cubed_shift_law"
1484:         ]
1485:         and checks[
```

Line 1679:

```text
1677:         "element_order_profile":
1678:             element_order_profile,
1679:         "kernel_order":
1680:             len(kernel),
1681:         "kernel_shift_rows": [
```

Line 1680:

```text
1678:             element_order_profile,
1679:         "kernel_order":
1680:             len(kernel),
1681:         "kernel_shift_rows": [
1682:             {
```

Line 1681:

```text
1679:         "kernel_order":
1680:             len(kernel),
1681:         "kernel_shift_rows": [
1682:             {
1683:                 key: value
```

Line 1689:

```text
1687:             }
1688:             for row
1689:             in kernel_shift_rows
1690:         ],
1691:         "rotation_conjugation_rows": [
```

Line 1699:

```text
1697:             }
1698:             for row
1699:             in kernel_conjugation_rows
1700:         ],
1701:         "fixed_kernel_elements": [
```

Line 1701:

```text
1699:             in kernel_conjugation_rows
1700:         ],
1701:         "fixed_kernel_elements": [
1702:             list(value)
1703:             for value
```

Line 1704:

```text
1702:             list(value)
1703:             for value
1704:             in fixed_kernel_elements
1705:         ],
1706:         "even_parity_kernel": [
```

Line 1706:

```text
1704:             in fixed_kernel_elements
1705:         ],
1706:         "even_parity_kernel": [
1707:             list(value)
1708:             for value
```

Line 1709:

```text
1707:             list(value)
1708:             for value
1709:             in even_parity_kernel
1710:         ],
1711:         "even_nonzero_rotation_orbit": [
```

## `scripts/audit_s3_sign_v4_d8_local_system_021.py`

Matched terms: kernel, triangle holonomy


Line 503:

```text
501: }
502: 
503: sign_kernel = {
504:     element
505:     for element in sheet_monodromy_group
```

Line 947:

```text
945:     "axis_action_is_sheet_sign_homomorphism":
946:         sign_homomorphism_failures == 0,
947:     "sign_kernel_is_a3":
948:         len(sign_kernel) == 3,
949:     "sign_image_is_c2":
```

Line 948:

```text
946:         sign_homomorphism_failures == 0,
947:     "sign_kernel_is_a3":
948:         len(sign_kernel) == 3,
949:     "sign_image_is_c2":
950:         sign_image == {identity3, role_swap},
```

Line 1073:

```text
1071: 
1072: print()
1073: print("== fundamental triangle holonomy ==")
1074: 
1075: for row in loop_rows:
```

Line 1085:

```text
1083: print()
1084: print("sheet_monodromy_group_order:", len(sheet_monodromy_group))
1085: print("sign_kernel_order:", len(sign_kernel))
1086: print("sign_image_order:", len(sign_image))
1087: print(
```

Line 1189:

```text
1187:     str(
1188:         sign_image == {identity3, role_swap}
1189:         and len(sign_kernel) == 3
1190:     ).lower(),
1191: )
```

Line 1383:

```text
1381:             )
1382:         ],
1383:         "sign_kernel_order":
1384:             len(sign_kernel),
1385:         "sign_image_order":
```

Line 1384:

```text
1382:         ],
1383:         "sign_kernel_order":
1384:             len(sign_kernel),
1385:         "sign_image_order":
1386:             len(sign_image),
```

Line 1387:

```text
1385:         "sign_image_order":
1386:             len(sign_image),
1387:         "sign_kernel": [
1388:             list(element)
1389:             for element in sorted(sign_kernel)
```

Line 1389:

```text
1387:         "sign_kernel": [
1388:             list(element)
1389:             for element in sorted(sign_kernel)
1390:         ],
1391:         "sign_image": [
```

Line 1515:

```text
1513:         "ab axes are exchanged. The individual edge actions "
1514:         "therefore generate the sign quotient C2 of S3, with "
1515:         "kernel A3. Every K5 triangle has nontrivial C2 "
1516:         "holonomy, so the b and ab axes cannot be globally "
1517:         "separated, although the carrier axis is globally fixed. "
```

Line 1530:

```text
1528:         "v4_axis_holonomy_is_sign_quotient_c2":
1529:             (
1530:                 len(sign_kernel) == 3
1531:                 and
1532:                 sign_image == {
```

Line 1674:

```text
1672:     len(sheet_monodromy_group),
1673: )
1674: print("sign_kernel_order:", len(sign_kernel))
1675: print("sign_image_order:", len(sign_image))
1676: print(
```

## `scripts/audit_signed_24_face_block_closure_025.py`

Matched terms: kernel


Line 47:

```text
45:     "native_deck",
46:     "uniform_toggle",
47:     "character_kernel",
48:     "character_togglers",
49:     "checks",
```

Line 75:

```text
73: native_deck = ns["native_deck"]
74: uniform_toggle = ns["uniform_toggle"]
75: character_kernel = ns["character_kernel"]
76: character_togglers = ns["character_togglers"]
77: source_checks = ns["checks"]
```

Line 379:

```text
377:             })
378: 
379: # Kernel orbits in each sign section.
380: kernel_orbits_by_sign = {}
381: 
```

Line 380:

```text
378: 
379: # Kernel orbits in each sign section.
380: kernel_orbits_by_sign = {}
381: 
382: for sign_name, sign_pairs in (
```

Line 397:

```text
395:             ]
396:             for deck_name
397:             in character_kernel
398:         }
399: 
```

Line 408:

```text
406:         unseen -= orbit
407: 
408:     kernel_orbits_by_sign[
409:         sign_name
410:     ] = tuple(sorted(
```

Line 415:

```text
413:     ))
414: 
415: kernel_orbit_profiles = {
416:     sign_name: dict(sorted(Counter(
417:         len(orbit)
```

Line 421:

```text
419:     ).items()))
420:     for sign_name, orbits
421:     in kernel_orbits_by_sign.items()
422: }
423: 
```

Line 509:

```text
507:     "sign_action_uses_geometric_character":
508:         (
509:             set(character_kernel)
510:             == {"identity", "a"}
511:             and
```

Line 515:

```text
513:             == {"b", "ab"}
514:         ),
515:     "positive_kernel_orbits_are_six_pairs":
516:         kernel_orbit_profiles[
517:             "positive"
```

Line 516:

```text
514:         ),
515:     "positive_kernel_orbits_are_six_pairs":
516:         kernel_orbit_profiles[
517:             "positive"
518:         ] == {2: 6},
```

Line 519:

```text
517:             "positive"
518:         ] == {2: 6},
519:     "negative_kernel_orbits_are_six_pairs":
520:         kernel_orbit_profiles[
521:             "negative"
```

Line 520:

```text
518:         ] == {2: 6},
519:     "negative_kernel_orbits_are_six_pairs":
520:         kernel_orbit_profiles[
521:             "negative"
522:         ] == {2: 6},
```

Line 655:

```text
653:     dict(sorted(uniform_toggle.items())),
654: )
655: print("character_kernel:", character_kernel)
656: print("character_togglers:", character_togglers)
657: print(
```

Line 662:

```text
660: )
661: print(
662:     "kernel_orbit_profiles:",
663:     kernel_orbit_profiles,
664: )
```

Line 663:

```text
661: print(
662:     "kernel_orbit_profiles:",
663:     kernel_orbit_profiles,
664: )
665: print()
```

Line 681:

```text
679:         "signed_face_system_with_twelve_positive_and_"
680:         "twelve_negative_five_state_partitions_related_by_"
681:         "the_character_kernel_identity_a_and_togglers_b_ab"
682:     )
683: else:
```

Line 854:

```text
852: 
853: audit_verdict = (
854:     "the_twelve_positive_twisted_face_blocks_extend_uniquely_to_a_v4_equivariant_twentyfour_block_signed_face_system_with_twelve_positive_and_twelve_negative_five_state_partitions_related_by_the_character_kernel_identity_a_and_togglers_b_ab"
855:     if audit_pass
856:     else
```

Line 964:

```text
962:     })
963: 
964: kernel_orbit_rows = {}
965: 
966: for sign_name, orbits in (
```

Line 967:

```text
965: 
966: for sign_name, orbits in (
967:     kernel_orbits_by_sign.items()
968: ):
969:     kernel_orbit_rows[sign_name] = [
```

Line 969:

```text
967:     kernel_orbits_by_sign.items()
968: ):
969:     kernel_orbit_rows[sign_name] = [
970:         [
971:             _pair_payload(pair_id)
```

Line 1097:

```text
1095:                 uniform_toggle.items()
1096:             )),
1097:         "character_kernel":
1098:             list(character_kernel),
1099:         "character_togglers":
```

Line 1098:

```text
1096:             )),
1097:         "character_kernel":
1098:             list(character_kernel),
1099:         "character_togglers":
1100:             list(character_togglers),
```

Line 1103:

```text
1101:         "sign_action_failure_count":
1102:             len(sign_action_failures),
1103:         "kernel_orbit_profiles":
1104:             kernel_orbit_profiles,
1105:         "signed_blocks":
```

Line 1104:

```text
1102:             len(sign_action_failures),
1103:         "kernel_orbit_profiles":
1104:             kernel_orbit_profiles,
1105:         "signed_blocks":
1106:             signed_block_rows,
```

Line 1111:

```text
1109:         "v4_block_action":
1110:             action_rows,
1111:         "kernel_orbits_by_sign":
1112:             kernel_orbit_rows,
1113:     },
```

Line 1112:

```text
1110:             action_rows,
1111:         "kernel_orbits_by_sign":
1112:             kernel_orbit_rows,
1113:     },
1114:     "checks":
```

Line 1127:

```text
1125:         "size four, each containing two positive and two negative "
1126:         "blocks. The sign is governed by the homomorphism "
1127:         "V4->C2 with kernel {identity,a}; b and ab exchange the "
1128:         "positive and negative sections. This is the exact "
1129:         "signed face-level closure compatible with the previously "
```

Line 1158:

```text
1156:                 ) == {1}
1157:             ),
1158:         "face_sign_character_kernel":
1159:             list(character_kernel),
1160:         "face_sign_character_togglers":
```

Line 1159:

```text
1157:             ),
1158:         "face_sign_character_kernel":
1159:             list(character_kernel),
1160:         "face_sign_character_togglers":
1161:             list(character_togglers),
```

Line 1196:

```text
1194:         "V4-equivariant signed double closure: twelve positive "
1195:         "and twelve negative five-state face blocks, related by "
1196:         "the character with kernel {identity,a}."
1197:     ),
1198: }
```

Line 1316:

```text
1314:     dict(sorted(uniform_toggle.items())),
1315: )
1316: print("character_kernel:", character_kernel)
1317: print("character_togglers:", character_togglers)
1318: print(
```

## `scripts/audit_six_orbit_pairwise_grammar_compatibility_026c.py`

Matched terms: kernel


Line 434:

```text
432:     "character_identity_zero":
433:         character.get(identity_name) == 0,
434:     "character_has_two_kernel_elements":
435:         Counter(character.values()) == {0: 2, 1: 2},
436:     "character_is_homomorphism":
```

Line 458:

```text
456:     raise SystemExit(1)
457: 
458: kernel_axis_candidates = tuple(
459:     name
460:     for name in nonidentity_names
```

Line 470:

```text
468: )
469: 
470: if len(kernel_axis_candidates) != 1 or len(togglers) != 2:
471:     raise SystemExit(
472:         "unexpected sign-character partition of nonidentity elements"
```

Line 475:

```text
473:     )
474: 
475: kernel_axis = kernel_axis_candidates[0]
476: 
477: # ------------------------------------------------------------------
```

Line 619:

```text
617:     grammar_shift_pairs = {
618:         "G0": (
619:             kernel_axis,
620:             kernel_axis,
621:         ),
```

Line 620:

```text
618:         "G0": (
619:             kernel_axis,
620:             kernel_axis,
621:         ),
622:         "G1": (
```

Line 623:

```text
621:         ),
622:         "G1": (
623:             kernel_axis,
624:             left_generator,
625:         ),
```

Line 628:

```text
626:         "G2": (
627:             right_generator,
628:             kernel_axis,
629:         ),
630:         "G3": (
```

Line 668:

```text
666:         "right_generator_is_toggler":
667:             character[right_generator] == 1,
668:         "side_generator_product_is_kernel_axis":
669:             multiply(
670:                 left_generator,
```

Line 672:

```text
670:                 left_generator,
671:                 right_generator,
672:             ) == kernel_axis,
673:         "four_grammar_shift_pairs_are_distinct":
674:             len(
```

Line 1413:

```text
1411:         "sign_character":
1412:             character,
1413:         "kernel_axis":
1414:             kernel_axis,
1415:         "togglers":
```

Line 1414:

```text
1412:             character,
1413:         "kernel_axis":
1414:             kernel_axis,
1415:         "togglers":
1416:             list(togglers),
```

## `scripts/audit_synthematic_total_534_transport_tower_020.py`

Matched terms: triangle holonomy


Line 1543:

```text
1541:         "the natural automorphism group Aut(V4) acting on the "
1542:         "three nonidentity native deck transformations a, b, "
1543:         "and ab. Test whether triangle holonomy permutes these "
1544:         "three V4 axes exactly as it permutes the carrier, b, "
1545:         "and ab roles. A positive result would replace the "
```

## `scripts/audit_v4_affine_character_cell_grammar_028h.py`

Matched terms: all-one, all_one


Line 43:

```text
41: uniform:
42: - two all-zero gauges;
43: - two all-one gauges.
44: 
45: A canonical all-zero gauge is selected lexicographically:
```

Line 768:

```text
766:                     0,
767:                 ),
768:             "all_one":
769:                 constant_values
770:                 == (
```

Line 795:

```text
793:     row
794:     for row in gauge_rows
795:     if row["all_one"]
796: ]
797: 
```

Line 1103:

```text
1101:             zero_gauges
1102:         ) == 2,
1103:     "all_one_gauge_count2":
1104:         len(
1105:             one_gauges
```

Line 1281:

```text
1279: )
1280: print(
1281:     "all_one_gauge_count:",
1282:     len(
1283:         one_gauges
```

Line 1307:

```text
1305:             ]
1306:         ).lower(),
1307:         "all_one="
1308:         + str(
1309:             row[
```

Line 1310:

```text
1308:         + str(
1309:             row[
1310:                 "all_one"
1311:             ]
1312:         ).lower(),
```

Line 1519:

```text
1517:                 zero_gauges
1518:             ),
1519:         "all_one_gauge_count":
1520:             len(
1521:                 one_gauges
```

Line 1554:

```text
1552:         "uses the transposed character relation. The constants are cell-"
1553:         "origin gauge data: two relative gauges produce the all-zero "
1554:         "normal form and two produce the all-one normal form."
1555:     ),
1556:     "boundary": {
```

Line 1607:

```text
1605:     "",
1606:     "With cell 0 fixed, the 16 relative origin gauges contain four",
1607:     "uniform-constant gauges: two all-zero and two all-one. The",
1608:     "canonical all-zero gauge shifts the cells by",
1609:     "",
```

Line 1723:

```text
1721: )
1722: print(
1723:     "all_one_gauge_count:",
1724:     len(
1725:         one_gauges
```

## `scripts/record_a5_cayley_v4_petersen_theorem_checkpoint_017.py`

Matched terms: kernel


Line 167:

```text
165:         (
166:             m16["five_point_action_image_size"] == 60
167:             and m16["five_point_action_kernel_size"] == 1
168:             and m16["homomorphism_failure_count"] == 0
169:         ),
```

## `scripts/support/project41_signed_face_character_support_025c.py`

Matched terms: kernel


Line 218:

```text
216:         )
217: 
218: character_kernel = tuple(sorted(
219:     deck_name
220:     for deck_name, bit
```

Line 338:

```text
336: 
337: # ---------------------------------------------------------------
338: # Kernel action on the twelve exact geometric pairs.
339: # ---------------------------------------------------------------
340: 
```

Line 342:

```text
340: 
341: unseen_exact = set(exact_pair_ids)
342: exact_kernel_orbits = []
343: 
344: while unseen_exact:
```

Line 351:

```text
349:             (seed, deck_name)
350:         ]
351:         for deck_name in character_kernel
352:     }
353: 
```

Line 356:

```text
354:     orbit &= exact_pair_ids
355: 
356:     exact_kernel_orbits.append(
357:         tuple(sorted(orbit))
358:     )
```

Line 362:

```text
360:     unseen_exact -= orbit
361: 
362: exact_kernel_orbits = tuple(sorted(
363:     exact_kernel_orbits,
364:     key=lambda orbit: orbit[0],
```

Line 363:

```text
361: 
362: exact_kernel_orbits = tuple(sorted(
363:     exact_kernel_orbits,
364:     key=lambda orbit: orbit[0],
365: ))
```

Line 367:

```text
365: ))
366: 
367: exact_kernel_orbit_size_profile = dict(
368:     sorted(Counter(
369:         len(orbit)
```

Line 370:

```text
368:     sorted(Counter(
369:         len(orbit)
370:         for orbit in exact_kernel_orbits
371:     ).items())
372: )
```

Line 509:

```text
507:     "toggle_character_is_homomorphism":
508:         not character_homomorphism_failures,
509:     "toggle_character_kernel_has_order2":
510:         len(character_kernel) == 2,
511:     "toggle_character_image_is_c2":
```

Line 510:

```text
508:         not character_homomorphism_failures,
509:     "toggle_character_kernel_has_order2":
510:         len(character_kernel) == 2,
511:     "toggle_character_image_is_c2":
512:         set(uniform_toggle.values())
```

Line 514:

```text
512:         set(uniform_toggle.values())
513:         == {0, 1},
514:     "kernel_is_identity_and_a":
515:         set(character_kernel)
516:         == {"identity", "a"},
```

Line 515:

```text
513:         == {0, 1},
514:     "kernel_is_identity_and_a":
515:         set(character_kernel)
516:         == {"identity", "a"},
517:     "togglers_are_b_and_ab":
```

Line 528:

```text
526:         candidate_orbit_exactness_profile
527:         == {(2, 2): 6},
528:     "exact_kernel_orbit_count6":
529:         len(exact_kernel_orbits) == 6,
530:     "exact_kernel_orbits_have_size2":
```

Line 529:

```text
527:         == {(2, 2): 6},
528:     "exact_kernel_orbit_count6":
529:         len(exact_kernel_orbits) == 6,
530:     "exact_kernel_orbits_have_size2":
531:         exact_kernel_orbit_size_profile
```

Line 530:

```text
528:     "exact_kernel_orbit_count6":
529:         len(exact_kernel_orbits) == 6,
530:     "exact_kernel_orbits_have_size2":
531:         exact_kernel_orbit_size_profile
532:         == {2: 6},
```

Line 531:

```text
529:         len(exact_kernel_orbits) == 6,
530:     "exact_kernel_orbits_have_size2":
531:         exact_kernel_orbit_size_profile
532:         == {2: 6},
533:     "state_block_action_failure_count_zero":
```

Line 561:

```text
559:     dict(sorted(uniform_toggle.items())),
560: )
561: print("character_kernel:", character_kernel)
562: print("character_togglers:", character_togglers)
563: print(
```

Line 599:

```text
597: 
598: print()
599: print("== kernel action on 12 exact geometric pairs ==")
600: print(
601:     "exact_kernel_orbit_count:",
```

Line 601:

```text
599: print("== kernel action on 12 exact geometric pairs ==")
600: print(
601:     "exact_kernel_orbit_count:",
602:     len(exact_kernel_orbits),
603: )
```

Line 602:

```text
600: print(
601:     "exact_kernel_orbit_count:",
602:     len(exact_kernel_orbits),
603: )
604: print(
```

Line 605:

```text
603: )
604: print(
605:     "exact_kernel_orbit_size_profile:",
606:     exact_kernel_orbit_size_profile,
607: )
```

Line 606:

```text
604: print(
605:     "exact_kernel_orbit_size_profile:",
606:     exact_kernel_orbit_size_profile,
607: )
608: 
```

Line 610:

```text
608: 
609: for orbit_index, orbit in enumerate(
610:     exact_kernel_orbits
611: ):
612:     print(
```

Line 613:

```text
611: ):
612:     print(
613:         "kernel_orbit_"
614:         + str(orbit_index)
615:         + ":",
```

Line 705:

```text
703:         "the_twelve_exact_twisted_face_carriers_are_the_"
704:         "positive_class_of_a_v4_equivariant_twentyfour_pair_"
705:         "system_with_incidence_character_v4_to_c2_kernel_"
706:         "identity_a_and_togglers_b_ab_while_the_twelve_"
707:         "five_state_face_blocks_carry_the_full_native_v4_action"
```

Line 721:

```text
719: )
720: print(
721:     "face_incidence_character_kernel_identity_a:",
722:     str(
723:         set(character_kernel)
```

Line 723:

```text
721:     "face_incidence_character_kernel_identity_a:",
722:     str(
723:         set(character_kernel)
724:         == {"identity", "a"}
725:     ).lower(),
```

## `sources/upstream/b32k-atomic-intermediate-cover-triad-009.py`

Matched terms: kernel


Line 23:

```text
21: BUNDLE = (
22:     ROOT
23:     / "18-g900-kernel-admission"
24:     / "artifacts/json/g60_native_generator_input_bundle_001.v1.json"
25: )
```

## `sources/upstream/b32k-atomic-line-graph-tower-008.py`

Matched terms: kernel


Line 21:

```text
19: BUNDLE = (
20:     ROOT
21:     / "18-g900-kernel-admission"
22:     / "artifacts/json/g60_native_generator_input_bundle_001.v1.json"
23: )
```

## `sources/upstream/b32k_atomic_deck_orbit_audit_005.json`

Matched terms: kernel

- `$.bundle_metadata.checks[4].detail`: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/18-g900-kernel-admission/artifacts/json/old_g60_to_current_g60_vertex_map_001.json`
- `$.bundle_metadata.summary.map_source`: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/18-g900-kernel-admission/artifacts/json/old_g60_to_current_g60_vertex_map_001.json`
- `$.sources.bundle`: `/data/data/com.termux/files/home/dev/cori/research/mathematics/thalean-graph-theory/18-g900-kernel-admission/artifacts/json/g60_native_generator_input_bundle_001.v1.json`

## `sources/upstream/b32k_atomic_intermediate_cover_triad_009.json`

Matched terms: kernel

- `$.sources.bundle`: `/data/data/com.termux/files/home/dev/cori/research/mathematics/thalean-graph-theory/18-g900-kernel-admission/artifacts/json/g60_native_generator_input_bundle_001.v1.json`

## `sources/upstream/b32k_atomic_line_graph_tower_008.json`

Matched terms: kernel

- `$.sources.bundle`: `/data/data/com.termux/files/home/dev/cori/research/mathematics/thalean-graph-theory/18-g900-kernel-admission/artifacts/json/g60_native_generator_input_bundle_001.v1.json`

## `sources/upstream/g60_native_generator_input_bundle_001.v1.json`

Matched terms: kernel

- `$.summary.map_source`: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/18-g900-kernel-admission/artifacts/json/old_g60_to_current_g60_vertex_map_001.json`
- `$.checks[4].detail`: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/18-g900-kernel-admission/artifacts/json/old_g60_to_current_g60_vertex_map_001.json`

## `sources/upstream/schlafli_534_shadow_test_018.v1.json`

Matched terms: kernel

- `$.input_g60_graph_csv`: `/data/data/com.termux/files/home/dev/cori/research/thalean-graph-theory/18-g900-kernel-admission/source/kernel_payload/g60_local_edges.csv`

