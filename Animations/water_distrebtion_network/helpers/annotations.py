from manim import *

def create_velocity_labels(network, pipe_mobjects):
    """Creates velocity labels for each pipe."""
    labels = {}
    for p in network.pipes:
        line = pipe_mobjects[p]
        angle = line.get_angle()
        
        # Ensure text is readable (not upside down)
        # If angle is > 90 or < -90, flip it?
        # Manim angles are in radians. PI/2 = 1.57
        # If angle > PI/2 or angle < -PI/2, the text might appear entering from right to left?
        # Actually user said "rotated right to it when vertical".
        # Vertical = PI/2.
        # Let's keep the rotation strictly aligned with the line for now, 
        # but maybe flip if it's going backwards (End < Start x).
        # Actually simplest is just rotate by line.get_angle().
        
        v_lbl = MathTex(f"v={p.velocity:.2f} m/s", font_size=16, color=WHITE)
        v_lbl.move_to(line.get_center())
        v_lbl.rotate(angle)
        
        # Shift "Above" the line relative to the line's orientation
        # "Above" means +Y in local frame.
        # We need normal vector.
        # Normal vector to line direction (cos t, sin t) is (-sin t, cos t)? Or (sin -t, cos t)?
        # Manim's UP is (0, 1, 0).
        # Rotating UP by angle gives the local "Above" direction.
        shift_vec = rotate_vector(UP, angle) 
        v_lbl.shift(0.2 * shift_vec)

        labels[p] = VGroup(v_lbl)
    return labels

def create_node_labels(network, node_mobjects):
    """Creates pressure labels for each node."""
    labels = {}
    for n in network.nodes.values():
        lbl_group = VGroup(
            Text(f"N{n.id}", font_size=16, weight=BOLD),
            Text(f"P: {n.pressure:.1f} kPa", font_size=14, color=WHITE)
        ).arrange(DOWN, buff=0.05).next_to(n.pos, DR, buff=0.05)
        bg = BackgroundRectangle(lbl_group, color=BLACK, fill_opacity=0.0, buff=0.05)
        labels[n] = VGroup(bg, lbl_group)
    return labels

def get_p_color(p, min_p, max_p):
    """Returns color based on pressure value interp within range."""
    if max_p == min_p: return interpolate_color(BLUE, RED, 0.5)
    val = (p - min_p) / (max_p - min_p)
    if val < 0.5:
        return interpolate_color(BLUE, YELLOW, val*2)
    else:
        return interpolate_color(YELLOW, RED, (val-0.5)*2)
