from manim import *
import numpy as np

def create_network_mobjects(network):
    """
    Creates Manim Mobjects for the water network.
    
    Args:
        network (WaterNetwork): The simulated network object.
        
    Returns:
        tuple: (pipe_mobjects_dict, node_mobjects_dict)
    """
    pipe_mobjects = {}
    node_mobjects = {}
    
    # create pipes
    for p in network.pipes:
        start = network.nodes[p.start_node].pos
        end = network.nodes[p.end_node].pos
        # Grey initially
        line = Line(start, end, stroke_width=p.diameter*20, color=GREY_C)
        pipe_mobjects[p] = line
        
    # create nodes
    for n in network.nodes.values():
        dot = Dot(n.pos, radius=0.05, color=GREY)
        node_mobjects[n] = dot
        
    return pipe_mobjects, node_mobjects
