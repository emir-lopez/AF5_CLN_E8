from datetime import UTC, datetime

from src.security import can_cancel

NOW = datetime(2026, 1, 2, 12, 0, tzinfo=UTC)
RECENT_ORDER = datetime(2026, 1, 2, 11, 0, tzinfo=UTC)
EXACTLY_24_HOURS_OLD = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
OVER_24_HOURS_OLD = datetime(2026, 1, 1, 11, 0, tzinfo=UTC)

def test_owner_within_24h():
    assert can_cancel("NEW", 1, 1, False, RECENT_ORDER, NOW)

def test_third_party_denied():
    assert not can_cancel("NEW", 1, 2, False, RECENT_ORDER, NOW)

def test_shipped_denied_even_admin():
    assert not can_cancel("SHIPPED", 1, 1, True, RECENT_ORDER, NOW)

def test_expired_denied():
    assert not can_cancel("NEW", 1, 1, False, OVER_24_HOURS_OLD, NOW)

def test_admin_can_cancel_another_users_new_order():
    assert can_cancel("NEW", 1, 2, True, RECENT_ORDER, NOW)

def test_owner_cannot_cancel_exactly_at_24_hours():
    assert not can_cancel("NEW", 1, 1, False, EXACTLY_24_HOURS_OLD, NOW)
