import pygame as P
class LCD():
    matrix = {"0" : {0,1,2,3,4,6},
              "1" : {3,4},
              "2" : {0,2,3,5,6},
              "3" : {0,5,6,3,4},
              "4" : {1,3,4,5},
              "5" : {0,1,4,5,6},
              "6" : {0,1,2,4,5,6},
              "7" : {0,3,4},
              "8" : {0,1,2,3,4,5,6},
              "9" : {0,1,3,4,5,6},
              }
    def __init__(self, color : P.Color = (255,50,50), offcolor : P.Color = (50, 0, 0)):
        self.color = color
        element = P.image.load("Circuit/element.png")
        offelement = element.copy()
        self.size = element.get_size()
        blitter = P.Surface(self.size)
        blitter.fill(color)
        element.blit(blitter, (0,0), special_flags = P.BLEND_MULT)
        relement = P.transform.rotate(element, 90)
        blitter.fill(offcolor)
        offelement.blit(blitter, (0,0), special_flags = P.BLEND_MULT)
        roffelement = P.transform.rotate(offelement, 90)
        self.pick = {(0,0) : offelement,
                     (1,0) : element,
                     (0,1) : roffelement,
                     (1,1) : relement}
        dif = 10
        w,h = self.size
        self.signsize = h+2*dif, 2*dif+2*h+w
        #ID : (X, Y, Rotation)
        self.positions = {0 : (dif, 0, 1),#top bar
                          1 : (0, dif, 0),#topside left bar
                          2 : (0, 2*dif+h, 0),#bottomside left bar
                          3 : (dif+h,dif,0),#topside right bar
                          4 : (dif+h,2*dif+h,0),#bottomside right bar
                          5 : (dif, dif+h, 1),#middle bar
                          6 : (dif, 2*(dif+h), 1)#bottom bar
                          }

    def estimate(self, letter_amount, x_spacing = 10):
        """Get (width, height) of rendering letters"""
        return ((self.signsize[0]+x_spacing)*letter_amount-x_spacing+1,self.signsize[1])
    
    def render(self, number, slots, x_spacing = 10, backgroundcolor = P.Color(0,0,0,0)):
        number = str(number)
        dif = slots-len(number)
        if dif > 0:number = "0"*dif+number
        T = P.Surface(((self.signsize[0]+x_spacing)*len(number)-x_spacing+1,self.signsize[1]), flags = P.SRCALPHA)
        T.fill(backgroundcolor)
        xbase = 0
        for char in number:
            for i in range(7):
                x,y,rot = self.positions[i]
                surface = self.pick[(i in self.matrix[char],rot)]
                T.blit(surface, (xbase+x,y))
            xbase += self.signsize[0]+x_spacing
        return T

if __name__ == "__main__":
    lcd = LCD()
    P.image.save(lcd.render(123456789, 15, backgroundcolor = P.Color(0,0,0)), "lcd.png")
