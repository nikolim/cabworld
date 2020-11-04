import pygame
import math

class Map: 
    def __init__(self, map_file):
        """
        Map for the cabworld definded by image
        @param map_file: map to create world
        """
        self.map_img = pygame.image.load(map_file)
        self.street_color = (175,171,171,255) #define color of street

    def calc_distance(self, pos1, pos2): 
        """
        Calculate distance between two objects
        @param pos1: position of 1.object
        @param pos2: position of 2.object 
        @return distance in pixels
        """
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)