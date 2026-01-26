from manim import *

def create_flow_label(pipe, flow_rate, pipe_name, direction=UP, buff=0.2):
    """
    Creates a LaTeX label for flow rate positioned next to the pipe.
    """
    # Format: Q_{name}
    txt = MathTex(
        f"Q_{{{pipe_name}}}",
        font_size=40, 
        color=BLACK
    )

    label = txt
    label.next_to(pipe, direction=direction, buff=buff)
    
    return label

def create_flow_arrow(pipe, direction=UP, buff=0.1):
    """
    Creates a directional arrow indicating flow, positioned relative to the pipe.
    By default places an arrow pointing RIGHT (standard flow) shifted by direction/buff.
    """
    # Create arrow pointing right
    # Size tuning: small but visible
    arrow = Arrow(start=LEFT, end=RIGHT, stroke_width=7, color=BLACK, max_tip_length_to_length_ratio=0.25)
    
    # Position relative to pipe
    arrow.next_to(pipe, direction=direction, buff=buff)
    
    return arrow


def create_head_label(head_value, position):
    """
    Creates a label for Hydraulic Head (H).
    Format: H = 100.00 m
    """
    txt = MathTex(
        f"H = {head_value:.2f} m",
        font_size=40,
        color=BLACK
    )
    # Add background rectangle for readability over lines/pipes
    bg = BackgroundRectangle(txt, fill_opacity=0.7, color=WHITE, buff=0.1)
    
    return VGroup(bg, txt).move_to(position)
