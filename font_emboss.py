import pygame as P
def surround(text, color = P.Color(200,200,200,200)):
    T = P.Surface((text.get_width()+2, text.get_height()+2), P.SRCALPHA)
    T.blit(text, (2,2))
    actuals = set()
    for x in range(T.get_width()):
        for y in range(T.get_height()):
            if T.get_at((x,y))[3]>127:
                actuals.add((x,y))
    for tup in actuals:
        for dtup in shift(*tup):
            if dtup not in actuals:
                T.set_at(dtup, color)
    return T

def shift(x,y):
    yield x+1, y
    yield x, y+1
    yield x-1, y
    yield x, y-1
