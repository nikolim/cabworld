import pygame
import math


class Cab:
    def __init__(self, cab_file, map, pos):
        """
        Cab moving on map trying to pickup passengers
        @param cab_file: icon for cab 
        @param map: to put the cab on 
        @param pos: position of the passenger 
        """
        self.map = map
        self.img_size = 40
        self.pos = pos
        self.angle = 0
        self.speed = 0
        self.radars = [0, 0, 0]  # 0: forward-move 1: left-turn 2: right-turn
        self.is_alive = True
        self.distance = 0
        self.time_spent = 0
        self.passenger = None
        self.next_passenger = None
        self.pick_up_possible = 0
        self.drop_off_possible = 0
        self.debug = False

        self.cab_img = pygame.image.load(cab_file)
        self.cab_img = pygame.transform.scale(
            self.cab_img, (self.img_size, self.img_size))
        self.rotate_cab_img = self.cab_img
        self.img_pos = [int(self.pos[0] - (self.img_size/2)),
                        int(self.pos[1] - (self.img_size/2))]

        # rewards
        self.pick_up_reward = 1000
        self.drop_off_reward = 1000
        # motivate cab to drive the shortest path
        self.path_penalty = - 10
        self.step_penalty = - 10
        self.wrong_pick_up_penalty = -100
        self.wrong_drop_off_penalty = -100
        self.rewards = 0
        self.check_radar()

    def check_radar(self):
        """
        Check if there is a street in front, on the left, on the right
        Uses compares color values
        """
        self.radars = [0, 0, 0]
        sensor_field = 40  # how far the sensors of the cab / driver can see

        front_x = self.pos[0] + \
            math.cos(math.radians(360 - self.angle)) * sensor_field
        front_y = self.pos[1] + \
            math.sin(math.radians(360 - self.angle)) * sensor_field

        if self.check_if_street(front_x, front_y):
            self.radars[0] = 1

        left_x = self.pos[0] + \
            math.cos(math.radians(360 - self.angle - 90)) * sensor_field
        left_y = self.pos[1] + \
            math.sin(math.radians(360 - self.angle - 90)) * sensor_field
        if self.check_if_street(left_x, left_y):
            self.radars[1] = 1

        right_x = self.pos[0] + \
            math.cos(math.radians(360 - self.angle + 90)) * sensor_field
        right_y = self.pos[1] + \
            math.sin(math.radians(360 - self.angle + 90)) * sensor_field
        if self.check_if_street(right_x, right_y):
            self.radars[2] = 1

    def calc_rewards(self):
        """
        Calculate current rewards
        """
        if self.passenger:
            self.rewards += self.path_penalty
        self.rewards += self.path_penalty

    def check_for_passengers(self):
        """
        Check if a pasenger can be picked up or dropped off
        """
        self.drop_off_possible = 0
        self.pick_up_possible = 0
        if self.passenger is None:
            # Empty cab -> check if pick-up is possible
            self.next_passenger = self.map.get_nearest_passenger(self.pos)
            if self.next_passenger:
                distance = self.map.calc_distance(
                    self.pos, self.next_passenger.pos)
                if distance == 0:
                    self.pick_up_possible = 1
        if self.passenger:
            # Occupied cab -> check if drop-off possible
            distance = self.map.calc_distance(
                self.pos, self.passenger.destination)
            if distance == 0:
                self.drop_off_possible = 1

    def update(self):
        """
        Update the values of the cab after movement
        """
        # rotate image
        self.rotate_cab_img = self.rot_center(self.cab_img, self.angle)
        # move cab
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        # keep track of distance and time
        self.distance += self.speed
        self.time_spent += 1
        self.img_pos = [int(self.pos[0]) - (self.img_size/2),
                        int(self.pos[1]) - (self.img_size/2)]
        # print(self.distance)

        self.check_radar()
        self.check_for_passengers()
        self.calc_rewards()

    def pick_up_passenger(self):
        """
        Picks up a the nearest passenger if available
        @param passenger: passenger to pick-up
        """
        if self.passenger is None:
            passenger = self.map.get_nearest_passenger(self.pos)
            if passenger:
                if self.map.calc_distance(self.pos, passenger.pos) == 0:
                    self.passenger = passenger
                    self.passenger.get_in_cab()
                    self.rewards += self.pick_up_reward
        else:
            self.rewards += self.wrong_pick_up_penalty

    def drop_off_passenger(self):
        """
        Drops off a passenger
        @param passenger: passenger to drop-off
        """
        if self.passenger:
            distance_pos_destination = self.map.calc_distance(
                self.pos, self.passenger.destination)
            if distance_pos_destination == 0:
                self.passenger.pos[0], self.passenger.pos[1] = self.pos[0], self.pos[1]
                self.passenger.reached_destination = True
                self.passenger.get_out_of_cab()
                self.passenger = None
                self.rewards += self.drop_off_reward
        else:
            self.rewards += self.wrong_drop_off_penalty

    def draw(self, screen):
        """
        Draw to cab on the map
        @param screen: to draw on
        """
        screen.blit(self.rotate_cab_img, self.img_pos)

    def rot_center(self, image, angle):
        """
        Rotate image around center
        @param image: image to rotate
        @param angle: angle to rotate the image
        """
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def check_if_street(self, x, y):
        """
        Check if there is street at a given position 
        @param x: x-Postion to check 
        @param y: y-Postion to check
        """
        delta = 10
        try:
            color = self.map.map_img.get_at(((int(x), int(y))))
            street_color = self.map.street_color
            red_similar = (
                street_color[0] - delta) < color[0] < (street_color[0] + delta)
            green_similar = (
                street_color[1] - delta) < color[1] < (street_color[1] + delta)
            blue_similar = (
                street_color[2] - delta) < color[2] < (street_color[2] + delta)
            return red_similar and green_similar and blue_similar
        except IndexError:
            return False
