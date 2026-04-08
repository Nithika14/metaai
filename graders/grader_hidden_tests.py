#!/usr/bin/env python3
"""PASS/FAIL: stress harness with long mixed action sequences."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))

from vaxgym.environment import REQUIRED_INFO_KEYS, VaxGymEnv


def main() -> int:
    scenarios = [
        "urban_phc_stable",
        "remote_phc_low_connectivity",
        "outage_near_expiry_crisis",
    ]
    pattern = [0, 1, 2, 3, 4, 5, 6, 7, -1, 999]
    for seed in range(5):
        for sc in scenarios:
            env = VaxGymEnv(seed=seed)
            env.reset(seed=seed, scenario=sc)
            for t in range(120):
                a = pattern[(seed + t) % len(pattern)]
                obs, _, te, tr, info = env.step(a)
                assert obs.shape == (22,)
                assert set(info.keys()) == REQUIRED_INFO_KEYS
                assert isinstance(info["reward_breakdown"], dict)
                if te or tr:
                    break
    print("PASS grader_hidden_tests")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print("FAIL grader_hidden_tests", exc)
        sys.exit(1)
