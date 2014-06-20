import numpy as np
import freenect
import pygame
import time
from centroid_manager import MaskCentroidManager, getDepthMap
from delta_manager import DeltaManager
from vec2d import vec2d
"""
Settings
"""
delta_x         = 30            #Delta movement (in px)
delta_y         = 10            #Delta movement (in px)
delta_interval  = 0.5           #Movement check interval (in s)
kinect_interval = 0.1           #Kinect refresh interval (in s)
kinect_crop     = 20            #cropped border size (in px)

def main(eventManager, main_thread):
    centroidManager = MaskCentroidManager(kinect_crop)
    deltaManager = DeltaManager(delta_x, delta_y)
    
    #sums the passed time to decide if centroids
    #should be checked for a movement
    time_passed = 0.0
    
    while main_thread.is_alive():

	time.sleep(kinect_interval)
        time_passed += kinect_interval
        centroid = centroidManager.getCentroid(getDepthMap())
        deltaManager.add_Centroid(vec2d(centroid))
        
        if time_passed >= delta_interval:
            #push event
            #eventManager.dispatch(*deltaManager.get_Move_Events())
            
            movement = deltaManager.get_Move_Events()
            time_passed = 0.0
            if movement != -1:
                dic = { 0 : pygame.K_RIGHT, 2 : pygame.K_LEFT, 1 : pygame.K_UP, 3 : pygame.K_DOWN }
                e = pygame.event.Event(pygame.KEYDOWN, key = dic[movement])
                pygame.event.post(e)
                print(["Right","Up","Left", "Down"][movement])
                

        
