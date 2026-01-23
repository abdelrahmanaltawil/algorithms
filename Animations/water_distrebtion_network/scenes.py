from manim import *
import numpy as np
import heapq
import sys
import os

# Ensure we can import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from helpers.physics import WaterNetwork
from helpers.geometry import create_network_mobjects
from helpers.annotations import create_velocity_labels, create_node_labels, get_p_color
from helpers.utils import load_config

# --- Load Configuration ---
script_dir = os.path.dirname(os.path.abspath(__file__))
INPUTS = load_config(os.path.join(script_dir, 'inputs.yaml'))
NET_CONFIG = INPUTS['network']
GLOBAL_PHYSICS = INPUTS['global']['physics']
DISPLAY_CONFIG = INPUTS['display']

config.pixel_height = 2160
config.pixel_width = 3840
config.frame_rate = 60
config.disable_caching = True

WX_BLUE = DISPLAY_CONFIG['colors']['water_blue']

class WaterDistributionScene(Scene):
    def construct(self):
        # 1. Physics: Setup and Solve Network from Config
        net = WaterNetwork()
        
        # Load Nodes
        for node_key, node_data in NET_CONFIG['nodes'].items():
            net.add_node(
                id=node_data['id'],
                x=node_data['pos'][0],
                y=node_data['pos'][1],
                elevation=node_data['elevation'],
                demand=node_data['demand']
            )
            
        # Load Pipes
        # Sorting by ID to ensure consistent indexing if needed
        sorted_pipes = sorted(NET_CONFIG['pipes'].items(), key=lambda item: item[1].get('id', 999))
        
        for pipe_key, pipe_data in sorted_pipes:
            net.add_pipe(
                start_id=pipe_data['start'],
                end_id=pipe_data['end'],
                length=pipe_data['length'],
                diameter=pipe_data['diameter'],
                c=GLOBAL_PHYSICS.get('default_roughness', 100)
            )
            
        # MANUAL FLOW SETTING (For Dead-End / Branch Line)
        # We set flow rates from config directly instead of solving
        sorted_pipe_keys = [k for k, v in sorted_pipes]
        
        for i, (pipe_key, pipe_data) in enumerate(sorted_pipes):
            # net.pipes list order matches insertion order.
            # Since we inserted in sorted order of ID, i should match if IDs are 0..N
            # But safer to just set it on the pipe object we just added implicitly?
            # Actually net.pipes is a list.
            # Let's verify: net.add_pipe appends to self.pipes.
            # So net.pipes[i] corresponds to sorted_pipes[i].
            
            p = net.pipes[i]
            if 'flow' in pipe_data:
                p.flow_rate = pipe_data['flow']
            else:
                p.flow_rate = 0 # Default or Warning
            
            # Update Hydraulic Properties (Head Loss, Velocity)
            p.calculate_head_loss()
            p.update_velocity()

        # No Loops defined for this topology
        
        # Propagate Pressure
        # Assuming Node 0 is source
        source_id = 0 
        # Find source node from config if marked
        for n_key, n_data in NET_CONFIG['nodes'].items():
            if n_data.get('type') == 'source':
                source_id = n_data['id']
                break
                
        net.calculate_pressures(source_id, GLOBAL_PHYSICS['source_pressure_head'])

        # 2. Geometry & Annotations
        title = Text("Branching Water Distribution System", font_size=36).to_edge(UP)
        subtitle = Text("Dead-End Network Simulation", font_size=24, color=BLUE).next_to(title, DOWN)
        self.play(Write(title), FadeIn(subtitle))
        
        pipe_mobjects, node_mobjects = create_network_mobjects(net)
        labels = create_velocity_labels(net, pipe_mobjects)
        # node_labels = create_node_labels(net, node_mobjects)
        
        # for n, lbl in node_labels.items():
        #     labels[n] = lbl

        # --- ANIMATION SEQUENCE ---

        # 1. Show Static Network (Faded In, Grey)
        self.play(
            FadeIn(VGroup(*pipe_mobjects.values())),
            FadeIn(VGroup(*node_mobjects.values())),
            FadeIn(VGroup(*labels.values())),
            run_time=1.5
        )
        self.wait(0.5)

        # 2. Global Time-Scheduled Flow Animation
        # Use Dijkstra's Algorithm to find min arrival time T for every node.
        
        def clamp(val, min_v, max_v):
            return max(min_v, min(val, max_v))
            
        # Initialize Dijkstra
        node_times = {nid: float('inf') for nid in net.nodes}
        node_times[0] = 0.0
        
        pq = [(0.0, 0)] # (time, node_id)
        pipe_schedules = {} # pipe_obj -> (start_time, duration)
        
        while pq:
            curr_time, u = heapq.heappop(pq)
            if curr_time > node_times[u]: continue
            
            downstream = net.get_downstream_neighbors(u)
            for v, p in downstream:
                if abs(p.velocity) > 1e-4:
                    phys_time = p.length / abs(p.velocity)
                    anim_time = clamp(phys_time / 60.0, 0.5, 2.5)
                else:
                    anim_time = 0.5
                
                arrival_time = curr_time + anim_time
                pipe_schedules[p] = (curr_time, anim_time, u, v)
                
                if arrival_time < node_times[v]:
                    node_times[v] = arrival_time
                    heapq.heappush(pq, (arrival_time, v))
        
        # Build Flat Animation List
        all_anims = []
        
        # 1. Pipes
        for p, (start_t, dur, u, v) in pipe_schedules.items():
            start_pos = net.nodes[u].pos
            end_pos = net.nodes[v].pos
            water_line = Line(start_pos, end_pos, stroke_width=p.diameter*20, color=WX_BLUE)
            
            if start_t > 0:
                anim = Succession(Wait(start_t), Create(water_line, run_time=dur, rate_func=linear))
            else:
                anim = Create(water_line, run_time=dur, rate_func=linear)
            all_anims.append(anim)
            
        # 2. Nodes
        for nid, t in node_times.items():
            if t == float('inf'): continue 
            if t > 0:
                anim = Succession(Wait(t), node_mobjects[net.nodes[nid]].animate.set_color(WX_BLUE).set_run_time(0.2))
            else:
                anim = node_mobjects[net.nodes[nid]].animate.set_color(WX_BLUE).set_run_time(0.2)
            all_anims.append(anim)

        # Play Everything Together
        self.play(AnimationGroup(*all_anims, lag_ratio=0))
        
        self.wait(1)
        
        # Phase 3: Pressure Heatmap
        heatmap_title = Text("Pressure Distribution Heatmap", font_size=28, color=YELLOW).next_to(title, DOWN)
        self.play(FadeOut(subtitle), Write(heatmap_title))
        
        # Legend
        bar = Rectangle(height=0.3, width=4).to_edge(DOWN, buff=1)
        bar.set_fill(color=[BLUE, YELLOW, RED], opacity=1)
        bar.rotate(PI)
        bar.set_stroke(width=0)
        
        pressures = [n.pressure for n in net.nodes.values()]
        min_p, max_p = min(pressures), max(pressures)
        
        min_lbl = Text(f"{min_p:.1f} kPa", font_size=16).next_to(bar, LEFT)
        max_lbl = Text(f"{max_p:.1f} kPa", font_size=16).next_to(bar, RIGHT)
        mid_lbl = Text("Pressure", font_size=16).next_to(bar, DOWN)
        
        legend = VGroup(bar, min_lbl, max_lbl, mid_lbl)
        self.play(FadeIn(legend))
        

        node_labels = create_node_labels(net, node_mobjects)
        for n, lbl in node_labels.items():
            labels[n] = lbl

        # Heatmap Coloring & Label Moving
        transforms = []
        for n in net.nodes.values():
            col = get_p_color(n.pressure, min_p, max_p)
            transforms.append(node_mobjects[n].animate.set_color(col).set_width(0.4).set_z_index(10))
            
            if n.id in node_labels:
                lbl = node_labels[n.id]
                transforms.append(lbl.animate.next_to(node_mobjects[n], UP, buff=0.15).set_z_index(20))
        
        for p in net.pipes:
            if p.flow_rate >= 0:
                u, v = net.nodes[p.start_node], net.nodes[p.end_node]
            else:
                u, v = net.nodes[p.end_node], net.nodes[p.start_node]
            
            start_col = get_p_color(u.pressure, min_p, max_p)
            end_col = get_p_color(v.pressure, min_p, max_p)
            
            line = pipe_mobjects[p]
            transforms.append(
                line.animate.set_stroke(opacity=1, width=p.diameter*20)
                .set_color(color=[start_col, end_col])
                .set_z_index(5)
            )
            
        for lbl in labels.values():
            if isinstance(lbl, VGroup): # Velocity Label
                 transforms.append(lbl.animate.set_z_index(20))

        self.play(*transforms, run_time=2)
        
        fade_outs = [FadeOut(labels[p]) for p in net.pipes if p in labels]
        self.play(*fade_outs)
        
        self.wait(3)
