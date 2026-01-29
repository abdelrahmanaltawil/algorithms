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
        flow_arrows = create_flow_arrows(config, network_group, pipes_map)
        flow_labels = create_flow_labels(config, pipes_map, values=False)
        
        self.play(Succession(
            Write(flow_labels),
            Create(flow_arrows),
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
        side_page = Rectangle(
            width=self.camera.frame.get_width() * 0.4,
            height=self.camera.frame.get_height()*0.8,
            color=BLACK,
            fill_opacity=0.5
        ).next_to(network_group, RIGHT, buff=2)
        self.play(Create(side_page))
        self.wait(1)

        # Define layout constants relative to side_page
        left_anchor = side_page.get_left()
        top_anchor = side_page.get_top()
        margin = 0.5 * RIGHT
        indent = 1.0 * RIGHT
        line_height = 0.8 * DOWN

        # Hardy Cross Algorithm Title
        title = Text("Hardy Cross Algorithm", color=BLACK, slant=ITALIC).scale(1.2)
        # Position: Top of page + down margin + left margin
        title.move_to(top_anchor - left_anchor + 1.0*DOWN + 3*RIGHT, aligned_edge=LEFT)
        self.play(Write(title))
        self.wait(1)

        # Step 1: initial guess
        step_1_title = Text("Step 1: Initial Guess", color=BLACK, slant=ITALIC).scale(0.8)
        # Position: Below main title
        step_1_title.next_to(title, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Write(step_1_title))
        self.wait(1)
        
        flow_initial_guess = create_flow_labels(config, pipes_map, values=True)
        self.play(ReplacementTransform(flow_labels, flow_initial_guess))
        self.play(Indicate(flow_initial_guess, color=YELLOW))
        self.wait(1)

        # Step 2: Calculate Energy
        step_2_title = Text("Step 2: Calculate Energy", color=BLACK, slant=ITALIC).scale(0.8)
        # Position: Below Step 1 title (space for Step 1 content if any, or fixed spacing)
        step_2_title.next_to(step_1_title, DOWN, buff=1.0, aligned_edge=LEFT)
        
        self.play(Write(step_2_title))
        self.wait(1)

        # Use align* environment for better equation alignment
        energy_equation_1 = MathTex(
            r"E &= \sum_i H_i", 
            tex_environment="align*",
            color=BLACK
        ).scale(1.0)
        
        # Indent equation from the title
        # Position: Below title combined with indent
        energy_equation_1.next_to(step_2_title, DOWN, buff=0.3, aligned_edge=LEFT)
        energy_equation_1.shift(indent)
        
        self.play(Write(energy_equation_1))
        self.wait(1)
        
        energy_equation_2 = MathTex(
            r"\text{where } H_i &= K_i Q_i^n", 
            tex_environment="align*",
            color=BLACK
        ).scale(1.0)
        
        # Position "Where" clause below, aligned left with the first equation
        energy_equation_2.next_to(energy_equation_1, DOWN, buff=0.2, aligned_edge=LEFT)
        
        self.play(Write(energy_equation_2))
        self.wait(1)

        # Step 3: Iterative Correction
        step_3_title = Text("Step 3: Iterative Correction", color=BLACK, slant=ITALIC).scale(0.8)
        # Position: Below Step 2 title (space for Step 2 content if any, or fixed spacing)
        step_3_title.next_to(energy_equation_2, DOWN, buff=1.0, aligned_edge=LEFT)
        step_3_title.shift(-indent)

        self.play(Write(step_3_title))
        self.wait(1)
        
        # Correction Formula
        correction_formula = MathTex(
            r"\Delta Q = - \frac{\sum H_i}{n \sum_i |H_i/Q_i|}",
            color=BLACK
        ).scale(1.0)
        
        # Indent equation
        correction_formula.next_to(step_3_title, DOWN, buff=0.3, aligned_edge=LEFT)
        correction_formula.shift(indent)
        
        self.play(Write(correction_formula))
        self.wait(1)
        
        # # Iteration Logic
        # from helpers.physics import HardyCrossSolver
        # # from helpers.annotations import create_loop_path # Already imported globally

        # solver = HardyCrossSolver(config)
        
        # # Label to show current loop's correction value
        # delta_q_label = MathTex(r"\Delta Q =", color=BLACK).scale(0.8)
        # # Position below the formula
        # delta_q_label.next_to(correction_formula, DOWN, buff=0.5, aligned_edge=LEFT)
        # delta_q_label.shift(0.5 * RIGHT) # Small indent for result
        
        # self.play(Write(delta_q_label))
        
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
