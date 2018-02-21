# Base level workspace functionality.

from __future__ import print_function
import os.path
import json

class Config(object):

    def __init__(s, path):
        """ Load and use config file """
        s.set_config_path(path)
        s._data = {}

    def load(s):
        """ Open and read file. """
        try:
            with open(s._config_path, "r") as f:
                s._data = json.load(f)
        except ValueError:
            raise RuntimeError("There was an issue reading the workspace. %s" % s._config_path)
        except FileNotFoundError:
            s._data = {}
        return s

    def refresh(s):
        """ Alias for load """
        return s.load()

    def save(s):
        """ Save data to the config """
        with open(s._config_path, "w") as f:
            json.dump(s._data, f, indent=4)
        return s

    def set_config_path(s, path):
        """ Change location of config file. """
        s._config_path = path
        s._config_path_dir = os.path.dirname(path)
        return s

    def set(s, group, attribute, value):
        """ Add some data to config """
        s._data[group] = s._data.get(group, {})
        s._data[group][attribute] = value
        return s

    def get(s, group, attribute, default=None):
        """ Get some data from config """
        cat = s._data.get(group, {})
        return cat.get(attribute, cat.get("default", default))

    def set_path(s, group, attribute, path):
        """ Add a relative path to config """
        return s.set(group, attribute, os.path.relpath(path, s._config_path_dir).replace(os.path.sep, "/"))

    def get_path(s, group, attribute):
        """ Get relative path from config """
        return os.path.realpath(os.path.join(s._config_path_dir, s.get(group, attribute, "")))

if __name__ == '__main__':
    test = os.path.join(os.path.dirname(__file__), "config_test.json")
    conf = Config(test)
    conf.set("category1", "key", "value")
    assert "value" == conf.get("category1", "key")
    assert "value2" == conf.get("category1", "key2", "value2")
    conf.set("category1", "default", "val-you")
    assert "val-you" == conf.get("category1", "missing")
    assert "val-you" == conf.get("category1", "missingtoo", "val-all")
    conf.set_path("path_test", "path", "file/over.here")
    assert os.path.realpath(os.path.join(os.path.dirname(test), "file/over.here")) == conf.get_path("path_test", "path")
    conf.save()
