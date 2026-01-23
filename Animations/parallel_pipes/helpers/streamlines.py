"""
Streamline path generation for parallel pipe flow.
Creates complete paths from inlet through parallel branches to outlet.
"""
from manim import *
import numpy as np


def compose_streamline_path(inlet_path, branch_path, outlet_path):
    """
    Composes a single continuous VMobject path from inlet -> branch -> outlet
    with smooth curved transitions at the junction points.
    
    Args:
        inlet_path (VMobject): Path for inlet pipe.
        branch_path (VMobject): Path for one parallel branch (A, B, or C).
        outlet_path (VMobject): Path for outlet pipe.
        
    Returns:
        VMobject: A single continuous path with smooth transitions.
    """
    # Sample key points from each path segment
    all_points = []
    
    # Inlet: sample points up to junction
    for alpha in [0.0, 0.5, 0.75, 0.95]:
        all_points.append(inlet_path.point_from_proportion(alpha))
    
    # Branch: sample points along the branch
    for alpha in [0.25, 0.5, 0.75]:
        all_points.append(branch_path.point_from_proportion(alpha))
    
    # Outlet: sample points from junction to end
    for alpha in [0.15, 1.0]:
        all_points.append(outlet_path.point_from_proportion(alpha))
    
    # Create smooth path through all points
    streamline = VMobject()
    streamline.set_points_smoothly(all_points)
    
    return streamline


def create_streamlines(pipes, flows, total_q):
    """
    Creates streamline paths and assigns particle counts based on flow ratios.
    
    Args:
        pipes (dict): Dictionary of pipe mobjects (VGroup of outline, path).
        flows (dict): Dictionary of flow rates for each branch.
        total_q (float): Total flow rate.
        
    Returns:
        list: List of tuples (streamline_path, particle_count, flow_fraction)
    """
    streamlines = []
    
    # Get inner paths (index 1 in VGroup)
    inlet_path = pipes['pipe_inlet'][1]
    outlet_path = pipes['pipe_D'][1]
    
    # Parallel branches
    branches = ['A', 'B', 'C']
    
    for branch_id in branches:
        branch_path = pipes[f'pipe_{branch_id}'][1]
        
        # Compose full streamline
        streamline = compose_streamline_path(inlet_path, branch_path, outlet_path)
        
        # Calculate flow fraction
        q_branch = flows[branch_id]
        fraction = q_branch / total_q
        
        # Particle count proportional to flow (total ~60 particles)
        count = max(5, int(fraction * 60))
        
        streamlines.append({
            'path': streamline,
            'count': count,
            'fraction': fraction,
            'branch_id': branch_id
        })
        
    return streamlines


def create_streamline_particles(streamlines, total_duration=8.0, num_layers=5):
    """
    Creates continuous looping particle animations for all streamlines.
    
    Args:
        streamlines (list): Output from create_streamlines.
        total_duration (float): Total animation duration.
        num_layers (int): Number of parallel layers per streamline.
        
    Returns:
        tuple: (VGroup of all particles, list of offset paths for cleanup)
    """
    all_particles = VGroup()
    all_paths = []
    
    for sl in streamlines:
        path = sl['path']
        count = sl['count']
        fraction = sl['fraction']
        
        # Particles per layer
        particles_per_layer = max(3, count // num_layers)
        
        for layer_idx in range(num_layers):
            # Offset from center
            offset = (layer_idx - (num_layers - 1) / 2) * 0.12
            
            # Velocity profile: center faster (parabolic)
            center_idx = (num_layers - 1) / 2
            r_ratio = abs(layer_idx - center_idx) / center_idx if center_idx > 0 else 0
            v_factor = 1.0 - 0.5 * (r_ratio ** 2)
            
            # Speed: faster flow = faster particles
            base_speed = 0.08
            speed = base_speed * v_factor * (fraction * 2 + 0.5)
            
            # Create offset path
            offset_path = create_offset_path(path, offset)
            all_paths.append(offset_path)
            
            # Create particles evenly distributed along path
            for i in range(particles_per_layer):
                initial_alpha = i / particles_per_layer
                dot = Dot(radius=0.04, color=WHITE).set_opacity(0.6 + 0.3 * v_factor)
                
                # Store virtual position as custom attribute
                dot.virtual_alpha = initial_alpha
                dot.speed = speed
                dot.path_ref = offset_path
                
                # Position initially
                dot.move_to(offset_path.point_from_proportion(initial_alpha))
                
                all_particles.add(dot)
    
    return all_particles, all_paths


def get_particle_updater(dt_scale=1.0):
    """
    Returns an updater function that moves particles continuously along their paths.
    
    Args:
        dt_scale (float): Speed multiplier.
        
    Returns:
        function: Updater function for particles.
    """
    def updater(particle, dt):
        # Update virtual position
        particle.virtual_alpha += particle.speed * dt * dt_scale
        
        # Wrap around when reaching the end
        particle.virtual_alpha = particle.virtual_alpha % 1.0
        
        # Move to new position on path
        new_pos = particle.path_ref.point_from_proportion(particle.virtual_alpha)
        particle.move_to(new_pos)
    
    return updater


def create_offset_path(original_path, offset_amount):
    """
    Creates a path offset perpendicular to the original path.
    
    Args:
        original_path (VMobject): The center path.
        offset_amount (float): Offset distance (positive = up/left normal).
        
    Returns:
        VMobject: Offset path.
    """
    if abs(offset_amount) < 0.001:
        return original_path.copy()
    
    offset_path = VMobject()
    
    # Sample points along the path and offset each
    num_samples = 200  # Increased for smoother paths
    offset_points = []
    
    for i in range(num_samples + 1):
        alpha = i / num_samples
        
        # Get point on path
        point = original_path.point_from_proportion(alpha)
        
        # Calculate tangent direction
        epsilon = 0.005
        alpha_next = min(alpha + epsilon, 1.0)
        alpha_prev = max(alpha - epsilon, 0.0)
        
        if alpha_next != alpha_prev:
            p_next = original_path.point_from_proportion(alpha_next)
            p_prev = original_path.point_from_proportion(alpha_prev)
            tangent = p_next - p_prev
            tangent = tangent / (np.linalg.norm(tangent) + 1e-9)
        else:
            tangent = np.array([1, 0, 0])
        
        # Normal vector (perpendicular in 2D: rotate 90 degrees)
        normal = np.array([-tangent[1], tangent[0], 0])
        
        # Offset point
        offset_point = point + normal * offset_amount
        offset_points.append(offset_point)
    
    # Use corners for strict adherence to calculated points (control via num_samples)
    offset_path.set_points_as_corners(offset_points)

    return offset_path
