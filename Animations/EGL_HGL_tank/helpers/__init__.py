"""Helpers package for EGL/HGL Tank animation.

This package contains modular helpers for:
- config: Configuration loading
- physics: EGL/HGL calculations
- geometry: Tank/pipe creation
- labels: Labels, annotations, symbols, and reference lines
"""
from .config import load_config
from .physics import calculate_egl_hgl
from .geometry import (
    create_components, create_fluid_body, create_walls, create_tank_extensions
)
from .annotations import (
    create_aligned_label, create_velocity_head_annotation,
    create_rotated_pipe_label, create_water_symbol, create_datum_line, create_flow_path
)
