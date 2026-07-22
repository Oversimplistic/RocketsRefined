from infodisplay import *
from physics.physics import *
from simulation.simulationconditions import frequency
from storedflightdata import FlightDataSummary, FlightLog
from state import *
from configs.trajectoryprofile import coastPeriodDuration

#a test loop to run the code
def simulation(output_as_text, xy_graph, rocketState, current_stage_index, simulation_data):
    """
    Run the full multi-stage rocket flight simulation loop.

    Integrates the rocket's state forward in time by dt using RK$ from launch until return to sea level.
    Handles burnouts, coast periods, staging, etc.
    Tracks key flight statistics (max altitude, max velocity, maxQ, burnout times/altitudes, etc.)
    Outputs a complete text and graphical summary of the flight.

    Args:
        output_as_text (Callable): Function that takes a 'FlightDataSummary' and prints it as text.
        xy_graph (Callable): Function that plots results
        rocketState (np.ndarray): Initial state vector
            [x, y, z, vx, vy, vz, m], where (x, y, z) is position, (vx, vy, vz) is velocity, and m is initial vehicle mass.
        current_stage_index (int): Defined index of current stage.
        simulation_data: Log object for telemetry data

    Returns:
        None. Results are emitted via `output_as_text` and `xy_graph`.
    """
    #simulation time, increases by 1/frequency per tick
    time = 0
    summary = FlightDataSummary()
    flight_log = FlightLog()

    #Time of stage ignition
    stage_ignition_time = 0
    #Time of current stage burnout
    burnout_time_current_stage = None
    #True when in a coast phase
    awaiting_separation = False

    #Runs until liftoff has occurred and the rocket has returned to sea level
    #time<1 ensures at least one tick runs even if starting on the ground.
    while time<1 or rocketState[2]>0:

        x,y,z,vx,vy,vz,m = rocketState

        #Total speed in m/s
        vxyz = math.sqrt(vx**2+vy**2+vz**2)

        #Dynamic pressure (indicator of structural/aerodynamic stress)
        q = 0.5 * get_air_density(z) * vxyz**2

        #Tracks peak altitude
        if z > summary.max_altitude:
            summary.max_altitude = z
            summary.max_altitude_time = time

        #Tracks peak velocity
        velocity = abs(vxyz)
        if velocity > summary.max_velocity:
            summary.max_velocity = velocity
            summary.max_velocity_time = time

        #Tracks MaxQ so far in flight
        if q > summary.max_q:
            summary.max_q = q
            summary.max_q_time = time

        #Current thrust at t
        current_thrust = get_thrust(time,stages[current_stage_index], stage_ignition_time)

        #Detects burnout of the current stage
        if not awaiting_separation and current_thrust <= 1 and burnout_time_current_stage is None:
            burnout_time_current_stage = time
            if summary.burnout_time is None:
                summary.burnout_time = time
                summary.burnout_altitude = z
            if current_stage_index < len(stages)-1:
                awaiting_separation = True
                print(f"Burnout of stage {current_stage_index+1} at t={time:.2f}s, altitude={z:.2f}m, coasting {coastPeriodDuration[current_stage_index]}s before separation")

        #Once the coast period has elapsed, separate and ignite the second stage
        if awaiting_separation and (time-burnout_time_current_stage) >= coastPeriodDuration[current_stage_index]:
            print(f"Staging at t={time:.2f}s, altitude={z:.2f}m")
            rocketState[6] -= stages[current_stage_index].dry_mass
            current_stage_index += 1
            stage_ignition_time = time
            burnout_time_current_stage = None
            awaiting_separation = False

        #Determines the guidance pitch angle
        theta = get_trajectory(time, vx, vy, vz)
        flight_log.log(time, rocketState, theta)

        #Advance the state by one time step using RK4 integration
        rocketState = rk4(rocketState, time, (1/frequency), stages[current_stage_index], stage_ignition_time)

        time+=(1/frequency)

    #Print the summary statistics for the flight
    output_as_text(summary)

    #Calls the graphing function in infodisplay for 2d graphing.
    xy_graph( simulation_data.time,simulation_data.velocity,"Time (s)", "Velocity (m/s)","Velocity vs Time",
              flight_log.time,flight_log.z,"Time (s)", "Altitude (m)","Altitude vs Time",
              flight_log.x,flight_log.z,"X (m)", "Z (m)", "X vs Z",
              simulation_data.time, simulation_data.drag, "Time (s)", "Drag (N)", "Drag vs Time"
              )


