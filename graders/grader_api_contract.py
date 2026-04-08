import sys
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        assert hasattr(env, 'reset')
        assert hasattr(env, 'step')
        assert hasattr(env, 'render')
        assert hasattr(env, 'state')
        assert hasattr(env, 'get_state')
        assert hasattr(env, 'action_space_summary')
        assert hasattr(env, 'observation_space_summary')
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: API format mismatched - {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
