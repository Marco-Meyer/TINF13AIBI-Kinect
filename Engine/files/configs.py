import string


options = None
import json as serializer
from . import version, config

def check_name(value, key="player name"):
    """Ensure that the name provided passes some basic checks
    such as a length check and a value check so that the name
    is not a value like "SERVER" or "SYSTEM", which could duplicate
    the name of the server.

    args:
        value - name

    keywords:
        key - key of config dict that holds this value
        used for the specific OptionTypeError

    """

    value = value.strip()
    if value.__class__.__name__ not in ["str", "unicode"]:
        raise OptionTypeError(key, "text")
    if len(value) < 2:
        raise OptionNameError()
    if value == ["SERVER"] or value == ["SYSTEM"]:
        raise OptionNameInvalidError()
    for key in value:
        if not key in string.printable:
            OptionNameCharacterError()
        if key in string.whitespace:
            if key != " ":
                OptionNameCharacterError()
    try: int(value)
    except:pass
    else:
        OptionNameNumberError()

from .configs_data import *

class OptionError(Exception):
    """Raised on error reading the config file. Or on a value error
    without a specific exception for it.

    """
    def __str__(self): return "Config file invalid"
class OptionRangeError(Exception):
    """Points out a specific error, being that a range
    rule is being broken by having been provided a value
    outside of the designated range.

    args:
        value - option key causing the error
        mi - minimum value of range
        ma - maximum value of range

    """
    def __init__(self, value, mi, ma):
        self.parameter = "Value for key %s is invalid. (Out of range %s to %s)" % (value,mi,ma-1)
    def __str__(self):
        return repr(self.parameter)
class OptionKeyError(Exception):
    """Raised on a specific key not existing

    args:
        value - key that doesn't exist

    """
    def __init__(self, value):
        self.parameter = "Key %s does not exist." % (value)
    def __str__(self):
        return repr(self.parameter)
class OptionTypeError(Exception):
    """Raised when an option in the config file is provided
    with a value type other than that which was exepcted.

    args:
        value - option key causing the error
        ttype - type expected

    """
    def __init__(self, value, ttype):
        self.parameter = "Type for key %s is invalid. Expected %s." % (value,ttype)
    def __str__(self):
        return repr(self.parameter)
class OptionNameError(Exception):
    """Raised when the name provided in a player config file is too short."""
    def __init__(self):
        self.parameter = "Name is too short, at least two letters are needed."
    def __str__(self):
        return repr(self.parameter)
class OptionNameInvalidError(Exception):
    """Used when a player attempts to use a name that is blocked or reserved."""
    def __init__(self):
        self.parameter = "Name is reserved, choose another."
    def __str__(self):
        return repr(self.parameter)
class OptionNameCharacterError(Exception):
    """Used when a player name contains illegal characters, such as tabs or
    unprintable characters.

    """
    def __init__(self):
        self.parameter = "Name contains at least one forbidden character, choose another."
    def __str__(self):
        return repr(self.parameter)
class OptionNameNumberError(Exception):
    """The message is "A name cannot be a number."
    Self-explanatory.

    """
    def __init__(self):
        self.parameter = "A name cannot be a number."
    def __str__(self):
        return repr(self.parameter)
class OptionPOTError(Exception):
    """Used for some specific options, is raised when the value provided
    is not a power of two.

    args:
        key - option key raising error

    """
    def __init__(self, key):
        self.key = key
    def __str__(self):
        return repr("%s has to be power of two" % self.key)



def check(options, rules = rules):
    """Ensures that the rules are followed for the options provided.

    args:
        options - options/config dict

    keywords:
        rules - rules to enforce with the options

    """
    s = ["str", "unicode"]
    for key in options:
        if not key.endswith(" comment"):
            if key in rules:
                c = rules[key]
            else:
                raise OptionKeyError(key)
            value = options[key]
            if c[0] == "U": continue
            elif c[0] == "POT":
                if not(((value & (value - 1)) == 0) and value):
                    raise OptionPOTError(key)
            elif c[0] == "R":
                if value not in list(range(c[1], c[2]+1)):
                    raise OptionRangeError(key, c[1], c[2]+1)
            elif c[0] == "B":
                if value not in list(range(0, 2)):
                    #print (value)
                    raise OptionRangeError(key, 0, 2)
            elif c[0] == "N1+":
                if value < 1:
                    raise OptionRangeError(key, 1, float("inf"))
            elif c[0] == "N0+":
                if value < 0:
                    raise OptionRangeError(key, 0, float("inf"))
            elif c[0] == "FN0+":
                if value < 0:
                    raise OptionRangeError(key, 0, float("inf"))
            elif c[0] == "N-1+":
                if value < -1:
                    raise OptionRangeError(key, -1, float("inf"))
            elif c[0] == "S":
                if value.__class__.__name__ not in s:
                    raise OptionTypeError(key, "text")
            elif c[0] == "Name":check_name(value,key)

            elif c[0] == "L":
                if value.__class__.__name__ != "list":
                    raise OptionTypeError(key, "list")

            elif c[0] == "C":
                if len(value) != 3:
                    raise OptionError()
                if sum(value) < 1:
                    raise OptionError()
            else:
                raise Exception("%s not valid rule type from %s" % (c[0], key))



def get_config(config = None):
    """Returns the default config if no args.
    When provided with a config dict, it compares the
    dict provided with that of the default and returns
    the config provided with updated keys.
  
    keywords:
        **config** : ``config``
            dict to compare to default

    """
    default = get_default()
    if config != None:
        for key in config:
            if not key.endswith(" comment"):
                default[key] = config[key]
    default["player name"] = default["player name"].strip()
    return default


def load_options():
    """Automatically loads the config file found in
    a user's config directory. Returns a decoded
    options dict.

    """
    try:
        with open(config, "rU") as f:
            options = serializer.load(f)
        check(options)
        if options["version"] < version:
            options["version"] = version.int
            options = get_config(options)
            save_options(options)
    except IOError:
        options = get_config()
        save_options(options)
    except Exception:
        print ("Options could not be loaded:")
        import traceback
        traceback.print_exc()
        options = get_config()
        save_options(options)
    else:
        o_o = options
        options = get_config(options)
        if o_o != options:
            save_options(options)
        del(o_o)
    globals()["clientoptions"] = options
    return options


valid_filenamechars = "%s%s-_.() " % (string.ascii_letters, string.digits)


def save_options(options):
    """Writes a config file with the options provided to
    the file's respective directory.

    args:
        options - options dict to be written into a file


    """
    with open(config, "wt") as f:
        f.write(serializer.dumps(options, indent = 4, sort_keys = True))
