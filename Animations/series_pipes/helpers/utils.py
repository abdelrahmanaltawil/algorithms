"""
Utility functions for configuration loading.
"""
import yaml
import os


def load_config(file_path):
    """
    Loads a YAML configuration file.
    
    Args:
        file_path: Path to the YAML configuration file.
        
    Returns:
        dict: Parsed configuration data.
        
    Raises:
        FileNotFoundError: If the configuration file doesn't exist.
        yaml.YAMLError: If the YAML file is malformed.
    """
    abs_path = os.path.abspath(file_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Configuration file not found: {abs_path}")
        
    with open(abs_path, 'r') as f:
        try:
            config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML file {abs_path}: {e}")
