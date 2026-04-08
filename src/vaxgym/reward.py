import numpy as np
from typing import Dict, Any

class RewardCalculator:
    def __init__(self, config):
        self.config = config
        
    def calculate(self, prev_state, action, next_state, info: Dict[str, Any]) -> float:
        breakdown = {
            "safe_delivery": 0.0, "breach": 0.0, "expiry_accel": 0.0,
            "battery_waste": 0.0, "recovery": 0.0, "stabilize": 0.0,
            "smart_redirect": 0.0, "sync_neglect": 0.0, "terminal_success": 0.0,
            "terminal_expiry": 0.0, "terminal_spoilage": 0.0, "total": 0.0
        }
        
        t_true = next_state.true_temperature
        
        if self.config.SAFE_TEMP_MIN <= t_true <= self.config.SAFE_TEMP_MAX:
            breakdown["safe_delivery"] += 1.0
            breakdown["stabilize"] += 0.5
        
        if t_true > self.config.SAFE_TEMP_MAX:
            breakdown["breach"] -= 2.0
            if t_true > self.config.CRITICAL_TEMP_HIGH:
                breakdown["breach"] -= 5.0
                
        if t_true < self.config.SAFE_TEMP_MIN:
            breakdown["breach"] -= 2.0
            
        prev_breach = not (self.config.SAFE_TEMP_MIN <= prev_state.true_temperature <= self.config.SAFE_TEMP_MAX)
        curr_safe = (self.config.SAFE_TEMP_MIN <= t_true <= self.config.SAFE_TEMP_MAX)
        if prev_breach and curr_safe:
            breakdown["recovery"] += 5.0
            
        if t_true > self.config.SAFE_TEMP_MAX:
            breakdown["expiry_accel"] -= 1.0
            
        wear_diff = abs(action.cooling_level - prev_state.previous_cooling_level)
        jerk_penalty = wear_diff * self.config.WEAR_PENALTY_WEIGHT
        
        if action.cooling_level > 0 and t_true < self.config.SAFE_TEMP_MIN:
            breakdown["battery_waste"] -= 2.0
        if next_state.battery_level < 10.0:
            breakdown["battery_waste"] -= 5.0
            
        breakdown["battery_waste"] -= jerk_penalty
            
        dist_to_edges = min(t_true - self.config.SAFE_TEMP_MIN, self.config.SAFE_TEMP_MAX - t_true)
        dist_clamped = max(-10.0, min(5.0, dist_to_edges)) 
        margin_penalty = np.exp(-dist_clamped * 2.0) * self.config.EXPONENTIAL_MARGIN_WEIGHT
        breakdown["stabilize"] -= margin_penalty
            
        if next_state.expiry_time_remaining < 10.0 and action.route_decision == 2:
            breakdown["smart_redirect"] += 3.0
        if next_state.connectivity == 1 and next_state.unsynced_records > 5 and action.sync_action == 0:
            breakdown["sync_neglect"] -= 2.0
            
        if info.get("delivery_status") == "delivered":
            if next_state.thermochromic_state != 2: 
                breakdown["terminal_success"] += 50.0
                
        if info.get("expiry_status") == "expired":
            breakdown["terminal_expiry"] -= 50.0
            
        if next_state.thermochromic_state == 2:
            breakdown["terminal_spoilage"] -= 50.0
            
        total = sum(breakdown.values())
        breakdown["total"] = total
        info["reward_breakdown"] = breakdown
        return total
