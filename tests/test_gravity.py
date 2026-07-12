import pytest
from physics.physics import get_gravity

@pytest.fixture
def starting_altitude():
    return 0

def test_gravity_at_launch_in_range(starting_altitude):
    assert 10>get_gravity(starting_altitude)>9.7

def test_gravity_at_infinity():
    assert 0.1 > get_gravity(100000000000000) >=0