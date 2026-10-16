# Native producer-version compatibility

Fork source is the Docker-declared immutableab025b4 (originalLean4.15). Compile with actual producerSDK4.27, initialOptionsautoImplicitfalse/maxHeartbeats800000. Firstbuild finds removed Info.ofOmissionInfo constructors in oldhelper; use exact officialproducer4.27 InfoTree helper implementation, without inventing omission logic or editing proof bytes. Originalfork/helper/build retained. GC/batch behavior is upstreampriorart, not a proposedmethod.

Secondbuild confirms currentproducer InfoTree.tactics adds rootGoals beforegoals; preserve fork tactic output using the currentgoals field, ignoring the extra root-goal metadata as the originalfork schema does. Remove retired Command.Context.tacticCache? field absent in currentSDK. No verification, sourcebody, timeout, GCdiscard or batchpolicy is changed.
