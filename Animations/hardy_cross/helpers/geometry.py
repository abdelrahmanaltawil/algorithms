from manim import *
import numpy as np

def create_network_mobjects(config):
    """
    Function to create Mobjects for the pipe network (nodes and pipes only).
    Returns a VGroup containing all elements.
    """
    network_group = VGroup()
    
    # 1. Create Nodes
    file_nodes = create_nodes(config)
    
    # 2. Create Pipes
    file_pipes = create_pipes(config, file_nodes)
    
    # 3. Create Tanks
    file_tanks = create_tanks(config)

    # Add tanks first (behind everything else usually, or depending on desired layering)
    for tank in file_tanks.values():
        network_group.add(tank)

    # Add pipes first so they are behind nodes
    for pipe in file_pipes.values():
        network_group.add(pipe)
        
    for node in file_nodes.values():
        network_group.add(node)

        
    return network_group

def get_node_pos(config, node_id):
    raw_pos = config['network']['nodes'][node_id]
    return np.array(raw_pos)

def create_tanks(config):
    tanks_map = {}
    tank_config = config['network'].get('tanks', {})
    
    for tank_id, data in tank_config.items():
        node_id = data['node']
        height = data['height']
        width = data['width']
        fill_level = data['fill_level']
        
        position = get_node_pos(config, node_id)
        
        # Shift position: The node position is usually the connection point. 
        # If the tank is sitting on top of the node (like a reservoir feeding the pipe),
        # we might want the tank bottom to be at position.
        # create_tank uses 'position' as the center of the bottom.
        
        tank = create_tank(height, width, fill_level, position=position)
        tanks_map[tank_id] = tank
        
    return tanks_map

def create_nodes(config):
    nodes_map = {}
    node_config = config['network']['nodes']
    visuals = config['visuals']
    
    for node_id, pos in node_config.items():
        # Skip external nodes if they are just for logic (start with IN)
        # if isinstance(node_id, str) and node_id.startswith("IN"):
        #     continue
            
        node = Circle(
            radius=0, 
            color=visuals['node_color'],
            fill_opacity=1
        )
        node.move_to(np.array(pos))
        nodes_map[node_id] = node
        
    return nodes_map

def create_pipes(config, nodes_map):
    pipes_map = {}
    pipe_config = config['network']['pipes']
    visuals = config['visuals']
    
    for pipe_id, data in pipe_config.items():
        start_id = data['start']
        end_id = data['end']
        
        # Get positions
        # If it's a known node Mobject, use its center. 
        # If it's an external point (IN_...), look it up in config directly.
        
        if start_id in nodes_map:
            start_pos = nodes_map[start_id].get_center()
        else:
            start_pos = get_node_pos(config, start_id)
            
        if end_id in nodes_map:
            end_pos = nodes_map[end_id].get_center()
        else:
            end_pos = get_node_pos(config, end_id)
        
        line = Line(
            start_pos, 
            end_pos, 
            stroke_width=visuals['pipe_stroke_width'], 
            color=visuals['pipe_color']
        )
        pipes_map[pipe_id] = line
        
    return pipes_map

def create_tank(height, width, fill_level, position=np.array([0, 0, 0]), water_color=BLUE, tank_color=BLACK, wall_thickness=0.2):
    """
    Creates a rectangular tank that is partially full with solid walls.
    
    Args:
        height (float): Total height of the tank.
        width (float): Total width of the tank (outer width).
        fill_level (float): Level of fluid between 0.0 (empty) and 1.0 (full).
        position (np.array): Center position of the tank's bottom (outer bottom).
        water_color: Color of the water.
        tank_color: Color of the tank walls.
        wall_thickness (float): Thickness of the walls.
        
    Returns:
        VGroup: Group containing tank walls and water.
    """
    
    # Dimensions
    # Outer width = width
    # Inner width = width - 2 * wall_thickness
    inner_width = width - 2 * wall_thickness
    
    # 1. Create Water (Rectangle)
    # Water sits inside the tank. Bottom of water is at bottom of inner tank.
    # Bottom of inner tank is at position.y + wall_thickness (if position is outer bottom)
    
    water_height = (height - wall_thickness) * fill_level
    if water_height < 0: water_height = 0
    if water_height > (height - wall_thickness): water_height = height - wall_thickness
    
    water = Rectangle(
        width=inner_width,
        height=water_height,
        color=water_color,
        fill_color=water_color,
        fill_opacity=0.5,
        stroke_width=0
    )
    
    # Calculate Water Position
    # Water bottom y = position.y + wall_thickness
    # Water center y = (position.y + wall_thickness) + water_height / 2
    water_bottom_y = position[1] + wall_thickness
    water_center_y = water_bottom_y + water_height / 2
    
    water.move_to(np.array([position[0], water_center_y, position[2]]))
    
    # 2. Create Walls (3 Rectangles)
    
    # Bottom Wall
    bottom_wall = Rectangle(
        width=width,
        height=wall_thickness,
        color=tank_color,
        fill_color=tank_color,
        fill_opacity=1,
        stroke_width=0
    )
    # Bottom wall center: x=position.x, y=position.y + wall_thickness/2
    bottom_wall.move_to(position + np.array([0, wall_thickness/2, 0]))
    
    # Left Wall
    left_wall = Rectangle(
        width=wall_thickness,
        height=height,
        color=tank_color,
        fill_color=tank_color,
        fill_opacity=1,
        stroke_width=0
    )
    # Left wall center:
    # x = position.x - width/2 + wall_thickness/2
    # y = position.y + height/2
    left_wall.move_to(position + np.array([-width/2 + wall_thickness/2, height/2, 0]))

    # Right Wall
    right_wall = Rectangle(
        width=wall_thickness,
        height=height,
        color=tank_color,
        fill_color=tank_color,
        fill_opacity=1,
        stroke_width=0
    )
    # Right wall center:
    # x = position.x + width/2 - wall_thickness/2
    # y = position.y + height/2
    right_wall.move_to(position + np.array([width/2 - wall_thickness/2, height/2, 0]))
    
    return VGroup(water, bottom_wall, left_wall, right_wall)
