import numpy as np
import math
from dataclasses import dataclass
from thrustdata import motors

motor = motors


#Drag Area numbers
radius = 0.18
dragArea = math.pi * radius**2

#Motor mass -> Stage mass ratio
massRatio = 1.3


#Rocket Design Factors
engine1 = "Cesaroni 40960O8000-P"
engine2 = "O5500X-PS"


@dataclass
class rocketParameters:
    drag_coefficient : float
    drag_area: float
    thrust_time_stamps: list
    thrust_values: list
    isp: float
    dry_mass: float
    wet_mass: float

stage1 = rocketParameters(
    drag_coefficient=0.25,
    drag_area=dragArea,
    thrust_time_stamps=motor[engine1].thrustTimes,
    thrust_values=motor[engine1].thrustValues,
    isp=motor[engine1].ISP,
    dry_mass=motor[engine1].dryMass*massRatio,
    wet_mass=motor[engine1].wetMass*massRatio
)

stage2 = rocketParameters(
    drag_coefficient=0.25,
    drag_area=dragArea,
    thrust_time_stamps=motor[engine2].thrustTimes,
    thrust_values=motor[engine2].thrustValues,
    isp=motor[engine2].ISP,
    dry_mass=motor[engine2].dryMass*massRatio,
    wet_mass=motor[engine2].wetMass*massRatio
)

stages = [stage1, stage2]
current_stage_index = 0

#x, y, z,
#vx, vy, vz,
#mass, theta
rocketState = np.array([0.0, 0.0, 0.0,
               0.0, 0.0, 0.0,
               stage1.wet_mass+stage2.wet_mass])