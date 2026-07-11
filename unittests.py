from dataclasses import dataclass

import numpy as np
import pytest
from thrustdata import motors
from physics import get_thrust, get_gravity, get_drag, derivatives, rk4
from state import stages
from state import rocketState
from simulationconditions import frequency
from rocketdesignconfig import configuredEngines


@pytest.fixture
def rocketParameters1():
    return stages[0]

@pytest.fixture
def rocketParameters2():
    return stages[1]

@pytest.fixture
def stage1_burnout__time():
    return stages[0].thrust_time_stamps[-1]

@pytest.fixture
def stage2_burnout__time(stage1_burnout__time):
    return (stages[1].thrust_time_stamps[-1]) + stage1_burnout__time

@pytest.fixture
def stage2_ignition_time(stage1_burnout__time):
    return stage1_burnout__time

@pytest.fixture
def stage_1_engine():
    return configuredEngines[0]

@pytest.fixture
def stage_2_engine():
    return configuredEngines[1]

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

#Thrust Tests
def test_thrust_pre_ignition(rocketParameters1):
    assert get_thrust(0.0, rocketParameters1, 0) == stages[0].thrust_values[0]

def test_thrust_at_burnout_stage_1(stage1_burnout__time):
    assert get_thrust(stage1_burnout__time, stages[0], 0) == 0

def test_thrust_at_burnout_stage_2(stage2_burnout__time, stage2_ignition_time):
    assert get_thrust(stage2_burnout__time, stages[1], stage2_ignition_time) == 0

def test_thrust_matches_discrete_data_stage_1():
    motor = motors
    time, thrust = motor[configuredEngines[0]].thrustTimes[3], motor[configuredEngines[0]].thrustValues[3]
    assert get_thrust(time, stages[0], 0) == thrust

def test_thrust_matches_discrete_data_stage_2(stage2_ignition_time):
    motor = motors
    time, thrust = motor[configuredEngines[1]].thrustTimes[3], motor[configuredEngines[1]].thrustValues[3]
    assert get_thrust(time+stage2_ignition_time, stages[1], stage2_ignition_time) == thrust

#Gravity Tests
def test_gravity_at_launch_in_range(starting_altitude):
    assert 10>get_gravity(starting_altitude)>9.7

def test_gravity_at_infinity():
    assert 0.1 > get_gravity(100000000000000) >=0

#Drag Tests
def test_stationary_drag(drag_coeff, drag_area):
    assert get_drag(0, 0, drag_coeff, drag_area) == 0

def test_stationary_drag_at_altitude(drag_coeff, drag_area):
    assert get_drag(0, 1000, drag_coeff, drag_area) == 0

def test_moving_drag(drag_coeff, drag_area):
    assert get_drag(10, 0, drag_coeff, drag_area) > 0

#Derivative Test
def test_derivative_function(rocketSt, rocketParameters1):
    result = derivatives(0, rocketSt, rocketParameters1, 0)
    assert result[0] == 0
    assert result[1] == 0
    assert result[2] == 0
    assert result[3] >= 0
    assert result[4] >= 0
    assert result[5] >= 0
    assert result[6] <= stages[0].wet_mass+stages[1].wet_mass

#RK4 Test
def test_rk4(rocketSt, dt):
    newState = rk4(rocketSt, 0, dt, stages[0], 0)
    assert not np.allclose(newState, rocketSt)
    assert newState[5] > rocketSt[5]