from os.path import join
import pygame as P
from threading import Timer
class Sounds():
    def __init__(self):
        self.sounds = {}
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
    
