import pygame
import math

class Map: 
    def __init__(self, map_file):
        """
        Map for the cabworld definded by image
        @param map_file: map to create world
        """
        self.map_img = pygame.image.load(map_file)
        self.street_color = (175,171,171,255) #define color of street
        self.passengers = []

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
        min_distance = 1000
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