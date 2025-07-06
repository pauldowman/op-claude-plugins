# How to get details of a dispute game

1. Each dispute game is a contract deployed on L1 (mainnet or sepolia). It is not deployed on L2. It is a proxy contract.
2. Get the ABI to learn what methods are available. You'll need to know which type of dispute game it is: `FaultDisputeGame` (permissionless dispute game), `PermissionedDisputeGame` (permissioned dispute game), `SuperFaultDisputeGame` (interop-enabled permissionless dispute agme), or `SuperPermissionedDisputeGame` (interop-enabled permissioned dispute game).
3. Use `cast` to call the method.
4. Don't guess at the meaning of constants. Use the tool to get dispute game constants.
5. The Optimism specs have more information about how fault proofs and dispute games work.
