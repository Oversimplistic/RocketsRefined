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

stage1 = rocketParameters(
    drag_coefficient=0.75,
    drag_area=dragArea,
    thrust_time_stamps=thrustDataTimeStamp,
    thrust_values=thrustDataThrustValue,
    isp=ISP,
    dry_mass=50
)

#x, y, z,
#vx, vy, vz,
#mass
rocketState = np.array([0.0, 0.0, 0.0,
               0.0, 0.0, 0.0,
               stage1.dry_mass])