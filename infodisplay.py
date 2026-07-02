#A place to put functions for displaying data (text, graphs, graphics, etc.)

from storedflightdata import *


def output_as_text(summary):
    print(f"Max Altitude was {summary.max_altitude:.2f} meters. This was reached at {summary.max_altitude_time:.2f} seconds\n"
          f"Max Velocity was {summary.max_velocity:.2f} meters per second. This was reached at {summary.max_velocity_time:.2f} seconds\n"
          f"MaxQ was {summary.max_q:.2f} Newtons. This was reached at {summary.max_q_time:.2f} seconds\n"
          f"Stage 1 burnout was reached at {summary.burnout_time:.2f} at {summary.burnout_altitude:.2f} meters"
          )


