# Core config file that extends to all others

from __future__ import print_function
import config
import os.path

class Project(config.Config):

    def __init__(s):
        config.Config.__init__(s, os.path.expanduser("~/project_config.json"))
        s.load()

Project = Project() # Single shared project class

if __name__ == '__main__':
    ws = os.path.join(os.path.dirname(__file__), "test_workspace.json")
    Project.set_path(ws).load().put("show", "mll", "/path/to/config").save()
