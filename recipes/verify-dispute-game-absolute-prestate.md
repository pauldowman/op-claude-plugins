# How to verify the absolute prestate of a dispute game

1. Get the value of `absolutePrestate` from the dispute game in question. You will need its contract address.
2. Fetch standard prestates configuration from the Superchain Registry.
3. Check if the `absolutePresate` matches one of the hashes in the standard prestates. If this network has 64-bit Cannon enabled the prestate hash should be the "cannon64" type. If this network has Interop enabled the prestate hash should be the "interop" type.
4. Check if the prestate hash matches `latest_stable` or `latest_rc` from the standard prestates config file.
