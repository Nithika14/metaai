"""Import smoke test as if running from repo root (PYTHONPATH=src)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_import_vaxgym_from_project_root_with_pythonpath() -> None:
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    sep = os.pathsep
    src = str(root / "src")
    env["PYTHONPATH"] = f"{src}{sep}{env['PYTHONPATH']}" if env.get("PYTHONPATH") else src
    code = (
        "import vaxgym; "
        "from vaxgym import REQUIRED_INFO_KEYS, VaxGymEnv; "
        "assert vaxgym.__version__; "
        "assert REQUIRED_INFO_KEYS == VaxGymEnv.REQUIRED_INFO_KEYS"
    )
    r = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(root),
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
