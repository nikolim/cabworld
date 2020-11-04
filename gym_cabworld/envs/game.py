import pygame
import math

from gym_cabworld.envs.cab_model import Cab 
from gym_cabworld.envs.map_model import Map
from gym_cabworld.envs.passenger_model import Passenger

screen_width = 1000
screen_height = 1000

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.map = Map('images/map.png')
        self.cab = Cab('images/cab.png', self.map, [65, 40])
        self.passenger = Passenger('images/person_1.png', self.map, [800,800],0,[65,40])
        self.game_speed = 60
        self.mode = 0

    def action(self, action):
        if action == 0:
            self.cab.speed = 25
        if action == 1:
            self.cab.angle += 90
        elif action == 2:
            self.cab.angle -= 90

        self.cab.update()
        self.cab.check_radar(self.screen)
        
    def evaluate(self):
        reward = 0
        if self.cab.goal:
            reward = 10000
        return reward

    def is_done(self):
        if not self.cab.is_alive or self.cab.goal:
            self.cab.current_check = 0
            self.cab.distance = 0
            return True
        return False

    def observe(self):
        r1,r2,r3 = self.cab.radars
        p1, p2 = self.cab.pos
        return tuple([r1,r2,r3,p1,p2])

    def view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.mode += 1
                    self.mode = self.mode % 3

        self.screen.blit(self.map.map_img, (0, 0))
        if self.mode == 1:
            self.screen.fill((0, 0, 0))
        self.cab.check_radar(self.screen)
        self.cab.draw(self.screen)
        self.passenger.draw(self.screen)
        
        if self.cab.passenger is None:
            if self.map.calc_distance(self.cab.pos, self.passenger.pos) < 25: 
                if not self.passenger.reached_destination:
                    self.cab.pick_up_passenger(self.passenger)

        if self.map.calc_distance(self.cab.pos, self.passenger.destination) < 25 and self.cab.passenger is not None: 
            self.cab.drop_off_passenger(self.passenger)

        pygame.display.flip()
        self.clock.tick(self.game_speed)
