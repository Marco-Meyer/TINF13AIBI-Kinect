#! python3.4
import pygame as P
from OpenGL.GL import *
from OpenGL.GLU import *
import shader

cached_res = (1,1)#global storage for last resolution

default = {"rotation" : (0,0,0),
           "scale" : 0.02,
           "fov" : 70,
           "translation" :(0,0, -10.0)}

delta = {"rotation" : [0,0,0],
           "scale" : 0.00,
           "fov" : 0,
           "translation" :[0,0,0]}
disco = False
import os
try:
    from json import load
    with open("calibration.txt") as f:
        default = load(f)
    print("Loaded Calibration File")
except FileNotFoundError:
    from json import dump
    with open("calibration.txt", "w") as f:
        dump(default, f)
    print("Created Calibration File")
except:
    import traceback
    traceback.print_exc()

override = False #manual calibration override
showmenu = False
menuselection = "rotation"
menuid = 0

def apply_delta(base, delta):
    new = {}
    for key, value in base.items():
        t = type(value)
        if t in {list, tuple}:
            new[key] =  [x+y for x,y in zip(value, delta[key])]
        elif t in {int, float, complex}:
            new[key] =  value+delta[key]
        else:
            raise NotImplementedError("No handling for type %s" % t)
    return new
menu = """
F1: Toggle Menu and Hotkeys
F2: Toggle Manual Override
F3: Increase FOV
F4: Decrease FOV
F5: Increase Scale
F6: Decrease Scale
F9: Decrease Selection
F10:Increase Selection
F11:change submenu
F12:change mainmenu
"""

def _changed(func):
    def new_handle(event):
        ret = func(event)
        if ret is False:
            setup_projection(cached_res)
        return ret
    return new_handle

@_changed
def handle_event(event):
    global override, showmenu, menuselection, menuid
    
    if event.type == P.KEYDOWN:
        if event.key == P.K_F1:
            showmenu = not showmenu
            if showmenu:
                print(menu)
                print("Hotkeys are now active")
            else:print("Hotkeys deactivated")
            return None
        if showmenu:
            k = event.key
            if k == P.K_F2:
                override = not override
                if override:
                    print("Override now active")
                else:
                    print("Override deactivated")
            elif k == P.K_F3:delta["fov"] += 1
            elif k == P.K_F4:delta["fov"] -= 1
            elif k == P.K_F5:delta["scale"] += 0.001
            elif k == P.K_F6:delta["scale"] -= 0.001
            elif k == P.K_F9:
                delta[menuselection][menuid] -= 5 if menuselection == "translation" else 0.1
            elif k == P.K_F10:
                delta[menuselection][menuid] += 5 if menuselection == "translation" else 0.1
            elif k == P.K_F12:
                menuid += 1
                if menuid > 2:
                    menuid -= 3
                print("Menu ID:%d" % menuid)
            elif k == P.K_F11:
                menuselection = "rotation" if menuselection == "translation" else "translation"
                print("In menu %s." % menuselection)
            else:return True
            print(delta[menuselection][menuid])
            return False
    return True
print(menu)
print("Hotkeys deactivated")
del(_changed)
class Calllist():
    """ openGL calllist wrapper"""
    def __init__(self):
        liste = glGenLists(1)
        glNewList(liste, GL_COMPILE)
        self.execute = lambda :glCallList(liste)
        self.list = liste
    def end(self):
        glEndList()
    def __del__(self):glDeleteLists(self.list,1)
    
class Texture():
    def __init__(self, textureID, width, height, dl = True):
        self.id = textureID
        self.width = width
        self.height = height
        if dl:self.get_DisplayList()
        
    def __del__(self):
        glDeleteTextures(self.id)
        
    def get_DisplayList(self):
        wh = self.width//2
        hh = self.height//2
        self.dl = Calllist()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glBegin(GL_QUADS)
        
        glTexCoord2f(0, 0); glVertex2f(-wh, -hh)
        glTexCoord2f(0, 1); glVertex2f(-wh, hh)
        glTexCoord2f(1, 1); glVertex2f(wh, hh)
        glTexCoord2f(1, 0); glVertex2f(wh, -hh)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        self.dl.end()
        
    def render_centered(self):
        wh = self.width//2
        hh = self.height//2
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(-wh, -hh)
        glTexCoord2f(0, 1); glVertex2f(-wh, hh)
        glTexCoord2f(1, 1); glVertex2f(wh, hh)
        glTexCoord2f(1, 0); glVertex2f(wh, -hh)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        
def Surface2Texture(surface):
    gl = GL_RGBA
    name = "RGBA"
    data = P.image.tostring(surface, name, 1)
    width, height = surface.get_size()
    textureID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureID)
    #linear interpolation
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    #prevent bleed
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
    #upload data
    glTexImage2D(GL_TEXTURE_2D,0,gl,width,height,0,gl,GL_UNSIGNED_BYTE,data)
    return Texture(textureID, width, height)

def init(resolution):
    P.display.set_mode(resolution, P.OPENGL|P.DOUBLEBUF|P.RESIZABLE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    setup_projection(resolution)
    
def setup_projection(resolution, config = default):
    global cached_res
    cached_res = resolution
    if override:config = apply_delta(config, delta)
    w,h = resolution
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    scale = config["scale"]
    glScalef(scale, scale, scale)
    gluPerspective(config["fov"],w/h,0.1,1000.0)
    glTranslatef(*config["translation"])
    x,y,z = config["rotation"]
    glRotatef(x, 1,0,0)
    glRotatef(y, 0,1,0)
    glRotatef(z, 0,0,1)
    
def render(surface):
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    texture = Surface2Texture(surface)
    glMatrixMode(GL_PROJECTION)
    if disco:
        import math
        import time
        t = time.clock()
        glColor3d(0.5+math.sin(t*2)*0.5,0.5+math.sin(4.5+t)*0.5,0.75+math.sin(0.25+t*1.1)*0.25)
    else:
        glColor3d(1,1,1)
    texture.render_centered()

if __name__ == "__main__":
    input("Press Enter to start pong with projection")
    import os
    os.system("pong.py POSTPROCESS:True")
    
