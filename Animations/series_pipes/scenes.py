"""
Series Pipes Animation
Visualizes flow through a series of connected pipes with varying diameters.
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


class SeriesPipesScene(Scene):
    """Main scene demonstrating flow through pipes in series."""
    
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
        
        # Get streamline path
        main_streamline = streamlines.get('main')
        if not main_streamline:
            print("Error: Main streamline not found!")
            return
        
        # Style streamline (invisible guide usually, but let's make it visible for debug if needed, or just rely on particles)
        main_streamline.set_style(fill_opacity=0, stroke_width=0)
        
        # Create simplified groups for fluid and walls
        fluid_body = VGroup()
        walls = VGroup()
        
        # Iterate through all pipes to collect their components
        # Order implies drawing order
        pipe_keys = ['pipe_inlet', 'pipe_A', 'pipe_outlet']
        
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
 
        fluid_body.set_z_index(1)
        walls.set_z_index(0)
        
        # Geometry Animation Sequence:
        self.play(FadeIn(fluid_body), run_time=1)        
        self.play(Create(walls), run_time=1.5)



        # --- Annotations & Physics Calcs ---
        # 1. Calculate Flows - Constant Q for Series
        total_q = phys_cfg['total_flow_rate']
        flows = {
            'inlet': total_q,
            'A': total_q,
            'outlet': total_q,
            'series_flow': total_q
        }
        
        # 2. Calculate Heads and Velocities
        combined_phys = {**INPUTS['physics']['fluid'], **INPUTS['physics']}
        node_heads, pipe_velocities = calculate_system_heads(nodes_cfg, pipes_cfg, flows, combined_phys)
        
        # Create Flow Labels (Q is constant, maybe just one label? or one per pipe to show equality)
        annotations_labels = VGroup()
        
        # Place labels
        # Inlet
        flow_lbl_inlet = create_flow_label(pipes['pipe_inlet'][1], flows['inlet'], "inlet", direction=UP, buff=1.2)
        
        # Pipe A
        flow_lbl_A = create_flow_label(pipes['pipe_A'][1], flows['A'], "A", direction=UP, buff=0.9)

        # Outlet
        flow_lbl_outlet = create_flow_label(pipes['pipe_outlet'][1], flows['outlet'], "outlet", direction=UP, buff=1.2)

        flow_lbls = VGroup(flow_lbl_inlet, flow_lbl_A, flow_lbl_outlet)
        self.play(Create(flow_lbls), run_time=0.5)


        
        self.play(FadeIn(annotations_labels))


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
        # Calculate alpha boundaries
        # Because the streamline is composed of 3 equal-segment-count paths,
        # the alpha boundaries are simply 1/3 and 2/3, regardless of physical length.
        
        alpha_1 = 1.0 / 3.0
        alpha_2 = 2.0 / 3.0
        
        # Get physical velocities (m/s)
        # Note: These might be very large numbers depending on Q and Diameter.
        # We need to scale them to "Animation Speed" (alpha per second).
        # We pick a reference, e.g., Inlet Speed = 0.1 alpha/sec.
        # Then others are scaled relatively.
        
        v_inlet = pipe_velocities['pipe_inlet']
        v_A = pipe_velocities['pipe_A']
        v_outlet = pipe_velocities['pipe_outlet']
        
        # Base speed factor
        base_anim_speed = 0.3 
        speed_factor = base_anim_speed / v_inlet
        
        anim_speeds = {
            'inlet': v_inlet * speed_factor,
            'A': v_A * speed_factor,
            'outlet': v_outlet * speed_factor
        }
        
        def get_variable_speed_updater(speeds, boundaries):
            b1, b2 = boundaries
            s_inlet = speeds['inlet']
            s_A = speeds['A']
            s_outlet = speeds['outlet']
            
            def update_particles(mob, dt):
                for dot in mob:
                    # Determine current speed based on alpha position
                    current_alpha = dot.virt_alpha
                    
                    if current_alpha < b1:
                        speed = s_inlet
                    elif current_alpha < b2:
                        speed = s_A
                    else:
                        # Outlet Section: Decay from s_A to s_outlet
                        # Simulate "Momentum Preservation" (Jet effect)
                        # V(alpha) = V_final + (V_initial - V_final) * exp(-(alpha - start) / tau)
                        
                        tau = 0.07 # Decay constant (alpha units)
                        delta_alpha = current_alpha - b2
                        decay_factor = np.exp(-delta_alpha / tau)
                        
                        speed = s_outlet + (s_A - s_outlet) * decay_factor
                    
                    # Update virtual alpha
                    dot.virt_alpha += speed * dt
                    
                    # Determine visibility and position
                    if 0 <= dot.virt_alpha <= 1:
                        dot.set_opacity(1)
                        # Get base position on path
                        base_pos = dot.path_ref.point_from_proportion(dot.virt_alpha)
                        # Apply offset (vertical shift relative to path tangent would be better, 
                        # but simple shift works for horizontal pipes)
                        dot.move_to(base_pos + UP * dot.virt_offset)
                    else:
                        dot.set_opacity(0)

            return update_particles

        # Particles
        particles = create_particles_with_offset(main_streamline, 60, speed=0.4) # Initial speed arg ignored by updater
        
        # Layering
        particles.set_z_index(100)
        
        self.add(particles)
        particles.add_updater(get_variable_speed_updater(anim_speeds, (alpha_1, alpha_2)))
        self.wait(6) # Wait long enough for batch to pass
        particles.clear_updaters()
        
        # Arrows (Flow Direction)
        arrow_inlet = create_flow_arrow(pipes['pipe_inlet'][1], direction=UP, buff=-0.15)
        arrow_A = create_flow_arrow(pipes['pipe_A'][1], direction=UP, buff=-0.15)
        arrow_outlet = create_flow_arrow(pipes['pipe_outlet'][1], direction=UP, buff=-0.15)
        
        arrows = VGroup(arrow_inlet, arrow_A, arrow_outlet).set_z_index(10)
        self.play(Create(arrows))

        self.wait(3)