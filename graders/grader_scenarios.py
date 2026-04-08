import sys
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        env.reset(scenario="outage_near_expiry_crisis")
        
        solved = False
        for i in range(25):
            obs, rew, term, trunc, info = env.step([3, 2, 1])
            if term and info["delivery_status"] == "delivered" and info["expiry_status"] != "spoiled":
                solved = True
                break
                
        if not solved:
            raise ValueError("Crisis scenario was unrecoverable even using perfect heuristics")
            
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
