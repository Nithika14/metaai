from vaxgym.environment import VaxGymEnv

def test_info_keys():
    env = VaxGymEnv()
    _, info = env.reset()
    
    expected_keys = [
        "reward_breakdown", "temp_breach_detected", "delivery_status",
        "expiry_status", "action_valid", "route_selected", "risk_level",
        "scenario_name", "breach_count", "step_count", 
        "thermochromic_alert_state", "sync_pending"
    ]
    
    for k in expected_keys:
        assert k in info, f"Info dictionary is missing required key: {k}"
