import yaml


def load_config(path):
    """Loads a YAML configuration file from a supplied address.
    Arguments:
        config {path} -- Path for configuration file.
    """

    try:
        with open(path, "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.SafeLoader)

        return config

    except FileNotFoundError:
        print("Missing YAML configuration at '%s'" % (path))
        exit(0)
