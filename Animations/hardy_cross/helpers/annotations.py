from manim import *
import numpy as np
import math

def create_flow_arrows(config, network_group, pipe_map):
    """
    Creates Arrow mobjects representing flow direction for each pipe.
    """
    arrows = VGroup()
    pipes_config = config['network']['pipes']
    
    for pipe_id, pipe_line in pipe_map.items():
        data = pipes_config.get(pipe_id)
        if not data: continue
            
        flow = data.get('initial_flow', 0)
        offset = np.array(data.get('label_offset', [0, 0, 0]))

        
        # Determine start and end points of the line
        start_point = pipe_line.get_start() + offset
        end_point = pipe_line.get_end() + offset
        
        # Calculate mid-point
        mid_point = (start_point + end_point) / 2
        
        # Determine direction based on flow sign
        # Positive flow: start -> end
        # Negative flow: end -> start
        if flow >= 0:
            direction_vector = end_point - start_point
        else:
            direction_vector = start_point - end_point
            
        # Normalize direction
        length = np.linalg.norm(direction_vector)
        if length > 0:
            unit_vector = direction_vector / length
        else:
            unit_vector = np.array([1, 0, 0])
            
        # Create Arrow
        # Place arrow at midpoint, pointing in flow direction
        arrow_length = 1.0
        
        arrow = Arrow(
            start=mid_point - unit_vector * (arrow_length / 2),
            end=mid_point + unit_vector * (arrow_length / 2),
            buff=0,
            color=BLACK,
            stroke_width=6
        )
        
        arrows.add(arrow)
        
    return arrows

def create_flow_labels(config, pipe_map, values=True):
    """
    Creates Text mobjects (MathTex) for flow values.
    """
    labels = VGroup()
    pipes_config = config['network']['pipes']
    visuals = config['visuals']
    
    for pipe_id, pipe_line in pipe_map.items():
        data = pipes_config.get(pipe_id)
        if not data: continue
        
        flow = data.get('initial_flow', 0)
        # Display absolute value for magnitude, direction is shown by arrow
        flow_mag = abs(flow)

        if values:
            label_text = MathTex(f"{flow_mag:.2f}", color=visuals['label_color'])
        else:
            label_text = MathTex(f"Q_{{pipe_id}}", color=visuals['label_color'])
        label_text.scale(0.7)
        
        # Position label
        # Use label_offset from config if available, relative to midpoint
        offset = np.array(data.get('label_offset', [0, 0, 0]), dtype=float)
        # Add 0.3 to the non-zero component's magnitude, preserving sign
        offset[offset != 0] = offset[offset != 0] + np.sign(offset[offset != 0]) * 0.3
        
        # Match the label's rotation to the line's current angle
        label_text.rotate(pipe_line.get_angle())
        label_text.move_to(pipe_line.get_center()+offset)

        labels.add(label_text)
        
    return labels

def create_loop_path(config, pipes_map, loop_id):
    """
    Creates a VGroup that highlights the loop pipes.
    """
    loop_group = VGroup()
    loops_config = config['network'].get('loops', {})
    if loop_id not in loops_config:
        return loop_group
        
    pipe_ids = loops_config[loop_id]
    
    for pid in pipe_ids:
        if pid in pipes_map:
            # Create a copy of the pipe line with highlight style
            original_pipe = pipes_map[pid]
            highlight = original_pipe.copy()
            highlight.set_stroke(color=ORANGE, width=12, opacity=0.5)
            loop_group.add(highlight)

    # add loop label
    loop_label = Text(f"{loop_id}", color=ORANGE, slant=ITALIC)
    loop_label.scale(2)
    loop_label.to_edge(DOWN)

    loop_group.add(loop_label)
            
    return loop_group

def create_correction_formula(network_group):
    """
    Returns a MathTex object for the Hardy Cross correction formula.
    """
    formula = MathTex(
        r"\Delta Q = \frac{E - \sum_i H_i}{n\sum_i \left(\frac{H_i}{Q_i}\right)}",
        color=BLACK
    )
    formula.scale(1.5)
    formula.next_to(network_group, RIGHT, buff=4)

    return formula

def create_side_page(camera_frame, network_group):
    """
    Creates the background rectangle for the side page document.
    """
    side_page = Rectangle(
        width=camera_frame.get_width() * 0.4,
        height=camera_frame.get_height() * 0.8,
        color=BLACK,
        fill_opacity=0.5
    ).next_to(network_group, RIGHT, buff=2)
    return side_page

def get_document_anchors(side_page):
    """
    Returns a dictionary of anchor points and standard margins.
    """
    return {
        'left': side_page.get_left(),
        'top': side_page.get_top(),
        'margin': 0.5 * RIGHT,
        'indent': 1.0 * RIGHT
    }

def create_algorithm_title(side_page):
    anchors = get_document_anchors(side_page)
    title = Text("Hardy Cross Algorithm", color=BLACK, slant=ITALIC).scale(1.2)
    # Position: Top of page + down margin + left margin
    title.move_to(anchors['top'] - anchors['left'] + 1.0*DOWN + 3*RIGHT, aligned_edge=LEFT)
    return title

def create_step_1_text(side_page, prev_mobject):
    step_1_title = Text("Step 1: Initial Guess", color=BLACK, slant=ITALIC).scale(0.8)
    # Position: Below previous object
    step_1_title.next_to(prev_mobject, DOWN, buff=0.8, aligned_edge=LEFT)
    return step_1_title

def create_step_2_text(side_page, prev_mobject):
    anchors = get_document_anchors(side_page)
    
    step_2_title = Text("Step 2: Calculate Energy", color=BLACK, slant=ITALIC).scale(0.8)
    step_2_title.next_to(prev_mobject, DOWN, buff=1.0, aligned_edge=LEFT)
    
    energy_equation_1 = MathTex(
        r"E &= \sum_i H_i", 
        tex_environment="align*",
        color=BLACK
    ).scale(1.0)
    energy_equation_1.next_to(step_2_title, DOWN, buff=0.3, aligned_edge=LEFT)
    energy_equation_1.shift(anchors['indent'])
    
    energy_equation_2 = MathTex(
        r"\text{where } H_i &= K_i Q_i^n", 
        tex_environment="align*",
        color=BLACK
    ).scale(1.0)
    energy_equation_2.next_to(energy_equation_1, DOWN, buff=0.2, aligned_edge=LEFT)
    
    # Return as a VGroup for easy iteration, but also keeping them accessible if needed
    return VGroup(step_2_title, energy_equation_1, energy_equation_2)

def create_step_3_text(side_page, prev_mobject):
    anchors = get_document_anchors(side_page)
    
    step_3_title = Text("Step 3: Iterative Correction", color=BLACK, slant=ITALIC).scale(0.8)
    step_3_title.next_to(prev_mobject, DOWN, buff=1.0, aligned_edge=LEFT)
    # Undo indent effect if prev_mobject was indented (like equation), 
    # but next_to aligns edge. If prev was indented, LEFT edge is indented.
    # We want titles aligned to main margin.
    # We can force alignment with step_3_title.move_to(..., aligned_edge=LEFT) preserving X from Title 1?
    # Simple fix: Shift back if needed, or align to side_page left + margin.
    # User's previous manual code: `step_3_title.shift(-indent)` after `next_to`.
    # Let's align explicitly to the margin to be safe.
    
    step_3_title.set_x((anchors['left'] + anchors['margin'])[0] + step_3_title.width/2)

    correction_formula = MathTex(
        r"\Delta Q = - \frac{\sum H_i}{n \sum_i |H_i/Q_i|}",
        color=BLACK
    ).scale(1.0)
    correction_formula.next_to(step_3_title, DOWN, buff=0.3, aligned_edge=LEFT)
    correction_formula.shift(anchors['indent'])
    
    delta_q_label = MathTex(r"\Delta Q =", color=BLACK).scale(0.8)
    delta_q_label.next_to(correction_formula, DOWN, buff=0.5, aligned_edge=LEFT)
    delta_q_label.shift(0.5 * RIGHT) # Small extra indent for result

    return VGroup(step_3_title, correction_formula, delta_q_label)
