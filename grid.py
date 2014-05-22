import numpy
from itertools import product
from random import randint
import copy
import sys
sys.path.append("Engine")
from sounds import Sounds 

#sounds = Sounds()

class Grid():
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.posses = tuple(product(range(x), range(y)))
        self.area = numpy.zeros((x,y),numpy.int32)
        #new tiles
        self.fresh = set()
        self.fill_random()
        self.fill_random()
        self.last = numpy.copy(self.area)

    def fill_random(self):
        """Fills in a random position with 2 or 4
        returns True if a spot was found."""
        for x,y in self.posses:
            if not self.area[x, y]:
                break
        else:
            return False#if the entire grid is full
        x,y = randint(0,self.x-1),randint(0,self.y-1)
        while self.area[x, y]:
            x,y = randint(0,self.x-1),randint(0,self.y-1)
        self.area[x, y] = 2 if randint(0,3) else 4#25% chance for a 4
        self.fresh.add((x,y))
        return True
    
    def move_slice(self, slice):
        """Merges and Moves all Tiles to the right in a horizontal slice"""
        movement = False
        blocked = set()

        #check the slice for merges
        for x in range(self.x-1, -1, -1):
            if slice[x]:
                if self.merge_point(x, slice, blocked):movement = True
        #move everything to the right
        innermove = True
        while innermove:
            innermove = False
            for x in range(self.x-2, -1, -1):
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
        for xi in range(x+1, self.x):
            if slice[xi] == val and xi not in blocked:#not already merged and has to be equal
                slice[xi] = val*2 
                slice[x] = 0
                self.addscore(val*2)
                blocked.add(xi)#prevent multiple merges per movement
                movement = True
                break
            elif slice[xi]:#different number
                break
        return movement
    
    def move(self, direction = 0):
        """Moves the entire Grid in direction"""
        used = set()
        if direction:self.area = numpy.rot90(self.area, direction)
        moves = False
        for y in range(self.y):
            if self.move_slice(self.area[:, y]):
                moves = True
                #sounds.timer_stop("Slide", 0.1)
                sounds.play_sound("Slide")

        if direction:self.area = numpy.rot90(self.area, 4-direction)
        return moves

    def check_merge(self):
        grid_twit = copy.deepcopy(self)
        grid_twit.move(1)
        grid_twit.move(2)
        if numpy.array_equal(grid_twit.area, self.area): return False
        return True

    def addscore(self, points):
        self.game.score += points
        self.game.scbar.refresh()#refreshes the scorebar with current score

    def reset(self):
        self.area = numpy.zeros((self.x,self.y),numpy.int32)
        self.fill_random()
        self.fill_random()
