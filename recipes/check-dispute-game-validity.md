# How to check if a dispute game is valid

1. Get the value of `rootClaim` from the dispute game. 
2. Get the value of `l2BlockNumber` from the dispute game.
3. Convert the l2 block number to hex using `cast 2h`.
3. Use `cast call` to call `optimism_outputAtBlock` on an L2 node (use op-node, not op-geth).
4. Compare the value of `outputRoot` with the `rootClaim` on the dispute game. If the block is not found it might be older than the node's archive history.
5. If `outputRoot` and `rootClaim` match then the game is valid. If not, it is invalid.
