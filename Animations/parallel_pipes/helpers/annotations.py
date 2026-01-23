from manim import *

def create_flow_label(flow_rate, position, pipe_name="Q"):
    """
    Creates a LaTeX label for flow rate.
    """
    # Format: Q_A = 0.12 m^3/s
    txt = MathTex(
        f"Q_{{{pipe_name}}} = {flow_rate:.3f} \\, m^3/s",
        font_size=20, # readable size
        color=YELLOW
    )
    
    # Add background for readability
    bg = BackgroundRectangle(txt, fill_opacity=0.8, color=BLACK, buff=0.1)
    label = VGroup(bg, txt)
    label.move_to(position)
    
    return label

def get_annotation_pos(pipe_path_mobject, offset=UP*0.5):
    """
    Gets a good position for the annotation (center of path + offset).
    """
    return pipe_path_mobject.get_center() + offset
