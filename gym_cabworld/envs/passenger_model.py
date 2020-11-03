import pygame
import math

class Passenger:
    def __init__(self, passenger_file, map, pos, angle):
        """
        """
        self.pos = pos
        self.angle = angle
        self.map = map 
        self.img_size = 30 
        self.passenger_img = pygame.image.load(passenger_file)
        self.passenger_img = pygame.transform.scale(self.passenger_img, (self.img_size, self.img_size))
        self.passenger_img_rot = self.rot_center(self.passenger_img, self.angle)
        self.center = [int(self.pos[0] + (self.img_size/2)), int(self.pos[1] + (self.img_size/2))]
        self.goal = [0,0]
        self.time_waiting = 0

    def draw(self, screen):
        screen.blit(self.passenger_img_rot, self.pos)

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image