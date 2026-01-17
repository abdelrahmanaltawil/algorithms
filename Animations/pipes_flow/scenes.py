from manim import *
import numpy as np
import os
import sys

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import (
    load_inputs, get_open_channel_velocity, get_closed_pipe_velocity,
    create_axes, create_velocity_profile_visuals, create_particles, get_particle_updater
)

# Load configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
INPUTS = load_inputs(os.path.join(script_dir, 'inputs.yaml'))
GLOBAL_INPUTS = INPUTS['global']


class OpenChannelProfile(Scene):
    def construct(self):
        cfg = INPUTS['scenes']['open_channel']
        geom = cfg['geometry']
        vis = cfg['visuals']
        
        title = Text("Open Channel Flow (Gravity)", font_size=36).to_edge(UP)
        title.set_color(BLACK)
        self.add(title)
        
        # Geometry
        v_max = geom['v_max']
        y_bed = geom['y_bed']
        y_surface = geom['y_surface']
        bed_x_start = geom['bed_x_start']
        bed_x_end = geom['bed_x_end']
        slope_angle = geom['slope_angle_deg'] * DEGREES
        
        # Axes
        axes = create_axes(cfg['axes']['x_range'], cfg['axes']['y_range'], vis['axes_config'])

        # Static Geometry
        p_bed_start = axes.c2p(bed_x_start, y_bed)
        p_bed_end = axes.c2p(bed_x_end, y_bed)
        bed_line = Line(p_bed_start, p_bed_end, color=BLACK, stroke_width=vis['bed_stroke_width'])
        
        p_surf_start = axes.c2p(bed_x_start, y_surface)
        p_surf_end = axes.c2p(bed_x_end, y_surface)
        hgl_line = Line(p_surf_start, p_surf_end, color=WHITE)
        
        water_poly = Polygon(
            p_bed_start, p_bed_end, 
            p_surf_end, p_surf_start,
            color=BLUE, fill_opacity=0.3, stroke_width=0
        )
        
        bed_line.next_to(water_poly, DOWN, buff=0.2)
        
        # Water Level Symbol
        wl_center_x = 5 
        p_symbol_tip = axes.c2p(wl_center_x, y_surface)
        
        triangle = Triangle(color=BLACK, fill_opacity=1, stroke_width=0).scale(0.2)
        triangle.rotate(180 * DEGREES)
        triangle.move_to(p_symbol_tip)
        triangle.shift(UP * triangle.height/2)
        
        wl_line = VGroup()
        for i in range(3):
            offset = 0.15 * (i + 1)
            width = 0.3 * (0.6 ** i)
            wl_line.add(Line(
                axes.c2p(wl_center_x - width, y_surface - offset),
                axes.c2p(wl_center_x + width, y_surface - offset),
                color=BLACK, stroke_width=5
            ))
        water_level_symbol = VGroup(triangle, wl_line)
        
        labels = VGroup(
            Text("Channel Bed", font_size=50, color=BLACK).next_to(bed_line, DOWN),
        )

        # Velocity Profile
        def vel_func(y):
             return get_open_channel_velocity(y, y_bed, y_surface, v_max)

        profile_group = create_velocity_profile_visuals(
            axes=axes,
            velocity_func=vel_func,
            y_range=[y_bed, y_surface],
            x_profile=0,
            v_viz_scale=GLOBAL_INPUTS['animation']['viz_scale_factor'],
            v_max=v_max
        )
        profile_curve, profile_fill, arrows, v_label = profile_group

        # Group and Rotate
        scene_group = VGroup(bed_line, hgl_line, water_poly, labels, profile_group, water_level_symbol)
        scene_group.rotate(slope_angle, about_point=ORIGIN)
        
        self.play(Create(bed_line), FadeIn(water_poly), Write(labels))
        self.play(Create(hgl_line), FadeIn(water_level_symbol))

        # Particle System
        particles = create_particles(axes, vel_func, [bed_x_start, bed_x_end], [y_bed, y_surface], slope_angle, GLOBAL_INPUTS['animation']['particle_count'])
        self.add(particles)
        
        updater = get_particle_updater(axes, particles, vel_func, [bed_x_start, bed_x_end], slope_angle)
        particles.add_updater(updater)
        
        self.wait(GLOBAL_INPUTS['animation']['wait_time_before_particles'])
        self.play(Create(arrows), Create(profile_curve), FadeIn(profile_fill), Write(v_label))
        self.wait(GLOBAL_INPUTS['animation']['wait_time_after_particles_start'])
        particles.remove_updater(updater)


class GravityPipeProfile(Scene):
    def construct(self):
        cfg = INPUTS['scenes']['gravity_pipe']
        geom = cfg['geometry']
        vis = cfg['visuals']
        
        title = Text("Partially Filled Pipe (Gravity)", font_size=36).to_edge(UP)
        title.set_color(BLACK)
        self.add(title)
        
        # Geometry
        dia = geom['diameter']
        depth = geom['water_depth']
        y_inv = geom['y_invert']
        y_surf = y_inv + depth
        y_top = y_inv + dia
        v_max = geom['v_max']
        x_start = geom['x_start']
        x_end = geom['x_end']
        slope_angle = geom['slope_angle_deg'] * DEGREES
        
        # Axes
        axes = create_axes(cfg['axes']['x_range'], cfg['axes']['y_range'])
        
        # Static Geometry
        p_start_bot = axes.c2p(x_start, y_inv)
        p_end_bot = axes.c2p(x_end, y_inv)
        p_start_top = axes.c2p(x_start, y_top)
        p_end_top = axes.c2p(x_end, y_top)
        p_start_surf = axes.c2p(x_start, y_surf)
        p_end_surf = axes.c2p(x_end, y_surf)
        
        water_poly = Polygon(
            p_start_bot, p_end_bot,
            p_end_surf, p_start_surf,
            color=BLUE, fill_opacity=0.3, stroke_width=0
        )

        wall_bot = Line(p_start_bot, p_end_bot, color=BLACK, stroke_width=vis['wall_stroke_width'])
        wall_top = Line(p_start_top, p_end_top, color=BLACK, stroke_width=vis['top_wall_stroke_width'])
        
        wall_bot.next_to(water_poly, DOWN, buff=0.2)
        hgl_line = Line(p_start_surf, p_end_surf, color=WHITE)
        
        labels = VGroup(
            Text("Pipe Wall", font_size=40, color=BLACK).next_to(wall_bot, DOWN),
        )

        # Velocity Profile
        def vel_func(y):
            return get_open_channel_velocity(y, y_inv, y_surf, v_max)

        profile_group = create_velocity_profile_visuals(
            axes=axes,
            velocity_func=vel_func,
            y_range=[y_inv, y_surf],
            x_profile=0,
            v_viz_scale=GLOBAL_INPUTS['animation']['viz_scale_factor'],
            v_max=v_max,
            num_arrows=vis['num_arrows']
        )
        profile_curve, profile_fill, arrows, v_label = profile_group

        # Group Replace & Rotate
        scene_group = VGroup(wall_bot, wall_top, water_poly, hgl_line, labels, profile_group)
        scene_group.rotate(slope_angle, about_point=ORIGIN)
        
        self.play(Create(wall_bot), Create(wall_top), FadeIn(water_poly), Write(labels))
        self.play(Create(hgl_line))

        # Particles
        particles = create_particles(axes, vel_func, [x_start, x_end], [y_inv, y_surf], slope_angle, GLOBAL_INPUTS['animation']['particle_count'])
        self.add(particles)
        
        updater = get_particle_updater(axes, particles, vel_func, [x_start, x_end], slope_angle)
        particles.add_updater(updater)
        
        self.wait(GLOBAL_INPUTS['animation']['wait_time_before_particles'])
        self.play(Create(arrows), Create(profile_curve), FadeIn(profile_fill), Write(v_label))
        self.wait(GLOBAL_INPUTS['animation']['wait_time_after_particles_start'])
        particles.remove_updater(updater)


class ClosedPipeProfile(Scene):
    def construct(self):
        cfg = INPUTS['scenes']['closed_pipe']
        geom = cfg['geometry']
        vis = cfg['visuals']
        
        title = Text("Closed Pipe (Pressure Flow)", font_size=36).to_edge(UP)
        title.set_color(BLACK)
        self.add(title)
        
        # Geometry
        dia = geom['diameter']
        y_bot = geom['y_bottom']
        y_top = y_bot + dia
        x_start = geom['x_start']
        x_end = geom['x_end']
        v_max = geom['v_max']
        slope_angle = geom['slope_angle_deg'] * DEGREES
        
        axes = create_axes(cfg['axes']['x_range'], cfg['axes']['y_range'])
        
        p_start_bot = axes.c2p(x_start, y_bot)
        p_end_bot = axes.c2p(x_end, y_bot)
        p_start_top = axes.c2p(x_start, y_top)
        p_end_top = axes.c2p(x_end, y_top)
        
        water_poly = Polygon(
            p_start_bot, p_end_bot,
            p_end_top, p_start_top,
            color=BLUE, fill_opacity=0.3, stroke_width=0
        )

        wall_bot = Line(p_start_bot, p_end_bot, color=BLACK, stroke_width=vis['wall_stroke_width'])
        wall_top = Line(p_start_top, p_end_top, color=BLACK, stroke_width=vis['wall_stroke_width'])
        
        wall_bot.next_to(water_poly, DOWN, buff=0.1)
        wall_top.next_to(water_poly, UP, buff=0.1)

        labels = VGroup(
            Text("Pipe Wall", font_size=30, color=BLACK).next_to(wall_bot, DOWN),
        )

        # Velocity Profile (Parabolic)
        def vel_func(y):
            return get_closed_pipe_velocity(y, y_bot, y_top, v_max)

        profile_group = create_velocity_profile_visuals(
            axes=axes,
            velocity_func=vel_func,
            y_range=[y_bot, y_top],
            x_profile=0,
            v_viz_scale=GLOBAL_INPUTS['animation']['closed_pipe_viz_scale'],
            v_max=v_max,
            num_arrows=vis['num_arrows']
        )
        profile_curve, profile_fill, arrows, v_label = profile_group

        # Group & Rotate
        scene_group = VGroup(wall_bot, wall_top, water_poly, labels, profile_group)
        scene_group.rotate(slope_angle, about_point=ORIGIN)
        
        self.play(Create(wall_bot), Create(wall_top), FadeIn(water_poly), Write(labels))
        
        # Particles
        particles = create_particles(axes, vel_func, [x_start, x_end], [y_bot, y_top], slope_angle, GLOBAL_INPUTS['animation']['particle_count'])
        self.add(particles)
        
        updater = get_particle_updater(axes, particles, vel_func, [x_start, x_end], slope_angle)
        particles.add_updater(updater)
        
        self.wait(GLOBAL_INPUTS['animation']['wait_time_before_particles'])
        self.play(Create(arrows), Create(profile_curve), FadeIn(profile_fill), Write(v_label))
        self.wait(GLOBAL_INPUTS['animation']['wait_time_after_particles_start'])
        particles.remove_updater(updater)
