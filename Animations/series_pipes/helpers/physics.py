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
    # Since we are calculating ratios, units cancel out as long as they are consistent across all pipes.
    
    k_factors = {}
    sum_k = 0
    
    for p in pipes_data:
        d = p['diameter_mm']
        l = p['length']
        
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

def calculate_velocity(flow_rate, diameter):
    """
    Calculates fluid velocity.
    Args:
        flow_rate (float): Volumetric flow rate (e.g., m^3/s).
        diameter (float): Pipe diameter (e.g., m).
    Returns:
        float: Velocity (e.g., m/s).
    """
    if diameter <= 0: return 0
    radius = diameter / 2
    area = np.pi * radius**2
    return flow_rate / area

def calculate_reynolds(v, d, nu):
    """
    Calculates Reynolds number.
    Args:
        v (float): Velocity (m/s)
        d (float): Diameter (m)
        nu (float): Kinematic viscosity (m^2/s)
    """
    if nu <= 0: return float('inf')
    return v * d / nu

def calculate_friction_factor(re, roughness, d):
    """
    Calculates friction factor using Swamee-Jain equation (turbulent)
    or 64/Re (laminar).
    
    Args:
        re (float): Reynolds number
        roughness (float): Absolute roughness (m)
        d (float): Pipe diameter (m)
    """
    if re < 2000:
        if re == 0: return 0
        return 64 / re
    else:
        # Swamee-Jain approximation for Darcy friction factor
        epsilon = roughness
        term1 = epsilon / (3.7 * d)
        term2 = 5.74 / (re ** 0.9)
        return 0.25 / (np.log10(term1 + term2) ** 2)

def calculate_head_loss(length, diameter, v, g=9.81, roughness=0.0015e-3, nu=1.0e-6):
    """
    Calculates head loss using Darcy-Weisbach equation.
    
    Args:
        length (float): Pipe length (m)
        diameter (float): Pipe diameter (m)
        v (float): Velocity (m/s)
        g (float): Gravity (m/s^2)
        roughness (float): Roughness height (m)
        nu (float): Kinematic viscosity (m^2/s)
        
    Returns:
        float: Head loss (m)
    """
    if diameter <= 0 or length <= 0: return 0
    
    re = calculate_reynolds(v, diameter, nu)
    f = calculate_friction_factor(re, roughness, diameter)
    
    # h_f = f * (L/D) * (v^2/2g)
    head_loss = f * (length / diameter) * (v**2 / (2 * g))
    return head_loss

def calculate_system_heads(nodes_config, pipes_config, flows, phys_config):
    """
    Calculates Hydraulic Head (H) at each node in the network.
    Assumes a linear topology: 0 -> 1 -> 2 -> 3 -> 4 -> 5
    """
    nu = float(phys_config.get('kinematic_viscosity', 1.0e-6))
    g = float(phys_config.get('gravity', 9.81))
    roughness = float(phys_config.get('default_roughness', 0.0015)) / 1000.0
    
    pipe_velocities = {}
    
    # 1. Calculate Velocities
    for key, data in pipes_config.items():
        pid = data['id'] # 'inlet', 'A', 'B', 'C', 'outlet'
        
        # In series, flow is constant, but let's look it up
        if pid in flows:
            q = flows[pid]
        else:
            q = flows.get('series_flow', 0) # Fallback
            
        d_mm = data['diameter_mm']
        d_m = d_mm / 1000.0
        
        v = calculate_velocity(q, d_m)
        pipe_velocities[key] = v

    # 2. Calculate Heads
    current_head = 100.0 
    node_heads = {}
    
    # Sequence of nodes and pipes
    # Node 0 -> Pipe inlet -> Node 1
    # Node 1 -> Pipe A -> Node 2
    # Node 2 -> Pipe outlet -> Node 5 (Outlet End)
    
    sequence = [
        (0, 'pipe_inlet', 1),
        (1, 'pipe_A', 2),
        (2, 'pipe_outlet', 5)
    ]
    
    node_heads[0] = current_head
    
    for start_node, pipe_key, end_node in sequence:
        if pipe_key not in pipes_config:
            continue
            
        p_data = pipes_config[pipe_key]
        v = pipe_velocities[pipe_key]
        d = p_data['diameter_mm'] / 1000.0
        l = p_data['length']
        
        hl = calculate_head_loss(l, d, v, g, roughness, nu)
        
        current_head -= hl
        node_heads[end_node] = current_head
    
    return node_heads, pipe_velocities
