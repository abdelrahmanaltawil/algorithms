# Pipe Flow Animations

This project contains Manim animations for visualizing different types of fluid flow profiles, including open channels, gravity pipes, and closed pressurized pipes.

## Prerequisites

To run these animations, you need:

*   **Python 3.7+**
*   **Manim Community Edition**: [Installation Guide](https://docs.manim.community/en/stable/installation.html)
*   **PyYAML**: For parsing the configuration file.

## Installation

1.  Clone the repository.
2.  Install the dependencies:
    ```bash
    pip install manim pyyaml numpy
    ```

## Project Structure

*   **`scenes.py`**: The main script containing the Manim scene classes:
    *   `OpenChannelProfile`: Visualizes velocity profiles in an open channel.
    *   `GravityPipeProfile`: Visualizes flow in a partially filled pipe (gravity flow).
    *   `ClosedPipeProfile`: Visualizes flow in a fully pressurized pipe.
*   **`inputs.yaml`**: A configuration file to adjust geometry, dimensions, and animation settings without modifying the code.
*   **`manim.cfg`**: Manim-specific configuration (quality, output directory, frame size).
*   **`helpers/`**: A directory containing helper functions and modules used by `scenes.py`.

## Usage

Navigate to the `Animations/pipes_flow` directory and run the Manim command.

### Rendering a Specific Scene

To render a scene (e.g., `OpenChannelProfile`) with low quality (fastest for preview):

```bash
manim -pql scenes.py OpenChannelProfile
```

*   `-p`: Preview the animation after rendering.
*   `-q`: Quality flag (`l` for low, `m` for medium, `h` for high, `k` for 4k).

### Available Scenes

*   `OpenChannelProfile`
*   `GravityPipeProfile`
*   `ClosedPipeProfile`

## Configuration

### `inputs.yaml`

You can customize the simulation parameters in `inputs.yaml`.

**Example:**
```yaml
scenes:
  open_channel:
    geometry:
      v_max: 5          # Maximum velocity
      slope_angle_deg: -5 # Channel slope
...
global:
  animation:
    particle_count: 50
```

### `manim.cfg`

This file controls the rendering output.
*   **Output Directory**: Defaults to `./results`
*   **Frame Size**: Configured to `frame_height = 50`, `frame_width = 100` (Manim units).
