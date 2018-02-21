# Base level workspace functionality.

from __future__ import print_function
import json

class Config(object):

    def __init__(s, path):
        """ Load and use config file """
        s._config_path = path
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
        """ Save data to the workspace """
        with open(s._config_path, "w") as f:
            json.dump(s._data, f, indent=4)
        return s

    def set_path(s, path):
        """ Change location of workspace file. """
        s._config_path = path
        return s

    def put(s, category, key, value):
        """ Add some data to workspace """
        s._data[category] = s._data.get(category, {})
        s._data[category][key] = value
        return s

    def get(s, category, key, default=None):
        """ Get some data from workspace """
        cat = s._data.get(category, {})
        return cat.get(key, cat.get("default", default))

if __name__ == '__main__':
    import os.path
    test = os.path.join(os.path.dirname(__file__), "config_test.json")
    conf = Config(test)
    conf.put("category1", "key", "value")
    assert "value" == conf.get("category1", "key")
    assert "value2" == conf.get("category1", "key2", "value2")
    conf.put("category1", "default", "val-you")
    assert "val-you" == conf.get("category1", "missing")
    assert "val-you" == conf.get("category1", "missingtoo", "val-all")
    conf.save()
