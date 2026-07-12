import numpy as np
import pytest
from physics.physics import derivatives, rk4
from state import stages, rocketState
from simulation.simulationconditions import frequency

@pytest.fixture
def rocketSt():
    return rocketState

@pytest.fixture
def dt():
    x = 1/frequency
    return x


#Derivative Test
def test_derivative_function(rocketSt):
    result = derivatives(0, rocketSt, stages[0], 0)
    assert result[0] == 0
    assert result[1] == 0
    assert result[2] == 0
    assert result[3] >= 0
    assert result[4] >= 0
    assert result[5] >= 0
    assert result[6] <= sum(stage.wet_mass for stage in stages)

#RK4 Test
def test_rk4(rocketSt, dt):
    newState = rk4(rocketSt, 0, dt, stages[0], 0)
    assert not np.allclose(newState, rocketSt)
    assert newState[5] > rocketSt[5]