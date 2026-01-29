from manim import *
from helpers.utils import load_config
from helpers.geometry import create_network_mobjects
from helpers.annotations import create_flow_arrows, create_flow_labels, create_loop_path, create_correction_formula

class HardyCrossScene(Scene):
    def construct(self):
        # Load configuration
        config = load_config("inputs.yaml")
        
        # Initialize Network
        # Now returns tuple: (network_group, nodes_map, pipes_map, tanks_map)
        network_group, nodes_map, pipes_map, tanks_map = create_network_mobjects(config)
        
        # Step 1: Show Network
        self.play(Create(network_group), run_time=2)
        self.wait(1)
        
        # Step 2: Show Initial Flows
        # Create arrows and labels
        flow_arrows = create_flow_arrows(config, network_group, pipes_map)
        flow_labels = create_flow_labels(config, pipes_map)
        
        self.play(Succession(
            Write(flow_labels),
            Create(flow_arrows),
            run_time=2
        ))
        self.wait(1)

        # Step 2: Flow Correction        
        # Highlight Loop 1
        loop1_highlight = create_loop_path(config, pipes_map, "Loop1")
        self.play(Create(loop1_highlight), run_time=1.5)
        self.wait(1)
        
        # Show Correction Formula
        formula_group = create_correction_formula()
        self.play(Write(formula_group))
        self.wait(2)
        
        # Cleanup Step 2 for next steps (optional, or keep for visual context)
        self.play(
            FadeOut(loop1_highlight),
            FadeOut(formula_group)
        )

