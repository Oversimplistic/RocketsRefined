import numpy as np
import math
from dataclasses import dataclass
from thrustdata import motors
from rocketdesignconfig import configuredEngines

motor = motors


#Drag Area numbers
radius = 0.09
dragArea = math.pi * radius**2

#Motor mass -> Stage mass ratio
massRatio = 1.3



@dataclass
class rocketParameters:
    drag_coefficient : float
    drag_area: float
    thrust_time_stamps: list
    thrust_values: list
    isp: float
    dry_mass: float
    wet_mass: float

def build_stage(engine_name):
    m = motor[engine_name]
    return rocketParameters(
        drag_coefficient=0.25,
        drag_area=dragArea,
        thrust_time_stamps=m.thrustTimes,
        thrust_values=m.thrustValues,
        isp=m.ISP,
        dry_mass=m.dryMass*massRatio,
        wet_mass=m.wetMass*massRatio
    )

stages = [build_stage(name) for name in configuredEngines]
current_stage_index = 0

#x, y, z,
#vx, vy, vz,
#mass, theta
rocketState = np.array([0.0, 0.0, 0.0,
               0.0, 0.0, 0.0,
               sum(s.wet_mass for s in stages)])