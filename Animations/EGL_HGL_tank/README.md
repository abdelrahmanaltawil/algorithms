# EGL/HGL Tank Animation

A Manim animation demonstrating **Energy Grade Line (EGL)** and **Hydraulic Grade Line (HGL)** behavior in a tank-to-tank pipe system with dynamic diameter changes.

## Features

- **Visual Hydraulics**: Real-time EGL/HGL calculation with step losses (minor) and slope losses (major)
- **Dynamic Animation**: Watch how changing Pipe 3's diameter affects the hydraulic profile
- **Configurable**: All parameters defined in `inputs.yaml`
- **Modular Code**: Clean separation of geometry, labels, and physics

## File Structure

```
EGL_HGL_tank/
├── scenes.py      # Main animation scene
├── geometry.py    # Tank/pipe geometry creation
├── labels.py      # Labels, symbols, and annotations
├── helpers.py     # Physics calculations (EGL/HGL)
├── inputs.yaml    # Configuration parameters
└── README.md      # This file
```

## Quick Start

```bash
# Low quality (fast preview)
manim -pql scenes.py EGL_HGL_Tank

# High quality (production)
manim -pqh scenes.py EGL_HGL_Tank
```

## Configuration

Edit `inputs.yaml` to customize:

| Parameter | Description |
|-----------|-------------|
| `tanks.tank1/tank2` | Tank dimensions and positions |
| `pipes.pipe1/2/3` | Pipe dimensions, positions, minor loss K factors |
| `hydraulics` | Initial head, friction factor |
| `global.quality` | Render quality (low/medium/high) |

## Physics Model

The animation uses the **Darcy-Weisbach equation** for head loss:

$$h_f = f \cdot \frac{L}{D} \cdot \frac{v^2}{2g}$$

Where:
- $h_f$ = Head loss (major)
- $f$ = Friction factor
- $L$ = Pipe length
- $D$ = Pipe diameter
- $v$ = Flow velocity

**Minor losses** are calculated as: $h_m = K \cdot \frac{v^2}{2g}$

## Dependencies

- Python 3.8+
- Manim Community Edition
- NumPy
- PyYAML
