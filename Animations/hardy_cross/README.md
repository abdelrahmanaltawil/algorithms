# Hardy Cross Method Animation

Manim animation visualizing the iterative solution of flow distribution in a pipe network using the Hardy Cross method.

## Overview

The animation demonstrates the convergence of flow rates in a closed loop system. It highlights:
1.  **Loop Definition**: Identification of closed loops within the network.
2.  **Iterative Balancing**: Step-by-step adjustment of flow rates based on head loss imbalance ($\sum h_f \neq 0$).
3.  **Correction Calculation**: Visualizing the calculation of $\Delta Q$ for each iteration.
4.  **Convergence**: The final state where head losses sum to zero around the loop.

## Structure

```
hardy_cross/
├── scenes.py           # Main animation scene
├── inputs.yaml         # Configuration (network topology, initial guessing)
├── manim.cfg           # Manim settings
├── helpers/
│   ├── geometry.py     # Network node and pipe construction
│   ├── physics.py      # Head loss and delta Q calculations
│   ├── annotations.py  # Loop direction, flow labels, and iteration data
│   └── utils.py        # Config loader
└── README.md
```

## Physics Logic

-   **Head Loss Formula**: Uses the general form $h_f = r \cdot Q \cdot |Q|^{n-1}$ (e.g., Hazen-Williams or Darcy-Weisbach).
-   **Correction Factor**: Calculates the flow adjustment $\Delta Q$ for each loop:
    $$ \Delta Q = - \frac{\sum h_f}{n \cdot \sum \frac{h_f}{Q}} $$
-   **Flow Update**: Updates flow rates $Q_{new} = Q_{old} + \Delta Q$, ensuring continuity at nodes.

## Usage

Run the animation using Manim:

```bash
manim -pql scenes.py HardyCrossScene
```
