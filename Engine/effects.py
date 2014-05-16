#! python3.4
import pygame as P
from itertools import product


class HorizontalSlide():
    def __init__(self, size, source, speed):
        self.surface = P.Surface(size)
        self.w,self.h = self.size = size
        self.source = source
        self.sw, self.sh = self.source.get_size()
        self.speed = speed
        self.location = 0
        
    def tick(self, dt = 20):
        self.location += self.speed * dt
        self.location %= self.sw
        loc = int(round(self.location,0))-self.sw
        while loc < self.w:
            self.surface.blit(self.source, (loc,0))
            loc += self.sw

class VerticalSlide(HorizontalSlide):
    def tick(self, dt = 20):
        self.location += self.speed * dt
        self.location %= self.sh
        loc = int(round(self.location,0))-self.sh
        while loc < self.h:
            self.surface.blit(self.source, (0,loc))
            loc += self.sh

class VectorSlide(HorizontalSlide):
    def __init__(self, *args):
        super(VectorSlide, self).__init__(*args)
        self.location = [0,0]
        
    def tick(self, dt = 20):
        self.location = ((self.location[0]+ (self.speed[0] * dt)) % self.sw,
                         (self.location[1]+ (self.speed[1] * dt)) % self.sh)
        
        xloc, yloc = [int(round(x,0)) for x in self.location]
        xloc -= self.sw
        yloc -= self.sh
        for x,y in product(range(xloc, self.w, self.sw), range(yloc, self.h, self.sh)):
            self.surface.blit(self.source, (x,y))

class VerticalDivergence():
    def __init__(self, size, source, speed):
        #size Y has to be even
        self.source = VerticalSlide((size[0], size[1]//2),source, -speed)
        self.surface = P.Surface(size)
        self.w,self.h = self.size = size
        self.center = (0,self.h//2)
        self.flips = (0,1)
        self.clamp = P.Rect(0,0,self.w, self.h//2)
    def tick(self, dt = 20):
        self.source.tick(dt)
        self.surface.blit(self.source.surface, (0,0), self.clamp)
        reverse = P.transform.flip(self.source.surface, *self.flips)
        self.surface.blit(reverse, self.center)

class HorizontalDivergence(VerticalDivergence):
    def __init__(self, size, source, speed):
        #size X has to be even
        self.source = HorizontalSlide((size[0]//2, size[1]),source, -speed)
        self.surface = P.Surface(size)
        self.w,self.h = self.size = size
        self.center = (self.w//2,0)
        self.flips = (1,0)
        self.clamp = P.Rect(0,0,self.w//2, self.h)
        
def repeated_surface(source, size, offset = (0,0)):
    surface = P.Surface(size)
    w,h = size
    xloc, yloc = offset
    sw, sh = source.get_size()
    xloc -= sw
    yloc -= sh
    for x,y in product(range(xloc, w, sw), range(yloc, h, sh)):
        surface.blit(source, (x,y))
    return surface
        
if __name__ == "__main__":
    
    bar = P.image.load("bar.png")
    P.image.save(repeated_surface(bar, (800, 600),(10,10)), "barmul.png")
    clock = P.time.Clock()
    slide = HorizontalSlide((400,100),bar, 0.1)
    P.init()
    D = P.display.set_mode((420,120))
    P.display.set_caption("Close Window to show next")
    running = True
    dt = 0#delta time since last frame in milliseconds
    while running:
        slide.tick(dt)
        for e in P.event.get():
            if e.type == P.QUIT:
                running = False
        D.blit(slide.surface, (10,10))
        P.display.flip()
        dt = clock.tick(200)
    
    surf = P.transform.rotate(bar, 90)
    slide = VerticalSlide((100,400),surf, 0.1)
    D = P.display.set_mode((120,420))
    running = True
    while running:
        slide.tick(dt)
        for e in P.event.get():
            if e.type == P.QUIT:
                running = False
        D.blit(slide.surface, (10,10))
        P.display.flip()
        dt = clock.tick(200)
    
    slide = VectorSlide((400,400),bar, (0.1,0.1))
    D = P.display.set_mode((420,420))
    running = True
    while running:
        slide.tick(dt)
        for e in P.event.get():
            if e.type == P.QUIT:
                running = False
        D.blit(slide.surface, (10,10))
        P.display.flip()
        dt = clock.tick(200)
    slide = VerticalDivergence((400,400),bar, 0.1)
    D = P.display.set_mode((420,420))
    running = True
    while running:
        slide.tick(dt)
        for e in P.event.get():
            if e.type == P.QUIT:
                running = False
        D.blit(slide.surface, (10,10))
        P.display.flip()
        dt = clock.tick(200)
    slide = HorizontalDivergence((400,200),bar, 0.1)
    D = P.display.set_mode((420,220))
    running = True
    while running:
        slide.tick(dt)
        for e in P.event.get():
            if e.type == P.QUIT:
                running = False
        D.blit(slide.surface, (10,10))
        P.display.flip()
        dt = clock.tick(200)
    P.quit()
