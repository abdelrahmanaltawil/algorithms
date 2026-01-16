"""Physics calculations for hydraulic systems."""
import numpy as np


def calculate_egl_hgl(points, diameters, initial_head, gravity, friction_factor, flow_rate, minor_loss_coefficients=None):
    """Calculates Energy Grade Line (EGL) and Hydraulic Grade Line (HGL) points.

    Computes the hydraulic profile along a path with variable cross-sections, 
    accounting for both major friction losses (slope) and minor losses (steps).

    Args:
        points (list): List of [x, y, z] points defining the path segments.
        diameters (list): List of diameters for each segment. Length must be len(points)-1.
        initial_head (float): The starting total energy head (elevation + pressure + velocity).
        gravity (float): Gravitational acceleration (g).
        friction_factor (float): Darcy-Weisbach friction factor 'f' (dimensionless).
        flow_rate (float): Volume flow rate (Q).
        minor_loss_coefficients (list, optional): List of minor loss coefficients (K) 
            for each segment. Defaults to None (all zeros).

    Returns:
        tuple: A tuple containing two lists:
            - egl_points (list): List of [x, y, z] points for the Energy Grade Line.
            - hgl_points (list): List of [x, y, z] points for the Hydraulic Grade Line.
    """
    path_points = [np.array(p) for p in points]
    
    if minor_loss_coefficients is None:
        ks = [0] * (len(path_points) - 1)
    else:
        ks = minor_loss_coefficients

    egl_points = []
    hgl_points = []
    current_head = initial_head
    
    for i in range(len(path_points) - 1):
        p_start = path_points[i]
        p_end = path_points[i+1]
        
        segment_length = np.linalg.norm(p_end - p_start)
        diameter = diameters[i]
        k = ks[i]
        
        if diameter <= 0.001: 
            velocity = 0
        else:
            area = np.pi * (diameter ** 2) / 4
            velocity = flow_rate / area
            
        velocity_head = (velocity**2) / (2 * gravity)
        minor_loss = k * velocity_head
        
        # Before minor loss
        egl_points.append([p_start[0], current_head, 0])
        hgl_points.append([p_start[0], current_head - velocity_head, 0])
        
        # After minor loss (step)
        current_head -= minor_loss
        egl_points.append([p_start[0], current_head, 0])
        hgl_points.append([p_start[0], current_head - velocity_head, 0])

        # Major loss (slope)
        if diameter > 0.001:
            head_loss = friction_factor * (segment_length / diameter) * velocity_head
        else:
            head_loss = 0
        current_head -= head_loss
        
        # End of segment
        egl_points.append([p_end[0], current_head, 0])
        hgl_points.append([p_end[0], current_head - velocity_head, 0])
        
    return egl_points, hgl_points
