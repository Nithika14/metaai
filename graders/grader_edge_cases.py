import sys
from vaxgym.environment import VaxGymEnv

def run():
    try:
        env = VaxGymEnv()
        
        # Test 1: Thermochromic alert
        env.reset()
        env.state_obj.temperature = 9.0
        _, _, _, _, info = env.step([0,0,0])
        if info["thermochromic_alert_state"] not in ["WARNING", "BREACH"]:
            raise ValueError("No thermochromic warning/breach registered above 8C")
            
        # Test 2: Battery drain logic
        env.reset()
        start_batt = env.state_obj.battery_level
        env.step([3, 0, 0])
        if env.state_obj.battery_level >= start_batt:
            raise ValueError("Active cooling failed to drain battery")
            
        # Test 3: Sync Pending isolation
        env.reset()
        env.state_obj.unsynced_records = 15
        env.state_obj.connectivity = 0 # OFFLINE
        _, _, _, _, info = env.step([0,0,0])
        if info["sync_pending"] is not True:
            raise ValueError("Sync pending flag was not raised correctly when offline")
            
        print("PASS")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
