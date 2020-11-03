import gym 
import gym_cabworld 
import time

env = gym.make('Cabworld-v0')
env.reset()
env.step(0)
env.render()

while True: 
    time.sleep(1)