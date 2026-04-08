"""API and info contract."""

from __future__ import annotations

import numpy as np

from vaxgym.environment import REQUIRED_INFO_KEYS, VaxGymEnv
from vaxgym.models import OBS_DIM

RB_KEYS = frozenset(
    {
        "safe_delivery",
        "breach",
        "expiry_accel",
        "battery_waste",
        "recovery",
        "stabilize",
        "smart_redirect",
        "sync_neglect",
        "terminal_success",
        "terminal_expiry",
        "terminal_spoilage",
        "total",
    }
)


def test_reset_and_info_keys() -> None:
    env = VaxGymEnv()
    obs, info = env.reset(seed=1, scenario="urban_phc_stable")
    assert obs.shape == (OBS_DIM,) and obs.dtype == np.float32
    assert set(info.keys()) == REQUIRED_INFO_KEYS


def test_step_five_tuple_and_info() -> None:
    env = VaxGymEnv()
    env.reset(seed=2, scenario="urban_phc_stable")
    out = env.step(0)
    assert len(out) == 5
    obs, reward, te, tr, info = out
    assert obs.shape == (OBS_DIM,)
    assert isinstance(reward, float)
    assert isinstance(te, bool) and isinstance(tr, bool)
    assert set(info.keys()) == REQUIRED_INFO_KEYS
    assert set(info["reward_breakdown"].keys()) == RB_KEYS


def test_invalid_action_no_crash() -> None:
    env = VaxGymEnv()
    env.reset(seed=0, scenario="urban_phc_stable")
    _, _, _, _, info = env.step(99)
    assert info["action_valid"] is False
    assert set(info.keys()) == REQUIRED_INFO_KEYS


def test_required_info_keys_exported() -> None:
    import vaxgym

    assert vaxgym.REQUIRED_INFO_KEYS == REQUIRED_INFO_KEYS == VaxGymEnv.REQUIRED_INFO_KEYS


def test_state_alias() -> None:
    env = VaxGymEnv()
    env.reset(seed=0, scenario="remote_phc_low_connectivity")
    env.step(4)
    assert env.state() == env.get_state()
    assert "thermochromic_alert_state" in env.state()


def test_render_string() -> None:
    env = VaxGymEnv()
    env.reset(seed=0, scenario="urban_phc_stable")
    txt = env.render(mode="text")
    assert isinstance(txt, str) and "VaxGym" in txt


def test_explain_reward_non_empty_after_step() -> None:
    from vaxgym.reward import explain_reward

    env = VaxGymEnv()
    env.reset(seed=0, scenario="outage_near_expiry_crisis")
    _, _, _, _, info = env.step(int(__import__("vaxgym.enums", fromlist=["VaxAction"]).VaxAction.ACTIVATE_ACTIVE_COOLING))
    ex = explain_reward(info["reward_breakdown"])
    assert isinstance(ex, str) and len(ex) > 0
