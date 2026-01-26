import yaml

def load_config(filepath):
    """
    Load simulation parameters from a YAML file.
    """
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)
