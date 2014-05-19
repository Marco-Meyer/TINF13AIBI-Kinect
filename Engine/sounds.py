import pygame as P

class Sounds():
    def __init__(self):
        self.sounds = {}
    def load_sound(file, path ="Sounds", ending =".ogg"):
        self.sounds[file] = P.mixer.Sound(join(path, file+ending))

    def play_sound(name):
        self.sounds[name].play()
