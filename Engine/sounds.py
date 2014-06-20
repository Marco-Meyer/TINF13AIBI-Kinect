from os.path import join
import pygame as P
from threading import Timer
import os
import time

class Sounds():
    def __init__(self):
        self.sounds = {}
        self.filenames = os.listdir("Sounds")
        for filename in self.filenames:
            base, ending = filename.split(".")           
            if base == 'Background':
                P.mixer.music.load(join("Sounds", base + "." + ending))
                print("Loaded "+base, ending + "\n")
            else:               
                self.load_sound(base, ending = "." + ending)
                print("Loaded "+base, ending)
                P.mixer.set_num_channels(100) 
            
    def load_sound(self, file, path ="Sounds", ending =".ogg"):
        self.sounds[file] = P.mixer.Sound(join(path, file+ending))

    def play_backgroundmusic(self):
        P.mixer.music.play(-1)
        P.mixer.music.set_volume(0.5)
        print("Play Background")
        
    def play_slide_sound(self):
        self.play_sound("Slide", 0, 175)
        
    def play_lose_sound(self):
        self.play_sound("Lose", 0)        
        
    def play_sound(self, name, loop = 0, duration = 100000): #loop=0 == play 1 time duration in ms
        self.sounds[name].play(loop, duration)
        #print(self.sounds[name].play(0, duration)) # print the channel
        print("Play " +name)
        
    def sound_volume(self, name, value):
        self.sounds[name].set_volume(value)


class NoSounds():
    def __init__(self, *args, **kwargs):
        self.sounds = {}
        for funcname in {"load_sound", "play_sound", "sound_volume",
                         "timer_stop", "sound_stop"}:
            setattr(self, funcname, self.do_nothing)
            
    def do_nothing(*args, **kwargs):pass


##    def timer_stop(self, name, time = 0.1):
##        print(self)
##        Timer(time, self.sound_stop, (self, name))
##        
##    def sound_stop(self, name, duration = 0):
##        time.sleep(duration)
##        self.sounds[name].stop()
##        print("stoped " +name)



##if __name__ == "__main__":
##    P.init()
##    i = 0
##    P.display.set_mode([10,10])
##    import sys
##    os.chdir("./../")
##    print(os.getcwd())
##    sounds = Sounds()
##    print(sounds.filenames)
##   # sounds.timer_stop("Slide", 0.1)
##   # sounds.sound_stop("Slide")
##
