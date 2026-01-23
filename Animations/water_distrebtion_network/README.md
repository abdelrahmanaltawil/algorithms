# Water Distribution Network Animation

A Manim animation simulating flow, pressure, and velocity in a **Dead-End / Branching** water distribution network.

## features

- **Physically Accurate Flow**: Uses manual flow solving based on downstream demand for tree-like topologies.
- **Global Time-Scheduling**: Visualizes continuous, non-overlapping flow paths using Dijkstra's algorithm to schedule animations based on physical travel time.
- **Dynamic Heatmap**: Visualizes pressure distribution with a color gradient (Blue $\to$ Red) and moving annotations.
- **Configurable**: Network topology, physics parameters, and display settings are defined in `inputs.yaml`.

## File Structure

```
water_distrebtion_network/
├── scenes.py       # Main Manim scene
├── inputs.yaml     # Configuration (Nodes, Pipes, Physics)
├── helpers/
│   ├── physics.py      # Network graph & hydraulic calculations
│   ├── geometry.py     # Manim Mobject creation
│   ├── annotations.py  # Labels & visual helpers
│   └── utils.py        # Config loading utilities
└── README.md       # This file
```

## Quick Start

Run the animation using Manim:

```bash
# Low Quality (Preview)
manim -pql scenes.py WaterDistributionScene

# High Quality
manim -pqh scenes.py WaterDistributionScene
```

## Configuration

Edit `inputs.yaml` to modify:
- **Topology**: Add/remove nodes and pipes.
- **Demands**: Change nodal demands.
- **Physics**: Adjust gravity, roughness, or source pressure.
- **Visuals**: Change colors or animation speed scales.
