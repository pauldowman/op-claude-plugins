# How to check if the safe head db is enabled in op-node

1. Find an L1 block number that's a day old.
2. Do `cast rpc optimism_safeHeadAtL1Block` for that block number.
3. If a valid result is returned then the safe head db is enabled.
4. Otherwise look for the error "safe head database not enabled".
