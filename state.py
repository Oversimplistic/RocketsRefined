import numpy as np
import math

#mass value of stage
mass1 = 50

#x, y, z,
#vx, vy, vz,
#mass
rocketState = np.array([0.0, 0.0, 0.0,
               0.0, 0.0, 0.0,
               mass1])

#simulation time, increases by 1/frequency per tick
time = 0

#Drag numbers
dragCoefficient = 0.75
radius = 0.25
dragArea = math.pi * radius**2

#Gravity for simulation, currently held as constant
def get_gravity(h):
    gravity = (6.67*10**-11)*(5.9722*10**24)/((6371000+h)**2)
    return gravity