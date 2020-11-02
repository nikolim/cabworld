import gym 
import gym_cabworld 
import time

env = gym.make('Cabworld-v0')
env.reset()
action = env.action_space.sample()
env.step(action)
env.render()

while True: 
    time.sleep(1)