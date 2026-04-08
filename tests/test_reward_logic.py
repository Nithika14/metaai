from vaxgym.environment import VaxGymEnv

def test_reward_breakdown_keys():
    env = VaxGymEnv()
    _, info = env.reset()
    breakdown = info["reward_breakdown"]
    
    expected_keys = [
        "safe_delivery", "breach", "expiry_accel", "battery_waste", 
        "recovery", "stabilize", "smart_redirect", "sync_neglect", 
        "terminal_success", "terminal_expiry", "terminal_spoilage", "total"
    ]
    
    for k in expected_keys:
        assert k in breakdown, f"Reward breakdown is missing required key: {k}"

def test_reward_sum():
    env = VaxGymEnv()
    _, info = env.reset()
    breakdown = info["reward_breakdown"]
    
    calculated_total = sum(v for k, v in breakdown.items() if k != "total")
    assert breakdown["total"] == calculated_total, "Reward total doesn't match sum of constituents"
