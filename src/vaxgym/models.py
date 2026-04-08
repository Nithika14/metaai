from dataclasses import dataclass
from typing import Dict, Any
from .enums import ThermochromicState, ConnectionStatus
import numpy as np

@dataclass
class VaxState:
    temperature: float 
    ambient_temp: float
    battery_level: float
    expiry_time_remaining: float
    distance_to_destination: float
    connectivity: ConnectionStatus
    thermochromic_state: ThermochromicState
    unsynced_records: int
    step_count: int
    breach_count: int
    
    true_temperature: float = 5.0
    sensor_drift: float = 0.0
    previous_cooling_level: int = 0
    
    def to_array(self) -> np.ndarray:
        return np.array([
            self.temperature, 
            self.ambient_temp,
            self.battery_level,
            self.expiry_time_remaining,
            self.distance_to_destination,
            float(self.connectivity),
            float(self.thermochromic_state),
            float(self.unsynced_records),
            float(self.step_count)
        ], dtype=np.float32)

@dataclass
class VaxAction:
    cooling_level: int
    route_decision: int
    sync_action: int
