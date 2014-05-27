import numpy
from itertools import product
from random import randint



class Grid():

    class StateChange():
        def __init__(self, direction):
            self.direction = direction
            self.movements = []
            
        def compute(self):
            self.moves = [(self.rot(x,y, self.direction),self.rot(xi,y, self.direction)) for y,x,xi in self.movements]
        
        def rot(self, x,y, times):
            return self.rot(y,4-x-1,times-1) if times else (x,y)
        
    def __init__(self, x,y, clone = False):
        if clone:self.area = numpy.copy(clone.area)
        else:self.area = numpy.zeros((x,y),numpy.int32)
        self.x = x
        self.y = y
        self.posses = tuple(product(range(x), range(y)))
        
        #new tiles
        self.fresh = set()
        self.fill_random()
        self.fill_random()
        self.last = numpy.copy(self.area)
        self.change = self.StateChange(0)
        self.change.compute()
        self.cur_y = -1
        
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
                    self.change.movements.append((self.cur_y, x, x+1))
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
                self.change.movements.append((self.cur_y, x, xi))
                if self.real:self.addscore(val*2)#else not real
                blocked.add(xi)#prevent multiple merges per movement
                movement = True
                break
            elif slice[xi]:#different number
                break
        return movement
    
    def move(self, direction = 0):
        """Moves the entire Grid in direction"""
        self.change = self.StateChange(direction)
        used = set()
        if direction:self.area = numpy.rot90(self.area, direction)
        moves = False
        for y in range(self.y):
            self.cur_y = y
            if self.move_slice(self.area[:, y]): moves = True            
        if direction:self.area = numpy.rot90(self.area, 4-direction)
        self.change.compute()
        return moves
    
    real = property(lambda self:hasattr(self, "game"), doc = "Tells if real or clone")

    def check_merge(self):
        grid_twit = Grid(self.x, self.y, clone = self)#was : copy.deepcopy(self)
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
