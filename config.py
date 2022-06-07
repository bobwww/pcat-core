import json


DEFAULTCFG =    {

    "sniffer":
    {
        "iface": ""
    },
    "analyzer":
    {
        "plugins": {
            "./example.py": ["argument1", "argument2"]
        },
        "rulesetPath": "./data/script.lcat",
        "skipRuleset": False
    },
    "enforcer":
    {
        "default": {
            "alert": False,
            "log": True,
            "send": True
        }
    },
    "logger": 
    {
        "uri": "mongodb://localhost:27017"
    },
    "sender":
    {
        "iface": "" 
    }

}


def __getshape(d):
    """
    Given a dictionary, returns its shape with value types.
    """
    if isinstance(d, dict):
        return {k: __getshape(d[k]) for k in d}
    else:
        # Replace all non-dict values with None.
        return type(d)

def validate_config(cfg: dict):
    """
    Given a config, verifies whether it matches the default shape.
    """
    if isinstance(cfg, dict):
        return __getshape(cfg) == __getshape(DEFAULTCFG)
    else:
        return False

def reset_config(path:str='.'):
    "Resets the JSON file to default."
    with open(path, 'w') as fd:
        json.dump(DEFAULTCFG, fd, indent=4)


def load_config(path:str):
    """
    Given a path to a JSON file, loads and returns it as dictionary.
    """
    with open(path, 'r') as fd:
        return json.load(fd)
    

def dump_config(cfg:str, path:str):
    """
    Given a dictionary and path, dumps it in JSON form.
    """
    with open(path, 'w') as fd:
        json.dump(cfg, fd, indent=4)
