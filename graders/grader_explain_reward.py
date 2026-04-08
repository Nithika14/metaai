import sys
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        _, info = env.reset()
        b = info.get("reward_breakdown", {})
        total = sum(v for k, v in b.items() if k != "total")
        if abs(b.get("total", 0) - total) > 1e-6:
            raise ValueError("Reward breakdown constituents do not match the reported total symmetrically")
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
