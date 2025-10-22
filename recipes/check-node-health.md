# How to check node health

1. Use op-workbench to list RPC URLs for the network (if it's not an Ethereum L1 network or testnet then it's probably an OP Stack L2). You'll need to know the following:
    - Mainnet or testnet
    - Production or dev environment
    - Which node type we're interested in: op-geth or op-node
2. Do a basic health check:
    - For op-geth or L1 geth start with `cast block-number`
    - For op-node start with `cast rpc optimism_syncStatus`
3. If the basic health check passes do a more advanced check:
    - For op-geth or L1 geth do `cast rpc eth_syncing`. It should return false if it's fully synced.
    - For op-node first find the latest block from op-geth, then convert it to hex with `cast 2h`, then do `cast rpc optimism_outputAtBlock` giving it that hex value as the block number.
