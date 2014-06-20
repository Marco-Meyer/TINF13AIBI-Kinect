import numpy as np
import freenect
import pygame
import time
import centroid_manager
import delta_manager


pygame.init()

"""
Settings
"""
delta           = 10            #Delta movement (in px)
delta_interval  = 2.0           #Movement check interval (in s)
kinect_interval = 0.2           #Kinect refresh interval (in s)
kinect_crop     = 20            #cropped border size

"""
Kinect Methods
"""
def getDepthImage()
    depth, timestamp = freenect.sync_get_depth()

    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)

    return depth


def main(eventManager)
    centroidManager = CentroidManager(kinect_crop)
    deltaManager = DeltaManager(delta)
    
    #sums the passed time to decide if centroids
    #should be checked for a movement
    time_passed = 0.0
    
    while 1:
        time.sleep(kinect_interval)
        time_passed += kinect_interval
        centroid = centroidManager.getCentroid(getDepthImage())
        deltaManager.add_Centroid(centroid)
        
        if time_passed >= delta_interval:
            #push event
            eventManager.push(deltaManager.get_Move_Events())
            time_passed = 0.0

        
