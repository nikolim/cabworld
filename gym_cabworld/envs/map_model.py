import csv
import math
import os
import random
import copy

import numpy as np
import pygame


class Map:
    def __init__(self, map_file, screen_size, game_mode, data_path):
        """
        Map for the cabworld defined by image
        @param map_file: map to create world
        """
        self.map_img = pygame.image.load(map_file)
        self.street_color = (175, 171, 171, 255)  # define color of street for radar
        self.passengers = []

        if game_mode < 4:
            map_file = "map.dat"
        else:
            map_file = "small_map.dat"

        map_dat_path = os.path.join(data_path, map_file)
        streets = []
        with open(map_dat_path, "r") as fd:
            reader = csv.reader(fd)
            for row in reader:
                streets.append([int(x) for x in row])

        self.streets = np.array(streets)
        self.grid_size = int(screen_size / len(self.streets))

        self.used_rand_pos = []

    def get_grid_size(self):
        return self.grid_size

    def add_passenger(self, passenger):
        """
        Add passenger to map
        @param passenger: passenger to add on map
        """
        self.passengers.append(passenger)

    def remove_passenger(self, passenger):
        """
        Remove passenger from map
        @param passenger: passenger to remove from map
        """
        if passenger in self.passengers:
            self.passengers.remove(passenger)

    def calc_distance(self, pos1, pos2):
        """
        Calculate distance between two objects
        @param pos1: position of 1.object
        @param pos2: position of 2.object
        @return distance in pixels
        """
        return round(math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2))

    def get_n_nearest_passengers(self, pos, n):
        """
        Get n nearest passenger
        @param pos: position of cab
        @return nearest passengers
        """
        distances = []
        passenger_dict = {}

        for tmp_passenger in self.passengers:
            if not tmp_passenger.reached_destination and not tmp_passenger.in_cab:
                tmp_distance = self.calc_distance(pos, tmp_passenger.pos)
                distances.append(tmp_distance)
                passenger_dict[tmp_distance] = tmp_passenger
        distances.sort()
        keys = distances[: (min(n, len(distances)))]
        passengers = [passenger_dict[key] for key in keys]
        return passengers

    def draw_passengers(self, screen):
        """
        Draw all the passengers on the map
        @param screen: to print on
        """
        for passenger in self.passengers:
            passenger.draw(screen)

    def all_passengers_reached_dest(self):
        """
        Test if all passengers on the map have reached their destination
        """
        for tmp_passenger in self.passengers:
            if not tmp_passenger.reached_destination:
                return False
        return True

    def get_random_pos_on_map(self):
        """
        Get random position on map (on the street)
        @return pos  in pixels
        """
        x, y = 0, 0
        while self.streets[y][x] != 1 or (x, y) in self.used_rand_pos:
            x = random.randint(0, len(self.streets) - 1)
            y = random.randint(0, len(self.streets) - 1)
        self.used_rand_pos.append((x, y))
        if len(self.used_rand_pos) > 10:
            self.used_rand_pos.pop(0)
        return [
            x * self.grid_size + int(self.grid_size / 2),
            y * self.grid_size + int(self.grid_size / 2),
        ]

    def add_n_to_map(self, tmp_map, pos, number):
        """
        Add number to map at certain
        @param map
        @param pos
        @param number
        @return map
        """
        x, y = pos
        x = int((x - (self.grid_size / 2)) / self.grid_size) - 1
        y = int((y - (self.grid_size / 2)) / self.grid_size) - 1
        tmp_map[y][x] += number
        return tmp_map

    def create_state_deck(self, cab_pos, cab_pass):
        """
        Create fully observed map
        @param cab_pos
        @return map
        """
        street_copy = copy.deepcopy(self.streets)
        tmp_map = street_copy[1:9, 1:9]
        n_passenger = 3
        passengers = self.get_n_nearest_passengers(cab_pos, n_passenger)
        for i, passenger in enumerate(passengers):
            tmp_map = self.add_n_to_map(tmp_map, passenger.pos, 2 + i)
            tmp_map = self.add_n_to_map(tmp_map, passenger.destination, 2 + i + n_passenger)
        cab_number = 9 if cab_pass else 8
        tmp_map = self.add_n_to_map(tmp_map, cab_pos, cab_number)
        tmp_map = tmp_map / 16
        return tmp_map.flatten()
