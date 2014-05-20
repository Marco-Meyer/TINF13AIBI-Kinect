from os.path import join
import pygame as P

class Sounds():
    def __init__(self):
        self.sounds = {}
    def load_sound(self, file, path ="Sounds", ending =".ogg"):
        self.sounds[file] = P.mixer.Sound(join(path, file+ending))

    def play_sound(self, name):
        self.sounds[name].play()

    def sound_volume(self, name, value):
        self.sounds[name].set_volume(value)

    def sound_stop(self, name):
        self.sounds[name].stop()
    
