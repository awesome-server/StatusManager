from datetime import datetime

import pytz
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


def strf_time_diff(t1, t2):
    diff = t1 - t2
    div = divmod(diff.seconds, 3600)
    hours = div[0]

    if hours > 0:
        return f"{hours} hour(s)"

    div = divmod(div[1], 60)
    minutes = div[0]
    seconds = div[1]

    if minutes > 0:
        return f"{minutes} minute(s)"
    else:
        return f"{seconds} second(s)"


def date_now():
    datetime.today().date()
