"""Label, annotation, and symbol creation functions for EGL/HGL Tank animation.

This module provides functions to create labels, annotations, symbols,
and reference lines for the hydraulic system animation.
"""
from manim import *
import numpy as np


# --- EGL/HGL Annotations ---

def create_aligned_label(pts, text, color, direction, segment_indices=(2, 3), offset=0.4):
    """Creates a text label aligned with the slope of a line segment.

    Args:
        pts (list): List of points defining the line segment(s).
        text (str): The text content for the label.
        color (str): The color of the label text.
        direction (np.array): Offset direction (UP, DOWN).
        segment_indices (tuple): Indices of the two points to use for angle/position (default: (2, 3)).
        offset (float): Distance to offset the label from the line (default: 0.4).

    Returns:
        MathTex: The rotated and positioned label.
    """
    i1, i2 = segment_indices
    p1 = pts[i1]
    p2 = pts[i2]
    angle = angle_of_vector(p2 - p1)
    
    label = MathTex(text, color=color, font_size=150, stroke_width=8)
    label.rotate(angle)
    label.move_to((p1 + p2) / 2)
    label.shift(rotate_vector(direction * offset, angle))
    return label


def create_velocity_head_annotation(egl_pt, hgl_pt, text_label):
    """Creates a dimension-style annotation for velocity head.

    Args:
        egl_pt (np.array): Point on the Energy Grade Line.
        hgl_pt (np.array): Point on the Hydraulic Grade Line.
        text_label (str or Mobject): Label text or Mobject.

    Returns:
        VGroup: Group containing arrows and label.
    """
    v_diff = egl_pt - hgl_pt
    v_len = np.linalg.norm(v_diff)
    v_unit = UP if v_len < 1e-3 else v_diff / v_len
    arrow_len = 2
    
    arrow_top = Arrow(
        start=egl_pt + v_unit * arrow_len, 
        end=egl_pt, 
        buff=0, color=BLACK, stroke_width=14, 
        tip_length=3, max_stroke_width_to_length_ratio=12
    )
    
    arrow_bottom = Arrow(
        start=hgl_pt - v_unit * arrow_len, 
        end=hgl_pt, 
        buff=0, color=BLACK, stroke_width=14, 
        tip_length=3, max_stroke_width_to_length_ratio=12
    )
    
    if isinstance(text_label, str):
        label = MathTex(text_label, color=BLACK, font_size=150)
    else:
        label = text_label
    
    label.next_to(arrow_top, UP, buff=0.1)
    return VGroup(arrow_top, arrow_bottom, label)


# --- Pipe Labels ---

def create_rotated_pipe_label(plane, cfg, comps, text, pipe_idx, direction):
    """Creates a label rotated to match a pipe's slope.
    
    Args:
        plane: The NumberPlane.
        cfg: Scene configuration dictionary.
        comps: List of component Mobjects [t1, t2, p1, p2, p3].
        text: Label text.
        pipe_idx: 1-based pipe index (1, 2, or 3).
        direction: Offset direction (UP or DOWN).
        buff: Buffer distance from pipe center.
        
    Returns:
        Tex: Positioned and rotated label.
    """
    p_key = f'pipe{pipe_idx}'
    p_dat = cfg['pipes'][p_key]
    
    if 'end_direction' in p_dat:
        pt1 = plane.c2p(*p_dat['start'])
        pt2 = plane.c2p(*p_dat['end_direction'])
        angle = angle_of_vector(pt2 - pt1)
    else:
        angle = 0
    
    lbl = Tex(text, font_size=150, color=BLACK)
    lbl.rotate(angle)
    
    pipe_mob = comps[pipe_idx + 1]
    center = pipe_mob.get_center()
    
    offset = rotate_vector(direction, angle)
    lbl.move_to(center + offset)
    return lbl


# --- Symbols ---

def create_water_symbol(point):
    """Creates a water surface symbol (inverted triangle with lines).
    
    Args:
        point: Position for the symbol tip.
        
    Returns:
        VGroup: Triangle and horizontal lines.
    """
    tri = Triangle(fill_color=BLACK, fill_opacity=1, stroke_color=BLACK)
    tri.scale(0.7).rotate(PI)
    tri.move_to(point, aligned_edge=DOWN)
    
    l1 = Line(LEFT*0.7, RIGHT*0.7, stroke_width=14, color=BLACK)
    l1.next_to(tri, DOWN, buff=0.4)
    
    l2 = Line(LEFT*0.3, RIGHT*0.3, stroke_width=14, color=BLACK)
    l2.next_to(l1, DOWN, buff=0.4)
    
    return VGroup(tri, l1, l2)


# --- Reference Lines ---

def create_datum_line(plane, y_level, x_range=(-8, 8)):
    """Creates a datum reference line.
    
    Args:
        plane: The NumberPlane.
        y_level: Y-coordinate for the datum.
        x_range: Tuple of (x_start, x_end).
        
    Returns:
        tuple: (datum_line, datum_label)
    """
    line = DashedLine(
        start=plane.c2p(x_range[0], y_level, 0),
        end=plane.c2p(x_range[1], y_level, 0),
        dash_length=0.39,
        color=BLACK,
        stroke_width=14
    )
    label = MathTex("Datum", color=BLACK, font_size=150)
    label.next_to(line, DOWN, buff=1)
    label.shift(LEFT * 40)
    
    return line, label


def create_flow_path(plane, points):
    """Creates the flow path visualization.
    
    Args:
        plane: The NumberPlane.
        points: List of [x, y, z] points.
        
    Returns:
        VMobject: The flow path line.
    """
    path = VMobject(color=YELLOW, stroke_width=14)
    visual_points = [plane.c2p(*p) for p in points]
    path.set_points_as_corners(visual_points)
    return path
