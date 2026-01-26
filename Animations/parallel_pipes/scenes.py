"""
Parallel Pipes Animation
Visualizes flow distribution through three parallel pipes with streamline-based particles.
"""
from manim import *
import numpy as np
import random
import sys
import os

# Add helpers to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from helpers.utils import load_config
from helpers.geometry import create_system_mobjects
from helpers.physics import calculate_parallel_flows, calculate_system_heads
from helpers.annotations import create_flow_label, create_head_label, create_flow_arrow

# Load configuration
script_dir = os.path.dirname(os.path.abspath(__file__))
INPUTS = load_config(os.path.join(script_dir, 'inputs.yaml'))


class ParallelPipesScene(Scene):
    """Main scene demonstrating parallel pipe flow."""
    
    def construct(self):
        # Load configuration
        nodes_cfg = INPUTS['network']['nodes']
        pipes_cfg = INPUTS['network']['pipes']
        disp_cfg = INPUTS['display']
        phys_cfg = INPUTS['physics']['fluid']
        
        # Build geometry (nodes, pipes, streamlines)
        nodes_mobs, pipes, streamlines = create_system_mobjects(
            nodes_cfg, pipes_cfg, disp_cfg
        )
        
        # Get streamline paths
        streamline_a = streamlines['A']
        streamline_b = streamlines['B']
        streamline_c = streamlines['C']
        
        # Style streamlines
        for sl in [streamline_a, streamline_b, streamline_c]:
            sl.set_style(fill_opacity=0.9, stroke_color=BLUE, stroke_width=2)
        
        # Create simplified groups for fluid and walls
        fluid_body = VGroup()
        walls = VGroup()
        
        # Iterate through all pipes to collect their components
        pipe_keys = ['pipe_inlet', 'pipe_A', 'pipe_B', 'pipe_C', 'pipe_outlet']
        
        for key in pipe_keys:
            if key in pipes:
                # pipes[key] is a group: [0]=Outline, [1]=Path(Fluid)
                outline = pipes[key][0]
                fluid = pipes[key][1]
                
                # Style fluid
                fluid.set_color(BLUE)
                
                # Add to respective global groups
                walls.add(outline)
                fluid_body.add(fluid)
        
        # Layering: Fluid ON TOP of Walls
        walls.set_z_index(0)
        fluid_body.set_z_index(1)
        
        # Animation Sequence:
        self.play(FadeIn(fluid_body), run_time=1)
        self.play(Create(walls), run_time=1.5)

        # --- Annotations & Physics Calcs ---
        # 1. Calculate Flows
        total_q = phys_cfg['total_flow_rate']
        parallel_data = [pipes_cfg[f'pipe_{pid}'] for pid in ['A', 'B', 'C']]
        flows = calculate_parallel_flows(total_q, parallel_data)
        flows['inlet'] = total_q
        flows['outlet'] = total_q
        
        # 2. Calculate Heads and Velocities
        # Merging physics inputs for convenience
        combined_phys = {**INPUTS['physics']['fluid'], **INPUTS['physics']}
        node_heads, pipe_velocities = calculate_system_heads(nodes_cfg, pipes_cfg, flows, combined_phys)
        
        # Create Flow Labels
        annotations_labels = VGroup()
        
        flow_lbl_inlet = create_flow_label(pipes['pipe_inlet'][1], flows['inlet'], "inlet", direction=UP, buff=0.6)
        flow_lbl_outlet = create_flow_label(pipes['pipe_outlet'][1], flows['outlet'], "outlet", direction=UP, buff=0.6)
        flow_lbl_A = create_flow_label(pipes['pipe_A'][1], flows['A'], "A", direction=UP, buff=0.6)
        flow_lbl_B = create_flow_label(pipes['pipe_B'][1], flows['B'], "B", direction=UP, buff=0.6)
        flow_lbl_C = create_flow_label(pipes['pipe_C'][1], flows['C'], "C", direction=DOWN, buff=0.6)

        # annotations_labels.add(flow_lbl_inlet, flow_lbl_outlet, flow_lbl_A, flow_lbl_B, flow_lbl_C)
        flow_lbls = VGroup(flow_lbl_inlet, flow_lbl_A, flow_lbl_B, flow_lbl_C, flow_lbl_outlet)
        self.play(Create(flow_lbls), run_time=0.5)

        # Head Labels at Nodes
        # Start Node (0), Junction 1 (1), Junction 2 (2), End Node (3)
        for nid, val in node_heads.items():
            if nid in nodes_mobs:
                pos = nodes_mobs[nid].get_center()
                
                label_offset = UP * 1.8 # General high placement
                if nid == 0: # Inlet Start
                     label_offset = UP * 1.2
                elif nid == 1: # Split
                     label_offset = UP * 1.2 + LEFT * 0.5
                elif nid == 2: # Merge
                     label_offset = UP * 1.2 + RIGHT * 0.5
                
                head_lbl = create_head_label(val, pos + label_offset)
                annotations_labels.add(head_lbl)
        
        # Layering: Annotations on top
        # annotations_labels.set_z_index(10)
        # self.play(FadeIn(annotations_labels))

        # --- Particle Animation ---
        def create_particles_with_offset(path, num_particles, speed, offset_range=0.3):
            """
            Generate particles for a batch injection.
            Particles start with negative alpha to flow in from the inlet.
            """
            particles = VGroup()
            for _ in range(num_particles):
                dot = Dot(radius=0.04, color=BLACK)
                
                # Distribute particles in a "batch" behind the inlet
                alpha = random.uniform(-0.5, 0.0)
                
                # Random offset from path center
                offset = random.uniform(-offset_range, offset_range)
                
                dot.virt_alpha = alpha      # Virtual position (starts before pipe)
                dot.virt_offset = offset    # Offset from path center
                dot.speed = speed           # Speed along path
                dot.path_ref = path         # Reference to path
                
                # Initial position (hidden)
                dot.set_opacity(0)
                base_pos = path.point_from_proportion(0)
                dot.move_to(base_pos)
                
                particles.add(dot)
            return particles
        
        def get_offset_path_updater():
            """
            Returns updater that moves particles along paths.
            Handles visibility (show only when 0 <= alpha <= 1).
            """
            def update_particles(mob, dt):
                for dot in mob:
                    # Update virtual position
                    dot.virt_alpha += dot.speed * dt
                        
                    # Determine visibility and position
                    if 0 <= dot.virt_alpha <= 1:
                        dot.set_opacity(1)
                        # Get base position on path
                        base_pos = dot.path_ref.point_from_proportion(dot.virt_alpha)
                        # Apply offset
                        dot.move_to(base_pos + np.array([0, dot.virt_offset, 0]))
                    else:
                        dot.set_opacity(0)
                        
            return update_particles
        
        # Factor to scale velocities for visualization
        damping_factor = 0.5
        A_v_factored = pipe_velocities['pipe_A'] * damping_factor
        B_v_factored = pipe_velocities['pipe_B'] * damping_factor
        C_v_factored = pipe_velocities['pipe_C'] * damping_factor
        
        # Create particles on each streamline
        all_particles = VGroup()
        
        # Branch A (top)
        particles_a = create_particles_with_offset(streamline_a, 15, A_v_factored, offset_range=0.12)
        all_particles.add(*particles_a)
        
        # Branch B (middle) - more particles
        particles_b = create_particles_with_offset(streamline_b, 20, B_v_factored, offset_range=0.10)
        all_particles.add(*particles_b)
        
        # Branch C (bottom)
        particles_c = create_particles_with_offset(streamline_c, 15, C_v_factored, offset_range=0.11)
        all_particles.add(*particles_c)
        
        # Layering: Boost Z-index to ensure on top of fluid
        all_particles.set_z_index(100)
        
        self.add(all_particles)
        all_particles.add_updater(get_offset_path_updater())
        self.wait(4)
        all_particles.clear_updaters()
        
        # Arrows (closer to pipe than labels)
        arrow_inlet = create_flow_arrow(pipes['pipe_inlet'][1], direction=UP, buff=-0.15)
        arrow_outlet = create_flow_arrow(pipes['pipe_outlet'][1], direction=UP, buff=-0.15)
        arrow_A = create_flow_arrow(pipes['pipe_A'][1], direction=UP, buff=-0.15)
        arrow_B = create_flow_arrow(pipes['pipe_B'][1], direction=UP, buff=-0.15)
        arrow_C = create_flow_arrow(pipes['pipe_C'][1], direction=DOWN, buff=-0.2)
        
        arrows = VGroup(arrow_inlet, arrow_A, arrow_B, arrow_C, arrow_outlet).set_z_index(10)
        self.play(Create(arrows))


        self.wait(3)