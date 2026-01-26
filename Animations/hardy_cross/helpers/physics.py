class HardyCrossSolver:
    """
    Class to handle the Hardy Cross iterative method calculations.
    """
    def __init__(self, network_data):
        self.network_data = network_data

    def calculate_head_loss(self, flow, k, n=2):
        # hf = k * Q^n
        return k * flow * abs(flow)**(n-1)

    def solve_iteration(self):
        # TODO: Implement one iteration of Hardy Cross
        pass
