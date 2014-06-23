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
delta_length    = 70
delta_interval  = 0.5           #Movement check interval (in s)
kinect_interval = 0.1           #Kinect refresh interval (in s)
kinect_crop     = 30            #Cropped border size (in px)
sleep_after_mv  = 1.5           #Time to sleep after Movement (in s)

def get_direction(angle, tolerance):
    if angle % 90 < 10 or angle%90 > 80:
        dire = (angle%360+45)//90
        if dire == 4:dire = 0
        return int(dire)
    else:return -1

def updateSurface(centroidManager):
        display = pygame.display.set_mode((640,480))

        draw = centroidManager.lastimage	
        pygame.draw.circle(draw, pygame.Color(255,0,0,255), centroidManager.getCentroid(getDepthMap()), 10)
        display.blit(draw, (0,0))

        pygame.display.update()

def main(eventManager, main_thread):
    def post(event):
        if main_thread and main_thread.is_alive():
            pygame.event.post(event)
            
    centroids = []
    centroidManager = MaskCentroidManager(kinect_crop, getDepthMap())
    
    #sums the passed time to decide if centroids
    #should be checked for a movement
    time_passed = 0.0
    lastmv = -1
    no_movement_count = 0
    not_in_field = False
    print("Starting kinect loop")
    while main_thread is None or main_thread.is_alive():

	time.sleep(kinect_interval)
        time_passed += kinect_interval
        x,y = centroid = vec2d(centroidManager.getCentroid(getDepthMap()))

        if x == 0 or y == 0:
            u = pygame.event.Event(pygame.USEREVENT, action = None)
            not_in_field = True
            post(u)
            continue
        
        centroids.append(centroid)        
        if main_thread is None:
            updateSurface(centroidManager)
                
        if time_passed >= delta_interval:
            
            for x in centroids[1:]:
                
                delta = x - centroids[0]
                delta.y *= 2
                s = "Delta:"+str(delta)+str(x)+ "->" + str(centroids[0])
                #print(s)
                if delta.length > delta_length: #and count_sleep <= 0:
                    direction = get_direction(delta.angle, 15)
                    if direction != -1:
                        if direction == 1 and no_movement_count < 2 or\
                           direction == 3 and no_movement_count < 3 or\
                           (direction == 0 or direction == 2) and no_movement_count < 3 or\
                           not_in_field and no_movement_count < 10:
                            print("movement cancelled " + ["Left","Down","Right", "Up"][direction])
                            not_in_field = False
                            break

                        print(["Left","Down","Right", "Up"][direction], str(centroids[0]) + "->" + str(x))
                        dic = { 2 : pygame.K_RIGHT, 0 : pygame.K_LEFT, 3 : pygame.K_UP, 1 : pygame.K_DOWN }
                        e = pygame.event.Event(pygame.KEYDOWN, key = dic[direction])
                        post(e)
                        no_movement_count = 0
                        break
                    
                    #else:
                        #direction = get_direction(delta.angle, 45)
                        #print("Movement unclear, could be", ["Right","Up","Left", "Down"][direction])

            centroids = [centroids[-1]]
            
            time_passed = 0.0
            no_movement_count += 1
            print(no_movement_count)
            #print(["Right","Up","Left", "Down"][movement])
            
if __name__ == "__main__":
    pygame.init()
    main(None, None)
    

        
