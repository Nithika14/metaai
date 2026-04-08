# VaxGym Environment Specification

## State Fields (Observation Space)
The `Box(9,)` state space tracks real-time transport physics dynamically:
1. `temperature`: Instantaneous core reading.
2. `ambient_temp`: External weather reading, driven by drift constants.
3. `battery_level`: Reserve power tracking usage of cooling hardware.
4. `expiry_time_remaining`: Degradation limits of the payload.
5. `distance_to_destination`: Absolute proximity to the mission target.
6. `connectivity`: 0 for OFFLINE, 1 for ONLINE.
7. `thermochromic_state`: Enum 0 (SAFE), 1 (WARNING), 2 (BREACH).
8. `unsynced_records`: Telemetry cached on-edge awaiting sync.
9. `step_count`: Elapsed time segments.

## Actions (Action Space)
The explicit `MultiDiscrete([4, 3, 2])` dictates interactions matching remote control logic:
- `cooling_level` (0-3): OFF, LOW, MEDIUM, HIGH. Cost scales quadratically.
- `route_decision` (0-2): STANDBY, CONTINUE, REROUTE_URGENT.
- `sync_action` (0-1): DO_NOTHING, ATTEMPT_SYNC. Fails if offline.

## Terminal Conditions
The environment terminates unconditionally if:
- `distance_to_destination <= 0`: Valid delivery (Terminal Success mapping).
- `expiry_time_remaining <= 0`: Viability threshold depleted (Terminal Expiry mapping).
- `thermochromic_state == BREACH`: Extreme heat triggers structural loss (Terminal Spoilage mapping).
- *Truncates* securely at `step_count >= 200`.

## Reward Terms 
Evaluated on every `step()`, calculating deltas:
- `safe_delivery`: +1.0 while maintaining 2C - 8C boundaries.
- `breach`: Heavy neg-margins (-2.0, -5.0) responding to threshold crossings.
- `expiry_accel`: -1.0 corresponding to out-of-boundary acceleration mapping.
- `battery_waste`: -2.0 for wasting AC while already below 2C, -5.0 for dead battery.
- `recovery`: +5.0 immediate delta reward for successfully plunging back into 2C - 8C safe zone.
- `smart_redirect`: +3.0 delta points for executing an emergency redirect effectively.
- `sync_neglect`: -2.0 points for accumulating cached tracking logs without dumping in online zones.

## Info Dict Contract
Provides `dict` transparency per Gym architecture natively tracking analytical context strictly containing:
- `reward_breakdown`: Internal `dict` containing the summation structure of all delta logic points.
- `scenario_name`: Currently loaded map condition.
- `temp_breach_detected`, `action_valid`, `route_selected`, `risk_level`, `breach_count`, `step_count`, `thermochromic_alert_state`, `sync_pending`, `delivery_status`, `expiry_status`.
