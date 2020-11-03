import gym
from gym import spaces
import numpy as np
from gym_cabworld.envs.game import Game

class CustomEnv(gym.Env):
    def __init__(self):
        self.pygame = Game()
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(np.array([0, 0, 0]), np.array([1,1,1]), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = Game()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view()