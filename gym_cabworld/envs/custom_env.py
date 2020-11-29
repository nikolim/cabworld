import gym
from gym import spaces
import numpy as np
from gym_cabworld.envs.game import Game


class CustomEnv(gym.Env):
    def __init__(self):
        """
        Create OpenAiGym with Pygame
        """
        self.pygame = Game()
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), np.array(
            [1, 1, 1, 1, 1, 1000, 1000, 360, 1000, 1000, 1000, 1000]), dtype=np.int)

    def reset(self):
        """
        Reset Game
        """
        del self.pygame
        self.pygame = Game()
        obs = self.pygame.observe()
        return obs

    def step(self, actions):
        """
        Execute one step in environment
        """
        self.pygame.action(actions)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        """
        Render PyGame
        """
        self.pygame.view()




