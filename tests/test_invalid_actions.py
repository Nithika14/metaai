import numpy as np
from vaxgym.environment import VaxGymEnv

def test_invalid_action_no_crash():
    env = VaxGymEnv()
    env.reset()
    
    try:
        # Heavily malformed action inputs
        env.step(np.array([-99, 999, 42]))
    except Exception as e:
        assert False, f"Environment crashed upon invalid action submission: {e}"
