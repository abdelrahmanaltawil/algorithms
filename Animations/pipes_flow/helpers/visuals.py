"""Visual helpers for pipe flow animations."""
from manim import *
import numpy as np
import random


def create_axes(x_range, y_range, config_dict=None):
    """Creates Manim Axes with optional configuration.

    Args:
        x_range: X-axis range.
        y_range: Y-axis range.
        config_dict: Optional axis configuration dict.

    Returns:
        Axes: Configured axes object.
    """
    axis_config = config_dict if config_dict else {"include_tip": False, "stroke_opacity": 0}
    return Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=16,
        y_length=8,
        axis_config=axis_config
    )


def create_velocity_profile_visuals(axes, velocity_func, y_range, x_profile, v_viz_scale, v_max, num_arrows=9, color=BLACK):
    """Creates velocity profile visualization with curve, fill, arrows, and label.

    Args:
        axes: The Axes object.
        velocity_func: Function returning velocity for a given y.
        y_range: Tuple (y_min, y_max).
        x_profile: X-position of the profile.
        v_viz_scale: Visual scale factor for velocity.
        v_max: Maximum velocity for label positioning.
        num_arrows: Number of arrows to display.
        color: Profile color.

    Returns:
        VGroup: Profile curve, fill, arrows, and label.
    """
    y_min, y_max = y_range
    
    # Profile Curve
    profile_curve = axes.plot_parametric_curve(
        lambda t: np.array([
            x_profile + velocity_func(t) * v_viz_scale,
            t,
            0
        ]),
        t_range=[y_min, y_max],
        color=color
    )

    # Filled Profile Area
    fill_points = [axes.c2p(x_profile, y_min)]
    steps = 40
    for i in range(steps + 1):
        t = y_min + (i/steps) * (y_max - y_min)
        val = x_profile + velocity_func(t) * v_viz_scale
        fill_points.append(axes.c2p(val, t))
    fill_points.append(axes.c2p(x_profile, y_max))
    profile_fill = Polygon(*fill_points, color=color, fill_opacity=0.3, stroke_width=0)

    # Arrows
    arrows = VGroup()
    for i in range(num_arrows + 1):
        y = y_min + (i/num_arrows) * (y_max - y_min)
        v = velocity_func(y)
        start_pt = axes.c2p(x_profile, y)
        end_pt = axes.c2p(x_profile + v * v_viz_scale, y)
        if v > 0.1:
            arrow = Arrow(start_pt, end_pt, buff=0, color=color, max_tip_length_to_length_ratio=0.1)
            arrows.add(arrow)

    # Velocity Label
    y_v_label = y_min + 0.6 * (y_max - y_min)
    v_label_pos = axes.c2p(x_profile + v_max * v_viz_scale + 0.5, y_v_label)
    v_label = MathTex(r"\vec{v}", color=color, font_size=70).move_to(v_label_pos)

    return VGroup(profile_curve, profile_fill, arrows, v_label)


def create_particles(axes, velocity_func, x_bounds, y_bounds, slope_angle=0, num_particles=50):
    """Creates particle dots for flow visualization.

    Args:
        axes: The Axes object.
        velocity_func: Velocity function.
        x_bounds: Tuple (x_start, x_end).
        y_bounds: Tuple (y_min, y_max).
        slope_angle: Rotation angle for sloped flows.
        num_particles: Number of particles.

    Returns:
        VGroup: Particle dots.
    """
    particles = VGroup()
    x_start, x_end = x_bounds
    y_min, y_max = y_bounds
    
    for _ in range(num_particles):
        dot = Dot(radius=0.05, color=BLACK)
        vx = random.uniform(x_start, x_end)
        vy = random.uniform(y_min, y_max)
        dot.virt_pos = np.array([vx, vy, 0])
        base_pos = axes.c2p(vx, vy)
        dot.move_to(rotate_vector(base_pos, slope_angle))
        particles.add(dot)
        
    return particles


def get_particle_updater(axes, particles, velocity_func, x_bounds, slope_angle=0):
    """Returns an updater function for particle animation.

    Args:
        axes: The Axes object.
        particles: VGroup of particles.
        velocity_func: Velocity function.
        x_bounds: Tuple (x_start, x_end).
        slope_angle: Rotation angle.

    Returns:
        function: Updater function for particles.
    """
    x_start, x_end = x_bounds
    
    def update_particles(mob, dt):
        for dot in mob:
            vx, vy, _ = dot.virt_pos
            v = velocity_func(vy)
            vx_new = vx + v * dt * 0.5
            if vx_new > x_end:
                vx_new = x_start
            dot.virt_pos = np.array([vx_new, vy, 0])
            raw_pos = axes.c2p(vx_new, vy)
            dot.move_to(rotate_vector(raw_pos, slope_angle))
    
    return update_particles
