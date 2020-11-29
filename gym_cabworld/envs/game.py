import os
import math
import pygame
from random import randint

from gym_cabworld.envs.cab_model import Cab
from gym_cabworld.envs.map_model import Map
from gym_cabworld.envs.passenger_model import Passenger

screen_width = 1000
screen_height = 1000
number_passengers = 2


class Game():
    def __init__(self, game_mode):
        """
        Create Pygame with map, cab, passenger
        """
        pygame.init()
        pygame.display.set_caption('Cabworld-v' + str(game_mode))
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        dirname = os.path.dirname(__file__)
        img_path = os.path.join(dirname, '..', 'images')

        self.map = Map(os.path.join(img_path, 'map_gen.png'))

        if game_mode == 0: 
            img = 'person_' + str(randint(1, 3)) + '.png'
            passenger = Passenger(os.path.join(img_path, img),
                                  self.map, [940,940], 0, [60,60])
            self.map.add_passenger(passenger)
            self.cab = Cab(os.path.join(img_path, 'cab.png'), self.map, [60, 60])

        elif game_mode == 1: 
            for _ in range(3):
                random_pos = self.map.get_random_pos_on_map()
                random_dest = self.map.get_random_pos_on_map()
                img = 'person_' + str(randint(1, 3)) + '.png'
                passenger = Passenger(os.path.join(img_path, img),
                                    self.map, random_pos, 0, random_dest)
                self.map.add_passenger(passenger)
            self.cab = Cab(os.path.join(img_path, 'cab.png'), self.map, [60, 60])

        elif game_mode == 2: 
            for _ in range(3):
                random_pos = self.map.get_random_pos_on_map()
                random_dest = self.map.get_random_pos_on_map()
                img = 'person_' + str(randint(1, 3)) + '.png'
                passenger = Passenger(os.path.join(img_path, img),
                                    self.map, random_pos, 0, random_dest)
                self.map.add_passenger(passenger)
            cab_rand_pos = self.map.get_random_pos_on_map()
            self.cab = Cab(os.path.join(img_path, 'cab.png'), self.map, cab_rand_pos)

        self.game_speed = 100000000
        self.mode = 0

    def action(self, action):
        """"
        Execute action on cab
        @param action: action to perform
        """
        # reset rewards 
        self.cab.rewards = 0

        if action == 0:
            self.cab.move_forward()
        if action == 1:
            self.cab.turn_left()
        elif action == 2:
            self.cab.turn_right()
        elif action == 3:
            self.cab.pick_up_passenger()
        elif action == 4:
            self.cab.drop_off_passenger()

        self.cab.update()

    def evaluate(self):
        """"
        Evaluate rewards
        @return reward
        """
        return self.cab.rewards

    def is_done(self):
        """"
        Check if all passengers have reached their destination
        @return bool
        """
        return self.map.all_passengers_reached_dest()

    def observe(self):
        """"
        Observe environment
        @return state of environment
        """
        # Possible actions
        r1, r2, r3 = self.cab.radars
        pick_up = self.cab.pick_up_possible
        drop_off = self.cab.drop_off_possible
        # own position
        pos_x, pos_y = self.cab.pos
        angle = self.cab.angle
        if self.cab.next_passenger:
            pass_x, pass_y = self.cab.next_passenger.pos
            dest_x, dest_y = self.cab.next_passenger.destination
        else:
            pass_x, pass_y = 0, 0
            dest_x, dest_y = 0, 0
        return tuple([r1, r2, r3, pick_up, drop_off, pos_x, pos_y, angle, pass_x, pass_y, dest_x, dest_y])

    def view(self):
        """"
        Render environment using Pygame
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
