"""Lab 6 - Step 5: tests aimed at >90% LINE coverage of parking_application.py
Run:  coverage run -m pytest CodeCoverageTest_parking_application.py
      coverage report -m
"""
import pytest
from test_parking_fee import parking_fee, find_slot, monthly_pass


# ---------- parking_fee ----------
def test_fee_unknown_vehicle():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("bus", 60, False, False)


def test_fee_negative_minutes():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -5, False, False)


def test_fee_free_period_ev_and_lost_ticket():
    # fee=0 branch, EV halving line, lost-ticket line
    assert parking_fee("car", 20, True, True) == 200


def test_fee_partial_hour_rounds_up():
    # 90 min -> 2 hours * 30 = 60 (hours += 1 line executed)
    assert parking_fee("car", 90, False, False) == 60


# ---------- find_slot ----------
def test_slot_full():
    assert find_slot("car", 0, False) == "full"


def test_slot_disabled():
    assert find_slot("car", 5, True) == "ground floor"


def test_slot_truck():
    assert find_slot("truck", 5, False) == "basement"


def test_slot_any_floor():
    assert find_slot("car", 5, False) == "any floor"


# ---------- monthly_pass ----------
def test_pass_bike_resident():
    assert monthly_pass("bike", True) == 400


def test_pass_car_non_resident():
    assert monthly_pass("car", False) == 1500


def test_pass_invalid_vehicle():
    with pytest.raises(ValueError, match="no pass"):
        monthly_pass("truck", False)
