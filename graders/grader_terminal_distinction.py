import sys
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        env.reset()
        env.state_obj.distance_to_destination = 0.5
        _, _, term, _, info = env.step([0,0,0])
        if not term:
            raise ValueError("Environment failed to terminate upon delivery")
        if info.get("delivery_status") != "delivered":
            raise ValueError("Incorrect delivery tag provided at terminal state")
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
