from vaxgym.environment import VaxGymEnv

def test_crisis_scenario_solvable():
    env = VaxGymEnv()
    env.reset(scenario="outage_near_expiry_crisis")
    
    solved = False
    for _ in range(25):
        # Action: HIGH cooling, REROUTE_URGENT, ATTEMPT_SYNC
        _, _, term, _, info = env.step([3, 2, 1])
        if term:
            if info["delivery_status"] == "delivered" and info["expiry_status"] != "spoiled":
                solved = True
            break
            
    assert solved, "The 'outage_near_expiry_crisis' scenario could not be solved using a max-effort heuristic"
