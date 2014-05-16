import os

join = os.path.join
import sys
if sys.platform.startswith("win"):
    appdata = os.environ["APPDATA"]
    project = join(appdata, "Kingine")
else:
    appdata = os.environ["HOME"]
    project = join(appdata, ".Kingine")

config = join(project, "config.txt")
temp = join(project, "RAM dir")

dirs = [project, temp]
for d in dirs:
    if not os.path.isdir(d):os.mkdir(d)



from .version import current
version = current

from . import configs
options = None
def init():
    """Load all options.
    """
    global options
    options = configs.load_options()
    
