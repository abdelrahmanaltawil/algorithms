from manim import *
import numpy as np
from helpers.physics import WaterNetwork
from helpers.geometry import create_network_mobjects
from helpers.annotations import create_velocity_labels, create_node_labels, get_p_color

config.pixel_height = 2160
config.pixel_width = 3840
config.frame_rate = 60

WX_BLUE = "#2980b9"

class WaterDistributionScene(Scene):
    def construct(self):
        # 1. Physics: Setup and Solve Network
        net = WaterNetwork()
        node_positions = {
            0: [-4, 2, 0], 1: [-2, 2, 0], 2: [0, 2, 0],
            3: [-2, 0, 0], 4: [0, 0, 0],
            5: [-2, -2, 0], 6: [0, -2, 0]
        }
        for nid, pos in node_positions.items():
            demand = 0.05 if nid != 0 else -0.3
            net.add_node(nid, pos[0], pos[1], elevation=10, demand=demand)
            
        pipes_def = [
            (0, 1, 200, 0.4), # P0
            (1, 2, 100, 0.2), # P1
            (3, 4, 100, 0.2), # P2
            (5, 6, 100, 0.2), # P3
            (1, 3, 100, 0.2), # P4
            (2, 4, 100, 0.2), # P5
            (3, 5, 100, 0.2), # P6
            (4, 6, 100, 0.2)  # P7
        ]
        for s, e, l, d in pipes_def:
            net.add_pipe(s, e, l, d)

        # Initial Guesses
        guesses = [0.3, 0.1, 0.05, 0.0, 0.15, 0.05, 0.05, 0.05]
        for i, g in enumerate(guesses):
            net.pipes[i].flow_rate = g

        # Loop Definition
        loop1 = [(1, 1), (5, 1), (2, -1), (4, -1)]
        loop2 = [(2, 1), (7, 1), (3, -1), (6, -1)]
        net.define_loops([loop1, loop2])
        
        # Solve
        net.solve_hardy_cross()
        net.calculate_pressures(0, 50.0)

        # 2. Geometry & Annotations
        title = Text("Water Distribution Network Simulation", font_size=36).to_edge(UP)
        subtitle = Text("Hardy Cross Method: Flow, Velocity & Pressure", font_size=24, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        
        pipe_mobjects, node_mobjects = create_network_mobjects(net)
        labels = create_velocity_labels(net, pipe_mobjects)
        node_labels = create_node_labels(net, node_mobjects)
        
        for n, lbl in node_labels.items():
            labels[n] = lbl

        # --- ANIMATION SEQUENCE ---

        # 1. Show Static Network (Faded In, Grey)
        self.play(
            FadeIn(VGroup(*pipe_mobjects.values())),
            FadeIn(VGroup(*node_mobjects.values())),
            FadeIn(VGroup(*labels.values())),
            run_time=1.5
        )
        self.wait(0.5)

        # 2. Recursive Asynchronous Flow
        # Construct ad-hoc Flow Adjacency
        flow_adj = {n_id: [] for n_id in net.nodes}
        for p in net.pipes:
            if p.flow_rate >= 0:
                u, v = p.start_node, p.end_node
            else:
                u, v = p.end_node, p.start_node
            flow_adj[u].append((v, p))

        # We need a function to generate the animation tree
        # To avoid infinite recursion in loops, we track depth or path.
        # But for animation construction, we can't easily pass state that updates *during* animation.
        # However, we can build the tree *assuming* the structure.
        # Since it's a DAG (for flow usually, or we stop at cycles)?
        # Hardy Cross solves for steady state, so flow is directional. 
        # Cycles are possible physically (circulation), but usually sources->sinks.
        # We'll use a `max_depth` to be safe.

        def clamp(val, min_v, max_v):
            return max(min_v, min(val, max_v))

        def get_flow_animation(u_id, depth=0):
            if depth > 10: return Wait(0.1) # Safety break
            
            branches = []
            
            # For each outgoing pipe
            for v_id, p in flow_adj[u_id]:
                # Create water line (New Instance for this branch)
                start_pos = net.nodes[u_id].pos
                end_pos = net.nodes[v_id].pos
                water_line = Line(start_pos, end_pos, stroke_width=p.diameter*20, color=WX_BLUE)
                
                # Animation Duration (T = L/v)
                if abs(p.velocity) > 1e-4:
                    phys_time = p.length / abs(p.velocity)
                    anim_time = clamp(phys_time / 60.0, 0.5, 2.5)
                else:
                    anim_time = 0.5
                
                # Branch Animation Sequence
                branch_anim = Succession(
                    # 1. Fill Pipe
                    Create(water_line, run_time=anim_time, rate_func=linear),
                    # 2. Color Destination Node (Instant)
                    node_mobjects[net.nodes[v_id]].animate.set_color(WX_BLUE).set_run_time(0.2),
                    # 3. Trigger Downstream recursively
                    get_flow_animation(v_id, depth+1)
                )
                branches.append(branch_anim)
            
            if not branches:
                return Wait(0.1) # Leaf node
            
            # Run all branches in parallel (async)
            return AnimationGroup(*branches)

        # Start from Source
        # Color Source Node first
        self.play(node_mobjects[net.nodes[0]].animate.set_color(WX_BLUE), run_time=0.2)
        
        # Build and Run Tree
        flow_anim_tree = get_flow_animation(0)
        self.play(flow_anim_tree)
        
        self.wait(1)
        
        # Phase 3: Pressure Heatmap
        heatmap_title = Text("Pressure Distribution Heatmap", font_size=28, color=YELLOW).next_to(title, DOWN)
        self.play(FadeOut(subtitle), Write(heatmap_title))
        
        # Legend
        bar = Rectangle(height=4, width=0.3).to_edge(RIGHT, buff=1)
        bar.set_fill(color=[BLUE, YELLOW, RED], opacity=1)
        bar.set_stroke(width=0)
        
        pressures = [n.pressure for n in net.nodes.values()]
        min_p, max_p = min(pressures), max(pressures)
        
        min_lbl = Text(f"{min_p:.1f} kPa", font_size=16).next_to(bar, DOWN)
        max_lbl = Text(f"{max_p:.1f} kPa", font_size=16).next_to(bar, UP)
        mid_lbl = Text("Pressure", font_size=16).rotate(PI/2).next_to(bar, LEFT)
        
        legend = VGroup(bar, min_lbl, max_lbl, mid_lbl)
        self.play(FadeIn(legend))
        
        # Heatmap Coloring
        transforms = []
        for n in net.nodes.values():
            col = get_p_color(n.pressure, min_p, max_p)
            transforms.append(node_mobjects[n].animate.set_color(col).set_width(0.4).set_z_index(10))
        
        # Bring base pipes to front and color them
        for p in net.pipes:
            if p.flow_rate >= 0:
                u, v = net.nodes[p.start_node], net.nodes[p.end_node]
            else:
                u, v = net.nodes[p.end_node], net.nodes[p.start_node]
            
            start_col = get_p_color(u.pressure, min_p, max_p)
            end_col = get_p_color(v.pressure, min_p, max_p)
            
            line = pipe_mobjects[p]
            # Ensure it's opaque, colorful, and ON TOP (z_index=5)
            # Water lines are z=0 by default.
            transforms.append(
                line.animate.set_stroke(opacity=1, width=p.diameter*20)
                .set_color(color=[start_col, end_col])
                .set_z_index(5)
            )
            
        # Also bring labels to front if they are to remain visible
        # (Though we fade them out right after, the fade out happens during or after transform?)
        # THe code says self.play(*transforms), then self.play(*fadeouts).
        # So labels should be visible during heatmap transition.
        for lbl in labels.values():
            transforms.append(lbl.animate.set_z_index(20))

        self.play(*transforms, run_time=2)
        
        # Remove labels
        fade_outs = [FadeOut(labels[p]) for p in net.pipes if p in labels]
        self.play(*fade_outs)
        
        self.wait(3)
