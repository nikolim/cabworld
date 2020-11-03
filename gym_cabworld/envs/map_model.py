import pygame

class Map: 
    def __init__(self, map_file):
        self.map_img = pygame.image.load(map_file)
        self.street_color = (175,171,171,255) #(red, green, blue, alpha)