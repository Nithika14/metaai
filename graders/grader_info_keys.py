import sys
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        _, info = env.reset()
        
        req_keys = [
            "reward_breakdown", "temp_breach_detected", "delivery_status", 
            "expiry_status", "action_valid", "route_selected", "risk_level", 
            "scenario_name", "breach_count", "step_count", 
            "thermochromic_alert_state", "sync_pending"
        ]
        
        for k in req_keys:
            if k not in info:
                raise KeyError(f"Info dict lacking explicit required key: {k}")
                
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
