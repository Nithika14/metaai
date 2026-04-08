import sys
import numpy as np
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        env.reset()
        try:
            env.step(np.array([99, -5, 20]))
        except Exception as e:
            raise ValueError(f"Crash on invalid action: {e}")
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
