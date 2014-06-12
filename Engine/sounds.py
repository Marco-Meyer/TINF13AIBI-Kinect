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
            print("Loaded "+base, ending)
            self.load_sound(base, ending = "." + ending)
            
    def load_sound(self, file, path ="Sounds", ending =".ogg"):
        self.sounds[file] = P.mixer.Sound(join(path, file+ending))

    def play_slide_sound(self):
        self.play_sound("Slide")
        self.sound_stop("Slide", 0.1)

    def play_lose_sound(self):
        self.play_sound("Lose")
        #self.sound_stop("Lose", 5)
        
        
    def play_sound(self, name):
        self.sounds[name].play()
        print("Play " +name)
        
    def sound_volume(self, name, value):
        self.sounds[name].set_volume(value)

    def timer_stop(self, name, time = 0.1):
        print(self)
        Timer(time, self.sound_stop, (self, name))
        
    def sound_stop(self, name, duration = 0):
        time.sleep(duration)
        self.sounds[name].stop()
        print("stoped " +name)

class NoSounds():
    def __init__(self, *args, **kwargs):
        self.sounds = {}
        for funcname in {"load_sound", "play_sound", "sound_volume",
                         "timer_stop", "sound_stop"}:
            setattr(self, funcname, self.do_nothing)
            
    def do_nothing(*args, **kwargs):pass


##if __name__ == "__main__":
##    P.init()
##    P.display.set_mode([10,10])
##    import sys
##    os.chdir("./../")
##    print(os.getcwd())
##    sounds = Sounds()
##    print(sounds.filenames)
##    sounds.play_sound("Slide")
##   # sounds.timer_stop("Slide", 0.1)
##   # sounds.sound_stop("Slide")

