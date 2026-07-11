import numpy as np

from atmosphere import get_atmospheric_temperature

#As values obviously vary widely between rockets, these are just illustrative values as a proof of concept
mach_points = np.array([
    0.0,0.2,0.4,0.6,0.7,0.8,0.85,0.9,
    0.95,1.0,1.05,1.1,1.2,1.4,1.6,
    2.0,2.5,3.0
])

cd_points = np.array([
    0.35,0.34,0.33,0.33,0.34,0.37,0.41,
    0.47,0.58,0.72,0.78,0.76,0.68,0.58,
    0.52,0.46,0.42,0.40
])

def get_mach(velocity,z):
    T = get_atmospheric_temperature(z)
    a = np.sqrt(1.4*287.05*T)
    M = velocity/a
    return M

#Currently zero angle of attack as wind is not yet modelled
def get_angle_of_attack():
    return 0

def get_drag_coefficient(velocity, altitude):
    M = get_mach(velocity, altitude)
    return np.interp(M, mach_points, cd_points) + 3*(get_angle_of_attack()**2)
