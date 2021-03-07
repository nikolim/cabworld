import os
from random import randint
import random

import pygame

from gym_farmworld.envs.tractor_model import Tractor
from gym_farmworld.envs.map_model import Map
from gym_farmworld.envs.hay_model import Hay

screen_width = 1000
screen_height = 1000

number_hay = 10  # initial
max_number_hay = 10
min_number_hay = 0
respawn_rate = 10000  # steps


class Game:
    def __init__(self, game_mode):
        """
        Create Pygame with map, cab, passenger
        """
        pygame.init()
        pygame.display.set_caption("Farmworld-v" + str(game_mode))
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        pygame.time.get_ticks()

        dirname = os.path.dirname(__file__)
        self.img_path = os.path.join(dirname, "..", "images")
        data_path = os.path.join(dirname, "..", "data")
        self.game_mode = game_mode

        assert game_mode in [0, 2]

        if game_mode == 0:
            img = "small_map_gen.png"
        else:
            img = "map_gen.png"

        self.map = Map(
            os.path.join(self.img_path, img), screen_width, game_mode, data_path
        )
        self.grid_size = self.map.get_grid_size()

        self.passenger_id = 0
        for _ in range(number_hay):
            self.add_hay()

        tractor_pos = self.map.get_random_pos_on_map()
        self.tractor = Tractor(
            os.path.join(self.img_path, "tractor.png"), os.path.join(self.img_path, "tactor_with_hay.png"), self.map,
            tractor_pos, self.grid_size
        )

        self.game_speed = int(self.grid_size * 1.5)
        self.mode = 0
        self.steps = 0

    def add_hay(self):
        """ "
        Add passenger with random position and destination on map
        """
        random_pos = self.map.get_random_pos_on_map()
        # random_dest = self.map.get_random_pos_on_map()
        random_dest = 150, 150
        img = "hay.png"
        passenger = Hay(
            os.path.join(self.img_path, img),
            self.map,
            random_pos,
            0,
            random_dest,
            self.grid_size,
            self.passenger_id,
        )
        self.map.add_passenger(passenger)
        self.passenger_id += 1

    def action(self, action):
        """ "
        Execute action on cab
        @param action: action to perform
        """
        # reset rewards
        self.tractor.rewards = 0

        if action == 0:
            self.tractor.move_up()
        elif action == 1:
            self.tractor.move_right()
        elif action == 2:
            self.tractor.move_down()
        elif action == 3:
            self.tractor.move_left()
        elif action == 4:
            self.tractor.pick_up_passenger()
        elif action == 5:
            self.tractor.drop_off_passenger()
        elif action == 6:
            self.tractor.do_nothing()

        self.steps += 1
        # repawn new hay
        if (
                len(self.map.passengers) < max_number_hay
                and self.steps % respawn_rate == 0
        ) or len(self.map.passengers) < min_number_hay:
            self.add_hay()

        self.tractor.update()

    def evaluate(self):
        """ "
        Evaluate rewards
        @return reward
        """
        return self.tractor.rewards

    def is_done(self):
        """ "
        Check if all passengers have reached their destination
        @return bool
        """
        return self.map.all_passengers_reached_dest()
        # return False

    def normalise(self, state):
        """ "
        Normalise state
        @param state
        @return normalised state
        """
        features = list(state)[:5]
        for i in range(5, len(state)):
            if state[i] == -1:
                features.append(-1)
            else:
                features.append(
                    abs(
                        round(
                            (state[i] - (1.5 * self.grid_size))
                            / (screen_width - (3 * self.grid_size)),
                            3,
                        )
                    )
                )
        return features

    def observe(self):
        """ "
        Observe environment
        @return state of environment
        """
        # Possible actions
        r1, r2, r3, r4 = self.tractor.radars
        hay = 1 if self.tractor.hay else -1
        pos_x, pos_y = self.tractor.pos

        state = [r1, r2, r3, r4, hay, pos_x, pos_y]

        if self.tractor.hay:
            state.append(self.tractor.hay.destination[0])
            state.append(self.tractor.hay.destination[1])
        else:
            state.append(self.tractor.next_hays[0].pos[0])
            state.append(self.tractor.next_hays[0].pos[1])

        return self.normalise(state)

    def view(self):
        """
        Render environment using Pygame
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.screen.blit(self.map.map_img, (0, 0))
        if self.mode == 1:
            self.screen.fill((0, 0, 0))

        self.tractor.check_radar()
        self.tractor.draw(self.screen)
        self.map.draw_passengers(self.screen)

        pygame.display.flip()
        self.clock.tick(self.game_speed)
