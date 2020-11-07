import pygame
import math

from gym_cabworld.envs.cab_model import Cab
from gym_cabworld.envs.map_model import Map
from gym_cabworld.envs.passenger_model import Passenger

screen_width = 1000
screen_height = 1000


class Game:
    def __init__(self):
        """
        Create Pygame with map, cab, passenger
        """
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.map = Map('images/map.png')
        passenger1 = Passenger('images/person_1.png',
                              self.map, [800, 800], 0, [65, 40])
        #passenger2 = Passenger('images/person_2.png',
        #                self.map, [710, 230], 0, [280, 800])
        self.map.add_passenger(passenger1)
        #self.map.add_passenger(passenger2)
        self.cab = Cab('images/cab.png', self.map, [65, 40])
        self.game_speed = 60
        self.mode = 0

    def action(self, action):
        """"
        Execute action on cab
        @param action: action to perform
        """
        if action == 0:
            self.cab.speed = 25
        if action == 1:
            self.cab.angle += 90
        elif action == 2:
            self.cab.angle -= 90
        elif action == 3:
            self.cab.pick_up_passenger()
        elif action == 4:
            self.cab.drop_off_passenger()

        self.cab.update()
        self.cab.check_radar()
        self.cab.check_for_passengers()

    def evaluate(self):
        """"
        Evaluate rewards
        @return reward
        """
        reward = 0
        if self.cab.goal:
            reward = 10000
        return reward

    def is_done(self):
        """"
        Check if cab has reached its goal
        @return bool
        """
        if not self.cab.is_alive or self.cab.goal:
            self.cab.current_check = 0
            self.cab.distance = 0
            return True
        return False

    def observe(self):
        """"
        Obsereve environment
        @return state of environment
        """
        # Possible actions
        r1, r2, r3 = self.cab.radars
        pick_up = self.cab.pick_up_possible
        drop_off = self.cab.drop_off_possible
        # own position
        p1, p2 = self.cab.pos
        return tuple([r1, r2, r3, pick_up, drop_off, p1, p2])

    def view(self):
        """"
        Render evironment using Pygame
        """
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
        self.cab.check_radar()
        self.cab.draw(self.screen)
        self.map.draw_passengers(self.screen)

        pygame.display.flip()
        self.clock.tick(self.game_speed)
