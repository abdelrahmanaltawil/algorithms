# Parallel Pipes Flow Animation

Manim animation of water flow through three parallel pipes with physics-based flow distribution.

## Overview

Visualizes a pipe system where flow splits through three parallel branches with different lengths and diameters, then converges. Uses streamline-based particles to show the flow distribution.

## Structure

```
parallel_pipes/
├── scenes.py           # Main animation scene
├── inputs.yaml         # Configuration (dimensions, physics)
├── manim.cfg           # Manim settings
├── helpers/
│   ├── geometry.py     # Pipe/node visual generation
│   ├── physics.py      # Flow distribution calculation
│   ├── annotations.py  # Flow rate labels
│   ├── streamlines.py  # Streamline path composition
│   └── utils.py        # Config loader
└── README.md
```

## Physics

- **Flow Distribution:** $Q_i \propto \sqrt{D_i^5 / L_i}$ (equal head loss)
- **Velocity Profile:** Parabolic $v = v_{max}(1 - r^2/R^2)$

## Usage

```bash
manim -pql scenes.py ParallelPipesScene
```
