#! python3.4
from __future__ import division, print_function
import pygame as P

from random import randint, choice
from os.path import join
from functools import reduce




if __name__ == "__main__":
    import sys
    sys.path.append("..")

from vec2d import vec2d
from Engine.effects import repeated_surface as repeat

class Chip():
    def __init__(self, length, connector, innercolor = P.Color(50,50,50), deviation = 3, bordercolor = P.Color(150,150,150)):
        size = length,length
        
        rect = P.Rect((0,0), size)
        innerrect = rect.inflate(-connector.indent*2,-connector.indent*2)
        self.surface = P.Surface(size, flags = P.SRCALPHA)
        self.surface.fill((0,0,0,0))
        
        insurface = self.surface.subsurface(innerrect)#P.Surface(self.innerrect.size)
        for x in range(insurface.get_width()):
            for y in range(insurface.get_height()):
                insurface.set_at((x,y),[z+randint(-deviation, deviation) for z in innercolor[:3]])
        innerlength = innerrect.width
        ele = (connector.spacing+connector.width)
        
        slots = innerlength//ele-2
        filled = slots*ele-connector.spacing
        rest = innerlength - filled
        if rest%2:
            print("Warning|electronics.py:could not center chip connectors, change chip size.")
            
        con1,con2,con3,con4 = connector.surfaces
        posses = tuple(range(connector.indent+rest//2, connector.indent+innerlength-rest//2, ele))
        self.dis = length-connector.length
        for z in posses:
            
            self.surface.blit(con2,(z,0))#top
            self.surface.blit(con4,(z,self.dis))#bottom
            
            self.surface.blit(con3, (0, z))#left
            self.surface.blit(con1, (self.dis, z))#right
            
        self.interfaces = posses#attachement nodes for circuit

    def get_interfaces(self, x,y):
        sides = {}
        sides["left"] = [vec2d(x, y+z) for z in self.interfaces]
        sides["right"] = [vec2d(self.dis+x, y+z) for z in self.interfaces]
        sides["top"] = [vec2d(x+z, y) for z in self.interfaces]
        sides["bottom"] = [vec2d(x+z, y+self.dis) for z in self.interfaces]
        return sides

    
class Fizzle():
    """electric fizzle on the Grid"""
    def __init__(self, surface, connection, speed = 1):
        self.connection = connection
        self.surface = surface
        self.pos = connection.start
        self.direction = self.end-self.start
        self.time = connection.time
        

class AnimFizzle():
    def __init__(self, grid,amount, speed, color = (250,250,100)):
        
        self.grid = grid
        connections = []
        for node in grid.nodes.values():
            connections.extend(node.connections)
        for c in connections:
            c.direction.length = speed
            c.scale_time(speed)            
        fizimage = P.image.load(join("Circuit","blib.png"))
        blitter = P.Surface(fizimage.get_size())
        blitter.fill(color)
        fizimage.blit(blitter, (0,0), special_flags = P.BLEND_MULT)
        self.fizzles = [Fizzle(choice(connections),fizimage) for _ in range(amount)]
        
    def render(self,surface):
        copy = self.grid.surface.copy()
        rects = [f.render(copy) for f in self.fizzles]
        surface.blit(copy, (0,0))
        return rects

Fi = 0
class Fizzle():
    """electric fizzle on the Grid"""
    def __init__(self, connection, surface):
        global Fi
        self.follow(connection)
        self.surface = surface
        self.fi = Fi
        Fi += 1
        
    def follow(self, connection):
        self.connection = connection
        self.direction = connection.direction
        self.pos = vec2d(connection.start)
        self.time = connection.time
        
    def render(self, target):
        self.time -= 1
        if self.time <= 0:
            self.follow(choice(self.connection.node.connections))
        self.pos += self.direction
        target.blit(self.surface, self.pos)

        
class Grid():
    delta = vec2d(-1,-1)

    class Node():
        def __init__(self, position):
            self.position = position
            self.connections = []
        def __repr__(self):
            return "Node(%s,%s)" % self.position

    class Connection():
        def __init__(self, start, end, node):
            self.start = start+Grid.delta
            self.end = end+Grid.delta
            self.direction = end-start
            self.node = node
        def scale_time(self, speed):
            self.time = (self.end-self.start).length/self.direction.length
            
    def __init__(self, size, chip, connector, positions, tilemap):
        self.size = size
        self.chip = chip
        self.length = connector.width+connector.spacing
        self.surface = P.Surface(size)
        self.surface.fill(tilemap.basecolor)
        
        chiplength = self.chip.surface.get_width()
        xshift = chiplength//2
        
        self.chipposs = []
        levels = set()
        rows = set()
        barrows = []
        barlines = []
        self.nodes = {}
        interfaces = {}

        outsidenode = self.Node((None,None))
        
        for x,y in positions:
            x,y = pos = (x-xshift, y-xshift)
            self.chipposs.append(pos)
            self.nodes[(x,y)] = self.Node((x,y))
            interfaces[(x,y)] = chip.get_interfaces(x,y)
            if y not in levels:
                levels.add(y)
                barlines += (y+interface for interface in chip.interfaces)
            if x not in rows:
                rows.add(x)
                barrows += (x+interface for interface in chip.interfaces)
                
        minstraight = 21
        
        #####Diagonals#####
        X = min(rows)
        XR = max(rows)+chiplength
        for y in levels:#left and right endconnectors
            ys = chip.interfaces
            
            if y == min(levels):spec = X-minstraight
            elif y == max(levels):spec = -X+minstraight
            else:spec = 0
            
            for yl in ys:
                yt = yl+y+spec
                tilemap.draw_line(self.surface, (X-minstraight,yl+y+1), (0,yt+1))
                tilemap.draw_line(self.surface, (XR+minstraight,yl+y+1), (size[0],yt+1))

        Y = min(levels)
        for x in rows:
            if x == min(rows):spec = 0#spec = Y-minstraight
            elif x == max(rows):spec = 0#spec = -Y+minstraight
            else:
                if x > size[0]//2:spec = Y-minstraight
                else:spec = -Y+minstraight
                    

            for xl in ys:
                xt = xl+x+spec
                tilemap.draw_line(self.surface, (x+xl+1, Y-minstraight),(xt+1, 0))

        ######Straight Connections######
        xs = min(rows)
        xe = max(rows)+chiplength
        bar = repeat(tilemap["h"], (xe-xs+2*minstraight, 5))
        for y in barlines:
            self.surface.blit(bar, (xs-minstraight, y-1))
        ys = min(levels)
        ye = size[1]#max(levels)+chiplength
        bar = repeat(tilemap["v"], (5, ye-ys+minstraight))
        for x in barlines:
            self.surface.blit(bar, (x-1, ys-minstraight))
        ######Chips######
        [self.surface.blit(chip.surface, pos) for pos in self.chipposs]

        ##################Fizzle Logic######################
        xs = list(rows)
        xs.sort()
        ys = list(levels)
        ys.sort()
        for x in rows:

            cons = [False, False]
            if xs[0] != x:#not left end
                leftx = xs[xs.index(x)-1]
                cons[0] = True
            if xs[-1] != x:#not right end
                rightx = xs[xs.index(x)+1]
                cons[1] = True
            for y in levels:

                localnode = self.nodes[(x,y)]
                if cons[0]:
                    leftnode = self.nodes[(leftx, y)]
                    for left, right in zip(interfaces[(leftx, y)]["right"],
                                           interfaces[(x,y)]["left"]):

                        localnode.connections.append(self.Connection(right, left, leftnode))
                if cons[1]:
                    rightnode = self.nodes[(rightx, y)]
                    for right, left in zip(interfaces[(rightx, y)]["left"],
                                           interfaces[(x,y)]["right"]):
                        localnode.connections.append(self.Connection(left, right, rightnode))
                if ys[-1] != y:
                    downy = ys[ys.index(y)+1]
                    downnode = self.nodes[(x, downy)]
                    for down, up in zip(interfaces[(x,downy)]["top"],
                                        interfaces[(x,y)]["bottom"]):
                        localnode.connections.append(self.Connection(up,down, downnode))
                if ys[0] != y:
                    upy = ys[ys.index(y)-1]
                    upnode = self.nodes[(x, upy)]
                    for up, down in zip(interfaces[(x,upy)]["bottom"],
                                        interfaces[(x,y)]["top"]):

                        localnode.connections.append(self.Connection(down,up, upnode))
                         
class TileMap():
    def __init__(self, outercolor = (10,10,150), innercolor = (250,250,250)):
        

        self.m = m = P.Color(*[(x+y)//2 for x,y in zip(innercolor, outercolor)])
        self.o = o = P.Color(*outercolor)
        self.i = i = P.Color(*innercolor)

        self.basecolor = outercolor
        size = 5,5
        l = 5
        self.tiles = {}

        S = P.Surface(size)
        PA = P.PixelArray(S)
        for x,color in zip(range(5), (o,m,i,m,o)):
            PA[x] = color
        self.tiles["v"] = S#vertical
        
        S = P.Surface(size)
        PA = P.PixelArray(S)
        for x,color in zip(range(5), (o,m,i,m,o)):
            PA[:, x] = color
        self.tiles["h"] = S#horizontal

    def __getitem__(self, key):
        return self.tiles[key]
        
    def save_images(self):
        for name, surface in self.tiles.items():

            P.image.save(surface, "_test_"+name+".png")
            
    def draw_line(self, surface, start, end):

        dif_x = end[0]-start[0]
        dif_y = end[1]-start[1]
        if not abs(dif_x) == abs(dif_y) and dif_y and dif_x:
            raise ValueError("Can only handle 45 Degree Diagonals. Dif: (%s,%s)" % (dif_x, dif_y))
        dir_x = dif_x//abs(dif_x) if dif_x else 0
        dir_y = dif_y//abs(dif_y) if dif_y else 0


        center = set()
        finish = end[0]+dir_x,end[1]+dir_y
        x, y = start
        while (x,y) != finish:
            center.add((x,y))
            x += dir_x
            y += dir_y
        middle = (get_surround(*c) for c in center)
        middle = reduce(set.union, middle)
        middle -= center
        {surface.set_at(c, self.i) for c in center}
        {surface.set_at(m, self.m) for m in middle}
            
def get_surround_full(x,y):
    return {(x+1, y),(x, y+1),(x-1, y),(x, y-1),
            (x+1,y+1),(x-1,y-1),(x+1,y-1),(x-1,y+1)}

def get_surround(x,y):
    return {(x+1, y),(x, y+1),(x-1, y),(x, y-1)}
    
def create_conductor(length, width, light = (200,200,200), dark = (127,127,127)):
    l = length//3
    T = P.Surface((length, width))
    T.fill(dark)
    data = P.PixelArray(T)
    data[l:l+length//10] = light
    return T

def get_rotated_conductors(length, width, light = (200,200,200), dark = (127,127,127)):
    data = [create_conductor(length, width, light, dark)]
    for x in range(3):
        data.append(P.transform.rotate(data[0], 90+x*90))
    return data
        

class Connector():
    """Container Class for Chip Connection Data"""
    def __init__(self, depth, length, width, spacing = 2, light = (200,200,200), dark = (127,127,127)):
        self.depth = depth
        self.spacing = spacing
        self.length = length
        self.width = width
        self.indent = length-depth
        self.surfaces = get_rotated_conductors(length, width, light, dark)

if __name__ == "__main__":
    
    P.init()
    connectors = Connector(3,10,3)
    chip = Chip(78, connectors)
    P.image.save(create_conductor(20,4), "_test_conductor.png")
    size = (480, 480)
    xdelta = size[0]//5
    positions = []
    for x in range(xdelta,size[0],xdelta):
        for y in range(xdelta,size[1],xdelta):
            print(x,y)
            positions.append((x,y))
    tilemap = TileMap()
    tilemap.save_images()
    testsurf = P.Surface((200,200))
    tilemap.draw_line(testsurf, (50,50),(0,100))
    P.image.save(testsurf, "_test_diagonal.png")
    grid = Grid(size, chip, connectors, positions, tilemap)
    P.image.save(grid.surface, "_test.png")
    symcon = Connector(2, 7, 2, 2)
    symbol = Chip(32, symcon)
    P.image.save(symbol.surface, "icon.png")
