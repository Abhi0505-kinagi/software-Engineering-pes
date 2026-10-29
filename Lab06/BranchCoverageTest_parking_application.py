"""Lab 6 - Step 7: tests aimed at >90% (here 100%) BRANCH coverage.
Run:  coverage run --branch -m pytest BranchCoverageTest_parking_application.py
      coverage report -m
"""
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ---------- parking_fee: validation ----------
def test_fee_unknown_vehicle():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("bus", 60, False, False)


def test_fee_negative_minutes():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


# ---------- parking_fee: minutes <= 30 (True / False) ----------
def test_fee_zero_minutes_is_free():
    assert parking_fee("car", 0, False, False) == 0


def test_fee_boundary_30_is_free():
    assert parking_fee("car", 30, False, False) == 0


def test_fee_boundary_31_is_charged():
    assert parking_fee("car", 31, False, False) == 30


# ---------- minutes % 60 != 0 (True / False) ----------
def test_fee_exact_hours_no_round_up():
    # 120 % 60 == 0 -> skip 'hours += 1'
    assert parking_fee("car", 120, False, False) == 60


def test_fee_partial_hour_rounds_up():
    assert parking_fee("car", 90, False, False) == 60


@pytest.mark.parametrize("vehicle,minutes,expected", [
    ("bike", 60, 10), ("car", 60, 30), ("truck", 60, 60),
    ("bike", 61, 20), ("truck", 125, 180),
])
def test_fee_rates_per_vehicle(vehicle, minutes, expected):
    assert parking_fee(vehicle, minutes, False, False) == expected


# ---------- is_ev and vehicle != "truck" (True / False) ----------
def test_fee_ev_car_gets_half():
    assert parking_fee("car", 120, True, False) == 30


def test_fee_ev_bike_gets_half():
    assert parking_fee("bike", 120, True, False) == 10


def test_fee_ev_truck_no_discount():
    assert parking_fee("truck", 60, True, False) == 60


def test_fee_non_ev_no_discount():
    assert parking_fee("car", 60, False, False) == 30


def test_fee_ev_odd_fee_floor_division():
    # bike 31 min -> 1h = 10 -> 10//2 = 5
    assert parking_fee("bike", 31, True, False) == 5


# ---------- lost_ticket (True / False) ----------
def test_fee_lost_ticket_adds_200():
    assert parking_fee("car", 60, False, True) == 230


def test_fee_lost_ticket_with_free_period():
    assert parking_fee("bike", 10, False, True) == 200


def test_fee_ev_discount_applied_before_penalty():
    # (120 min car = 60) -> EV 30 -> +200
    assert parking_fee("car", 120, True, True) == 230


# ---------- find_slot ----------
def test_slot_full_zero():
    assert find_slot("car", 0, False) == "full"


def test_slot_full_negative():
    assert find_slot("car", -3, True) == "full"


def test_slot_one_free_is_not_full():
    assert find_slot("car", 1, False) == "any floor"


def test_slot_disabled():
    assert find_slot("car", 5, True) == "ground floor"


def test_slot_disabled_truck_priority():
    # disabled check comes before truck check
    assert find_slot("truck", 5, True) == "ground floor"


def test_slot_truck():
    assert find_slot("truck", 5, False) == "basement"


def test_slot_bike_any_floor():
    assert find_slot("bike", 5, False) == "any floor"


# ---------- monthly_pass ----------
def test_pass_bike_non_resident():
    assert monthly_pass("bike", False) == 500


def test_pass_bike_resident():
    assert monthly_pass("bike", True) == 400


def test_pass_car_non_resident():
    assert monthly_pass("car", False) == 1500


def test_pass_car_resident():
    assert monthly_pass("car", True) == 1200


def test_pass_truck_invalid():
    with pytest.raises(ValueError, match="no pass"):
        monthly_pass("truck", False)


def test_pass_unknown_invalid():
    with pytest.raises(ValueError):
        monthly_pass("bus", True)
