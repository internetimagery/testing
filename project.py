# Core config file that extends to all others

from __future__ import print_function
import config
import os.path

class Project(config.Config):

    def __init__(s):
        config.Config.__init__(s, os.path.expanduser("~/project_config.json"))
        s.load()

    def new(s):
        """ Set up new project information """
        s.put("studio", "name", "pixar")
        s.put("init", "save_dir", "/$FILM/$TREE/$SCENE/$SHOT")
        return s

Project = Project() # Single shared project class

if __name__ == '__main__':
    ws = os.path.join(os.path.dirname(__file__), "test_workspace.json")
    Project.set_path(ws).new().put("show", "mll", "/path/to/config")
    Project.put("show", "aba", {"010/0010": "/path/to/scene/config.json"})
    Project.put("shot", "010/0010", "/path/to/shot/config.json").save()
