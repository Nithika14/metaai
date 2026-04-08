from vaxgym.environment import VaxGymEnv

def test_terminal_distance():
    env = VaxGymEnv()
    env.reset()
    env.state_obj.distance_to_destination = 1.0
    _, _, term, _, info = env.step([0, 0, 0])
    
    assert term, "Environment should terminate upon delivery"
    assert info["delivery_status"] == "delivered", "Incorrect delivery tag on valid finish"

def test_terminal_spoilage():
    env = VaxGymEnv()
    env.reset()
    env.state_obj.temperature = 12.0 # Huge breach
    for _ in range(5):
        _, _, term, _, info = env.step([0, 0, 0])
        if term and info["expiry_status"] == "spoiled":
            return
    assert False, "Failed to terminate immediately upon permanent spoilage threshold logic"
