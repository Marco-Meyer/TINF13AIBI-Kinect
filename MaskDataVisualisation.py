import pygame as pygame
import gfxdraw as gfxdraw
import os as os
import sys as sys


pygame.init()


class MaskDataInfo:
    outlines = []
    centroid = []

    def __init__(self, outlines = [], centroids = []):
        self.outlines = outlines
        self.centroids = centroids
        

class MaskDataVisualisation:

    @staticmethod
    def saveMaskInfos(mask, path = None):
        """saves all infos about a mask in path directory"""
        size = mask.get_size()
        raw = MaskDataVisualisation.getSurfaceFromMask(mask)
        connectedObjects = MaskDataVisualisation.getConnectedObjects(mask)
        if path != None:
            if not os.path.exists(path):
                os.makedirs(path)
            pygame.image.save(raw, os.path.join(path, "Mask_SetPixels.png"))
            pygame.image.save(connectedObjects, os.path.join(path, "Mask_ConnectedObjects.png"))
        else:
            pygame.image.save(raw, "Mask_SetPixels.png")
            pygame.image.save(connectedObjects, "Mask_ConnectedObjects.png")
            
        
    @staticmethod
    def displayMask(mask):
        """displays a surface that shows all set pixels of a mask"""
        size = mask.get_size()
        displaySurface = pygame.display.set_mode(size, pygame.RESIZABLE)
        displaySurface.blit(MaskDataVisualisation.getSurfaceFromMask(mask), (0, 0))
        pygame.display.flip()

    @staticmethod
    def displayConnectedObjects(mask):
        """displays a surface that shows all connected objects of a mask"""
        size = mask.get_size()
        displaySurface = pygame.display.set_mode(size, pygame.RESIZABLE)
        displaySurface.blit(MaskDataVisualisation.getConnectedObjects(mask), (0, 0))
        pygame.display.flip()

    @staticmethod
    def displayCollidingPixels(mask1, mask2):
        """displays a surface that shows all colliding objects of a mask"""
        size = mask1.get_size()
        displaySurface = pygame.display.set_mode(size)
        overlaps = pygame.mask.Mask(size)
        overlaps.draw(mask1.overlap_mask(mask2, (0, 0)), (0, 0))
        maskInfos = []
        maskInfos.append(MaskDataVisualisation.getConnectedObjectsInfo(mask1))
        maskInfos.append(MaskDataVisualisation.getConnectedObjectsInfo(mask2))
        for i in range(len(maskInfos)):
            for j in range(len(maskInfos[i].outlines)):
                for k in range(len(maskInfos[i].outlines[j])):
                    displaySurface.set_at(maskInfos[i].outlines[j][k], (255, 0, 0))
            for j in range(len(maskInfos[i].centroids)):
                displaySurface.fill((0, 0, 255), pygame.Rect(maskInfos[i].centroids[j][0]-1, maskInfos[i].centroids[j][1]-1, 3, 3))     
        for y in range(size[1]):
            for x in range(size[0]):
                if(overlaps.get_at((x, y)) > 0 and displaySurface.get_at((x, y)) == (255, 0, 0)):
                    displaySurface.set_at((x, y), (255, 255, 0)) 
                        
        pygame.display.flip()

    @staticmethod
    def getSurfaceFromMask(mask):
        """returns a surface with all set pixels in mask"""
        size = mask.get_size()
        displaySurface = pygame.Surface(size)
        surfarray = pygame.surfarray.pixels_red(displaySurface)
        for y in range(0, size[1]):
            for x in range(0, size[0]):
                if (mask.get_at((x, y)) > 0):
                    surfarray[x][y] = 255
        return displaySurface

    @staticmethod
    def getConnectedObjects(mask):
        """returns surface that shows connected elements"""
        surface = pygame.Surface(mask.get_size())
        objects = mask.connected_components()
        for i in range(len(objects)):
            centroid = objects[i].centroid()
            outline = objects[i].outline()
            for j in range(len(outline)):
                surface.set_at(outline[j], (255, 0, 0))
            surface.fill((0, 0 ,255), pygame.Rect((centroid[0] - 1, centroid[1] - 1), (3, 3)))
        return surface

        
    @staticmethod
    def getConnectedObjectsInfo(mask):
        """returns an object that contains informations about a mask such as outlining points of connected objects and their center"""
        surface = pygame.Surface(mask.get_size())
        objects = mask.connected_components()
        outlines = []
        centroids = []
        for i in range(len(objects)):
            centroids.append(objects[i].centroid())
            outlines.append(objects[i].outline(5))
        return MaskDataInfo(outlines, centroids)

            
            
                
             
if __name__ == "__main__":
    surface1 = pygame.Surface((1200, 900))
    surface1.fill((0, 0, 0))
    surface2 = pygame.Surface((1200, 900))
    surface2.fill((0, 0, 0))
    
    pygame.draw.rect(surface1, (255, 0, 0), pygame.Rect(60, 60, 150, 100))
    pygame.draw.rect(surface2, (255, 0, 0), pygame.Rect(0, 0, 150, 100))
    pygame.draw.ellipse(surface1, (255, 0, 0), pygame.Rect(200, 200, 100, 100))

    mask1 = pygame.mask.from_threshold(surface1, (255, 1, 1), (255, 255, 255))
    mask2 = pygame.mask.from_threshold(surface2, (255, 1, 1), (255, 255, 255))

    #MaskDataVisualisation.displayConnectedObjects(mask1)
    #MaskDataVisualisation.displayCollidingPixels(mask1, mask2)
    #MaskDataVisualisation.displayMask(mask1)
    MaskDataVisualisation.saveMaskInfos(mask1)

    while 1:
        for e in pygame.event.get():
            
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
