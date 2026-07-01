from dataclasses import dataclass

@dataclass
class FlightDataSummary:
    max_altitude: float=0.0
    max_altitude_time: float=0.0

    max_velocity: float=0.0
    max_velocity_time: float=0.0

    max_q: float=0.0
    max_q_time: float=0.0

    burnout_time: float=None
    burnout_altitude: float=None

