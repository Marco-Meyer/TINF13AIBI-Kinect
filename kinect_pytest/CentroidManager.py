import numpy as np
import freenect
import pygame as pygame
import time

pygame.init()

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
	
class MaskCentroidManager():
        def __init__(self, crop):
                self.croprect = pygame.Rect(480-crop*2, 640-crop*2, crop, crop)
		self.lastimage = pygame.Surface((1,1))


                
        def getCentroid(self, image):
                mask = pygame.mask.from_threshold(self._get_surf(image), (127,127,127),(75,75,75,255))
                return mask.centroid()
        
	def _get_surf(self, depthImage):
		sface = pygame.Surface((480, 640))
		arr = pygame.surfarray.pixels_green(sface)
		arr[:] = depthImage[:]
		arr = pygame.surfarray.pixels_red(sface)
		arr[:] = depthImage[:]
		arr = pygame.surfarray.pixels_blue(sface)
		arr[:] = depthImage[:]
		del(arr)
		sface = pygame.transform.chop(sface, self.croprect)
		image =  pygame.transform.rotate(sface,-90)
		self.lastimage = image
		return image
                
def getDepthMap():    
    depth, timestamp = freenect.sync_get_depth()
 
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
 
    return depth

if(__name__ == "__main__"):
	initMap = getDepthMap()
	centroidManager = MaskCentroidManager(20)

	while 1:
		time.sleep(0.1)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				break

		display = pygame.display.set_mode((640,480))

		draw = centroidManager.lastimage	
		pygame.draw.circle(draw, pygame.Color(255,0,0,255), centroidManager.getCentroid(getDepthMap()), 10)
		display.blit(draw, (0,0))
		
		#display.blit(centroidManager._getPyGameSurface(getDepthMap()), (320,0))
		
		#display.blit(centroidManager._getPyGameSurface(initMap), (0,240))

		pygame.display.update()
		print("Rendering")



