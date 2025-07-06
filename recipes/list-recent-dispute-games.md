# How to list recent dispute games

1. Get the address of the `DisputeGameFactoryProxy` contract from the superchain registry. This is on the L1 (Ethereum mainnet).
2. Figure out a starting block number. For blocks in the last 24 hours use the latest block, then based on the block time (available from the superchain registry) calculate the number of blocks to go back. E.g.: latest_block - (num_seconds_in_24_hours / block_time)
2. Using cast, get the logs with the signature "DisputeGameCreated(address,uint32,bytes32)"
3. Topic 1 (second item in the array) is the address of the dispute game created

