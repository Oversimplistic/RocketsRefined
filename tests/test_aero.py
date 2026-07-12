import pytest
from physics.physics import get_drag
from state import stages


@pytest.fixture
def drag_coeff():
    return stages[0].drag_coefficient

@pytest.fixture
def drag_area():
    return stages[0].drag_area

def test_stationary_drag(drag_coeff, drag_area):
    assert get_drag(0, 0, drag_coeff, drag_area) == 0

def test_stationary_drag_at_altitude(drag_coeff, drag_area):
    assert get_drag(0, 1000, drag_coeff, drag_area) == 0

def test_moving_drag(drag_coeff, drag_area):
    assert get_drag(10, 0, drag_coeff, drag_area) > 0