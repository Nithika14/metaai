import numpy as np
from vaxgym.environment import VaxGymEnv

def test_reset():
    env = VaxGymEnv()
    obs, info = env.reset(seed=42)
    assert obs.shape == env.observation_space.shape
    assert isinstance(info, dict)
    
def test_reset_scenario():
    env = VaxGymEnv()
    obs, info = env.reset(scenario="easy_stable_delivery")
    assert info["scenario_name"] == "easy_stable_delivery"
