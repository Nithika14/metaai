#!/usr/bin/env python3
"""PASS/FAIL: observations are finite and within documented envelopes."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))

import numpy as np

from vaxgym.environment import VaxGymEnv


def main() -> int:
    env = VaxGymEnv(seed=0)
    obs, _ = env.reset(seed=0, scenario="outage_near_expiry_crisis")
    assert np.isfinite(obs).all()
    for _ in range(80):
        obs, _, _, _, _ = env.step(0)
        assert np.isfinite(obs).all()
        assert -10.0 <= float(obs[0]) <= 45.0
    print("PASS grader_observation_bounds")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print("FAIL grader_observation_bounds", exc)
        sys.exit(1)
