from state import *
from simulation.simulationconditions import standardGravity
from atmosphere import *
from storedflightdata import simulationDataLog
from configs.trajectoryprofile import get_trajectory
from dragcoefficientdatasource import get_drag_coefficient


#Calls the central log for storing of telemetry data at each step of integration
simulation_data = simulationDataLog()


def get_gravity(h):
    """
    Calculates local gravitational acceleration using Newtonian mechanics

    Args:
        h (float): height from sea level in metres

    Returns:
        float: Gravitational acceleration in m/s^2
    """

    #G * M_Earth / (R_Earth + h)^2
    gravity = (6.67*10**-11)*(5.9722*10**24)/((6371000+h)**2)
    return gravity

#A function to get thrust via interpolation, this can be improved by a more efficient search, e.g. a modified binary search
def get_thrust(time, rocketParameters, stage_ignition_time):
    """
    Gets the thrust at a given time using linear interpolation of a predefined thrust curve (time stamps vs thrust values)

    Note: This performs a linear search through thrust values, for higher resolution data a more efficient algorithm would be preferable

    Args:
        time (float): Elapsed mission time
        rocketParameters: Object containing thrust values
        stage_ignition_time (float): Ignition time of the current stage in seconds. Used to convert mission time to stage-relative time
    """
    #Converts mission time to relative-stage time
    time = time - stage_ignition_time
    times = rocketParameters.thrust_time_stamps
    values = rocketParameters.thrust_values

    #Before the curve begins, use the first value
    if time <= times[0]: return values[0]
    #Thrust becomes zero at the end of the curve, allows for incomplete thrust curves to be used in models
    if time >= times[-1]: return 0

    #interpolate values between the two nearest defined time stamps
    for i in range(1, len(times)):
        if times[i] > time:
            t1, t2 = times[i-1], times[i]
            y1, y2 = values[i-1], values[i]

            return y1 + (time - t1) * (y2 - y1) / (t2 - t1)

    return 0


def get_drag(velocity, altitude, drag_coefficient, drag_area):
    """
    Calculates the aerodynamic force magnitude using the standard drag equation.

    Args:
        velocity (float): Speed in m/s
        altitude (float): Altitude in metres above sea level (used to determine local air density)
        drag_coefficient (float): Dimensionless drag coefficient
        drag_area (float): Reference area of drag in metres square

    Returns:
        float: Drag force magnitude, in Newtons.
    """
    #Calculates drag
    airDensity = get_air_density(altitude)
    drag = 0.5 * airDensity * velocity**2 * drag_coefficient * drag_area
    return drag

def derivatives(t, state, rocketParameters, stage_ignition_time):
    """
    Computes the time-derivatives of the rocket's state vector at time t.

    This function forms the basis of the RK4 integrator. It accounts for thrust, gravity, aerodynamic drag, and propellant mass consumption.

    Args:
        t (float): Current elapsed mission time in seconds
        state (np.array): Current state vector
            [x, y, z, vx, vy, vz, m], where (x, y, z) is position, (vx, vy, vz) is velocity, and m is current vehicle mass.
        rocketParameters: Object containing vehicle properties (drag area, dry mass, ISP, thrust curve, etc.) 'drag_coefficient' is updated on this object each call.
        stage_ignition_time (float): Ignition time of the current stage in seconds.

    Returns:
        np.array: Time-derivatives of the rocket's state vector at time t.
            [dx, dy, dz, dvx, dvy, dvz, dm]
    """

    x, y, z, vx, vy, vz, m = state

    #Total speed (magnitude of velocity vector)
    vxyz = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)

    #Values of forces acting on the rocket at this instant
    thrust = get_thrust(t, rocketParameters, stage_ignition_time)
    gravity = get_gravity(z)
    rocketParameters.drag_coefficient = get_drag_coefficient(vxyz, z)
    drag = get_drag(vxyz, z, rocketParameters.drag_coefficient, rocketParameters.drag_area)

    #Recirds telemetry for this step
    simulation_data.log(t, drag, z, vxyz, thrust, gravity)

    #Desired pitch angle
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

    #Sum forces along each axis
    Fx, Fy, Fz = thrustX+Fx_drag, 0, thrustZ + Fz_drag - gravity * m

    #Newton's second law, a = F/m
    ax, ay, az = Fx/m, Fy/m, Fz/m

    #Velocity is the derivative of position
    dx, dy, dz = vx, vy, vz

    #Acceleration is the derivative of velocity
    dvx, dvy, dvz = ax, ay, az

    #Mass decrease is proportional to thrust and ISP.
    #Cut off of 1N thrust is largely arbitrary but sufficient for our purposes as 1N
    if thrust>1 and m>rocketParameters.dry_mass: dm = -thrust/(rocketParameters.isp * standardGravity)
    else: dm = 0

    return np.array([dx, dy, dz, dvx, dvy, dvz, dm])

def rk4(rocketState, t, dt, rocketParameters, stage_ignition_time):
    """
    Advances the rocket's state by one time-step using the 4th-order Runge-Kutta (RK4) numerical integration method

    Args:
        rocketState (np.array): Rocket's state vector at time t.
            [x, y, z, vx, vy, vz, m]
        t (float): Current elapsed mission time in seconds.
        dt (float): Time step in seconds.
        rocketParameters: Object containing vehicle properties, passed to the derivatives function
        stage_ignition_time (float): Ignition time of the current stage in seconds.

    Returns:
        np.array: Updated state vector after advancing by dt
    """
    state = rocketState

    #Samples the derivative across four points, obtaining higher-order accuracy than simple Euler integration
    k1 = derivatives(t, state, rocketParameters, stage_ignition_time)
    k2 = derivatives(t + dt/2, state + (dt/2)*k1, rocketParameters, stage_ignition_time)
    k3 = derivatives(t + dt/2, state + (dt/2)*k2, rocketParameters, stage_ignition_time)
    k4 = derivatives(t + dt, state + dt*k3, rocketParameters, stage_ignition_time)

    newState = state + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

    return newState





