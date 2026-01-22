import numpy as np

class Pipe:
    def __init__(self, start_node, end_node, length, diameter, roughness_c=100):
        self.start_node = start_node
        self.end_node = end_node
        self.length = length  # m
        self.diameter = diameter  # m
        self.c = roughness_c
        self.flow_rate = 0.0  # m^3/s, initial guess
        self.velocity = 0.0
        self.head_loss = 0.0

    def calculate_head_loss(self):
        # Hazen-Williams equation: hf = 10.67 * L * Q^1.852 / (C^1.852 * D^4.87)
        q_abs = abs(self.flow_rate)
        if q_abs < 1e-9:
            self.head_loss = 0
            return 0
        
        loss = (10.67 * self.length * (q_abs ** 1.852)) / (self.c ** 1.852 * self.diameter ** 4.87)
        self.head_loss = loss * np.sign(self.flow_rate)
        return self.head_loss

    def update_velocity(self):
        area = np.pi * (self.diameter / 2)**2
        self.velocity = self.flow_rate / area if area > 0 else 0

class Node:
    def __init__(self, id, x, y, elevation=0, demand=0):
        self.id = id
        self.pos = np.array([x, y, 0])
        self.elevation = elevation # m
        self.demand = demand # m^3/s (+ is demand OUT, - is source IN)
        self.head = 0.0
        self.pressure = 0.0 # kPa

class WaterNetwork:
    def __init__(self):
        self.nodes = {}
        self.pipes = []
        self.loops = []

    def add_node(self, id, x, y, elevation=0, demand=0):
        self.nodes[id] = Node(id, x, y, elevation, demand)

    def add_pipe(self, start_id, end_id, length, diameter, c=130):
        self.pipes.append(Pipe(start_id, end_id, length, diameter, c))

    def define_loops(self, loop_indices):
        self.loops = loop_indices

    def solve_hardy_cross(self, max_iter=100, tol=1e-5):
        for _ in range(max_iter):
            max_correction = 0
            for loop in self.loops:
                sum_h = 0
                sum_h_prime = 0
                for pipe_idx, direction in loop:
                    p = self.pipes[pipe_idx]
                    k = 10.67 * p.length / (p.c ** 1.852 * p.diameter ** 4.87)
                    h_loss = k * abs(p.flow_rate)**1.852 * np.sign(p.flow_rate)
                    h_segment = h_loss * direction
                    sum_h += h_segment
                    if abs(p.flow_rate) > 1e-9:
                        sum_h_prime += abs(h_segment) / abs(p.flow_rate)
                
                if sum_h_prime == 0: continue
                delta_q = -sum_h / (1.852 * sum_h_prime)
                
                for pipe_idx, direction in loop:
                    self.pipes[pipe_idx].flow_rate += delta_q * direction
                max_correction = max(max_correction, abs(delta_q))
                
            if max_correction < tol: break
        
        for p in self.pipes:
            p.calculate_head_loss()
            p.update_velocity()

    def calculate_pressures(self, source_node_id, source_head):
        self.nodes[source_node_id].head = source_head
        visited = set([source_node_id])
        queue = [source_node_id]
        adj = {n: [] for n in self.nodes}
        for i, p in enumerate(self.pipes):
            adj[p.start_node].append((p.end_node, p, 1))
            adj[p.end_node].append((p.start_node, p, -1))
            
        while queue:
            u_id = queue.pop(0)
            u = self.nodes[u_id]
            for v_id, pipe, direction in adj[u_id]:
                if v_id not in visited:
                    if direction == 1:
                        self.nodes[v_id].head = u.head - pipe.head_loss
                    else:
                        self.nodes[v_id].head = u.head + pipe.head_loss
                    visited.add(v_id)
                    queue.append(v_id)
        
        for n in self.nodes.values():
            n.pressure = 9.81 * (n.head - n.elevation)
