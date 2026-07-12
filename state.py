import numpy as np
import math
from dataclasses import dataclass

from dragcoefficientdatasource import cd_points
from thrustdata import motors
from configs.rocketdesignconfig import configuredEngines, radius, stageStructuralMass


motor = motors


#Drag Area numbers
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

def build_stage(engine_name):
    m = motor[engine_name]
    index = configuredEngines.index(engine_name)
    structuralMass = stageStructuralMass[index]
    return rocketParameters(
        drag_coefficient=cd_points[0],
        drag_area=dragArea,
        thrust_time_stamps=m.thrustTimes,
        thrust_values=m.thrustValues,
        isp=m.ISP,
        dry_mass=m.dryMass + structuralMass,
        wet_mass=m.wetMass + structuralMass,
    )

stages = [build_stage(name) for name in configuredEngines]
current_stage_index = 0

#x, y, z,
#vx, vy, vz,
#mass, theta
rocketState = np.array([0.0, 0.0, 0.0,
               0.0, 0.0, 0.0,
               sum(s.wet_mass for s in stages)])