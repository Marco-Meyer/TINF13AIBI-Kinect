import pygame as P
from random import *
from array import array
import sys
sys.path.append("Engine")
from itertools import product
import numpy
from functools import singledispatch
P.init()
W,H = FIELD = (4,4)
GRID = 120#Size of grid squares
resw, resh = resolution = W*GRID, H*GRID

GRIDh = GRID//2#half the size of a grid
GRIDv = GRIDh//2#quarter "
D = P.display.set_mode(resolution)
P.display.set_caption("2048 YAC")

from events import Manager
F = P.font.Font(None, 70)#System default font @ 70 size

####GAMEEVENTS####
EM = Manager()
eventnames = {"game_start" : "grid","game_end" : "grid","game_frame_start" : "displaysurface","game_logic_start" : "grid",
              "movement_start" : ("grid", "direction"), "game_frame_end" : "displaysurface"}
[EM.register_event(name, argnames = args) for name, args in eventnames.items()]
print(EM)
##################

class Grid():
    def __init__(self, x,y):
        self.x = x
        self.y = y
        #grid data is saved in a numpy 2d array
        self.area = numpy.zeros((x,y),numpy.int32)
        #new tiles
        self.fresh = set()
        
    def fill_random(self):
        """Fills in a random position with 2 or 4
        returns True if a spot was found."""
        for x,y in posses:
            if not self.area[x, y]:
                break
        else:
            return False#if the entire grid is full
        x,y = randint(0,W-1),randint(0,H-1)
        while self.area[x, y]:
            x,y = randint(0,W-1),randint(0,H-1)
        self.area[x, y] = 2 if randint(0,3) else 4#25% chance for a 4
        self.fresh.add((x,y))
        return True
    
    def move_slice(self, slice):
        """Merges and Moves all Tiles to the right in a horizontal slice"""
        movement = False
        blocked = set()

        #check the slice for merges
        for x in range(W-1, -1, -1):
            if slice[x]:
                if self.merge_point(x, slice, blocked):movement = True
        #move everything to the right
        innermove = True
        while innermove:
            innermove = False
            for x in range(W-2, -1, -1):
                if slice[x] and not slice[x+1]:
                    slice[x+1] = slice[x]
                    slice[x] = 0
                    movement = True
                    innermove = True
        return movement
    
    def merge_point(self, x, slice, blocked):
        """Checks the Tile for mergability"""
        movement = False
        val = slice[x]
        for xi in range(x+1, W):
            if slice[xi] == val and xi not in blocked:#not already merged and has to be equal
                slice[xi] = val*2
                slice[x] = 0
                blocked.add(xi)#prevent multiple merges per movement
                movement = True
                break
            elif slice[xi]:#different number
                break
        return movement
    
    def move(self, direction = 0):
        """Moves the entire Grid in direction"""
        EM.dispatch("movement_start", self, direction)
        used = set()
        if direction:self.area = numpy.rot90(self.area, direction)
        moves = False
        for y in range(H):
            if self.move_slice(self.area[:, y]): moves = True
        if direction:self.area = numpy.rot90(self.area, 4-direction)
        return moves

grid = Grid(W,H)

def rot90(x,y, times):
    #not sure if it's working
    print(x,y, "rotation")
    return rot90(H-y-1, x, times-1) if times else (x,y)


assert(rot90(3,2,4) == (3,2))

def pos_gen():
    yield from product(range(W), range(H))
    
posses = tuple(pos_gen())#all (x,y) pairs of the grid

def blit_centered(target, blitter, pos):
    """Blits blitter centered on pos onto target"""
    x,y = pos
    xd, yd = blitter.get_size()
    target.blit(blitter, (x-xd//2,y-yd//2))

    
#colors
background = P.Color("light grey")
base = P.Color(250, 250, 250)
clock = P.time.Clock()
grid.fill_random()
grid.fill_random()
text = { 2**x : F.render(str(2**x), 1, (0,0,0), base) for x in range(20)}
freshs = { 2**x : F.render(str(2**x), 1, (127,127,127), base) for x in range(20)}
deltas = { 2**x : F.render(str(2**x), 1, (0,0,150), base) for x in range(20)}

marker = P.Color(200,100,100)
grid.last = numpy.copy(grid.area)
EM.dispatch("game_start", grid)
if __name__ == "__main__":
    while 1:
        #####EVENTBLOCK#####
        for e in P.event.get():
            if e.type == P.QUIT:
                P.quit()
                sys.exit()
            elif e.type == P.KEYDOWN:
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
                    if grid.move(direction-1):
                        grid.fill_random()
                    
        #####LOGICBLOCK#####
        EM.dispatch("game_logic_start", grid)
        #####RENDERBLOCK#####
        D.fill(background)
        EM.dispatch("game_frame_start", D)
        delta = grid.area != grid.last
        for x,y in posses:
            val = grid.area[x, y]
            rect = x*GRID+GRIDv,y*GRID+GRIDv,GRIDh,GRIDh
            P.draw.rect(D, base, rect, 0)
            if val:
                pos = x*GRID+GRIDh,y*GRID+GRIDh
                if (x,y) in grid.fresh:blit_centered(D, freshs[val],pos)
                elif delta[x,y]:blit_centered(D, deltas[val],pos)
                else:blit_centered(D, text[val],pos)
        EM.dispatch("game_frame_end", D)
        P.display.flip()
        clock.tick(60)
