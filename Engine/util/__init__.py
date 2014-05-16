def list_inc(x, sub):
    return sub[(sub.index(x)+1) % len(sub)]
def list_sub(x, sub):
    return sub[(sub.index(x)-1) % len(sub)]
from re import compile

allowed = compile(" [0-9+*/.-]")

class ProhibitedInput(Exception):pass

def math_eval(s):
    """eval()'uate a mathematical expression safely""" 
    if allowed.match(s):#only numbers and operators
        raise ProhibitedInput("Usage of forbidden characters.")
    else:
        return eval(s)
        
def math_eval_repl(s, replacements = {}):
    """eval()'uate a mathematical expression safely, with replacement dict of {old : new}""" 
    for old, new in replacements.items():
        s = s.replace(old, new)
    if allowed.match(s):#only numbers and operators
        raise ProhibitedInput("Usage of forbidden characters outside of replacement names.")
    else:
        return eval(s)

def rect_to_verts(r):
    """get Vertex List for x,y,x2,y2 rect"""
    return (r[0],r[1], 
            r[2],r[1],
            r[2],r[3],
            r[0],r[3])
    
def size_to_pos_rect(rect):
    """Convert rect of x,y,w,h to x,y,x2,y2"""
    return rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3]
def pos_to_size_rect(rect):
    """Convert rect of x,y,x2,y2 to x,y,w,h"""
    return rect[0],rect[1],rect[2]-rect[0], rect[3]-rect[1]

def string_filter(string, start, end):
    """filter out characters between starts and ends"""
    level = 0
    new = ""
    for c in string:
        if c == start:level += 1
        elif c == end:level -=1
        elif not level:new += c
    return new

def open_file(path):
    import webbrowser
    webbrowser.open(path)
