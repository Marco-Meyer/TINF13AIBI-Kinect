#! python3.4
import pygame as P
from random import randint



if __name__ == "__main__":
    import sys
    sys.path.append("..")
from Circuit import paths
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
                insurface.set_at((x,y),[x+randint(-deviation, deviation) for x in innercolor[:3]])
        innerlength = innerrect.width
        ele = (connector.spacing+connector.width)
        
        slots = innerlength//ele-2
        filled = slots*ele-connector.spacing
        rest = innerlength - filled
        if rest%2:
            print("Warning|electronics.py:could not center chip connectors, change chip size.")
            
        con1,con2,con3,con4 = connector.surfaces
        posses = tuple(range(connector.indent+rest//2, connector.indent+innerlength-rest//2, ele))
        y = length-connector.length
        for x in posses:
            mx = x
            
            self.surface.blit(con2,(mx,0))#top
            self.surface.blit(con4,(mx,y))#bottom
            
            self.surface.blit(con3, (0, mx))#left
            self.surface.blit(con1, (y, mx))#right
            
        self.interfaces = posses#attachement nodes for circuit
    
        
class Grid():
    def __init__(self, size, chip, connector, positions, tilemap):
        self.size = size
        self.chip = chip
        self.length = connector.width+connector.spacing
        self.surface = P.Surface(size)
        self.surface.fill(tilemap.basecolor)
        xshift = self.chip.surface.get_width()//2
        self.chipposs = []
        levels = set()
        rows = set()
        barrows = []
        barlines = []
        for x,y in positions:
            x,y = pos = (x-xshift, y-xshift)
            self.chipposs.append(pos)
            if y not in levels:
                levels.add(y)
                barlines += (y+interface for interface in chip.interfaces)
            if x not in rows:
                rows.add(x)
                barrows += (x+interface for interface in chip.interfaces)
        bar = repeat(tilemap["h"], (size[0], 5))
        for y in barlines:
            self.surface.blit(bar, (0, y-1))
        bar = repeat(tilemap["v"], (5, size[1]))
        for x in barlines:
            self.surface.blit(bar, (x-1, 0))
        [self.surface.blit(chip.surface, pos) for pos in self.chipposs]
        
    
class TileMap():
    def __init__(self, outercolor = (0,150,0), innercolor = (250,250,250)):
        
        middlecolor = P.Color(*[(x+y)//2 for x,y in zip(innercolor, outercolor)])
        outercolor = P.Color(*outercolor)
        innercolor = P.Color(*innercolor)
        self.basecolor = outercolor
        size = 5,5
        l = 5
        self.tiles = {}
        #shortcuts
        m = middlecolor
        o = outercolor
        i = innercolor


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
            P.image.save(surface, name+".png")
    
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
    tilemap = TileMap()
    tilemap.save_images()
    grid = Grid(size, chip, connectors, positions, tilemap)
    P.image.save(grid.surface, "test.png")
