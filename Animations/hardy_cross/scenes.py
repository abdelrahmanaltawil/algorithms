from manim import *
from helpers.utils import load_config
from helpers.geometry import create_network_mobjects

class HardyCrossScene(Scene):
    def construct(self):
        # Load configuration
        config = load_config("inputs.yaml")
        
        # Initialize Network
        network_group = create_network_mobjects(config)
        self.add(network_group)
        
        self.wait(2)
