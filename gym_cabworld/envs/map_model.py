import pygame
import math

class Map: 
    def __init__(self, map_file):
        self.map_img = pygame.image.load(map_file)
        self.street_color = (175,171,171,255) #(red, green, blue, alpha)

    def calc_distance(self, pos1, pos2): 
        return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)