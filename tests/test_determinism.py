import numpy as np
from vaxgym.environment import VaxGymEnv

def test_determinism():
    env1 = VaxGymEnv()
    o1, _ = env1.reset(seed=10)
    
    env2 = VaxGymEnv()
    o2, _ = env2.reset(seed=10)
    
    assert np.array_equal(o1, o2), "Resetting with same seed gives different observations"
    
    action = np.array([1, 1, 1])
    step1 = env1.step(action)
    step2 = env2.step(action)
    
    assert np.array_equal(step1[0], step2[0]), "Deterministic environments diverge on identical step"
    assert step1[1] == step2[1], "Rewards differ"
    assert step1[2] == step2[2], "Terminated mismatch"
