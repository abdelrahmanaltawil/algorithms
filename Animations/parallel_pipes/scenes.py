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
from helpers.config import load_config
from helpers.geometry import create_system_mobjects

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
        
        # Build geometry - get the paths
        nodes, pipes, geo_labels = create_system_mobjects(nodes_cfg, pipes_cfg, disp_cfg)
        
        # Show each pipe separately with labels
        # Inlet pipe (starting)
        inlet = pipes['pipe_inlet'][1].copy()
        inlet.set_style(fill_opacity=0, stroke_color=GREEN, stroke_width=4)
        
        # Outlet pipe (ending)
        outlet = pipes['pipe_D'][1].copy()
        outlet.set_style(fill_opacity=0, stroke_color=RED, stroke_width=4)
        
        # Base pipes (main paths) - thinner stroke
        branch_a = pipes['pipe_A'][1].copy()
        branch_a.set_style(fill_opacity=0, stroke_color=BLUE, stroke_width=2)
        
        branch_b = pipes['pipe_B'][1].copy()
        branch_b.set_style(fill_opacity=0, stroke_color=BLUE, stroke_width=2)
        
        branch_c = pipes['pipe_C'][1].copy()
        branch_c.set_style(fill_opacity=0, stroke_color=BLUE, stroke_width=2)
        
        # Create base streamlines (without visual offset lines)
        from helpers.streamlines import compose_streamline_path
        
        # Get base paths
        inlet_path = pipes['pipe_inlet'][1]
        outlet_path = pipes['pipe_D'][1]
        
        # Compose full streamlines for each branch
        streamline_a = compose_streamline_path(inlet_path, pipes['pipe_A'][1], outlet_path)
        streamline_b = compose_streamline_path(inlet_path, pipes['pipe_B'][1], outlet_path)
        streamline_c = compose_streamline_path(inlet_path, pipes['pipe_C'][1], outlet_path)
        
        # Style streamlines (optional - can hide if you only want particles)
        for sl in [streamline_a, streamline_b, streamline_c]:
            sl.set_style(fill_opacity=0, stroke_color=BLUE, stroke_width=2)
        
        streamlines = VGroup(streamline_a, streamline_b, streamline_c)
        
        # Display full pipe groups (Outline + Inner Path) to show thickness/walls
        # Display full pipe groups (Outline + Inner Path) to show thickness/walls
        
        # Create simplified groups for fluid and walls
        # Using pre-generated geometry from helper which handles diameter variations correctly
        fluid_body = VGroup()
        walls = VGroup()
        
        # Iterate through all pipes to collect their components
        # Order doesn't strictly matter for VGroup collection, but logical for debugging
        pipe_keys = ['pipe_inlet', 'pipe_A', 'pipe_B', 'pipe_C', 'pipe_D']
        
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
        
        # Layering: Fluid ON TOP of Walls (z-index higher)
        # This prevents the black wall lines from cutting through the blue fluid at junctions
        walls.set_z_index(0)
        fluid_body.set_z_index(1)
        
        # Animation Sequence matches user request:
        # 1. Fluid fills the system (Blue)
        self.play(Create(fluid_body), run_time=1.5)
        
        # 2. Walls appear "around" the fluid
        self.play(Create(walls), run_time=1.5)
        
        # 3. Particles appear (Streamlines lines skipped)
        self.wait(1)
        
        # --- Particle Animation with offset sampling ---
        
        def create_particles_with_offset(path, num_particles, speed, offset_range=0.3):
            """Generate particles distributed along path with random offset from center."""
            particles = VGroup()
            for _ in range(num_particles):
                dot = Dot(radius=0.04, color=BLACK)
                
                # Random initial position along path (0 to 1)
                alpha = random.uniform(0, 1)
                
                # Random offset from path center (sampled from distribution)
                offset = random.uniform(-offset_range, offset_range)
                
                dot.virt_alpha = alpha      # Virtual position on path
                dot.virt_offset = offset    # Offset from path center
                dot.speed = speed           # Speed along path
                dot.path_ref = path         # Reference to path
                
                # Set initial position with offset
                base_pos = path.point_from_proportion(alpha)
                dot.move_to(base_pos + np.array([0, offset, 0]))
                particles.add(dot)
            return particles
        
        def get_offset_path_updater():
            """Returns updater that moves particles along paths with offset."""
            def update_particles(mob, dt):
                for dot in mob:
                    # Update virtual position
                    dot.virt_alpha += dot.speed * dt
                    # Wrap around when reaching end
                    dot.virt_alpha = dot.virt_alpha % 1.0
                    # Get base position on path
                    base_pos = dot.path_ref.point_from_proportion(dot.virt_alpha)
                    # Apply offset (perpendicular to flow direction - simplified as Y offset)
                    dot.move_to(base_pos + np.array([0, dot.virt_offset, 0]))
            return update_particles
        
        # Create particles on each streamline
        all_particles = VGroup()
        base_speed = 0.08
        
        # Branch A (top) - particles
        # Reduced offset to keep inside pipe (Diameter ~0.34 units -> Radius ~0.17)
        particles_a = create_particles_with_offset(streamline_a, 15, base_speed, offset_range=0.12)
        all_particles.add(*particles_a)
        
        # Branch B (middle) - more particles (higher flow)
        # Reduced offset (Diameter ~0.28 units -> Radius ~0.14)
        particles_b = create_particles_with_offset(streamline_b, 20, base_speed * 1.2, offset_range=0.10)
        all_particles.add(*particles_b)
        
        # Branch C (bottom) - particles
        # Reduced offset (Diameter ~0.31 units -> Radius ~0.155)
        particles_c = create_particles_with_offset(streamline_c, 15, base_speed, offset_range=0.11)
        all_particles.add(*particles_c)
        
        # Layering: Particles (2) > Fluid (1) > Walls (0)
        all_particles.set_z_index(2)
        
        # Add particles to scene
        self.add(all_particles)
        
        # Add updater for continuous motion
        all_particles.add_updater(get_offset_path_updater())
        
        # Let animation run
        self.wait(8)
        
        # Remove updaters before ending
        all_particles.clear_updaters()
        self.wait(1)
