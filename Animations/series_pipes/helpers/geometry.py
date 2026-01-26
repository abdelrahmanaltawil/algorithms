from manim import *
import numpy as np

def get_pipe_visual_width(diameter_mm, scale_factor):
    """Calculates visual stroke width based on diameter."""
    return diameter_mm * scale_factor * 10 # Multiplier for visibility

def create_pipe_path(start_pos, end_pos, pipe_config):
    """
    Generates the VMobject path for a pipe based on its type.
    """
    pipe_type = pipe_config.get('type', 'straight')
    
    path = VMobject()
    path.set_points_as_corners([start_pos, start_pos]) # Init
    
    if pipe_type == 'straight':
        path.set_points_as_corners([start_pos, end_pos])
        
    elif pipe_type == 'arc':
        angle = pipe_config.get('arc_angle', 0)
        if angle == 0:
             path.set_points_as_corners([start_pos, end_pos])
        else:
             # Manim's ArcBetweenPoints
             # angle < 0 curves one way, > 0 the other
             path = ArcBetweenPoints(start_pos, end_pos, angle=angle)
             
    elif pipe_type in ['rectangular_top', 'rectangular_bottom']:
        offset_y = pipe_config.get('offset_y', 0)
        radius = 1.5  # Increased for smoother transitions
        
        # Adjust radius if offset is small
        if abs(offset_y) < radius:
            radius = abs(offset_y)
            
        # Coordinates
        x1, y1 = start_pos[0], start_pos[1]
        x2, y2 = end_pos[0], end_pos[1] # y2 should be same as y1 usually
        y_pipe = y1 + offset_y
        
        # Directions
        # If offset > 0 (Top): Up -> Right -> Down
        # If offset < 0 (Bottom): Down -> Right -> Up
        
        sign = 1 if offset_y > 0 else -1
        
        # Points for geometric construction
        # P1: Start
        # P2_pre_turn: (x1, y_pipe - sign*R)
        # Turn 1 Center: (x1 + R, y_pipe - sign*R)
        # P2_post_turn: (x1 + R, y_pipe)
        
        # P3_pre_turn: (x2 - R, y_pipe)
        # Turn 2 Center: (x2 - R, y_pipe - sign*R)
        # P3_post_turn: (x2, y_pipe - sign*R)
        # P4: End
        
        p1 = start_pos
        p2_pre = np.array([x1, y_pipe - sign*radius, 0])
        p2_post = np.array([x1 + radius, y_pipe, 0])
        
        p3_pre = np.array([x2 - radius, y_pipe, 0])
        p3_post = np.array([x2, y_pipe - sign*radius, 0])
        p4 = end_pos
        
        # Construct Path segments
        path = VMobject()
        path.set_points_as_corners([p1, p1]) # Initialize
        
        # 1. Vertical Rise
        l1 = Line(p1, p2_pre)
        path.append_points(l1.get_points())
        
        # 2. First Turn (90 deg)
        # From Vertical to Horizontal
        # Top: Up to Right. Tangent UP (PI/2) -> Angle -PI/2 (Clockwise) ??
        # No, Up is PI/2. Right is 0. Delta is -PI/2.
        # Bot: Down to Right. Tangent DOWN (-PI/2 or 3PI/2). Right is 0. Delta is +PI/2 (Counter-Clockwise).
        
        start_angle = PI/2 if sign > 0 else -PI/2
        sweep_angle = -PI/2 if sign > 0 else PI/2
        
        # Arc center determination
        # Center is (x1 + R, y_pipe - sign*R)
        arc_center1 = np.array([x1 + radius, y_pipe - sign*radius, 0])
        
        # ArcBetweenPoints is easier if we know points?
        # But simple Arc is cleaner for exact 90 deg.
        arc1 = Arc(radius=radius, start_angle=PI - start_angle, angle=sweep_angle, arc_center=arc_center1)
        # Wait, start_angle definition for Arc: 0 is Right.
        # For Top: Center is (x1+R, y_pipe-R). Start point is (x1, y_pipe-R). This is LEFT of center. So Angle is PI.
        # End point is (x1+R, y_pipe). This is TOP of center. Angle is PI/2.
        # Sweep is PI -> PI/2. Delta is -PI/2. Correct.
        
        # For Bot: Center is (x1+R, y_pipe-(-R)) = (x1+R, y_pipe+R). 
        # Start point is (x1, y_pipe+R). LEFT of center. Angle PI.
        # End point is (x1+R, y_pipe). BOTTOM of center. Angle 3PI/2 (-PI/2).
        # Sweep is PI -> 3PI/2. Delta +PI/2? No.
        # PI to -PI/2 is -1.5PI...
        # Let's verify angles.
        # Arc 1 Top: Start at PI (Left). Sweep -PI/2 (CW) to PI/2 (Up). Correct.
        # Arc 1 Bot: Start at PI (Left). Sweep +PI/2 (CCW) to 3PI/2 (Down)? No, 3PI/2 is down.
        # Wait, if y_pipe is below, center is (x1+R, y_pipe+R).
        # P2_pre is (x1, y_pipe+R). Left of center. PI.
        # P2_post is (x1+R, y_pipe). Below center. -PI/2.
        # PI to -PI/2 is +PI/2 direction? No. PI + PI/2 = 3PI/2. Yes.
        
        angle_start1 = PI
        angle_sweep1 = -sign * PI/2
        
        arc1 = Arc(radius=radius, start_angle=angle_start1, angle=angle_sweep1, arc_center=arc_center1)
        path.append_points(arc1.get_points())
        
        # 3. Horizontal Run
        l2 = Line(p2_post, p3_pre)
        path.append_points(l2.get_points())
        
        # 4. Second Turn (90 deg)
        # From Horizontal to Vertical
        # Top: Right to Down.
        # Bot: Right to Up.
        # Center 2: (x2 - R, y_pipe - sign*R)
        arc_center2 = np.array([x2 - radius, y_pipe - sign*radius, 0])
        
        # Top: Start P3_pre (x2-R, y_pipe). Relative to center: UP (PI/2).
        # End P3_post (x2, y_pipe-R). Relative to center: RIGHT (0).
        # Sweep: PI/2 -> 0. Angle -PI/2.
        
        # Bot: Start P3_pre (x2-R, y_pipe). Relative: DOWN (-PI/2).
        # End P3_post (x2, y_pipe+R). Relative: RIGHT (0).
        # Sweep: -PI/2 -> 0. Angle +PI/2.
        
        angle_start2 = sign * PI/2
        angle_sweep2 = -sign * PI/2
        
        arc2 = Arc(radius=radius, start_angle=angle_start2, angle=angle_sweep2, arc_center=arc_center2)
        path.append_points(arc2.get_points())
        
        # 5. Vertical Drop
        l3 = Line(p3_post, p4)
        path.append_points(l3.get_points())
        
    return path

def create_system_mobjects(nodes_config, pipes_config, display_config):
    """
    Creates Manim mobjects for all nodes, pipes, and streamlines.
    
    Returns:
        tuple: (node_mobjects, pipe_mobjects, streamlines)
            - node_mobjects: dict mapping node_id -> Dot mobject
            - pipe_mobjects: dict mapping pipe_key -> VGroup(outline, path)
            - streamlines: dict mapping branch_id -> full streamline path
    """
    node_mobjects = {}
    pipe_mobjects = {}
    
    # Scale
    scale = display_config['scales']['pipe_width_factor']
    
    # 1. Create Nodes (Invisible - used only for positioning)
    for key, data in nodes_config.items():
        pos = np.array(data['pos'])
        dot = Dot(point=pos, color=WHITE, radius=0.08).set_opacity(0)
        node_mobjects[data['id']] = dot
    
    # 2. Create Pipes
    old_width = 0 # To handle outline transition
    for key, data in pipes_config.items():
        start_id = data['start_node']
        end_id = data['end_node']
        
        start_pos = node_mobjects[start_id].get_center()
        end_pos = node_mobjects[end_id].get_center()
        
        # Path (Inner / Main Fill)
        path = create_pipe_path(start_pos, end_pos, data)
        path.set_color(BLUE)
        
        # Stroke Width visual
        width = get_pipe_visual_width(data['diameter_mm'], scale)
        path.set_stroke(width=width)
        
        # Outline (Outer / Border)
        outline = path.copy()
        outline.set_color(BLACK)
        outline.set_stroke(width=width + 16)
        
        if old_width != 0 and abs(width - old_width) > 1:

            max_width = max(width, old_width)*0.011

            cap = Line(
                start_pos + [0, max_width/2, 0],
                start_pos - [0, max_width/2, 0],
                stroke_width= 16,
                stroke_color= BLACK
            )
            outline.add(cap)
        
        pipe_group = VGroup(outline, path)
        pipe_mobjects[key] = pipe_group
        old_width = width


    # 3. Create Streamline for Series
    # Sequence: inlet -> A -> B -> C -> outlet
    streamlines = {}
    
    # 3. Create Streamline for Series
    # Dynamic sequence based on pipe keys in standard order if possible, 
    # but for this specific "series" template we can just look for what we know.
    # Updated for simple case: inlet -> A -> outlet
    
    # We can try to sort them or just list the potential ones.
    # Let's check which ones exist.
    possible_keys = ['pipe_inlet', 'pipe_A', 'pipe_outlet']
    actual_keys = [k for k in possible_keys if k in pipe_mobjects]
    
    if actual_keys:
        # Collect paths
        paths = [pipe_mobjects[k][1] for k in actual_keys]
        
        # Compose them
        full_streamline = _compose_multi_segment_path(paths)
        streamlines['main'] = full_streamline

    return node_mobjects, pipe_mobjects, streamlines


def _compose_multi_segment_path(path_list):
    """
    Composes a single continuous VMobject path from a list of sequential paths.
    
    Args:
        path_list (list): List of VMobjects (pipes) in order.
        
    Returns:
        VMobject: A single continuous path.
    """
    all_points = []
    
    for path in path_list:
        # Sample points along the path
        # 10 samples per segment is usually enough for straight lines
        # For curves we might want more, but Manim handles linear interpolation well
        for alpha in np.arange(0, 1.05, 0.05): # inclusive of 1 approx
            # Clamp alpha to 1
            if alpha > 1: alpha = 1
            all_points.append(path.point_from_proportion(alpha))
            
    # Create smooth path through all points
    streamline = VMobject()
    if all_points:
        streamline.set_points_as_corners(all_points)
        # Optional: verify smoothness?
        # For series pipes which are corners, corners is correct.
    
    return streamline

