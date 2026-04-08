# Design Rationale: VaxGym to VaxGuard AI
### Conceptual Context

VaxGym operates as the Gymnasium-grade simulation of the real-world **Super Aura / VaxGuard AI hardware**. While VaxGym evaluates software policies autonomously, its structural roots lie entirely within the physical sensors, thermal mechanics, and public-health logistics present in Indian remote Primary Health Centres (PHCs).

#### Real-World Equivalencies
- **TMP117 Sensors -> Core Trackers**: In the real world, the TMP117 sensor manages hyper-accurate temperature sampling. In VaxGym, this maps perfectly to the instantaneous `state.temperature` updates responding to ambient drift arrays. 
- **Active Peltier + Fan Cooling -> `CoolingLevel` Actions**: The physical Peltier module draws extreme voltage to drain ambient enclosure heat. This directly translates to the RL's `COOLING_POWER` variables where the cost of stabilizing vaccines drops internal metrics but brutally drains the simulated offline `battery_level`.
- **Thermochromic Alert Trigger -> Failsafe Spoilage State**: When real thermochromic labels trigger past 8°C permanently, the vaccines are voided visually. In the sim, breaching `CRITICAL_TEMP_HIGH` trips the exact `ThermochromicState.BREACH`, rendering the cargo terminal immediately with `-50.0` points.
- **Offline / Sync Constraints -> Network Scenarios**: Remote transport in India has notorious dead zones. Real Edge models process offline; VaxGym strictly rewards tracking data internally and only flushing `sync_action=1` when passing through connectivity windows.

By simulating the friction points between battery constraints, thermal momentum, expiry speed tracking, and routing logic, VaxGym builds models that seamlessly port to actual microcontroller edge inferences.
