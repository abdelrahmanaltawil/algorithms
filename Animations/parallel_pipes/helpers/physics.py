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
    Assumes a specific topology: Start -> Junction 1 -> (Parallel) -> Junction 2 -> End
    Also calculates velocity for each pipe.
    
    Args:
        nodes_config (dict): Nodes data
        pipes_config (dict): Pipes data
        flows (dict): Flow rates by pipe ID/key suffix (e.g. 'A', 'inlet')
        phys_config (dict): Physics settings (viscosity, roughness, gravity)
        
    Returns:
        tuple: (node_heads, pipe_velocities)
            - node_heads: dict {node_id: head_value}
            - pipe_velocities: dict {pipe_key: velocity}
    """
    nu = float(phys_config.get('kinematic_viscosity', 1.0e-6))
    g = float(phys_config.get('gravity', 9.81))
    roughness = float(phys_config.get('default_roughness', 0.0015)) / 1000.0 # convert mm to m if needed
    
    # Map friendly names to full keys if needed, but flows usually uses 'A', 'B', etc.
    # pipes_config keys are 'pipe_inlet', 'pipe_A', etc.
    
    pipe_velocities = {}
    
    # 1. Calculate Velocities
    # We need to match flow keys to pipe config keys
    # Flow keys: 'inlet', 'outlet', 'A', 'B', 'C'
    # Pipe keys: 'pipe_inlet', 'pipe_outlet', 'pipe_A', ...
    
    for key, data in pipes_config.items():
        # extract short id from key or data['id']
        # data['id'] is like 'inlet', 'A', '1', etc.
        pid = data['id']
        
        if pid in flows:
            q = flows[pid]
            d_mm = data['diameter_mm']
            d_m = d_mm / 1000.0
            
            v = calculate_velocity(q, d_m)
            pipe_velocities[key] = v
        else:
            pipe_velocities[key] = 0.0
            
    # 2. Calculate Heads
    # Assume arbitrary start head (Reference)
    current_head = 100.0 
    node_heads = {}
    
    # -- Node 0 (Start) --
    # Start Node ID: 0
    start_node_id = 0
    node_heads[start_node_id] = current_head
    
    # -- Pipe Inlet (Node 0 -> Node 1) --
    # Get pipe data
    p_inlet = pipes_config['pipe_inlet']
    v_inlet = pipe_velocities['pipe_inlet']
    d_inlet = p_inlet['diameter_mm'] / 1000.0
    l_inlet = p_inlet['length']
    
    hl_inlet = calculate_head_loss(l_inlet, d_inlet, v_inlet, g, roughness, nu)
    
    # Head at Node 1 (Split)
    head_node_1 = current_head - hl_inlet
    node_heads[1] = head_node_1
    
    # -- Parallel Section (Node 1 -> Node 2) --
    # Theorically head loss should be same for all parallel pipes.
    # We will compute for Branch A and use it (or average them?)
    # ideally they differ slightly due to the approximation in calculate_parallel_flows
    # Let's use Branch A as reference for the visual drop.
    
    p_a = pipes_config['pipe_A']
    v_a = pipe_velocities['pipe_A']
    d_a = p_a['diameter_mm'] / 1000.0
    l_a = p_a['length']
    
    hl_a = calculate_head_loss(l_a, d_a, v_a, g, roughness, nu)
    
    head_node_2 = head_node_1 - hl_a
    node_heads[2] = head_node_2
    
    # -- Outlet Pipe (Node 2 -> Node 3) --
    p_out = pipes_config['pipe_outlet']
    v_out = pipe_velocities['pipe_outlet']
    d_out = p_out['diameter_mm'] / 1000.0
    l_out = p_out['length']
    
    hl_out = calculate_head_loss(l_out, d_out, v_out, g, roughness, nu)
    
    head_node_3 = head_node_2 - hl_out
    node_heads[3] = head_node_3
    
    return node_heads, pipe_velocities
