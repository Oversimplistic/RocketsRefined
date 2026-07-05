from state import *
from simulationconditions import frequency, standardGravity
from atmosphere import *
from storedflightdata import simulationDataLog
from trajectoryprofile import get_trajectory

simulation_data = simulationDataLog()

#Gravity for simulation
def get_gravity(h):
    gravity = (6.67*10**-11)*(5.9722*10**24)/((6371000+h)**2)
    return gravity

#A function to get thrust via interpolation, this can be improved by a more efficient search, e.g. a modified binary search
def get_thrust(time, rocketParameters, stage_ignition_time):
    time = time - stage_ignition_time
    times = rocketParameters.thrust_time_stamps
    values = rocketParameters.thrust_values

    if time <= times[0]: return values[0]
    if time >= times[-1]: return 0

    #interpolate values
    for i in range(1, len(times)):
        if times[i] > time:
            t1, t2 = times[i-1], times[i]
            y1, y2 = values[i-1], values[i]

            return y1 + (time - t1) * (y2 - y1) / (t2 - t1)

    return 0

#Calculates drag
def get_drag(velocity, altitude, drag_coefficient, drag_area):
    airDensity = get_air_density(altitude)
    drag = 0.5 * airDensity * velocity**2 * drag_coefficient * drag_area
    return drag

def derivatives(t, state, rocketParameters, stage_ignition_time):


    x, y, z, vx, vy, vz, m = state

    vxyz = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)
    thrust = get_thrust(t, rocketParameters, stage_ignition_time)
    gravity = get_gravity(z)
    drag = get_drag(vxyz, z, rocketParameters.drag_coefficient, rocketParameters.drag_area)
    simulation_data.log(t, drag, z, vxyz, thrust, gravity)

    theta = get_trajectory(t, vx, vy, vz)

    #Resolve thrust into components
    thrustX = thrust * math.sin(theta)
    thrustZ = thrust * math.cos(theta)

    #Resolve drag into components
    if vxyz >0:
        Fx_drag = -drag * (vx / vxyz)
        Fz_drag = -drag * (vz / vxyz)
    else:
        Fx_drag, Fz_drag = 0, 0

    Fx, Fy, Fz = thrustX+Fx_drag, 0, thrustZ + Fz_drag - gravity * m

    ax, ay, az = Fx/m, Fy/m, Fz/m
    dx, dy, dz = vx, vy, vz
    dvx, dvy, dvz = ax, ay, az

    #Mass decrease is proportional to thrust and ISP.
    #Cut off of 10N thrust is largely arbitrary but sufficient for our purposes as 10N
    if thrust>1 and m>rocketParameters.dry_mass: dm = -thrust/(rocketParameters.isp * standardGravity)
    else: dm = 0

    return np.array([dx, dy, dz, dvx, dvy, dvz, dm])

def rk4(rocketState, t, dt, rocketParameters, stage_ignition_time):
    state = rocketState

    k1 = derivatives(t, state, rocketParameters, stage_ignition_time)
    k2 = derivatives(t + dt/2, state + dt*k1, rocketParameters, stage_ignition_time)
    k3 = derivatives(t + dt/2, state + dt*k2, rocketParameters, stage_ignition_time)
    k4 = derivatives(t + dt, state + dt*k3, rocketParameters, stage_ignition_time)

    newState = state + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

    return newState





