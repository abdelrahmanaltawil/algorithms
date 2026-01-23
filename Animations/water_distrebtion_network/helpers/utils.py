import yaml
import os

def load_config(file_path):
    """
    Loads a YAML configuration file.
    
    Args:
        file_path (str): Absolute or relative path to the YAML file.
        
    Returns:
        dict: The configuration dictionary.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
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
