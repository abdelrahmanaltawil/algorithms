from manim import *
from helpers.utils import load_config
from helpers.geometry import create_network_mobjects
from helpers.annotations import create_flow_arrows, create_flow_labels, create_loop_path, create_correction_formula

class HardyCrossScene(MovingCameraScene):
    def construct(self):
        # Load configuration
        config = load_config("inputs.yaml")
        
        # Initialize Network
        # Now returns tuple: (network_group, nodes_map, pipes_map, tanks_map)
        network_group, nodes_map, pipes_map, tanks_map = create_network_mobjects(config)
        
        # Preprossing: Show Network
        self.play(Create(network_group), run_time=2)
        self.wait(1)
        
        # Preprossing: Show system
        # Create arrows and labels
        flow_labels = create_flow_labels(config, pipes_map, values=False)
        
        self.play(Succession(
            Write(flow_labels),
            run_time=2
        ))
        self.wait(1)

        # Preprossing: show loop paths
        # Initialize the first loop
        loop_ids = list(config['network']['loops'].keys())
        current_loop_path = create_loop_path(config, pipes_map, loop_ids[0])
        self.play(Create(current_loop_path))

        # Transition through the rest
        for loop_id in loop_ids[1:] + [loop_ids[0]]:
            next_loop_path = create_loop_path(config, pipes_map, loop_id)
            self.play(
                ReplacementTransform(current_loop_path, next_loop_path),
                run_time=0.8
            )
            current_loop_path = next_loop_path # Update reference
            self.wait(0.5)

        # change camera position to give sapce in right side
        self.play(
            self.camera.frame.animate.set_width(self.camera.frame.get_width() * 1.2) # Zoom out 1.5x
            .move_to(network_group.get_center() + RIGHT * 7), # Shift right
            run_time=2
        )

        # create side page for algorithm steps
        from helpers.annotations import (
            create_side_page, create_algorithm_title, 
            create_step_1_text, create_step_2_text, create_step_3_text
        )
        
        side_page = create_side_page(self.camera.frame, network_group)
        self.play(Create(side_page))
        self.wait(1)

        # Hardy Cross Algorithm Title
        title = create_algorithm_title(side_page)
        self.play(Write(title))
        self.wait(1)

        # Step 1: initial guess
        step_1_title = create_step_1_text(side_page, title)
        self.play(Write(step_1_title))
        self.wait(1)
        
        flow_initial_guess = create_flow_labels(config, pipes_map, values=True)
        flow_arrows_guess = create_flow_arrows(config, network_group, pipes_map)
        self.play(ReplacementTransform(flow_labels, flow_initial_guess))
        self.play(Create(flow_arrows_guess))
        self.play(Indicate(VGroup(flow_initial_guess, flow_arrows_guess), color=YELLOW))
        self.wait(1)

        # Step 2: Calculate Energy
        step_2_group = create_step_2_text(side_page, step_1_title)
        # Animate elements sequentially
        for mobj in step_2_group:
            self.play(Write(mobj))
            self.wait(0.5)
        self.wait(1)

        # Step 3: Iterative Correction
        # step_2_group[-1] is the last equation "where H = ..."
        step_3_group = create_step_3_text(side_page, step_2_group[-1])
        
        # Elements: [Title, Formula, DeltaQLabel]
        step_3_title = step_3_group[0]
        correction_formula = step_3_group[1]
        delta_q_label = step_3_group[2]
        
        # Write title and formula
        self.play(Write(step_3_title))
        self.wait(0.5)
        self.play(Write(correction_formula))
        self.wait(1)
        self.play(Write(delta_q_label))
        
        # # Iteration Logic
        # from helpers.physics import HardyCrossSolver

        # solver = HardyCrossSolver(config)
        
        # num_iterations = 2 
        
        # for i in range(num_iterations):
        #     # Solve one iteration (returns corrections for all loops)
        #     corrections = solver.solve_iteration()
            
        #     for loop_id, delta_q in corrections.items():
        #         if abs(delta_q) < 0.01: continue

        #         # Highlight Loop
        #         loop_path = create_loop_path(config, pipes_map, loop_id)
        #         self.play(Create(loop_path), run_time=1.0)
                
        #         # Show Correction Value
        #         val_text = MathTex(f"{delta_q:.2f}", color=RED).scale(0.8)
        #         val_text.next_to(delta_q_label, RIGHT)
                
        #         self.play(Write(val_text))
        #         self.wait(0.5)
                
        #         # Apply updates to config so create_flow_labels picks them up
        #         for pid in solver.current_flows:
        #             config['network']['pipes'][pid]['initial_flow'] = solver.current_flows[pid]
                    
        #         # Create NEW labels
        #         updated_labels = create_flow_labels(config, pipes_map)
                
        #         # Re-create arrows too if direction flipped (flow sign change)
        #         updated_arrows = create_flow_arrows(config, network_group, pipes_map)
                
        #         # Animate transition
        #         self.play(
        #             Transform(flow_labels, updated_labels),
        #             Transform(flow_arrows, updated_arrows),
        #             FadeOut(loop_path),
        #             FadeOut(val_text), 
        #             run_time=1.5
        #         )
                
        # self.wait(2)
