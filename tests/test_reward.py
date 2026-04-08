"""Reward math."""

from __future__ import annotations

from vaxgym import config as cfg
from vaxgym.reward import compute_step_components, explain_reward, public_reward_breakdown, total_from_breakdown


def test_compute_step_components_total() -> None:
    bd = compute_step_components(
        safe_delivery_event=True,
        breach_this_step=False,
        expiry_accel_units=0.0,
        battery_waste_units=1.0,
        recovery=True,
        stabilize_good=False,
        smart_redirect=True,
        sync_neglect=False,
    )
    t = total_from_breakdown(bd)
    assert t == (
        cfg.R_SAFE_DELIVERY - cfg.R_BATTERY_WASTE_UNIT + cfg.R_RECOVERY_BONUS + cfg.R_REDIRECT_SMART
    )


def test_explain_reward_includes_total_line() -> None:
    pub = public_reward_breakdown(compute_step_components(
        safe_delivery_event=False,
        breach_this_step=True,
        expiry_accel_units=0.0,
        battery_waste_units=0.0,
        recovery=False,
        stabilize_good=False,
        smart_redirect=False,
        sync_neglect=False,
    ))
    text = explain_reward(pub)
    assert "breach" in text.lower() or "−" in text
