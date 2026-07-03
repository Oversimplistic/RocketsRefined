from infodisplay import output_as_text, xy_graph
from physics import *
from storedflightdata import FlightDataSummary, FlightLog, simulationDataLog
from state import rocketState

#a test loop to run the code

#simulation time, increases by 1/frequency per tick
time = 0


summary = FlightDataSummary()
flight_log = FlightLog()


while time<1 or rocketState[2]>0:

    x,y,z,vx,vy,vz,m = rocketState

    q = 0.5 * get_air_density(z) * vz**2

    if z > summary.max_altitude:
        summary.max_altitude = z
        summary.max_altitude_time = time

    velocity = abs(math.sqrt((vx**2)+(vy**2)+(vz**2)))

    if velocity > summary.max_velocity:
        summary.max_velocity = velocity
        summary.max_velocity_time = time

    if q > summary.max_q:
        summary.max_q = q
        summary.max_q_time = time

    if summary.burnout_time is None and get_thrust(time,stage1) <= 1:
        summary.burnout_time = time
        summary.burnout_altitude = z

    theta = get_trajectory(time, vx, vy, vz)
    flight_log.log(time, rocketState, theta)
    #print(rocketState)
    rocketState = rk4(rocketState, time, (1/frequency), stage1)

    time+=(1/frequency)

#print(state_history)

output_as_text(summary)

#Calls the graphing function in infodisplay for 2d graphing.
xy_graph( simulation_data.time,simulation_data.velocity,"Time (s)", "Velocity (m/s)","Velocity vs Time",
          flight_log.time,flight_log.z,"Time (s)", "Altitude (m)","Altitude vs Time",
          flight_log.x,flight_log.z,"X (m)", "Z (m)", "X vs Z",
          simulation_data.time, simulation_data.drag, "Time (s)", "Drag (N)", "Drag vs Time"
          )


