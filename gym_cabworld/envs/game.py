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
        self.map = Map('images/map_gen.png')
        random_pos = self.map.get_random_pos_on_map()
        passenger1 = Passenger('images/person_1.png',
                              self.map, random_pos, 0, [60, 60])
        #passenger2 = Passenger('images/person_2.png',
        #                self.map, [710, 230], 0, [280, 800])
        self.map.add_passenger(passenger1)
        #self.map.add_passenger(passenger2)
        self.cab = Cab('images/cab.png', self.map, [60, 60])
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
        Obsereve environment
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
            pass_x, pass_y = 0,0
            dest_x, dest_y = 0,0
        return tuple([r1, r2, r3, pick_up, drop_off, pos_x, pos_y, angle, pass_x, pass_y, dest_x, dest_y])

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



