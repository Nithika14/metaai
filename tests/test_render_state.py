from vaxgym.environment import VaxGymEnv

def test_render_output_type():
    env = VaxGymEnv()
    env.reset()
    result = env.render(mode="text")
    assert isinstance(result, str), "render() must return a string as required"

def test_state_aliasing():
    env = VaxGymEnv()
    env.reset()
    assert env.state() is env.get_state(), "state() and get_state() do not exactly resolve identical handles"
