"""EGL/HGL Tank Animation Scene.

This module contains the main Manim scene demonstrating Energy Grade Line (EGL)
and Hydraulic Grade Line (HGL) in a tank-pipe system with dynamic diameter changes.
"""
from manim import *
import numpy as np
import os
import sys

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers import (
    load_config, calculate_egl_hgl, create_aligned_label, create_velocity_head_annotation,
    create_components, create_fluid_body, create_walls, create_tank_extensions,
    create_rotated_pipe_label, create_water_symbol, create_datum_line, create_flow_path
)

# --- Configuration ---
script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG = load_config(os.path.join(script_dir, 'inputs.yaml'))
GLOBAL_CONF = CONFIG['global']
config.background_color = GLOBAL_CONF['background_color']
config.media_dir = os.path.join(script_dir, "media")

# Set Resolution
quality = GLOBAL_CONF.get('quality', 'low')
if quality == 'high':
    config.pixel_height = 2160
    config.pixel_width = 3840
    config.frame_rate = 60
elif quality == 'medium':
    config.pixel_height = 1080
    config.pixel_width = 1920
    config.frame_rate = 60
else:  # low
    config.pixel_height = 480
    config.pixel_width = 854
    config.frame_rate = 30


class EGL_HGL_Tank(Scene):
    """Demonstrates EGL/HGL in a tank-pipe system with dynamic diameter changes."""
    
    def construct(self):
        cfg = CONFIG['scenes']['egl_hgl_tank']
        hyd = cfg['hydraulics']
        phys = CONFIG['global']['physics']
        
        plane = NumberPlane()
        plane.add_coordinates()
        
        # === GEOMETRY ===
        comps = create_components(plane, cfg)
        fluid = create_fluid_body(comps)
        walls = create_walls(fluid)
        
        # Tank Extensions (Open Tops)
        t1_mask, t1_wall_l, t1_wall_r = create_tank_extensions(
            plane, cfg['tanks']['tank1'], DL, config.background_color
        )
        t2_mask, t2_wall_l, t2_wall_r = create_tank_extensions(
            plane, cfg['tanks']['tank2'], UR, config.background_color
        )
        
        self.add(fluid, walls, t1_mask, t2_mask, t1_wall_l, t1_wall_r, t2_wall_l, t2_wall_r)
        self.play(
            FadeIn(fluid), Create(walls),
            Create(t1_wall_l), Create(t1_wall_r),
            Create(t2_wall_l), Create(t2_wall_r)
        )
        
        # === DATUM LINE ===
        t2_bottom_y = cfg['tanks']['tank2']['position'][1] - cfg['tanks']['tank2']['height']
        datum_line, datum_label = create_datum_line(plane, t2_bottom_y)
        self.play(Create(datum_line), Write(datum_label))
        
        # === FLOW PATH ===
        flow_path = create_flow_path(plane, cfg['flow_path']['points'])
        self.play(Create(flow_path))
        
        # === HYDRAULICS SETUP ===
        t1_h = cfg['tanks']['tank1']['height']
        p1_h = cfg['pipes']['pipe1']['height']
        p2_h = cfg['pipes']['pipe2']['height']
        p3_h = cfg['pipes']['pipe3']['height']
        t2_h = cfg['tanks']['tank2']['height']
        diameters = [t1_h, p1_h, p2_h, p3_h, t2_h]
        
        flow_rate = 1.2 * p1_h  # Reference velocity * diameter
        k_coefficients = [
            cfg['pipes']['pipe1'].get('minor_loss_k', 0),
            cfg['pipes']['pipe2'].get('minor_loss_k', 0),
            cfg['pipes']['pipe3'].get('minor_loss_k', 0)
        ]
        
        # Calculate EGL/HGL
        egl_pts, hgl_pts = calculate_egl_hgl(
            points=cfg['flow_path']['points'][1:-1],
            diameters=diameters[1:],
            initial_head=hyd['initial_head'],
            gravity=phys['gravity'],
            friction_factor=hyd['friction_factor'],
            flow_rate=flow_rate,
            minor_loss_coefficients=k_coefficients
        )
        
        egl_visual_pts = [plane.c2p(*p) for p in egl_pts]
        hgl_visual_pts = [plane.c2p(*p) for p in hgl_pts]
        
        egl_line = VMobject(color=RED, stroke_width=4)
        egl_line.set_points_as_corners(egl_visual_pts)
        
        hgl_line = VMobject(color=GREEN, stroke_width=4)
        hgl_line.set_points_as_corners(hgl_visual_pts)
        
        egl_label = create_aligned_label(egl_visual_pts, "EGL", RED, UP)
        hgl_label = create_aligned_label(hgl_visual_pts, "HGL", GREEN, DOWN)
        
        self.play(Create(egl_line), Write(egl_label))
        self.play(Create(hgl_line), Write(hgl_label))
        
        # === PIPE LABELS ===
        lbl_p1 = create_rotated_pipe_label(plane, cfg, comps, "Pipe 1", 1, DOWN)
        lbl_p2 = create_rotated_pipe_label(plane, cfg, comps, "Pipe 2", 2, DOWN)
        lbl_p3 = create_rotated_pipe_label(plane, cfg, comps, "Pipe 3", 3, DOWN)
        self.play(Write(lbl_p1), Write(lbl_p2), Write(lbl_p3))
        
        dim_p1 = create_rotated_pipe_label(plane, cfg, comps, '12"', 1, UP, buff=0.35)
        dim_p2 = create_rotated_pipe_label(plane, cfg, comps, '8"', 2, UP, buff=0.25)
        dim_p3 = create_rotated_pipe_label(plane, cfg, comps, '10"', 3, UP, buff=0.25)
        self.play(Write(dim_p1), Write(dim_p2), Write(dim_p3))
        
        # === WATER SYMBOLS ===
        ws1 = create_water_symbol(plane.c2p(-5.75, 2, 0))
        ws2 = create_water_symbol(plane.c2p(5.75, -0.5, 0))
        self.play(Create(ws1), Create(ws2))
        
        # === ANIMATION: Dynamic Pipe 3 ===
        self.wait(1)
        p3_height_tracker = ValueTracker(p3_h)
        
        # Geometry Updater
        def update_geometry(mob):
            d3 = p3_height_tracker.get_value()
            new_comps = create_components(plane, cfg, p3_height=d3)
            new_fluid = create_fluid_body(new_comps)
            
            if mob == fluid:
                mob.become(new_fluid)
            elif mob == walls:
                mob.become(create_walls(new_fluid))
            
            # Update Pipe 3 labels
            p3_center = new_comps[4].get_center()
            visual_buff = 0.25
            lbl_p3.move_to(p3_center + DOWN * (d3/2 + visual_buff))
            dim_p3.move_to(p3_center + UP * (d3/2 + visual_buff))
        
        fluid.add_updater(update_geometry)
        walls.add_updater(update_geometry)
        
        # Hydraulics Updater
        def update_hydraulics(mob):
            d3 = p3_height_tracker.get_value()
            current_diameters = [t1_h, p1_h, p2_h, d3, t2_h]
            
            new_egl, new_hgl = calculate_egl_hgl(
                points=cfg['flow_path']['points'][1:-1],
                diameters=current_diameters[1:-1],
                initial_head=hyd['initial_head'],
                gravity=phys['gravity'],
                friction_factor=hyd['friction_factor'],
                flow_rate=flow_rate,
                minor_loss_coefficients=k_coefficients
            )
            
            new_visual_egl = [plane.c2p(*p) for p in new_egl]
            new_visual_hgl = [plane.c2p(*p) for p in new_hgl]
            
            if mob == egl_line:
                mob.set_points_as_corners(new_visual_egl)
            elif mob == hgl_line:
                mob.set_points_as_corners(new_visual_hgl)
        
        egl_line.add_updater(update_hydraulics)
        hgl_line.add_updater(update_hydraulics)
        
        # Velocity Head Annotations
        v_heads = VGroup()
        
        def update_v_heads(mob):
            d3 = p3_height_tracker.get_value()
            current_diameters = [t1_h, p1_h, p2_h, d3, t2_h]
            
            egl, hgl = calculate_egl_hgl(
                points=cfg['flow_path']['points'][1:-1],
                diameters=current_diameters[1:],
                initial_head=hyd['initial_head'],
                gravity=phys['gravity'],
                friction_factor=hyd['friction_factor'],
                flow_rate=flow_rate,
                minor_loss_coefficients=k_coefficients
            )
            e_pts = [plane.c2p(*p) for p in egl]
            h_pts = [plane.c2p(*p) for p in hgl]
            
            # Midpoints for each pipe (3 points per segment: top, bottom, end)
            def make_annot(e, h, d, idx):
                area = np.pi * (d ** 2) / 4 if d > 0 else 1
                v = flow_rate / area if d > 0 else 0
                vh = (v**2) / (2 * phys['gravity'])
                txt = r"\frac{V_%d^2}{2g} = %.2f'" % (idx+1, vh)
                return create_velocity_head_annotation(e, h, txt)
            
            new_group = VGroup(
                make_annot((e_pts[1]+e_pts[2])/2, (h_pts[1]+h_pts[2])/2, p1_h, 0),
                make_annot((e_pts[4]+e_pts[5])/2, (h_pts[4]+h_pts[5])/2, p2_h, 1),
                make_annot((e_pts[7]+e_pts[8])/2, (h_pts[7]+h_pts[8])/2, d3, 2)
            )
            mob.become(new_group)
        
        v_heads.add_updater(update_v_heads)
        self.play(Create(v_heads))
        
        # Animate diameter change
        self.play(p3_height_tracker.animate.set_value(p3_h * 1.5), run_time=2)
        self.wait(0.5)
        self.play(p3_height_tracker.animate.set_value(p3_h * 0.5), run_time=2)
        self.wait(1)
