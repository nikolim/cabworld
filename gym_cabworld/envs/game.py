import pygame
import math

screen_width = 1000
screen_height = 1000
check_point = ((1200, 660), (1250, 120), (190, 200), (1030, 270), (250, 475), (650, 690))

class Map: 
    def __init__(self, map_file):
        self.map_img = pygame.image.load(map_file)

class Car:
    def __init__(self, car_file, map, pos):
        self.surface = pygame.image.load(car_file)
        self.surface = pygame.transform.scale(self.surface, (50, 50))
        self.rotate_surface = self.surface
        self.map = map 
        self.pos = pos
        self.angle = 0
        self.speed = 0
        self.center = [self.pos[0] + 25, self.pos[1] + 25]
        self.radars = []
        self.is_alive = True
        self.current_check = 0
        self.prev_distance = 0
        self.cur_distance = 0
        self.goal = False
        self.check_flag = False
        self.distance = 0
        self.time_spent = 0

    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)
        
    def check_collision(self):
        self.is_alive = True
        for p in self.four_points:
            if self.map.map_img.get_at((int(p[0]), int(p[1]))) == (255, 255, 255, 255):
                self.is_alive = False
                break

    def check_radar(self, screen):

        # how far the sensors of the car / driver can see
        sensor_field = 40

        front_x = self.center[0] + math.cos(math.radians(360 - self.angle)) * sensor_field
        front_y = self.center[1] + math.sin(math.radians(360 - self.angle)) * sensor_field

        right_x = self.center[0] + math.cos(math.radians(360 - self.angle + 90)) * sensor_field
        right_y = self.center[1] + math.sin(math.radians(360 - self.angle + 90)) * sensor_field

        left_x = self.center[0] + math.cos(math.radians(360 - self.angle - 90)) * sensor_field
        left_y = self.center[1] + math.sin(math.radians(360 - self.angle - 90)) * sensor_field

        # check for street color (175,171,171, 255) 255 = alpha
        if self.map.map_img.get_at(((int(front_x), int(front_y)))) == (175,171,171,255):
            print("Street in front")

        if self.map.map_img.get_at(((int(right_x), int(right_y)))) == (175,171,171,255):
            print("Street on the right")
        
        if self.map.map_img.get_at(((int(left_x), int(left_y)))) == (175,171,171,255):
            print("Street on the left")

        # Draw sensors
        # pygame.draw.line(screen, (255,255,255), (self.center[0], self.center[1]), (front_x, front_y), 5)
        # pygame.draw.line(screen, (255,255,255), (self.center[0], self.center[1]), (left_x, left_y), 5)
        # pygame.draw.line(screen, (255,255,255), (self.center[0], self.center[1]), (right_x, right_y), 5)


    def check_checkpoint(self):
        p = check_point[self.current_check]
        self.prev_distance = self.cur_distance
        dist = get_distance(p, self.center)
        if dist < 70:
            self.current_check += 1
            self.prev_distance = 9999
            self.check_flag = True
            if self.current_check >= len(check_point):
                self.current_check = 0
                self.goal = True
            else:
                self.goal = False

        self.cur_distance = dist

    def update(self):

        # pixels per action
        self.speed = 25        

        # rotate image
        self.rotate_surface = rot_center(self.surface, self.angle)

        # move cab
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed

        # keep track of distance and time
        self.distance += self.speed
        self.time_spent += 1
    
        # center = start cords + img-size 
        self.center = [int(self.pos[0]) + 25, int(self.pos[1]) + 25]
        

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.map = Map('images/map.png')
        self.car = Car('images/cab.png', self.map, [65, 40])
        self.game_speed = 60
        self.mode = 0


    def action(self, action):
        if action == 0:
            self.car.speed += 2
        if action == 1:
            self.car.angle += 90
        elif action == 2:
            self.car.angle -= 90

        self.car.update()
        # self.car.check_collision()
        self.car.check_checkpoint()
        # car check radar
        

    def evaluate(self):
        reward = 0
        """
        if self.car.check_flag:
            self.car.check_flag = False
            reward = 2000 - self.car.time_spent
            self.car.time_spent = 0
        """
        if not self.car.is_alive:
            reward = -10000 + self.car.distance

        elif self.car.goal:
            reward = 10000
        return reward

    def is_done(self):
        if not self.car.is_alive or self.car.goal:
            self.car.current_check = 0
            self.car.distance = 0
            return True
        return False

    def observe(self):
        # return state
        radars = self.car.radars
        ret = [0, 0, 0, 0, 0]
        for i, r in enumerate(radars):
            ret[i] = int(r[1] / 30)

        return tuple(ret)

    def view(self):
        # draw game
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

        pygame.draw.circle(self.screen, (255, 255, 0), check_point[self.car.current_check], 70, 1)
        
        self.car.draw(self.screen)
        self.car.check_radar(self.screen)

        pygame.display.flip()
        self.clock.tick(self.game_speed)


def get_distance(p1, p2):
	return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image