import sys
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        env.reset()
        res = env.render(mode="text")
        if not isinstance(res, str):
            raise TypeError("render() output must strictly be a string")
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
