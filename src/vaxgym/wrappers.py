import gymnasium as gym
import numpy as np

class VaxAnalytics(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        
    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self.temp_history = [self.unwrapped.state_obj.true_temperature]
        self.energy_consumed = 0.0
        self.total_uptime = 0
        return obs, info
        
    def step(self, action):
        prev_batt = self.unwrapped.state_obj.battery_level
        prev_temp = self.unwrapped.state_obj.true_temperature
        
        obs, reward, terminated, truncated, info = self.env.step(action)
        
        curr_batt = self.unwrapped.state_obj.battery_level
        curr_temp = self.unwrapped.state_obj.true_temperature
        
        self.temp_history.append(curr_temp)
        self.total_uptime += 1
        self.energy_consumed += max(0.0, prev_batt - curr_batt)
        
        kelvins = np.array(self.temp_history) + 273.15
        exp_sum = np.sum(np.exp(-10000.0 / kelvins))
        
        if exp_sum > 0:
            avg_exp = exp_sum / len(kelvins)
            mkt_kelvin = -10000.0 / np.log(avg_exp)
            info["vaxanalytics_mkt_stability"] = mkt_kelvin - 273.15
        else:
            info["vaxanalytics_mkt_stability"] = curr_temp
            
        info["vaxanalytics_energy_per_dose"] = self.energy_consumed / max(1, self.total_uptime)
        info["vaxanalytics_thermal_latency"] = abs(curr_temp - prev_temp)

        return obs, reward, terminated, truncated, info
