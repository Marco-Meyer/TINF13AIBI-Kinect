from util import caching
from . import version
from .configs import check_name
from random import randint

##R : Range
##B : Boolean
##U : Undefined
##N1+ : 1 to inf
##N0+ : 0 to inf
##FN0+ : 0 to inf (float)
##N-1+ : -1 to inf
##S : Text
##POT: power of two
##C : 3 part color


rules = {"texture filter" : ("B",),
         "fullscreen" : ("N-1+",),
         "force alpha" : ("B",),
         "camera mode" : ("R",0,2),
         "mods" : ("B",),
         "interpolation" : ("B",),
         "vsync" : ("B",),
         "anisotropy" : ("R", 0, 16),
         "multisampling" : ("R", 0, 3),
         "version" : ("N1+",),
         "language" : ("S",),
         "window resolution" : ("U",),
         "fps limit" : ("N0+",),
         "netspeed" : ("N1+",),
         "double buffer" : ("B",),
         "mousewheel zoom" : ("B",),
         "player color" : ("C",),
         "player name" : ("Name",),
         "dithering" : ("B",),
         "priority" : ("R", 0,6),
         "mipmaps" : ("R",0,2),
         "chat line limit" : ("N1+",),
         "net packet size" : ("POT",9,15),
         "window position" : ("U",),
         "window mode" : ("R",0,2),
         "logic thread" : ("B",),
         "mouse camera" : ("B",),
         "supersampling" : ("FN0+",),
         "texture LoD bias" : ("R", -5, 5),
         "shaders" : ("B",),
         "use controller" : ("B",),
         "texture quality" : ("R",0,2),
            }


@caching.cache_copy
def get_default():
    
    default = {"window position" : [0,0],
               "window position comment" : "Starting position in [x,y] of the window. [-1,-1] for let OS decide.",
               "fullscreen" : 0,
               "fullscreen comment" : "0 for windowed, -1 for across all screens, otherwise 1 for primary monitor, 2 for secondary monitor and so on.",
               "version" : version.int,
               "version comment" : "Version of config file. Don't edit it.",
               "language" : "english",
               "language comment" : "Name of language to use.",
               "fps limit" : 200,
               "fps limit comment" : "Frames per Second may not go above this limit. 0 for unlimited. Unlimited is not recommended.",
               "shaders" : 1,
               "shaders comment" : "Use GPU programs for a variety of effects",
               }
    import getpass
    try: check_name(getpass.getuser())
    except Exception as e:
        default["player name"] = "Player %d" % randint(0,10000)
        raise e
    else:default["player name"] = getpass.getuser()
    return default
