import pygame as P
from random import randint

class Chip():
    def __init__(self, length, connector, innercolor = P.Color(50,50,50), deviation = 3, bordercolor = P.Color(150,150,150)):
        size = length,length
        
        self.rect = P.Rect((0,0), size)
        self.innerrect = self.rect.inflate(-connector.indent*2,-connector.indent*2)
        self.surface = P.Surface(size, flags = P.SRCALPHA)
        self.surface.fill((0,0,0,0))
        
        self.insurface = self.surface.subsurface(self.innerrect)#P.Surface(self.innerrect.size)
        for x in range(self.insurface.get_width()):
            for y in range(self.insurface.get_height()):
                self.insurface.set_at((x,y),[x+randint(-deviation, deviation) for x in innercolor[:3]])
        innerlength = self.innerrect.width
        ele = (connector.spacing+connector.width)
        
        slots = innerlength//ele-2
        filled = slots*ele-connector.spacing
        rest = innerlength - filled
        dif = rest//2
        
        if rest%2:
            print("Warning|electronics.py:could not center chip connectors, change chip size.")
            
        con = connector.surfaces[1]
        con2 = connector.surfaces[3]
        posses = tuple(range(dif, innerlength-dif, ele))
        y = length-connector.length
        for x in posses:
            mx = connector.indent+x
            self.surface.blit(con,(mx,0))
            self.surface.blit(con2,(mx,y))
        con = connector.surfaces[0]
        con2 = connector.surfaces[2]
        x = length-connector.length
        for y in posses:
            my = connector.indent+y
            self.surface.blit(con, (0, my))
            self.surface.blit(con2, (x, my))

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
    connectors = Connector(3,10,3)
    chip = Chip(59, connectors)
    P.image.save(chip.surface, "test.png")
    P.image.save(create_conductor(20,4), "conductor.png")
