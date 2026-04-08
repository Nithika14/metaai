import sys
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        env.reset()
        if env.state() is not env.get_state():
            raise ValueError("state() and get_state() handle resolution mismatch")
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
