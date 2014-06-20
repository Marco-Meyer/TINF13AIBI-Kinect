#! python2.7
#Use Python 3 features from the future:
from __future__ import division, print_function

#Build Configs
SOUNDS = True

import pygame as P
from random import *
from array import array
import sys
sys.path.append("Engine")
from itertools import product
import numpy
from os.path import join

from Circuit import electronics
from Circuit import lcd
from score import Score
from grid import Grid
import os
import time
import atexit

class Game():
    def __init__(self, grid, score, scorebar):
        self.grid = grid
        grid.game = self
        self.score = score
        score.game = self
        self.scbar = scorebar
        scorebar.game = self

def convertToGreyScale(surface):
    for x in range(surface.get_size()[0]):
        for y in range(surface.get_size()[1]):
            color = surface.get_at((x, y))
            greyscale = int(0.2989*color[0] + 0.5871 * color[1] + 0.114 * color[2])
            surface.set_at((x, y), (greyscale, greyscale, greyscale))




P.init()
gameover = False
W,H = FIELD = (4,4)
GRID = 150#Size of grid squares
resw, resh = resolution = W*GRID, H*GRID
#Sizes of Scorebar
vext = 110
vextH = 110//2
reswH = resw//2
shadowd = 4
side = 100
GRIDh = GRID//2#half the size of a grid
GRIDv = GRIDh//2#quarter "
pixels = (resw, resh+vext)
P.display.set_icon(P.image.load(join("Circuit", "icon.png")))
P.display.set_caption("2048 Kinergie", "2048")
S = P.display.set_mode(pixels)
print("Resolution:",pixels)
D = S.subsurface((0,vext, resw, resh))
#Upper Surface ('Scorebar')
U1 = S.subsurface((0, 0, reswH, vext))
U2 = S.subsurface((reswH, 0, reswH, vext))


if SOUNDS:
    from sounds import Sounds
else:
    from sounds import NoSounds as Sounds
from events import Manager
F = P.font.Font(None, 70)#System default font @ 70 size
scF = P.font.Font(None, 36)#Font of Scorebar @ 36 size
loadtext = F.render("Loading", 1, (255,255,255),(0,0,0))

r = S.blit(loadtext, (reswH-loadtext.get_width()//2,
                      pixels[1]//2-loadtext.get_height()//2))

P.display.update(r)
del(r,loadtext)
#Sound
volume = 0.5 #between 0.0 - 1.0
slidetime = 0.1
losetime = 1

#Design
bgU = P.image.load(join('Images', 'monitor.png'))

####GAMEEVENTS####
EM = Manager()
eventnames = {"game_start" : "grid","game_end" : "grid","game_frame_start" : "displaysurface","game_logic_start" : "grid",
              "movement_start" : ("grid", "direction"), "game_frame_end" : "displaysurface"}
[EM.register_event(name, argnames = args) for name, args in eventnames.items()]
print(EM)
##################

class Scorebar():
    def __init__(self):
        self.ld = lcd.LCD()
        self.labCur = scF.render("Score", True, (61, 61, 61))
        self.labHig = scF.render("Highscore", True, (61, 61, 61))
        self.refresh()
    def refresh(self):
        U1.blit(bgU, (0,0))
        U2.blit(bgU, (0,0))
        target = (reswH/2, vextH/3+10)
        blit_centered(U1, self.labCur, target)
        blit_centered(U2, self.labHig, target)

        advCur = self.ld.render("%s" % (score.current), 6)
        advHig = self.ld.render("%s" % (score.highest), 6)

        target = (reswH/2, vextH/3*4-3)
        blit_centered(U1, advCur, target)
        blit_centered(U2, advHig, target)

def new_Round():
    global gameover
    gameover = False
    score.next_Round()
    grid.reset()

def pos_gen():
    return tuple(product(range(W), range(H)))

def blit_centered(target, blitter, pos):
    """Blits blitter centered on pos onto target"""
    x,y = pos
    xd, yd = blitter.get_size()
    target.blit(blitter, (x-xd//2,y-yd//2))
    
#####INITBLOCK#####

#electronics
connectors = electronics.Connector(3,10,3)
chip = electronics.Chip(98, connectors)
xdelta = resw//5
centers = {}
for ix,x in enumerate(range(xdelta,resw,xdelta)):
    for iy,y in enumerate(range(xdelta,resh,xdelta)):
        centers[ix,iy] = (x,y)
        
tilemap = electronics.TileMap()
elegrid = electronics.Grid(resolution, chip, connectors, centers.values(), tilemap)
fizzles = electronics.AnimFizzle(elegrid, 50, 1)

#score
score = Score()
scbar = Scorebar()

#grid
posses = pos_gen()#all (x,y) pairs of the grid
grid = Grid(W,H)

#game
game = Game(grid, score, scbar)

#sound
sounds = Sounds()

#colors
background = P.Color("light grey")
marker = P.Color(200,100,100)
gocolor = P.Color(255, 0, 0, 100)

#surface
text = { 2**x : F.render(str(2**x), 1, (250,250,250)) for x in range(20)}
freshs = { 2**x : F.render(str(2**x), 1, (127,127,127)) for x in range(20)}
deltas = { 2**x : F.render(str(2**x), 1, (50,50,200)) for x in range(20)}

#Game Over-Surface
GO = P.Surface((resw, resh), P.SRCALPHA)
GO.fill(gocolor)
gof = F.render("Game Over", True, (255, 255, 255))
blit_centered(GO, gof, (resw/2, resh/2))

#misc
clock = P.time.Clock()
EM.dispatch("game_start", grid)
can_move = True
busy = idle = move_timeout = 0
next_resource_print = time.time()+5
show_moves = False

#autosave
import threading
main_thread = threading.current_thread()#unfortunately when debugging this returns the debugger
def periodic_save():
    while main_thread.is_alive():
        time.sleep(7)
        score.save()
        print("Autosaved")
        
threading.Thread(target=periodic_save, name="AutoSaver").start()


def load_music (self, file, path ="Sounds", ending = ".mp3"):
    self.music[file] = P.mixer.music.load(join(path, file+ending))



if __name__ == "__main__":

    ####Background Sound####   
    sounds.play_backgroundmusic()  
    
    while 1:
        timer = time.time()
        #####EVENTBLOCK#####
        for e in P.event.get():
            if e.type == P.QUIT:
                P.quit()
                sys.exit()

            elif e.type == P.KEYDOWN and not gameover:
                direction = 0
                if e.key == P.K_RIGHT:
                    direction = 1
                elif e.key == P.K_UP:
                    direction = 2
                elif e.key == P.K_LEFT:
                    direction = 3
                elif e.key == P.K_DOWN:
                    direction = 4
                if direction:
                    grid.fresh = set()
                    grid.last = numpy.copy(grid.area)
                    EM.dispatch("movement_start", grid, direction-1)                  
                    if grid.move(direction-1):
                        #####Slide-Sound########
                        sounds.play_slide_sound()                       
                        grid.fill_random()                        
                        if grid.area.all() and not gameover:#grid full and not yet gameover
                            if not grid.check_merge():
                                move_timeout = timer + 3 #1 second gameover
                                ####Lose Sound####
                                sounds.play_lose_sound()                              
                                gameover = True
                else:
                    if e.key == P.K_m:
                        show_moves = not show_moves
                        continue                                    
            elif e.type == P.KEYDOWN and gameover:
                if move_timeout <= timer and e.key == P.K_RIGHT:
                    score.save()
                    new_Round()

        
                    
        #####LOGICBLOCK#####
        EM.dispatch("game_logic_start", grid)

        #####RENDERBLOCK#####
        fizzles.render(D)
        EM.dispatch("game_frame_start", D)
        delta = grid.area != grid.last #elementwise check for matrix
        for x,y in posses:
            pos = centers[(x,y)]
            val = grid.area[x, y]
            if val:
                if (x,y) in grid.fresh:blit_centered(D, freshs[val],pos)
                elif delta[x,y]:blit_centered(D, deltas[val],pos)
                else:blit_centered(D, text[val],pos)

        #Transition
        clip = P.image.load(join("Images", "clip.png"))
        clip = P.transform.smoothscale(clip, (32, 13))
        D.blit(clip, (29, 0))
        D.blit(clip, (239, 0))
        D.blit(clip, (329, 0))
        D.blit(clip, (539, 0))


        if gameover: 
            convertToGreyScale(D)
            D.blit(GO, (0,0))

        ###DEBUG VISUALISATION###
        if show_moves:
            for start,end in grid.change.moves:
                start = centers[start]; end = centers[end]
                P.draw.circle(D, (255,255,255), start, 30,1)
                P.draw.line(D, (255,255,255), start, end)
                P.draw.circle(D, (50,250,250), end, 10,1)

            
        EM.dispatch("game_frame_end", D)
        P.display.flip()
        idlestart = time.time()
        clock.tick(60)
        #Resource evaluation
        post = time.time()
        busy += idlestart-timer
        idle += post-idlestart
        if timer > next_resource_print:
            next_resource_print = timer+5
            print("Was idling {}% the last 5 seconds""".format(int((100*idle)/(idle+busy))))
            busy = idle = 0
