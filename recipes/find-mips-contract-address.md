How to find the MIPS contract address:

To find the actual MIPS contract being used, navigate from SystemConfigProxy like this:
1. SystemConfigProxy.disputeGameFactory gives the DisputeGameFactory address
2. DisputeGameFactory.gameImpls(0) gives the FaultDisputeGame address.
3. FaultDisputeGame.vm gives the MIPS contract address.

The same can be done to check which MIPS contract is being used by the PermissionedDisputeGame:
1. DisputeGameFactory.gameImpls(1) gives the PermissionedDisputeGame address.
2. PermissionedDisputeGame.vm gives the MIPS contract address.
