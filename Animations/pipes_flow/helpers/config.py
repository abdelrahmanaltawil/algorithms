"""Configuration loading utilities."""
import yaml


def load_config(config_path):
    """Loads a YAML configuration file.

    Args:
        config_path (str): The absolute path to the YAML configuration file.

    Returns:
        dict: The configuration dictionary loaded from the file.
    """
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
