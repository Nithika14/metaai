"""Observation round-trip."""

from __future__ import annotations

import numpy as np

from vaxgym.models import OBS_DIM, VaxObservation


def test_to_array_shape() -> None:
    vo = VaxObservation(
        internal_temp_c=4.0,
        ambient_temp_c=30.0,
        clinic_storage_temp_c=4.2,
        time_remaining_minutes=100,
        batch_expiry_minutes=200,
        battery_percent=70.0,
        backup_power_percent=50.0,
        cooling_system_health=0.9,
        sensor_health=0.88,
        thermochromic_alert_state=0,
        electricity_status=1,
        distance_to_primary_km=10.0,
        distance_to_alternate_km=12.0,
        traffic_index=0.3,
        connectivity_status=0,
        sync_pending=True,
        vaccines_remaining=2,
        breach_count=0,
        delivered=0,
        expired=False,
        step_count=3,
        risk_level_encoded=1.0,
    )
    a = vo.to_array()
    assert a.shape == (OBS_DIM,) and a.dtype == np.float32
