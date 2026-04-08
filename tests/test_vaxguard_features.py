"""VaxGuard-aligned dynamics: thermochromic, battery cooling, sync, breach >8°C."""

from __future__ import annotations

from vaxgym.environment import REQUIRED_INFO_KEYS, VaxGymEnv
from vaxgym.enums import ConnectivityStatus, VaxAction
from vaxgym.models import thermochromic_from_temp


def test_thermochromic_red_strictly_above_8c() -> None:
    """Indicator stays non-red on the 8.0 °C boundary; flips to red above the band."""
    assert thermochromic_from_temp(8.0) != 2
    assert thermochromic_from_temp(8.0 + 1e-6) == 2
    assert thermochromic_from_temp(5.0) == 0


def test_active_cooling_drains_battery() -> None:
    env = VaxGymEnv(seed=0)
    env.reset(seed=0, scenario="urban_phc_stable")
    b0 = env.state()["battery_percent"]
    env.step(int(VaxAction.ACTIVATE_ACTIVE_COOLING))
    b1 = env.state()["battery_percent"]
    assert b1 < b0


def test_active_cooling_reduces_temperature_vs_power_saver_baseline() -> None:
    """Cooling boost lowers thermal pull relative to a no-boost step (power saver worsens pull)."""
    cool = VaxGymEnv(seed=0)
    cool.reset(seed=0, scenario="urban_phc_stable")
    saver = VaxGymEnv(seed=0)
    saver.reset(seed=0, scenario="urban_phc_stable")
    assert cool.state()["internal_temp_c"] == saver.state()["internal_temp_c"]
    cool.step(int(VaxAction.ACTIVATE_ACTIVE_COOLING))
    saver.step(int(VaxAction.ENABLE_POWER_SAVER_MODE))
    assert cool.state()["internal_temp_c"] < saver.state()["internal_temp_c"]


def test_sync_pending_clears_when_online_sync() -> None:
    env = VaxGymEnv(seed=0)
    env.reset(seed=0, scenario="urban_phc_stable")
    st = env.state()
    st["connectivity_status"] = int(ConnectivityStatus.ONLINE)
    # scenario urban starts sync_pending False — use monkeypatch on internal state
    env._state.sync_pending = True  # type: ignore[attr-defined]
    env._state.connectivity_status = int(ConnectivityStatus.ONLINE)  # type: ignore[attr-defined]
    env.step(int(VaxAction.SYNC_LOGS_WHEN_CONNECTED))
    assert env.state()["sync_pending"] is False
    _, _, _, _, info = env.step(int(VaxAction.CONTINUE_PRIMARY_DELIVERY))
    assert set(info.keys()) == REQUIRED_INFO_KEYS


def test_sync_stays_pending_offline() -> None:
    env = VaxGymEnv(seed=0)
    env.reset(seed=0, scenario="remote_phc_low_connectivity")
    assert env.state()["connectivity_status"] == int(ConnectivityStatus.OFFLINE)
    assert env.state()["sync_pending"] is True
    env.step(int(VaxAction.SYNC_LOGS_WHEN_CONNECTED))
    assert env.state()["sync_pending"] is True


def test_sync_neglect_when_online_and_pending_without_sync_action() -> None:
    env = VaxGymEnv(seed=0)
    env.reset(seed=0, scenario="urban_phc_stable")
    env._state.sync_pending = True  # type: ignore[attr-defined]
    env._state.connectivity_status = int(ConnectivityStatus.ONLINE)  # type: ignore[attr-defined]
    _, _, _, _, info = env.step(int(VaxAction.CONTINUE_PRIMARY_DELIVERY))
    assert info["sync_pending"] is True
    assert info["reward_breakdown"]["sync_neglect"] < 0.0
    assert set(info.keys()) == REQUIRED_INFO_KEYS


def test_thermochromic_in_info_matches_internal() -> None:
    env = VaxGymEnv(seed=0)
    env.reset(seed=0, scenario="urban_phc_stable")
    _, _, _, _, info = env.step(int(VaxAction.CONTINUE_PRIMARY_DELIVERY))
    st = env.state()["internal_temp_c"]
    assert info["thermochromic_alert_state"] == thermochromic_from_temp(float(st))
