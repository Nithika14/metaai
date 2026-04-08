from .models import VaxState
from .enums import ConnectionStatus, ThermochromicState
import numpy as np

def create_scenario(name: str, config, np_random: np.random.Generator) -> VaxState:
    noise_seed = float(np_random.normal(0, 0.01))
    
    if name == "outage_near_expiry_crisis":
        return VaxState(
            temperature=8.5, 
            ambient_temp=35.0,
            battery_level=25.0,
            expiry_time_remaining=15.0, 
            distance_to_destination=25.0, 
            connectivity=ConnectionStatus.OFFLINE,
            thermochromic_state=ThermochromicState.WARNING,
            unsynced_records=5,
            step_count=0,
            breach_count=1,
            true_temperature=8.5,
            sensor_drift=noise_seed,
            previous_cooling_level=0
        )
    elif name == "remote_low_connectivity":
        return VaxState(
            temperature=6.0,
            ambient_temp=30.0,
            battery_level=80.0,
            expiry_time_remaining=config.DEFAULT_EXPIRY_STEPS,
            distance_to_destination=40.0,
            connectivity=ConnectionStatus.OFFLINE,
            thermochromic_state=ThermochromicState.SAFE,
            unsynced_records=10,
            step_count=0,
            breach_count=0,
            true_temperature=6.0,
            sensor_drift=noise_seed,
            previous_cooling_level=0
        )
    else: 
        return VaxState(
            temperature=5.0,
            ambient_temp=25.0,
            battery_level=100.0,
            expiry_time_remaining=config.DEFAULT_EXPIRY_STEPS,
            distance_to_destination=20.0,
            connectivity=ConnectionStatus.ONLINE,
            thermochromic_state=ThermochromicState.SAFE,
            unsynced_records=0,
            step_count=0,
            breach_count=0,
            true_temperature=5.0,
            sensor_drift=noise_seed,
            previous_cooling_level=0
        )
        
def apply_scenario_dynamics(name: str, state: VaxState, config, np_random: np.random.Generator):
    # Process environmental changes (drift + injects)
    if name == "easy_stable_delivery":
        state.ambient_temp += np_random.uniform(-0.5, 0.5)
    elif name == "remote_low_connectivity":
        state.ambient_temp += np_random.uniform(-1.0, 1.0)
        if state.connectivity == ConnectionStatus.OFFLINE and np_random.random() < 0.1:
            state.connectivity = ConnectionStatus.ONLINE
        elif state.connectivity == ConnectionStatus.ONLINE and np_random.random() < 0.2:
            state.connectivity = ConnectionStatus.OFFLINE
    elif name == "outage_near_expiry_crisis":
        state.ambient_temp += np_random.uniform(-0.5, 2.0) 
        if state.connectivity == ConnectionStatus.OFFLINE and np_random.random() < 0.3:
            state.connectivity = ConnectionStatus.ONLINE
            
    state.ambient_temp = max(10.0, min(50.0, state.ambient_temp))
