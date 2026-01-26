# Series Pipes Flow Animation

Manim animation visualizing fluid flow through a series of connected pipes with varying diameters, demonstrating fundamental fluid dynamics principles.

## Overview

The animation shows a single batch of fluid moving through a sequence: **Inlet (Large) → Pipe A (Small) → Outlet (Large)**. It highlights:
1.  **Continuity Principle**: Velocity increases in narrower pipes ($A_1V_1 = A_2V_2$).
2.  **Momentum Preservation**: Fluid exiting the narrow pipe maintains its high velocity briefly ("Jet Effect") before decelerating.
3.  **Visual Clarity**: Explicit wall geometry, clean vertical joints, and batch particle flow.

## Structure

```
series_pipes/
├── scenes.py           # Main animation scene
├── inputs.yaml         # Configuration (dimensions, physics)
├── manim.cfg           # Manim settings
├── helpers/
│   ├── geometry.py     # Pipe/node visual construction
│   ├── physics.py      # Head and velocity calculations
│   ├── annotations.py  # Labels and arrows
│   └── utils.py        # Config loader
└── README.md
```

## Configuration

The simulation parameters are defined in `inputs.yaml`:

-   **Network**: Node positions and pipe dimensions (Length, Diameter).
-   **Physics**: Fluid properties (Flow Rate, Viscosity).
-   **Display**: Colors and scaling factors.

Modify `inputs.yaml` to change the system topology or flow conditions without touching the code.

## Physics Logic

-   **Variable Speed**: Particle velocity is updated dynamically based on the current pipe section's diameter.
-   **Momentum Decay**: Outlet velocity is modeled as:
    $$V(\alpha) = V_{slow} + (V_{fast} - V_{slow}) \cdot e^{-(\alpha - \alpha_0) / \tau}$$
    simulating the gradual dissipation of kinetic energy.

## Usage

Run the animation using Manim:

```bash
manim -pql scenes.py SeriesPipesScene
```
