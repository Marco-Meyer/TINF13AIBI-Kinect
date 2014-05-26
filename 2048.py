#! python3.4
import pygame as P
from random import *
from array import array
import sys
sys.path.append("Engine")
from itertools import product
import numpy
from os.path import join
from sounds import Sounds
import copy
from Circuit import electronics
from Circuit import lcd
from score import Score
from grid import Grid

class Game():
    def __init__(self, grid, score, scorebar):
        self.grid = grid
        grid.game = self
        self.score = score
        score.game = self
        self.scbar = scorebar
        scorebar.game = self
        
P.init()
gameover = False
W,H = FIELD = (4,4)
GRID = 150#Size of grid squares
resw, resh = resolution = W*GRID, H*GRID
#Sizes of Scorebar
vext = 110
vextH = vext/2
reswH = resw/2
shadowd = 4
side = 100
GRIDh = GRID//2#half the size of a grid
GRIDv = GRIDh//2#quarter "
pixels = (resw, resh+vext)
S = P.display.set_mode(pixels)
print("Resolution:",pixels)
D = S.subsurface((0,vext, resw, resh))
#Upper Surface ('Scorebar')
U1 = S.subsurface((0, 0, reswH, vext))
U2 = S.subsurface((reswH, 0, reswH, vext))
P.display.set_caption("2048 Kinergie")

from events import Manager
F = P.font.Font(None, 70)#System default font @ 70 size
scF = P.font.Font(None, 36)#Font of Scorebar @ 36 size

#Sound
volume = 0.5 #between 0.0 - 1.0
sound_time = 0.1


#Design
bgU = P.image.load(join('Images', 'monitor.png'))
bgD = P.image.load(join('Images', 'background.png'))


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
        self.refresh()
    def refresh(self):
        U1.blit(bgU, (0,0))
        U2.blit(bgU, (0,0))
        self.labCur = scF.render("Score", True, (61, 61, 61))
        self.labHig = scF.render("Highscore", True, (61, 61, 61))
        blit_centered(U1, self.labCur, (reswH/2, vextH/3+10))
        blit_centered(U2, self.labHig, (reswH/2, vextH/3+10))

        advCur = self.ld.render("%s" % (score.current), 6)
        advHig = self.ld.render("%s" % (score.highest), 6)
        blit_centered(U1, advCur, (reswH/2, vextH/3*4-3))
        blit_centered(U2, advHig, (reswH/2, vextH/3*4-3))

def rot90(x,y, times):
    #not sure if it's working
    print(x,y, "rotation")
    return rot90(H-y-1, x, times-1) if times else (x,y)

def new_Round():
    global gameover
    gameover = False
    score.next_Round()
    grid.reset()

assert(rot90(3,2,4) == (3,2))

def pos_gen():
    yield from product(range(W), range(H))

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
centers = []
for x in range(xdelta,resw,xdelta):
    for y in range(xdelta,resh,xdelta):
        centers.append((x,y))
tilemap = electronics.TileMap()
elegrid = electronics.Grid(resolution, chip, connectors, centers, tilemap)

#score
score = Score()
scbar = Scorebar()

#grid
posses = tuple(pos_gen())#all (x,y) pairs of the grid
grid = Grid(W,H)

#game
game = Game(grid, score, scbar)

#sound
sounds = Sounds()

#colors
background = P.Color("light grey")
base = P.Color(250, 250, 250)
shadow = P.Color(100, 100, 100)
marker = P.Color(200,100,100)
gocolor = P.Color(255, 0, 0, 100)

#surface
text = { 2**x : F.render(str(2**x), 1, (0,0,0)) for x in range(20)}
freshs = { 2**x : F.render(str(2**x), 1, (127,127,127)) for x in range(20)}
deltas = { 2**x : F.render(str(2**x), 1, (0,0,150)) for x in range(20)}

#Game Over-Surface
GO = P.Surface((resw, resh), P.SRCALPHA)
GO.fill(gocolor)
gof = F.render("Game Over", True, (0, 0, 0))
blit_centered(GO, gof, (resw/2, resh/2))

#misc
clock = P.time.Clock()
EM.dispatch("game_start", grid)

if __name__ == "__main__":

    ####Background Sound####
    sounds.play_sound("Background")

    while 1:
        
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
                        grid.fill_random()
                        ###########Slide############
                        if grid.area.all() and not gameover:#grid full and not yet gameover
                            if not grid.check_merge():

                                ####Lose Sound####
                                sounds.timer_stop("Lose", 0.1)
                                sounds.play_sound("Lose")
                                gameover = True

                                gameover = True                              

            elif e.type == P.KEYDOWN and gameover:
               new_Round()
                    
        #####LOGICBLOCK#####
        EM.dispatch("game_logic_start", grid)

        #####RENDERBLOCK#####
        #D.fill(background)
        D.blit(elegrid.surface, (0,0))
        EM.dispatch("game_frame_start", D)
        delta = grid.area != grid.last #elementwise check for matrix
        for (x,y), pos in zip(posses,centers):
            val = grid.area[x, y]
            #rectshadow = x*GRID+GRIDh-side/2+shadowd, y*GRID+GRIDh-side/2+shadowd, side, side
            #P.draw.rect(D, shadow, rectshadow, 0)
            #rect = x*GRID+GRIDh-side/2, y*GRID+GRIDh-side/2, side, side
            #P.draw.rect(D, base, rect, 0)
            if val:
                #pos = x*GRID+GRIDh,y*GRID+GRIDh
                if (x,y) in grid.fresh:blit_centered(D, freshs[val],pos)
                elif delta[x,y]:blit_centered(D, deltas[val],pos)
                else:blit_centered(D, text[val],pos)
        if gameover:
            D.blit(GO, (0,0))
        EM.dispatch("game_frame_end", D)
        P.display.flip()
        clock.tick(60)
