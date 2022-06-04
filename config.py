import yaml

#   Shape of the config file for validation
DEFAULTSHAPE = {
    'default': {
        'alert': bool,
        'send': bool,
        'log': bool
    }
}

#   Default config for when config file is corrupted
DEFAULTCFG = {
    'default': {
        'alert': False,
        'send': True,
        'log': True
    }
}
# !! Make sure the two above dicts are with the EXACT same shape !!

def __getshape(d):
    """
    Given a dictionary, returns its shape with value types.
    """
    if isinstance(d, dict):
        return {k: __getshape(d[k]) for k in d}
    else:
        # Replace all non-dict values with None.
        return type(d)

def validate_config(cfg):
    """
    Given a config, verifies whether it matches the default shape.
    """
    if isinstance(cfg, dict):
        return __getshape(cfg) == DEFAULTSHAPE


def load_config(path):
    """
    Given a path to a YAML file, loads and returns it as dictionary.
    """
    with open(path, 'r') as fd:
        return yaml.safe_load(fd)
    

def dump_config(cfg, path):
    """
    Given a dictionary and path, dumps it in YAML form.
    """
    with open(path, 'w') as fd:
        yaml.safe_dump(cfg, fd)

