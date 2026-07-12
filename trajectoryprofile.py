from dataclasses import dataclass
import math

@dataclass
class trajectory:
    pitchOverTime: float
    pitchOverDurationTime: float
    pitchOverAngle: float


#All values are arbitrary and placeholders.
profile = trajectory(
    pitchOverTime = 1.5,
    pitchOverDurationTime = 1,
    pitchOverAngle = 0.02
)




def get_trajectory(t, vx, vy, vz):
    if t > profile.pitchOverTime and t < profile.pitchOverTime + profile.pitchOverDurationTime:
        theta = profile.pitchOverAngle #Pitch it
    elif t>= profile.pitchOverTime + profile.pitchOverDurationTime:
        theta = math.atan2(vx ,vz) #Align with Velocity
    else:
        theta = 0 #Vertical
    return theta

