import numpy as np
import math
from dataclasses import dataclass
from thrustdata import thrustDataTimeStamp, thrustDataThrustValue, ISP


#Drag Area numbers
radius = 0.25
dragArea = math.pi * radius**2



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
    thrust_time_stamps=thrustDataTimeStamp,
    thrust_values=thrustDataThrustValue,
    isp=ISP,
    dry_mass=10,
    wet_mass=50
)

stage2 = rocketParameters(
    drag_coefficient=0.25,
    drag_area=dragArea,
    thrust_time_stamps=thrustDataTimeStamp,
    thrust_values=thrustDataThrustValue,
    isp=ISP,
    dry_mass=10,
    wet_mass=50
)

stages = [stage1, stage2]
current_stage_index = 0

#x, y, z,
#vx, vy, vz,
#mass, theta
rocketState = np.array([0.0, 0.0, 0.0,
               0.0, 0.0, 0.0,
               stage1.wet_mass+stage2.wet_mass])