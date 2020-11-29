import gym
from gym import spaces
import numpy as np
from gym_cabworld.envs.game import Game
from gym_cabworld.envs.game_marl import MarlGame


class CustomEnv(gym.Env):
    def __init__(self):
        """
        Create OpenAiGym with Pygame
        """
        self.pygame = Game(0)
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), np.array(
            [1, 1, 1, 1, 1, 1000, 1000, 360, 1000, 1000, 1000, 1000]), dtype=np.int)

    def reset(self):
        """
        Reset Game
        """
        del self.pygame
        self.pygame = Game(0)
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

class CustomEnv1(CustomEnv):
    def __init__(self):
        """
        Create OpenAiGym with Pygame
        """
        self.pygame = Game(1)
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), np.array(
            [1, 1, 1, 1, 1, 1000, 1000, 360, 1000, 1000, 1000, 1000]), dtype=np.int)
    
    def reset(self):
        """
        Reset Game
        """
        del self.pygame
        self.pygame = Game(1)
        obs = self.pygame.observe()
        return obs


class CustomEnv2(CustomEnv):
    def __init__(self):
        """
        Create OpenAiGym with Pygame
        """
        self.pygame = Game(2)
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), np.array(
            [1, 1, 1, 1, 1, 1000, 1000, 360, 1000, 1000, 1000, 1000]), dtype=np.int)

    def reset(self):
        """
        Reset Game
        """
        del self.pygame
        self.pygame = Game(2)
        obs = self.pygame.observe()
        return obs

class MarlEnv(CustomEnv):
    def __init__(self):
        """
        Create OpenAiGym with Pygame
        """
        self.pygame = MarlGame()
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), np.array(
            [1, 1, 1, 1, 1, 1000, 1000, 360, 1000, 1000, 1000, 1000]), dtype=np.int)
    
    def reset(self):
        """
        Reset Game
        """
        del self.pygame
        self.pygame = MarlGame()
        obs = self.pygame.observe()
        return obs