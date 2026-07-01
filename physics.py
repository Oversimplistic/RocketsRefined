from state import *
from simulationconditions import frequency
import math
from thrustdata import thrustDataTimeStamp, thrustDataThrustValue, ISP
from atmosphere import *

#A function to get thrust via interpolation, this can be improved by a more efficient search, e.g. a modified binary search
def get_thrust(time):
    times = thrustDataTimeStamp
    values = thrustDataThrustValue

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
def get_drag(velocity):
    z = rocketState[2]
    airDensity = get_air_density2(z)
    drag = 0.5 * airDensity * velocity**2 * dragCoefficient * dragArea
    return math.copysign(drag, velocity)

def derivatives(t, state):
    x,y,z,vx,vy,vz,m = state

    thrust = get_thrust(t)

    #Temporarily just has thrust on z angle
    gravity = get_gravity(z)
    Fx, Fy, Fz = 0, 0, thrust-get_drag(vz)-gravity*m

    ax, ay, az = Fx/m, Fy/m, Fz/m

    dx, dy, dz = vx, vy, vz

    dvx, dvy, dvz = ax, ay, az

    #Mass decrease is proportional to thrust and ISP.
    #Cut off of 10N thrust is largely arbitrary but sufficient for our purposes as 10N
    if thrust>1: dm = -thrust/(ISP*gravity)
    else: dm = 0

    return np.array([dx, dy, dz, dvx, dvy, dvz, dm])

def rk4(rocketState, t, dt):
    state = rocketState

    k1 = derivatives(t, state)
    k2 = derivatives(t + dt/2, state + dt*k1)
    k3 = derivatives(t + dt/2, state + dt*k2)
    k4 = derivatives(t + dt, state + dt*k3)

    newState = state + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

    return newState

#a test loop to run the code

while time<1 or rocketState[2]>0:
    print(rocketState)
    rocketState = rk4(rocketState, time, (1/frequency))

    time+=(1/frequency)

