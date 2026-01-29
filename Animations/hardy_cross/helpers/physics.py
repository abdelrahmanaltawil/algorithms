import numpy as np

class HardyCrossSolver:
    """
    Class to handle the Hardy Cross iterative method calculations.
    """
    def __init__(self, config):
        self.config = config
        self.pipes = config['network']['pipes']
        self.loops = config['network']['loops']
        # Map pipe IDs to their current flow
        self.current_flows = {pid: data.get('initial_flow', 0) for pid, data in self.pipes.items()}
        # Map pipe IDs to resistance
        self.resistances = {pid: data.get('resistance', 1) for pid, data in self.pipes.items()}

    def get_flow(self, pipe_id):
        return self.current_flows.get(pipe_id, 0)

    def calculate_head_loss(self, flow, k, n=2):
        # hf = k * Q * |Q|^(n-1) -> for n=2, k * Q * |Q|
        return k * flow * abs(flow)**(n-1)

    def solve_iteration(self, n=2):
        """
        Calculates and applies one iteration of Hardy Cross correction on all loops.
        Returns a dictionary of {loop_id: delta_q} containing the corrections applied.
        Note: Corrections are calculated based on current state at the start of loop processing.
        Usually, updates are applied loop-by-loop or simultaneously.
        Here we will process loop-by-loop and update immediately as is common.
        """
        loop_corrections = {}
        
        for loop_id, pipe_ids in self.loops.items():
            numerator = 0.0
            denominator = 0.0
            
            # 1. Determine Start Node for traversal
            # We assume connected pipes.
            if len(pipe_ids) < 2: continue

            p0_id = pipe_ids[0]
            p0 = self.pipes[p0_id]
            p1 = self.pipes[pipe_ids[1]]
            
            # Intersection of P0 and P1
            nodes0 = {p0['start'], p0['end']}
            nodes1 = {p1['start'], p1['end']}
            shared = list(nodes0.intersection(nodes1))
            
            if not shared: continue
            shared_node = shared[0] # node B
            
            # Start node is the other node of P0
            if p0['start'] == shared_node:
                curr_node = p0['end'] 
            else:
                curr_node = p0['start']
            
            # 2. Traverse Loop
            # Store directions for update step
            pipe_directions = {} # pid -> direction (+1 or -1)

            for pid in pipe_ids:
                data = self.pipes[pid]
                start, end = data['start'], data['end']
                
                # Determine direction relative to traversal
                if curr_node == start:
                    target = end
                    direction = 1 # Moving with pipe def
                elif curr_node == end:
                    target = start
                    direction = -1 # Moving against pipe def
                else:
                    direction = 1 # Warning
                    target = end
                
                pipe_directions[pid] = direction
                curr_node = target
                
                # Calculation
                q = self.current_flows[pid]
                r = self.resistances[pid]
                
                # Flow relative to loop = q * direction
                q_loop = q * direction
                
                # Head Loss = r * q_loop * |q_loop|^(n-1)
                h_loss = r * q_loop * abs(q_loop)**(n-1)
                
                # Deriv = n * r * |q_loop|^(n-1)
                deriv = n * r * abs(q_loop)**(n-1)
                
                numerator += h_loss
                denominator += deriv
            
            # 3. Calculate Correction
            if denominator == 0:
                delta_q = 0
            else:
                delta_q = - numerator / denominator
                
            loop_corrections[loop_id] = delta_q
            
            # 4. Apply Correction Immediately
            for pid in pipe_ids:
                direction = pipe_directions[pid]
                # If loop flow is delta_q (clockwise), and pipe is traversed with direction,
                # we add delta_q. If traversed against, we add delta_q * (-1)?
                # Wait: delta_q is Circulation correction.
                # If pipe traversal is clockwise (direction relative to pipe def),
                # New Flow = Old Flow + delta_q * direction
                self.current_flows[pid] += delta_q * direction
                
        return loop_corrections
