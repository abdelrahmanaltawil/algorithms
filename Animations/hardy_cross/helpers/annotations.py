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

def create_flow_labels(config, pipe_map):
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
        
        label_text = MathTex(f"Q = {flow_mag}", color=visuals['label_color'])
        label_text.scale(0.7)
        
        # Position label
        # Use label_offset from config if available, relative to midpoint
        offset = np.array(data.get('label_offset', [0, 0, 0]))
        offset[offset != 0] = math.copysign(abs(offset[offset != 0]) + 0.3, offset[offset != 0])
        
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
            
    return loop_group

def create_correction_formula():
    """
    Returns a MathTex object for the Hardy Cross correction formula.
    """
    formula = MathTex(
        r"\Delta Q = -\frac{\sum r Q |Q|^{n-1}}{\sum n r |Q|^{n-1}}",
        color=BLACK
    )
    formula.scale(1.2)
    formula.to_edge(DOWN)

    return formula
