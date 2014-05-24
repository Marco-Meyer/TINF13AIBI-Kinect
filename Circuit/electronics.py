#! python3.4
import pygame as P
from random import randint

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
                insurface.set_at((x,y),[x+randint(-deviation, deviation) for x in innercolor[:3]])
        innerlength = innerrect.width
        ele = (connector.spacing+connector.width)
        
        slots = innerlength//ele-2
        filled = slots*ele-connector.spacing
        rest = innerlength - filled
        if rest%2:
            print("Warning|electronics.py:could not center chip connectors, change chip size.")
            
        con1,con2,con3,con4 = connector.surfaces
        posses = tuple(range(rest//2, innerlength-rest//2, ele))
        y = length-connector.length
        for x in posses:
            mx = connector.indent+x
            
            self.surface.blit(con2,(mx,0))#top
            self.surface.blit(con4,(mx,y))#bottom
            
            self.surface.blit(con3, (0, mx))#left
            self.surface.blit(con1, (y, mx))#right
            
        self.interfaces = posses#attachement nodes for circuit
    
        
class Grid():
    def __init__(self, size, chip, connector, positions):
        self.size = size
        self.chip = chip
        self.length = connector.width+connector.spacing
        self.surface = P.Surface(size)
        xshift = self.chip.surface.get_width()//2
        for x,y in positions:
            self.surface.blit(chip.surface, (x-xshift, y-xshift))

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
    #P.image.save(chip.surface, "test.png")
    P.image.save(create_conductor(20,4), "conductor.png")
    size = (480, 480)
    xdelta = size[0]//5
    positions = []
    for x in range(xdelta,size[0],xdelta):
        for y in range(xdelta,size[1],xdelta):
            print(x,y)
            positions.append((x,y))
    grid = Grid(size, chip, connectors, positions)
    P.image.save(grid.surface, "test.png")
