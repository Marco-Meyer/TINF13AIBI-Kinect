import numpy as np
import freenect
import pygame as pygame
import time

class CentroidManager:

	def __init__(self, initialImage, size):
		self._size = size
		self._initialImage = initialImage

	def getCentroid(self, currentImage):
		return self._getCentroid(self._getDeltaImage(currentImage))

	def _getCentroid(self, surface):
		pMask = pygame.mask.from_threshold(surface, (255,255,255,255), (255,255,255,255))
		return pMask.centroid()
        
	def _getDeltaImage(self, currentImage):
		return self._getPyGameSurface(self._initialImage - currentImage)

	def _getPyGameSurface(self, depthImage):
		sface = pygame.Surface(self._size)
		arr = pygame.surfarray.pixels_green(sface)
		arr[:] = depthImage[:]
		arr = pygame.surfarray.pixels_red(sface)
		arr[:] = depthImage[:]
		arr = pygame.surfarray.pixels_blue(sface)
		arr[:] = depthImage[:]
		del(arr)
		
		pxArray = pygame.PixelArray(sface)
		pxArray.replace(pygame.Color(255,255,255,255), pygame.Color(0,0,0,255), 0.2)
		pxArray.replace(pygame.Color(255,255,255,255), pygame.Color(255,255,255,255), 0.9)
		del(pxArray)

		return pygame.transform.rotate(sface,-90)   

def getDepthMap():    
    depth, timestamp = freenect.sync_get_depth()
 
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
 
    return depth

if(__name__ == "__main__"):
	initMap = getDepthMap()
	centroidManager = CentroidManager(initMap, (480, 640))

	while 1:
		time.sleep(0.1)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				break

		display = pygame.display.set_mode((640,480))

		draw = centroidManager._getDeltaImage(getDepthMap())
		pygame.draw.circle(draw, pygame.Color(255,0,0,255), centroidManager.getCentroid(getDepthMap()), 10)
		display.blit(draw, (0,0))
		
		#display.blit(centroidManager._getPyGameSurface(getDepthMap()), (320,0))
		
		#display.blit(centroidManager._getPyGameSurface(initMap), (0,240))

		pygame.display.update()
		print("Rendering")



