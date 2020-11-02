import gym 
import gym_cabworld 
env = gym.make('Cabworld-v0')
env.reset()
action = env.action_space.sample()
env.step(action)
env.render()

while True: 
    pass