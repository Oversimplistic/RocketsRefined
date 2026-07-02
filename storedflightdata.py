from dataclasses import dataclass, field

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


@dataclass
class FlightLog:
    time:list=field(default_factory=list)
    x: list = field(default_factory=list)
    y: list = field(default_factory=list)
    z: list = field(default_factory=list)
    vx: list = field(default_factory=list)
    vy: list = field(default_factory=list)
    vz: list = field(default_factory=list)
    mass: list = field(default_factory=list)

    def log(self, t, state):
        x,y,z,vx,vy,vz,m = state
        self.time.append(t)
        self.x.append(x); self.y.append(y); self.z.append(z); self.vx.append(vx); self.vy.append(vy); self.vz.append(vz);self.mass.append(m)

@dataclass
class simulationData:
    drag:list=field(default_factory=list)
    altitude:list=field(default_factory=list)
    velocity:list=field(default_factory=list)
    thrust:list=field(default_factory=list)
    gravity:list=field(default_factory=list)

    def log(self, drag, altitude, velocity, thrust, gravity):
        self.drag.append(drag); self.altitude.append(altitude); self.velocity.append(velocity); self.thrust.append(thrust); self.gravity.append(gravity)