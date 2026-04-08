import gymnasium as gym
from vaxgym.environment import VaxGymEnv
import numpy as np
import time

def run_demo():
    print("=" * 60)
    print("VaxGym Env Offline Execution Demo")
    print("=" * 60)
    env = VaxGymEnv()
    
    print("Action Space:", env.action_space_summary())
    print("Observation Space:", env.observation_space_summary())
    
    scenarios = ["easy_stable_delivery", "remote_low_connectivity", "outage_near_expiry_crisis"]
    
    for scenario in scenarios:
        print(f"\n[{scenario.upper()}] Init...")
        
        obs, info = env.reset(scenario=scenario)
        done = False
        step = 0
        
        while not done and step < 15: # Limited steps for demonstration
            # Request explicit print due to rigid string-returning setup
            rendered_state = env.render(mode="text")
            if rendered_state:
                print(rendered_state)
            
            state = env.get_state()
            
            # Simulated edge AI inference heuristics 
            cooling = 3 if state.temperature > 7.0 else 1 if state.temperature > 5.0 else 0
            route = 2 if state.expiry_time_remaining < 15.0 else 1
            sync = 1 if (state.unsynced_records > 5 and state.connectivity == 1) else 0
                
            action = np.array([cooling, route, sync])
            print(f"-> Agent Executes [Cooling={cooling}, Route={route}, Sync={sync}]")
            
            obs, reward, terminated, truncated, info = env.step(action)
            
            print(f"-> Reward: {reward:.2f}")
            print("-" * 60)
            
            done = terminated or truncated
            step += 1
            time.sleep(0.05)
            
        if done:
            print(f"Scenario Terminated. Delivery: {info.get('delivery_status')} | Expiry: {info.get('expiry_status')}")
            print(f"Final Reward Breakdown:", info["reward_breakdown"])

if __name__ == "__main__":
    run_demo()
