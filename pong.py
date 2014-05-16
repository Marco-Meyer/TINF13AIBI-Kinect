#! python3.4
names = set(dir())
##################VARIABLES####################
MAXBALLS = 3
BALLSPAWNRATE = 500
PLAYERS = 1
RESOLUTION = 1200,700 #1200 700
SQUARESIZERANGE = 10,150
INVISCENTER = 100
AIPLAYERS = 1
POSTPROCESS = False
GRID = True
###############################################
newnames = set(dir())
variables = newnames-names-{"names"}
import sys
sys.path.append("Engine")
for overwrite in sys.argv[1:]:
    try:
        name, value = overwrite.split(":")
        if name in variables:
            globals()[name] = eval(value)
        else: raise KeyError("%s not a valid variable" % name)
    except:
        import traceback
        traceback.print_exc()

import pygame
from pygame import gfxdraw
from random import randint
import effects

if POSTPROCESS:
    try:
        import projection
    except:
        POSTPROCESS = False
        print("Problem with OpenGL Init, skipping.")
    #projection.init(RESOLUTION)
else:
    projection = False

pygame.init()
#Controls
controlmapping = [[pygame.K_w, pygame.K_s],
                  [pygame.K_UP, pygame.K_DOWN],
                  [pygame.K_t, pygame.K_g],
                  [pygame.K_o, pygame.K_l]
                  ]
colormapping = [(255,50,50),
                (50,255,50),
                (50,50,255),
                (255,255,50),
                (50,255,255),
                (255,50,255),
                ]
resw, resh = RESOLUTION

padwidth = 21
padheight = 120
playerlocations = []
for i in range(PLAYERS+AIPLAYERS):
    if i % 2:
        playerlocations.append(-1-(i//2))
    else:
        playerlocations.append(1+i//2)

pause = True if PLAYERS else False

clock = pygame.time.Clock()

score = [0,0]
boardcolors = ((0,0,0),(255,255,255)) if INVISCENTER else ((255,255,255),(0,0,0))
fon = pygame.font.Font(None, 40)


#animations= []
base = pygame.image.load("paddle.png")
#for i in range(PLAYERS+AIPLAYERS):
    
padanim= effects.VerticalDivergence((padwidth, padheight),
                                        base, 0.02)
def setup_sizes():
    global invisrect, area, surf, cenw, cenh
    cenw, cenh = resw//2, resh//2 
    
    if projection:
        projection.init(RESOLUTION)
        surf = pygame.Surface(RESOLUTION)
    else:
        surf = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)
    if INVISCENTER:
        invisrect = pygame.Rect(cenw-INVISCENTER//2, 0, INVISCENTER, resh)
    area = pygame.Rect(0,0,resw,resh)
    for p in paddles:
        if p.placement < 0:
            p.rect.x = 20+resw-(-p.placement)*20-padwidth
    for b in balls:
        b.rect.clamp_ip(area)


def randcolor():
    return (randint(50, 255), randint(50,255), randint(50, 255))
def update_caption():
    s = "Pong (Paused | Press Space to play)" if pause else "Pong"
    pygame.display.set_caption(s)

class AI():
    def __init__(self, paddle):
        self.paddle = paddle
        self.placement = paddle.placement
    def __call__(self):
        if self.placement < 0:
            data = list(filter(lambda ball:ball.m_x > 0, balls))
        else:
            data = list(filter(lambda ball:ball.m_x < 0, balls))
        #data = [(ball.rect.x, ball) for ball in data]
        if data:
            data.sort(key = lambda ball:ball.rect.x)
            closest = data[0] if self.placement > 0 else data[-1]
            delta =  closest.rect.centery - self.paddle.rect.centery
            if delta > 0:self.paddle.rect.y += min(speed, delta)
            else:self.paddle.rect.y -= min(speed, -delta)
        
class Paddle():
    def __init__(self, placement, control, color):
        self.color = color
        self.placement = placement
        if control == "AI":
            self.ai = AI(self)
        else:
            self.ai = None
            self.upk, self.downk = control
        if placement > 0:
            x = 21*placement-21
        else:
            x = 21+resw-(-placement)*21-padwidth
        self.rect = pygame.Rect(x, 300, padwidth, padheight)
        self.colored = pygame.Surface(self.rect.size)
        self.colored.fill(self.color)
    def render(self):
        surf.blit(padanim.surface, self.rect)
        #multiply color onto animation pixel by pixel:
        surf.blit(self.colored, self.rect, None, pygame.BLEND_MULT)

        
    def update(self, keys):
        if self.ai:self.ai()
        elif keys[self.upk]:
            self.rect.y -= speed
        elif keys[self.downk]:
            self.rect.y += speed
        self.rect.clamp_ip(area)
        
def apply_grid(surface, val = 50, step = 5):
    arr = pygame.PixelArray(surface)
    arr[::step] = (val,val,val)
    arr[:,::step] = (val,val,val)

class Ball():
    def __init__(self, x,y, dire = 0):
        s = randint(*SQUARESIZERANGE)
        self.bounced = 0
        self.rect = pygame.Rect(x,y,s,s)
        self.m_x = 2 if dire else -3
        self.m_y = randint(1,5) if randint(0,1) else randint(-5, -1)
        self.col = pygame.Color(*randcolor())
        
    def update(self):
        r = self.rect
        r.move_ip(self.m_x, self.m_y)
        if r.y < 0:
            self.m_y = abs(self.m_y)
        elif r.bottom > resh:
            self.m_y = - abs(self.m_y)

        hit = False
        for p in paddles:
            if r.colliderect(p):
                x = self.rect.x
                self.bounced += 1
                if cenw-x < 0:#rightside
                    self.m_x = randint(-2, -1)-self.bounced
                else:
                    self.m_x = randint(1, 2)+self.bounced
                self.m_y = -(p.rect.centery - self.rect.centery)//15
                hit = True
        if not hit:
            if r.right > resw:
                self.m_x = randint(-5, -1)
                self.col = pygame.Color(*randcolor())
                score[0] += 1
                self.bounced = 0
                r.x = resw-5-self.rect.width
            elif r.x < 0:
                self.m_x = randint(1, 5)
                self.col = pygame.Color(*randcolor())
                score[1] += 1
                self.bounced = 0
                r.x = 5

    def render(self):
        pygame.draw.rect(surf, self.col, self.rect)
        
paddles = []
balls = []
setup_sizes()
balls = [Ball(cenw, cenh)]
update_caption()
for i in range(PLAYERS):
    paddles.append(Paddle(playerlocations[i], controlmapping[i], colormapping[i]))
for i in range(PLAYERS, AIPLAYERS+PLAYERS):
    paddles.append(Paddle(playerlocations[i], "AI", colormapping[i]))
speed = 15
spawn = len(balls)*BALLSPAWNRATE
unstable = False
import time
from math import sin
while 1:
    if unstable:
        resw, resh = RESOLUTION = unstable
        setup_sizes()
        unstable = False
    #####EVENTBLOCK#####
    for e in pygame.event.get():
        
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.VIDEORESIZE:
            unstable = e.size
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_SPACE:
                pause = not pause
                update_caption()

        elif e.type == pygame.KEYDOWN:
            if projection:projection.handle_event(e)

    #####LOGICBLOCK#####
    keys = pygame.key.get_pressed()
    if not pause:
        spawn -= 1
        if spawn <= 0 and len(balls) < MAXBALLS:
            balls.append(Ball(cenw,cenh))
            spawn = len(balls)*BALLSPAWNRATE
        [p.update(keys) for p in paddles]
        [b.update() for b in balls]
    
    #####RENDERBLOCK#####
    padanim.tick()
    surf.fill((0,0,0))
    if GRID:apply_grid(surf, (sin(time.clock())+2)*25)

    [b.render() for b in balls]
    [p.render() for p in paddles]
    
    if INVISCENTER:
        pygame.gfxdraw.box(surf, invisrect, (255,255,255))
    board = fon.render("%d : %d" % tuple(score), 0, *boardcolors)
    surf.blit(board, (cenw-board.get_width()//2,80))
    if projection:
        projection.render(surf)
    pygame.display.flip()
    clock.tick(60)

