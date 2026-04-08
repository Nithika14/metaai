import os
import sys
import gymnasium as gym
import pandas as pd
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from vaxgym.environment import VaxGymEnv
from vaxgym.wrappers import VaxAnalytics

gym.register(id='VaxGym-v0', entry_point='vaxgym.environment:VaxGymEnv')

class AnalyticsCallback(BaseCallback):
    def __init__(self, log_path="logs/efficiency_curve.csv"):
        super().__init__()
        self.log_path = log_path
        self.data = []
        
    def _on_step(self):
        for idx, done in enumerate(self.locals.get("dones", [])):
            if done:
                info = self.locals["infos"][idx]
                self.data.append({
                    "episode": len(self.data),
                    "energy_per_dose": info.get("vaxanalytics_energy_per_dose", 0.0),
                    "episode_reward": info.get("episode", {}).get("r", 0.0),
                    "mkt_stability": info.get("vaxanalytics_mkt_stability", 0.0)
                })
        return True
        
    def _on_training_end(self):
        pd.DataFrame(self.data).to_csv(self.log_path, index=False)

def main():
    os.makedirs("models", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    base_env = VaxGymEnv()
    wrapped_env = VaxAnalytics(base_env)
    env = Monitor(wrapped_env) 

    policy_kwargs = dict(net_arch=[dict(pi=[256, 256], vf=[256, 256])])
    model = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=1)
    
    callback = AnalyticsCallback()
    model.learn(total_timesteps=100000, callback=callback)
    
    model.save("models/vaxgym_pilot_best")
    
    obs, info = env.reset()
    trajectory_data = []
    
    for _ in range(500):
        t_pos = env.unwrapped.state_obj.temperature
        amb_temp = env.unwrapped.state_obj.ambient_temp
        
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, term, trunc, info = env.step(action)
        
        trajectory_data.append({
            "step": env.unwrapped.state_obj.step_count,
            "temperature": t_pos,
            "ambient": amb_temp,
            "energy_used": info.get("vaxanalytics_energy_per_dose", 0.0),
            "reward": reward
        })
        
        if term or trunc:
            break
            
    pd.DataFrame(trajectory_data).to_csv("logs/eval_trajectory.csv", index=False)

if __name__ == "__main__":
    main()
