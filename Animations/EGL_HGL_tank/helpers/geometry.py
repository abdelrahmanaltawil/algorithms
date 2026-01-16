"""Geometry creation functions for EGL/HGL Tank animation.

This module provides functions to create the visual geometry (tanks, pipes,
fluid body, walls) for the hydraulic system animation.
"""
from manim import *
import numpy as np


def create_tank(plane, width, height, position, aligned_edge=DL):
    """Creates a tank rectangle positioned on the plane.
    
    Args:
        plane: The NumberPlane for coordinate conversion.
        width: Tank width.
        height: Tank height.
        position: [x, y] position in plane coordinates.
        aligned_edge: Alignment edge (default DL for bottom-left).
        
    Returns:
        Rectangle: The tank Mobject.
    """
    tank = Rectangle(width=width, height=height)
    tank.move_to(plane.c2p(*position), aligned_edge=aligned_edge)
    return tank


def create_pipe(plane, width, height, start, end_direction=None):
    """Creates a pipe rectangle, optionally rotated.
    
    Args:
        plane: The NumberPlane for coordinate conversion.
        width: Pipe length (visual width).
        height: Pipe diameter (visual height).
        start: [x, y] start position.
        end_direction: [x, y] direction point for rotation. If None, horizontal.
        
    Returns:
        Rectangle: The pipe Mobject.
    """
    pipe = Rectangle(width=width, height=height)
    pt1 = plane.c2p(*start)
    pipe.move_to(pt1, aligned_edge=LEFT)
    
    if end_direction is not None:
        pt2 = plane.c2p(*end_direction)
        angle = angle_of_vector(pt2 - pt1)
        pipe.rotate(angle, about_point=pipe.get_edge_center(LEFT))
    
    return pipe


def create_components(plane, cfg, p3_height=None):
    """Creates all tank and pipe components.
    
    Args:
        plane: The NumberPlane for coordinate conversion.
        cfg: Scene configuration dictionary.
        p3_height: Optional override for Pipe 3 height (for animation).
        
    Returns:
        list: [tank1, tank2, pipe1, pipe2, pipe3] Mobjects.
    """
    _p3_h = p3_height if p3_height is not None else cfg['pipes']['pipe3']['height']
    
    # Tanks
    t1 = create_tank(
        plane, 
        cfg['tanks']['tank1']['width'],
        cfg['tanks']['tank1']['height'],
        cfg['tanks']['tank1']['position'],
        DL
    )
    t2 = create_tank(
        plane,
        cfg['tanks']['tank2']['width'],
        cfg['tanks']['tank2']['height'],
        cfg['tanks']['tank2']['position'],
        UR
    )
    
    # Pipes
    p1 = create_pipe(
        plane,
        cfg['pipes']['pipe1']['width'],
        cfg['pipes']['pipe1']['height'],
        cfg['pipes']['pipe1']['start'],
        cfg['pipes']['pipe1'].get('end_direction')
    )
    p2 = create_pipe(
        plane,
        cfg['pipes']['pipe2']['width'],
        cfg['pipes']['pipe2']['height'],
        cfg['pipes']['pipe2']['start'],
        cfg['pipes']['pipe2'].get('end_direction')
    )
    p3 = create_pipe(
        plane,
        cfg['pipes']['pipe3']['width'],
        _p3_h,
        cfg['pipes']['pipe3']['start'],
        cfg['pipes']['pipe3'].get('end_direction')
    )
    
    return [t1, t2, p1, p2, p3]


def create_fluid_body(components):
    """Creates the fluid body from component union.
    
    Args:
        components: List of tank/pipe Mobjects.
        
    Returns:
        Union: Styled fluid body.
    """
    fluid = Union(*components)
    fluid.set_style(fill_color=BLUE, fill_opacity=0.5, stroke_width=0)
    return fluid


def create_walls(fluid):
    """Creates wall outlines from fluid body.
    
    Args:
        fluid: The fluid body Mobject.
        
    Returns:
        VMobject: Styled wall outline.
    """
    walls = fluid.copy()
    walls.set_style(fill_opacity=0, stroke_color=BLACK, stroke_width=4)
    return walls


def create_tank_extensions(plane, tank_cfg, position_edge, bg_color, ext_length=0.5):
    """Creates extended walls and mask for open-top tank.
    
    Args:
        plane: The NumberPlane.
        tank_cfg: Tank configuration dict with width, height, position.
        position_edge: Alignment edge (DL or UR).
        bg_color: Background color for the mask.
        ext_length: Extension length above tank.
        
    Returns:
        tuple: (mask_line, left_wall, right_wall)
    """
    temp = Rectangle(
        width=tank_cfg['width'], 
        height=tank_cfg['height']
    ).move_to(plane.c2p(*tank_cfg['position']), aligned_edge=position_edge)
    
    ul = temp.get_corner(UL)
    ur = temp.get_corner(UR)
    
    mask = Line(ul, ur, color=bg_color, stroke_width=8)
    wall_l = Line(ul - UP*0.1, ul + UP * ext_length, color=BLACK, stroke_width=4)
    wall_r = Line(ur - UP*0.1, ur + UP * ext_length, color=BLACK, stroke_width=4)
    
    return mask, wall_l, wall_r
