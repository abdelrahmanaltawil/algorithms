"""Configuration loading utilities."""
import yaml


def load_inputs(inputs_path):
    """Loads a YAML inputs file.

    Args:
        inputs_path (str): The absolute path to the YAML inputs file.

    Returns:
        dict: The inputs dictionary loaded from the file.
    """
    with open(inputs_path, 'r') as f:
        return yaml.safe_load(f)
