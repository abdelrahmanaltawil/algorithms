import numpy as np

def calculate_parallel_flows(total_Q, pipes_data):
    """
    Calculates flow rate for parallel pipes assuming equal head loss.
    Uses simplified relationship Q ~ sqrt(D^5 / L) for turbulent flow.
    
    Args:
        total_Q (float): Total inflow.
        pipes_data (list): List of dicts with 'diameter_mm', 'length', 'id'.
        
    Returns:
        dict: Mapping of pipe_id -> flow_rate
    """
    # Conductivity factor K_i = sqrt(D^5 / L)
    # Since D is in mm and L in m, we just need relative values, units cancel if consistent.
    
    k_factors = {}
    sum_k = 0
    
    for p in pipes_data:
        d = p['diameter_mm']
        l = p['length']
        
        # Avoid division by zero
        if l <= 0: l = 0.001
        
        k = np.sqrt((d ** 5) / l)
        k_factors[p['id']] = k
        sum_k += k
        
    # Distribute Q
    flows = {}
    for pid, k in k_factors.items():
        if sum_k > 0:
            flows[pid] = total_Q * (k / sum_k)
        else:
            flows[pid] = 0
            
    return flows

def calculate_velocity(flow_rate, diameter_mm):
    """
    Calculates fluid velocity (m/s).
    Args:
        flow_rate (m^3/s): Volumetric flow.
        diameter_mm (float): Diameter in mm.
    Returns:
        float: Velocity in m/s.
    """
    if diameter_mm <= 0: return 0
    d_m = diameter_mm / 1000.0
    area = np.pi * (d_m / 2)**2
    return flow_rate / area if area > 0 else 0
