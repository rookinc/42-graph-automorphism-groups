# Project 42 Quotient-Frame Orbit Certificate 004

Audit pass: `True`

Scope: certifies the three-member automorphism orbit of the natural quotient partition. It does not claim global completeness among all admissible quotient partitions.

## Group action

- Automorphism count: `720`
- Partition orbit size: `3`
- Partition action image order: `6`
- Action kernel order: `120`
- Kernel centralizer order: `6`

## P0

Associated involution: `tau0`

Partition action: `[0, 2, 1]`

Blocks:

- `0 1`
- `2 3`
- `4 5`
- `6 7`
- `8 9`
- `10 11`
- `12 13`
- `14 15`
- `16 17`
- `18 19`
- `20 21`
- `22 23`
- `24 25`
- `26 27`
- `28 29`

Involution cycles:

- `(0 1)`
- `(2 3)`
- `(4 5)`
- `(6 7)`
- `(8 9)`
- `(10 11)`
- `(12 13)`
- `(14 15)`
- `(16 17)`
- `(18 19)`
- `(20 21)`
- `(22 23)`
- `(24 25)`
- `(26 27)`
- `(28 29)`

## P1

Associated involution: `tau1`

Partition action: `[2, 1, 0]`

Blocks:

- `0 11`
- `1 28`
- `2 25`
- `3 12`
- `4 19`
- `5 26`
- `6 23`
- `7 14`
- `8 17`
- `9 20`
- `10 29`
- `13 24`
- `15 22`
- `16 21`
- `18 27`

Involution cycles:

- `(0 11)`
- `(1 28)`
- `(2 25)`
- `(3 12)`
- `(4 19)`
- `(5 26)`
- `(6 23)`
- `(7 14)`
- `(8 17)`
- `(9 20)`
- `(10 29)`
- `(13 24)`
- `(15 22)`
- `(16 21)`
- `(18 27)`

## P2

Associated involution: `tau2`

Partition action: `[1, 0, 2]`

Blocks:

- `0 29`
- `1 10`
- `2 13`
- `3 24`
- `4 27`
- `5 18`
- `6 15`
- `7 22`
- `8 21`
- `9 16`
- `11 28`
- `12 25`
- `14 23`
- `17 20`
- `19 26`

Involution cycles:

- `(0 29)`
- `(1 10)`
- `(2 13)`
- `(3 24)`
- `(4 27)`
- `(5 18)`
- `(6 15)`
- `(7 22)`
- `(8 21)`
- `(9 16)`
- `(11 28)`
- `(12 25)`
- `(14 23)`
- `(17 20)`
- `(19 26)`

## Forty-five-pair census

- Union pair count: `45`
- Pairwise block-disjoint: `True`

## Checks

- `partition_count_is_3`: `True`
- `all_partition_block_counts_are_15`: `True`
- `all_tau_orders_are_2`: `True`
- `all_tau_orbit_partitions_match`: `True`
- `all_covering_edge_counts_pass`: `True`
- `union_pair_count_is_45`: `True`
- `pairwise_block_disjoint`: `True`
- `partition_action_is_S3`: `True`
- `kernel_order_is_120`: `True`
- `centralizer_order_is_6`: `True`
