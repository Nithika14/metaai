import sys
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        _, info = env.reset()
        
        req = [
            "safe_delivery", "breach", "expiry_accel", "battery_waste", 
            "recovery", "stabilize", "smart_redirect", "sync_neglect", 
            "terminal_success", "terminal_expiry", "terminal_spoilage", "total"
        ]
        
        for k in req:
            if k not in info.get("reward_breakdown", {}):
                raise KeyError(f"Reward breakdown missing parameter: {k}")
                
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
