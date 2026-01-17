"""Helpers package for pipes_flow animation.

This package contains modular helpers for:
- config: Configuration loading
- physics: Velocity profiles and EGL/HGL calculations
- visuals: Velocity profile graphics, particles, and updaters
"""
from .inputs_loader import load_inputs
from .physics import get_open_channel_velocity, get_closed_pipe_velocity, calculate_egl_hgl
from .visuals import create_axes, create_velocity_profile_visuals, create_particles, get_particle_updater
