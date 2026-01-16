"""Physics calculations for pipe flow profiles."""
import numpy as np


def get_open_channel_velocity(y, y_bed, y_surface, v_max):
    """Calculates velocity for open channel flow (1/7 power law).

    Args:
        y: Y-coordinate (or array) to evaluate.
        y_bed: Bottom boundary.
        y_surface: Top (free surface) boundary.
        v_max: Maximum velocity.

    Returns:
        Velocity value(s) at the given y-coordinate(s).
    """
    y_clipped = np.clip(y, y_bed, y_surface)
    depth = y_surface - y_bed
    if depth == 0:
        return np.zeros_like(y)
    rel_y = (y_clipped - y_bed) / depth
    return v_max * np.power(rel_y, 1/7)


def get_closed_pipe_velocity(y, y_bottom, y_top, v_max):
    """Calculates parabolic velocity profile for closed pipe flow.

    Args:
        y: Y-coordinate to evaluate.
        y_bottom: Pipe bottom.
        y_top: Pipe top.
        v_max: Maximum velocity (at center).

    Returns:
        Velocity at the given y-coordinate.
    """
    R = (y_top - y_bottom) / 2
    y_center = (y_top + y_bottom) / 2
    r = abs(y - y_center)
    if r >= R:
        return 0
    return v_max * (1 - (r/R)**2)


def calculate_egl_hgl(points, initial_head, gravity, friction_factor, flow_velocity):
    """Calculates EGL and HGL points along a path.

    Simplified 1D hydraulics with constant velocity and friction losses.

    Args:
        points: List of path points.
        initial_head: Starting total energy head.
        gravity: Gravitational acceleration.
        friction_factor: Head loss per unit length.
        flow_velocity: Flow velocity.

    Returns:
        tuple: (egl_points, hgl_points) lists.
    """
    path_points = [np.array(p) for p in points]
    velocity_head = (flow_velocity**2) / (2 * gravity)
    
    egl_points = []
    hgl_points = []
    current_head = initial_head
    
    for i, point in enumerate(path_points):
        if i > 0:
            seg_len = np.linalg.norm(point - path_points[i-1])
            head_loss = friction_factor * seg_len
            current_head -= head_loss
        
        egl_pos = np.array([point[0], current_head, 0])
        hgl_pos = np.array([point[0], current_head - velocity_head, 0])
        
        egl_points.append(egl_pos)
        hgl_points.append(hgl_pos)
        
    return egl_points, hgl_points
