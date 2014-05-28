import freenect
import cv2
import numpy as np
import pygame
pygame.init()
 
"""
Grabs a depth map from the Kinect sensor and creates an image from it.
"""
def getDepthMap():    
    depth, timestamp = freenect.sync_get_depth()
 
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
 
    return depth

size = 480,640
def get_depth_surface():
    depth = getDepthMap()
    sface =pygame.Surface(size)
    arr = pygame.surfarray.pixels_green(sface)
    arr[:] = depth[:]
    arr = pygame.surfarray.pixels_red(sface)
    arr[:] = depth[:]
    arr = pygame.surfarray.pixels_blue(sface)
    arr[:] = depth[:]
    del(arr)
    return pygame.transform.rotate(sface,-90)   
print("Startup complete")
import time
while 1:
    time.sleep(0.1)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            break
    surf = pygame.display.set_mode((640,480))

    surf.blit(get_depth_surface(),(0,0))
    pygame.display.update()
    print("Rendering")

