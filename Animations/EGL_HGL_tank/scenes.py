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
INPUTS = load_config(os.path.join(script_dir, 'inputs.yaml'))
GLOBAL_INPUTS = INPUTS['global']


class EGL_HGL_Tank(Scene):
    """Demonstrates EGL/HGL in a tank-pipe system with dynamic diameter changes."""
    
    def construct(self):
        cfg = INPUTS['scenes']['egl_hgl_tank']
        hyd = cfg['hydraulics']
        phys = GLOBAL_INPUTS['physics']
        
        plane = NumberPlane(
            x_range=[-50, 50, 1],    # Covers full frame_width of 30
            y_range=[-15, 15, 1],    # Covers full frame_height of 14
            x_length=100,
            y_length=30
        )
        plane.add_coordinates()
        
        # === GEOMETRY ===
        comps = create_components(plane, cfg)
        fluid = create_fluid_body(comps)
        walls = create_walls(fluid)
        
        # Tank Extensions (Open Tops)
        t1_mask, t1_wall_l, t1_wall_r = create_tank_extensions(
            plane, cfg['tanks']['tank1'], DL, config.background_color, ext_length=2
        )
        t2_mask, t2_wall_l, t2_wall_r = create_tank_extensions(
            plane, cfg['tanks']['tank2'], DL, config.background_color
        )
        
        self.add(fluid, walls, t1_mask, t2_mask, t1_wall_l, t1_wall_r, t2_wall_l, t2_wall_r)
        self.play(
            FadeIn(fluid), Create(walls),
            Create(t1_wall_l), Create(t1_wall_r),
            Create(t2_wall_l), Create(t2_wall_r)
        )
        
        # === DATUM LINE ===
        t2_bottom_y = cfg['tanks']['tank2']['position'][1]
        datum_line, datum_label = create_datum_line(plane, t2_bottom_y, x_range=(-50, 50))
        self.play(Create(datum_line), Write(datum_label))
        
        # === FLOW PATH ===
        
        # === HYDRAULICS SETUP ===
        # Now visual height = actual diameter (unified dimensions: 1 unit = 1 ft)
        p1_d = cfg['pipes']['pipe1']['height']  # 12" = 1.0 ft
        p2_d = cfg['pipes']['pipe2']['height']  # 8" = 0.667 ft  
        p3_d = cfg['pipes']['pipe3']['height']  # 10" = 0.833 ft
        
        diameters = [p1_d, p2_d, p3_d]
        
        # Flow rate to match reference: V1²/2g=0.62', V2²/2g=3.19', V3²/2g=1.30'
        flow_rate = 5.0  # ft³/s
        k_coefficients = [
            cfg['pipes']['pipe1'].get('minor_loss_k', 0),
            cfg['pipes']['pipe2'].get('minor_loss_k', 0),
            cfg['pipes']['pipe3'].get('minor_loss_k', 0)
        ]
        
        # Calculate EGL/HGL
        egl_pts, hgl_pts = calculate_egl_hgl(
            points=cfg['flow_path']['points'][1:-1],
            diameters=diameters,
            initial_head=hyd['initial_head'],
            gravity=phys['gravity'],
            friction_factor=hyd['friction_factor'],
            flow_rate=flow_rate,
            minor_loss_coefficients=k_coefficients
        )
        
        egl_visual_pts = [plane.c2p(*p) for p in egl_pts]
        hgl_visual_pts = [plane.c2p(*p) for p in hgl_pts]
        
        egl_line = VMobject(color=RED, stroke_width=14)
        egl_line.set_points_as_corners(egl_visual_pts)
        
        hgl_line = VMobject(color=GREEN, stroke_width=14)
        hgl_line.set_points_as_corners(hgl_visual_pts)
        
        egl_label = create_aligned_label(egl_visual_pts, "EGL", RED, UP, segment_indices=(2, 3), offset=1.0)
        hgl_label = create_aligned_label(hgl_visual_pts, "HGL", GREEN, DOWN, segment_indices=(2, 3), offset=1.0)
        
        # === PIPE LABELS ===
        lbl_p1 = create_rotated_pipe_label(plane, cfg, comps, "Pipe 1", 1, DOWN * (p1_d/2 + 1.5))
        lbl_p2 = create_rotated_pipe_label(plane, cfg, comps, "Pipe 2", 2, DOWN * (p2_d/2 + 1.5))
        lbl_p3 = create_rotated_pipe_label(plane, cfg, comps, "Pipe 3", 3, DOWN * (p3_d/2 + 1.5))
        
        # Add white background behind Pipe 3 label so datum line doesn't pass through
        lbl_p3_bg = BackgroundRectangle(lbl_p3, color=WHITE, fill_opacity=1, buff=0.15)
        lbl_p3_group = VGroup(lbl_p3_bg, lbl_p3)
        
        dim_p1 = create_rotated_pipe_label(plane, cfg, comps, '12"', 1, UP * (p1_d/2 + 1.5))
        dim_p2 = create_rotated_pipe_label(plane, cfg, comps, '8"', 2, UP * (p2_d/2 + 1.5))
        dim_p3 = create_rotated_pipe_label(plane, cfg, comps, '10"', 3, UP * (p3_d/2 + 1.5))
        
        # === WATER SYMBOLS ===
        tank1 = cfg['tanks']['tank1']
        tank2 = cfg['tanks']['tank2']
        ws1 = create_water_symbol(plane.c2p(tank1['position'][0]+tank1['width']/2, tank1['position'][1] + tank1['height'], 0))   # Tank 1 water surface
        ws2 = create_water_symbol(plane.c2p(tank2['position'][0]+tank2['width']/2, tank2['position'][1] + tank2['height'], 0))    # Tank 2 water surface


        # === ANIMATION: Labels and Symbols ===
        self.play(Write(lbl_p1), Write(lbl_p2), Create(lbl_p3_group), 
                    Write(dim_p1), Write(dim_p2), Write(dim_p3), 
                    Create(ws1), Create(ws2)
                    )


        # === ANIMATION: EGL/HGL Lines ===
        self.play(Create(egl_line), Write(egl_label))
        self.play(Create(hgl_line), Write(hgl_label))
        
        
        # === ANIMATION: Dynamic Pipe 3 ===
        self.wait(1)
        p3_tracker = ValueTracker(p3_d)  # Now unified: visual height = actual diameter
        
        # Geometry Updater
        def update_geometry(mob):
            d3 = p3_tracker.get_value()
            new_comps = create_components(plane, cfg, p3_height=d3)
            new_fluid = create_fluid_body(new_comps)
            
            if mob == fluid:
                mob.become(new_fluid)
            elif mob == walls:
                mob.become(create_walls(new_fluid))
            
            # Update Pipe 3 labels
            p3_center = new_comps[4].get_center()
            visual_buff = 1.5
            lbl_p3.move_to(p3_center + DOWN * (d3/2 + visual_buff))
            
            # Update Pipe 3 dimension value (convert ft to inches for display)
            d3_inches = d3 * 12  # Convert feet to inches
            new_dim_p3 = Tex(f'{d3_inches:.1f}"', font_size=150, color=BLACK)
            new_dim_p3.move_to(p3_center + UP * (d3/2 + visual_buff))
            dim_p3.become(new_dim_p3)
            
            # Also update background rectangle position
            lbl_p3_bg.move_to(lbl_p3.get_center())
        
        fluid.add_updater(update_geometry)
        walls.add_updater(update_geometry)
        
        # Hydraulics Updater
        def update_hydraulics(mob):
            d3 = p3_tracker.get_value()  # Same value for visual and hydraulics
            current_diameters = [p1_d, p2_d, d3]
            
            new_egl, new_hgl = calculate_egl_hgl(
                points=cfg['flow_path']['points'][1:-1],
                diameters=current_diameters,
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
        def make_velocity_annotation(e_pts, h_pts, d, idx, phys):
            """Create a single velocity head annotation."""
            area = np.pi * (d ** 2) / 4 if d > 0 else 1
            v = flow_rate / area if d > 0 else 0
            vh = (v**2) / (2 * phys['gravity'])
            txt = r"\frac{V_%d^2}{2g} = %.2f'" % (idx+1, vh)
            return create_velocity_head_annotation(e_pts, h_pts, txt)
        
        # Initialize with current values
        e_pts = egl_visual_pts
        h_pts = hgl_visual_pts
        
        v_head_1 = make_velocity_annotation(
            e_pts[0] + (e_pts[1] - e_pts[0]) * 0.25, h_pts[0] + (h_pts[1] - h_pts[0]) * 0.25, p1_d, 0, phys
        )
        v_head_2 = make_velocity_annotation(
            e_pts[2] + (e_pts[3] - e_pts[2]) * 0.25, h_pts[2] + (h_pts[3] - h_pts[2]) * 0.25, p2_d, 1, phys
        )
        v_head_3 = make_velocity_annotation(
            e_pts[4] + (e_pts[5] - e_pts[4]) * 0.25, h_pts[4] + (h_pts[5] - h_pts[4]) * 0.25, p3_d, 2, phys
        )
        
        v_heads = VGroup(v_head_1, v_head_2, v_head_3)
        
        # Animate each equation appearing with Write animation
        self.play(
            Write(v_head_1),
            Write(v_head_2),
            Write(v_head_3),
            lag_ratio=0.3,
            run_time=2
        )
        
        # Now add updater for dynamic changes
        def update_v_heads(mob):
            d3 = p3_tracker.get_value()
            current_diameters = [p1_d, p2_d, d3]
            
            egl, hgl = calculate_egl_hgl(
                points=cfg['flow_path']['points'][1:-1],
                diameters=current_diameters,
                initial_head=hyd['initial_head'],
                gravity=phys['gravity'],
                friction_factor=hyd['friction_factor'],
                flow_rate=flow_rate,
                minor_loss_coefficients=k_coefficients
            )
            new_e_pts = [plane.c2p(*p) for p in egl]
            new_h_pts = [plane.c2p(*p) for p in hgl]
            
            new_group = VGroup(
                make_velocity_annotation(new_e_pts[0] + (new_e_pts[1] - new_e_pts[0]) * 0.25, new_h_pts[0] + (new_h_pts[1] - new_h_pts[0]) * 0.25, p1_d, 0, phys),
                make_velocity_annotation(new_e_pts[2] + (new_e_pts[3] - new_e_pts[2]) * 0.25, new_h_pts[2] + (new_h_pts[3] - new_h_pts[2]) * 0.25, p2_d, 1, phys),
                make_velocity_annotation(new_e_pts[4] + (new_e_pts[5] - new_e_pts[4]) * 0.25, new_h_pts[4] + (new_h_pts[5] - new_h_pts[4]) * 0.25, d3, 2, phys)
            )
            mob.become(new_group)
        
        v_heads.add_updater(update_v_heads)
        self.add(v_heads)  # Ensure VGroup is added to scene for updater to work
        
        # Animate diameter change (repeat twice)
        self.play(p3_tracker.animate.set_value(p3_d * 1.5), run_time=2)
        self.wait(0.5)
        self.play(p3_tracker.animate.set_value(p3_d * 0.9), run_time=2)
        self.wait(0.5)
        
        # Second iteration
        self.play(p3_tracker.animate.set_value(p3_d * 1.5), run_time=2)
        self.wait(0.5)
        self.play(p3_tracker.animate.set_value(p3_d * 0.9), run_time=2)
        self.wait(1)
