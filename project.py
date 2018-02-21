# Base level workspace functionality.

from __future__ import print_function
import os.path
import json

class Project(object):

    def __init__(s):
        s._config_path = os.path.expanduser("~/project_workspace.json")
        s.load()

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
        return s._data.get(category, {}).get(key, defualt)

Project = Project() # Single workspace class

if __name__ == '__main__':
    ws = os.path.join(os.path.dirname(__file__), "test_workspace,json")
    Project.set_path(ws).load().put("scene", "aba", "/path/to/config").save()
