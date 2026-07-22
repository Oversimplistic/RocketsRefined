from dataclasses import dataclass
import math

@dataclass
class trajectory:
    """
    Defines the parameters of the pitch-over manoeuvre on ascent

    The pitch-over applies a brief, controlled, tilt to the rocket to allow the gravity turn to begin.

    Attributes:
        pitchOverTime (float): Time in seconds after launch for the pitch-over to begin
        pitchOverDurationTime (float): How long in seconds it will take for the pitch-over to happen
        pitchOverAngle (float): Angle in radians commanded during the maneuver
    """
    pitchOverTime: float
    pitchOverDurationTime: float
    pitchOverAngle: float


#All values are arbitrary and placeholders.
profile = trajectory(
    pitchOverTime = 1.5,
    pitchOverDurationTime = 1,
    pitchOverAngle = 0.02
)

#Duration in seconds of the coast period between stages within the flight plan
coastPeriodDuration = [20,0]


def get_trajectory(t, vx, vy, vz):
    """
    Determines the attitude of the rocket according to the trajectory parameters

    Trajectory follows three phases:
        1. Vertical ascent
        2. Pitch over
        3. Gravity Turn

    Args:
        t (float): Current elapsed mission time in seconds
        vx (float): X velocity
        vy (float): Y velocity (currently unused, but kept in arguments for future use)
        vz (float): Z velocity

    Returns:
        float: the desired attitude of the rocket in radians
    """
    if t > profile.pitchOverTime and t < profile.pitchOverTime + profile.pitchOverDurationTime:
        #Within pitch-over manoeuvre: apply pitch-over angle
        theta = profile.pitchOverAngle #Pitch it
    elif t>= profile.pitchOverTime + profile.pitchOverDurationTime:
        #After pitch-over manoeuvre, align with velocity vector
        theta = math.atan2(vx ,vz)
    else:
        #Remain vertical prior to pitch-over manoeuvre
        theta = 0
    return theta

