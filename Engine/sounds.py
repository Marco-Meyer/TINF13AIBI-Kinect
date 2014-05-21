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
            print(base, ending)
            self.load_sound(base, ending = "." + ending)
            self.play_sound(base)
            self.sound_volume(base, 1.0)
            time.sleep(5)
    def load_sound(self, file, path ="Sounds", ending =".ogg"):
        self.sounds[file] = P.mixer.Sound(join(path, file+ending))

    def play_sound(self, name):
        self.sounds[name].play()

    def sound_volume(self, name, value):
        self.sounds[name].set_volume(value)

    def timer_stop(self, name, time = 0.1):
        Timer(time, self.sound_stop, (self, name))

    def sound_stop(self, name):
        self.sounds[name].stop()
    
if __name__ == "__main__":
    P.init()
    import sys
    os.chdir("./../")
    print(os.getcwd())
    sounds = Sounds()
    print(sounds.filenames)
