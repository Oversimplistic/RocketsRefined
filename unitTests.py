from dataclasses import dataclass

import pytest
from thrustdata import motors
from physics import get_thrust
from state import rocketParameters, stage1, stage2
from state import engine1, engine2


@pytest.fixture
def rocketParameters1():
    return stage1

@pytest.fixture
def rocketParameters2():
    return stage2

@pytest.fixture
def stage1_burnout__time():
    x = len(stage1.thrust_time_stamps)
    return stage1.thrust_time_stamps[x-1]

@pytest.fixture
def stage2_burnout__time(stage1_burnout__time):
    x = len(stage2.thrust_time_stamps)
    return (stage2.thrust_time_stamps[x-1]) + stage1_burnout__time

@pytest.fixture
def stage2_ignition_time(stage1_burnout__time):
    return stage1_burnout__time

@pytest.fixture
def stage_1_engine():
    return engine1

@pytest.fixture
def stage_2_engine():
    return engine2



#Thrust Tests
def test_thrust_pre_ignition(rocketParameters1):
    assert get_thrust(0.0, rocketParameters1, 0) == stage1.thrust_values[0]

def test_thrust_at_burnout_stage_1(stage1_burnout__time):
    assert get_thrust(stage1_burnout__time, stage1, 0) == 0

def test_thrust_at_burnout_stage_2(stage2_burnout__time, stage2_ignition_time):
    assert get_thrust(stage2_burnout__time, stage2, stage2_ignition_time) == 0

def test_thrust_matches_discrete_data_stage_1():
    motor = motors
    time, thrust = motor[engine1].thrustTimes[3], motor[engine1].thrustValues[3]
    assert get_thrust(time, stage1, 0) == thrust

def test_thrust_matches_discrete_data_stage_2(stage2_ignition_time):
    motor = motors
    time, thrust = motor[engine2].thrustTimes[3], motor[engine2].thrustValues[3]
    assert get_thrust(time+stage2_ignition_time, stage2, stage2_ignition_time) == thrust
