import os
import csv
import pygame
import math
import random
import numpy as np

class Map: 
    def __init__(self, map_file):
        """
        Map for the cabworld definded by image
        @param map_file: map to create world
        """
        self.map_img = pygame.image.load(map_file)
        self.street_color = (175,171,171,255) #define color of street for radar
        self.passengers = []

        dirname = os.path.dirname(__file__)
        map_dat_path = os.path.join(dirname, '..', '..', 'map.dat')
        streets = []
        with open(map_dat_path, 'r') as fd:
            reader = csv.reader(fd)
            for row in reader:
                streets.append([int(x) for x in row])
        self.streets =  np.array(streets)

    def add_passenger(self, passenger): 
        """
        Add passenger to map
        @param passenger: passenger to add on map
        """
        self.passengers.append(passenger)

    def calc_distance(self, pos1, pos2): 
        """
        Calculate distance between two objects
        @param pos1: position of 1.object
        @param pos2: position of 2.object 
        @return distance in pixels
        """
        return round(math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2))

    def get_nearest_passenger(self, pos): 
        """
        Get nearest passenger 
        @param pos: position of cab
        @return nearest passenger
        """
        nearest_passenger = None 
        min_distance = 100000
        for tmp_passenger in self.passengers: 
            if not tmp_passenger.reached_destination:
                tmp_distance = self.calc_distance(pos, tmp_passenger.pos)
                if tmp_distance < min_distance:
                    nearest_passenger = tmp_passenger
        return nearest_passenger
    
    def draw_passengers(self, screen):
        """
        Draw all the passengers on the map
        @param screen: to print on
        """
        for passenger in self.passengers: 
            if not passenger.in_cab:
                screen.blit(passenger.passenger_img_rot, passenger.img_pos)

    def all_passengers_reached_dest(self):
        """
        Test if all passengers on the map have reached their destination
        """
        for tmp_passenger in self.passengers: 
            if not tmp_passenger.reached_destination: 
                return False 
        return True

    def get_random_pos_on_map(self): 
        x,y = 0,0
        while self.streets[x][y] != 1: 
            x = random.randint(0,24)
            y = random.randint(0,24)
        return [y*40+20, x*40+20]

    def create_layer(self, pos): 
        layer = np.ones((25,25))
        x, y = pos 
        x = int((x - 20) / 40)
        y = int((y -20) / 40)
        layer[x][y] = 1 
        return layer
        
    def create_state_deck(self, cab_pos): 
        # 1 layer -> map
        street_layer = self.streets
        # 2 layer -> cab 
        cab_layer = self.create_layer(cab_pos)
        # 3 layer -> passenger pos
        passenger = self.passengers[0]
        pass_pos_layer = self.create_layer(passenger.pos)
        # 4 layer -> passenger dest
        pass_dest_layer = self.create_layer(passenger.destination)

        state_deck = np.array([street_layer, cab_layer, pass_pos_layer, pass_dest_layer])
        return state_deck