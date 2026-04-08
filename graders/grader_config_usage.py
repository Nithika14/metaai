#!/usr/bin/env python3
"""PASS/FAIL: critical thresholds live in config, not literals in transitions."""

from __future__ import annotations

import inspect
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "src"))

import vaxgym.config as cfg
import vaxgym.environment as environment


def main() -> int:
    src = inspect.getsource(environment)
    assert "cfg.CATASTROPHIC_SPOILAGE_TEMP_C" in src
    assert "cfg.SAFE_TEMP_MIN_C" in src and "cfg.SAFE_TEMP_MAX_C" in src
    assert hasattr(cfg, "SAFE_TEMP_MIN_C") and hasattr(cfg, "MAX_EPISODE_STEPS")
    print("PASS grader_config_usage")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print("FAIL grader_config_usage", exc)
        sys.exit(1)
