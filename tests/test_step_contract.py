from vaxgym.environment import VaxGymEnv

def test_step_contract():
    env = VaxGymEnv()
    env.reset()
    action = env.action_space.sample()
    result = env.step(action)
    
    assert len(result) == 5, "Step must return 5 values"
    obs, reward, terminated, truncated, info = result
    
    assert obs.shape == env.observation_space.shape
    assert isinstance(reward, float)
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)
