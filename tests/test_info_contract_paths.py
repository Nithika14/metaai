"""info dict must expose REQUIRED_INFO_KEYS on every code path (terminal, truncation, etc.)."""

from __future__ import annotations

import pytest

import vaxgym.config as vcfg
from vaxgym.environment import REQUIRED_INFO_KEYS, VaxGymEnv
from vaxgym.enums import VaxAction


def test_info_keys_when_truncated(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(vcfg, "MAX_EPISODE_STEPS", 3)
    env = VaxGymEnv(seed=0)
    env.reset(seed=0, scenario="urban_phc_stable")
    truncated = False
    for _ in range(4):
        _, _, te, tr, info = env.step(int(VaxAction.WAIT_AND_STABILIZE))
        assert set(info.keys()) == REQUIRED_INFO_KEYS
        if tr:
            truncated = True
            break
        if te:
            pytest.fail("unexpected early termination in truncation probe")
    assert truncated


def test_info_keys_when_terminated_spoilage(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(vcfg, "CATASTROPHIC_SPOILAGE_TEMP_C", 7.05)
    env = VaxGymEnv(seed=0)
    env.reset(seed=0, scenario="outage_near_expiry_crisis")
    terminated = False
    for _ in range(40):
        _, _, te, _, info = env.step(int(VaxAction.CONTINUE_PRIMARY_DELIVERY))
        assert set(info.keys()) == REQUIRED_INFO_KEYS
        if te:
            terminated = True
            assert info["delivery_status"] == "failed_spoilage_temp"
            break
    assert terminated


def test_reset_info_matches_contract() -> None:
    for name in ("urban_phc_stable", "remote_phc_low_connectivity", "outage_near_expiry_crisis"):
        env = VaxGymEnv()
        _, info = env.reset(seed=1, scenario=name)
        assert set(info.keys()) == REQUIRED_INFO_KEYS
