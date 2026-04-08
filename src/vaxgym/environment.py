import gymnasium as gym
from gymnasium import spaces
import numpy as np
from .config import EnvConfig
from .models import VaxState, VaxAction
from .enums import ThermochromicState, ConnectionStatus
from .reward import RewardCalculator
from .scenarios import create_scenario, apply_scenario_dynamics

class VaxGymEnv(gym.Env):
    metadata = {"render_modes": ["text"]}
    
    def __init__(self):
        super().__init__()
        self.config = EnvConfig()
        self.reward_calculator = RewardCalculator(self.config)
        self.current_scenario = "easy_stable_delivery"
        self.state_obj = None
        self.action_space = spaces.MultiDiscrete([4, 3, 2])
        low_obs = np.array([-20.0, -20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=np.float32)
        high_obs = np.array([100.0, 100.0, 100.0, 1000.0, 1000.0, 1.0, 2.0, 1000.0, 10000.0], dtype=np.float32)
        self.observation_space = spaces.Box(low=low_obs, high=high_obs, dtype=np.float32)
        
    def reset(self, seed=None, scenario=None):
        super().reset(seed=seed)
        self.current_scenario = scenario if scenario is not None else "easy_stable_delivery"
        self.state_obj = create_scenario(self.current_scenario, self.config, self.np_random)
        info = self._get_info()
        info["reward_breakdown"] = {k: 0.0 for k in [
            "safe_delivery", "breach", "expiry_accel", "battery_waste", 
            "recovery", "stabilize", "smart_redirect", "sync_neglect", 
            "terminal_success", "terminal_expiry", "terminal_spoilage", "total"
        ]}
        return self._get_obs(), info
        
    def step(self, action):
        cooling_level = max(0, min(3, int(action[0])))
        route_decision = max(0, min(2, int(action[1])))
        sync_action = max(0, min(1, int(action[2])))

        vax_action = VaxAction(cooling_level=cooling_level, route_decision=route_decision, sync_action=sync_action)
        prev_state = VaxState(**self.state_obj.__dict__)
        
        self.state_obj.step_count += 1
        self.state_obj.unsynced_records += 1
        apply_scenario_dynamics(self.current_scenario, self.state_obj, self.config, self.np_random)
        
        delta_t_ambient = self.state_obj.ambient_temp - self.state_obj.true_temperature
        cop = max(0.2, 1.0 - (abs(delta_t_ambient) / 50.0))
        cooling_effect = self.config.COOLING_POWER[vax_action.cooling_level] * cop
        dT_dt = (self.config.THERMAL_CONDUCTIVITY_K * delta_t_ambient) + cooling_effect + self.config.PASSIVE_HEAT_Q
        self.state_obj.true_temperature += dT_dt
        
        self.state_obj.sensor_drift += float(self.np_random.normal(0.0, 0.001))
        sensor_noise = float(self.np_random.normal(0.0, 0.01))
        self.state_obj.temperature = self.state_obj.true_temperature + self.state_obj.sensor_drift + sensor_noise
        self.state_obj.previous_cooling_level = vax_action.cooling_level
        
        drain = self.config.BATTERY_DRAIN_BASE + self.config.BATTERY_DRAIN_COOLING[vax_action.cooling_level]
        if vax_action.sync_action == 1 and self.state_obj.connectivity == ConnectionStatus.ONLINE:
            drain += self.config.BATTERY_DRAIN_SYNC
            self.state_obj.unsynced_records = 0
            
        self.state_obj.battery_level = max(0.0, self.state_obj.battery_level - drain)
        if self.state_obj.battery_level == 0.0:
            vax_action.cooling_level = 0 
            
        dist_change = 1.0 
        if vax_action.route_decision == 2:
            dist_change = 2.0 
        self.state_obj.distance_to_destination = max(0.0, self.state_obj.distance_to_destination - dist_change)
        
        expiry_decrement = 1.0
        if self.state_obj.true_temperature > self.config.SAFE_TEMP_MAX:
            expiry_decrement *= self.config.EXPIRY_ACCEL_FACTOR
            self.state_obj.breach_count += 1
            if self.state_obj.true_temperature > self.config.CRITICAL_TEMP_HIGH:
                self.state_obj.thermochromic_state = ThermochromicState.BREACH
            else:
                self.state_obj.thermochromic_state = ThermochromicState.WARNING
        elif self.state_obj.true_temperature < self.config.SAFE_TEMP_MIN:
            self.state_obj.breach_count += 1

        self.state_obj.expiry_time_remaining = max(0.0, self.state_obj.expiry_time_remaining - expiry_decrement)
        
        info = self._get_info()
        terminated = False
        truncated = False
        
        if self.state_obj.distance_to_destination <= 0:
            terminated = True
            info["delivery_status"] = "delivered"
        elif self.state_obj.expiry_time_remaining <= 0:
            terminated = True
            info["expiry_status"] = "expired"
        elif self.state_obj.thermochromic_state == ThermochromicState.BREACH:
            terminated = True
            info["expiry_status"] = "spoiled"
            
        if self.state_obj.step_count >= 200:
            truncated = True
            
        if "delivery_status" not in info: info["delivery_status"] = "en_route"
        if "expiry_status" not in info: info["expiry_status"] = "valid"
            
        reward = self.reward_calculator.calculate(prev_state, vax_action, self.state_obj, info)
        return self._get_obs(), reward, terminated, truncated, info
        
    def _get_obs(self):
        return self.state_obj.to_array()
        
    def _get_info(self):
        return {
            "temp_breach_detected": self.state_obj.true_temperature > self.config.SAFE_TEMP_MAX or self.state_obj.true_temperature < self.config.SAFE_TEMP_MIN,
            "action_valid": True,
            "route_selected": "default", 
            "risk_level": "high" if self.state_obj.thermochromic_state != ThermochromicState.SAFE else "low",
            "scenario_name": self.current_scenario,
            "breach_count": self.state_obj.breach_count,
            "step_count": self.state_obj.step_count,
            "thermochromic_alert_state": self.state_obj.thermochromic_state.name,
            "sync_pending": self.state_obj.unsynced_records > 0
        }
        
    def render(self, mode="text"):
        if mode == "text":
            return f"--- VaxGym Step {self.state_obj.step_count} [{self.current_scenario}] ---\nTemp: {self.state_obj.temperature:.2f}C\nBattery: {self.state_obj.battery_level:.1f}%\nDist To Dest: {self.state_obj.distance_to_destination:.1f}"
            
    def state(self): return self.state_obj
    def get_state(self): return self.state()
    
    def action_space_summary(self):
        return "MultiDiscrete space [cooling_level(0-3), route_decision(0-2), sync_action(0-1)]."
        
    def observation_space_summary(self):
        return "Continuous box vector containing true_temp, ambient_temp, battery, expiry, distance, connectivity, thermochromic, unsynced_records, step_count."
