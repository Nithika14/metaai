import sys
import numpy as np
from vaxgym.environment import VaxGymEnv

def run():
    try:
        e1, e2 = VaxGymEnv(), VaxGymEnv()
        o1, _ = e1.reset(seed=99)
        o2, _ = e2.reset(seed=99)
        if not np.array_equal(o1, o2):
            raise ValueError("Seed determinism failed on initial reset")
            
        a = [1, 1, 1]
        n1 = e1.step(a)
        n2 = e2.step(a)
        
        if not np.array_equal(n1[0], n2[0]) or n1[1] != n2[1]:
            raise ValueError("Seed determinism failed on steps")
            
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
