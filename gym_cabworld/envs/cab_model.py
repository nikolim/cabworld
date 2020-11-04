import pygame
import math

class Cab:
    def __init__(self, cab_file, map, pos):
        self.map = map 
        self.img_size = 50 
        self.cab_img = pygame.image.load(cab_file)
        self.cab_img = pygame.transform.scale(self.cab_img, (self.img_size, self.img_size))
        self.rotate_cab_img = self.cab_img
        self.pos = pos
        self.center = [int(self.pos[0] + (self.img_size/2)), int(self.pos[1] + (self.img_size/2))]
        self.angle = 0
        self.speed = 0
        self.radars = [0,0,0] # 0: forward-move 1: left-turn 2: right-turn 
        self.is_alive = True
        self.goal = False
        self.distance = 0
        self.time_spent = 0
        self.passenger = None
        self.debug = False

    def check_radar(self, screen):

        self.radars = [0,0,0]
        # how far the sensors of the cab / driver can see
        sensor_field = 35
        
        front_x = self.center[0] + math.cos(math.radians(360 - self.angle)) * sensor_field
        front_y = self.center[1] + math.sin(math.radians(360 - self.angle)) * sensor_field

        if self.check_if_street(front_x, front_y):
            self.radars[0] = 1

        left_x = self.center[0] + math.cos(math.radians(360 - self.angle - 90)) * sensor_field
        left_y = self.center[1] + math.sin(math.radians(360 - self.angle - 90)) * sensor_field
        if self.check_if_street(left_x, left_y):
            self.radars[1] = 1

        right_x = self.center[0] + math.cos(math.radians(360 - self.angle + 90)) * sensor_field
        right_y = self.center[1] + math.sin(math.radians(360 - self.angle + 90)) * sensor_field
        if self.check_if_street(right_x, right_y):
            self.radars[2] = 1
        
        # Draw sensors
        if self.debug:
            pygame.draw.line(screen, (255,255,255), (self.center[0], self.center[1]), (front_x, front_y), 5)
            pygame.draw.line(screen, (255,255,255), (self.center[0], self.center[1]), (left_x, left_y), 5)
            pygame.draw.line(screen, (255,255,255), (self.center[0], self.center[1]), (right_x, right_y), 5) 
        
        # if no possible action, drive backwards 
        while all(i == 0 for i in self.radars): 
            self.speed = -5
            self.update()
            self.check_radar(screen)

    def update(self):
        # rotate image
        self.rotate_cab_img = self.rot_center(self.cab_img, self.angle)
        # move cab
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        # keep track of distance and time
        self.distance += self.speed
        self.time_spent += 1
        # center = start cords + img-size 
        self.center = [int(self.pos[0]) + 25, int(self.pos[1]) + 25]

    def pick_up_passenger(self, passenger): 
        self.passenger = passenger
    
    def draw(self, screen):
        screen.blit(self.rotate_cab_img, self.pos)
        
    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def check_if_street(self, x,y): 
        delta = 10
        color = self.map.map_img.get_at(((int(x), int(y))))
        street_color = self.map.street_color
        red_similar = (street_color[0] - delta) <  color[0] < (street_color[0] + delta)
        green_similar = (street_color[1] - delta) <  color[1] < (street_color[1] + delta)
        blue_similar = (street_color[2] - delta) <  color[2] < (street_color[2] + delta)
        return red_similar and green_similar and blue_similar