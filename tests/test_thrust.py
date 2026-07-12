import pytest
from physics.physics import get_thrust
from state import stages
from configs.rocketdesignconfig import configuredEngines
from thrustdata import motors
from simulation.simulationconditions import frequency
from state import rocketState

@pytest.fixture
def starting_altitude():
    return 0

@pytest.fixture
def drag_coeff(rocketParameters1):
    return rocketParameters1.drag_coefficient

@pytest.fixture
def drag_area(rocketParameters1):
    return rocketParameters1.drag_area

@pytest.fixture
def rocketSt():
    return rocketState

@pytest.fixture
def dt():
    x = 1/frequency
    return x

def test_thrust_at_burnouts():
    for stage in stages:
        burnout = stage.thrust_time_stamps[-1]
        assert get_thrust(burnout, stage, stages[0].thrust_time_stamps[-1]) == stage.thrust_values[0]

def test_thrust_pre_ignition():
    assert get_thrust(0.0, stages[0], 0) == stages[0].thrust_values[0]

def test_thrust_matches_discrete_data_stage_1():
    for stage, engine in zip(stages, configuredEngines):
        time = motors[engine].thrustTimes[3]
        thrust = motors[engine].thrustValues[3]
        #3 is an arbitrary value in this instance
        assert get_thrust(time, stage, 0) == thrust

