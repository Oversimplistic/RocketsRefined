# Rockets Refined - A Trajectory Simulator for Sounding Rockets

A physics-based sounding rocket simulator written in Python, using RK4 numerical integration to model powered ascent under thrust, drag, gravity, and a standard atmosphere model.

## Overview

This project simulates a single-stage rocket's vertical flight, using real motor thrust-curve data (Cesaroni 40960O8000-P) and the 1976 ISA standard atmosphere model for air density. State (position, velocity, mass) is integrated forward in real time using 4th-order Runge Kutta.

Built as a personal project to combine and expand my knowledge of numerical methods, flight mechanics, and general software engineering practice ahead of starting my engineering degree.

## Features

- RK4 Integration of motion equations
- Motor-thrust curve interpolation of real-world data
- Prescribed gravity turn and downrange modelling/tracking
- Mass-flow modelling from thrust and specific impulse (Isp)
- Support for two stages using different rocket motors
- ISA-based atmospheric density model (drag varies with altitude)
- Altitude-dependent gravity
- Flight event tracking (max altitude, max velocity, max dynamic pressure, burnout)
- Automatic plotting of data (altitude, downrange motion, velocity, thrust, and drag)

## Current Limitations

- Only a two-dimensional ascent profile - no lateral motion yet
- Only supports two stages
- No wind or dispersion modelling
- Not yet validated against real flight data

## How to run

```bash
python simulation.py
```
This runs the simulation until the rocket returns to the ground, prints a flight summary, and graphs key data.

## Requirements

- Python 3.x
- numpy
- matplotlib

## Roadmap

- [x] Add 2D capability (downrange distance)
- [x] Add a prescribed gravity turn for proof of concept
- [ ] Extend to 3D (lateral tracking)
- [ ] Add aerodynamic-driven gravity turn logic
- [x] Multi-stage support
- [ ] Monte Carlo dispersion analysis (wind, thrust variance)
- [ ] Validation against real flight telemetry

## Key Learnings

- Numerical Methods (4th-order Runge-Kutta, etc.)
- Debugging
- Object Orientated Programming
- Git integration


