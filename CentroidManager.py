import numpy as np
import pygame as pygame

class CentroidManager:

    def __init__(self, initialImage)
        self._initialImage = initialImage

    def getCentroid(self, currentImage):
        return self._getCentroid(self._getDeltaImage(currentImage))
        
    def _getCentroid(self, surface):
        pMask = pygame.mask.from_surface(surface)
        return pMask
        
    def _getDeltaImage(self, currentImage):
        return self._getPyGameSurface(self._initialImage - currentImage)

    def _getPyGameSurface(self, depthImage):
        sface = pygame.Surface(size)
        arr = pygame.surfarray.pixels_green(sface)
        arr[:] = depthImage[:]
        arr = pygame.surfarray.pixels_red(sface)
        arr[:] = depthImage[:]
        arr = pygame.surfarray.pixels_blue(sface)
        arr[:] = depthImage[:]
        del(arr)
        
        return pygame.transform.rotate(sface,-90)   
    
