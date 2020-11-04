import random
import time
import gym 
import gym_cabworld 

env = gym.make('Cabworld-v0')
env.reset()

# initial random step
state, reward, is_done, info = env.step(0)

print(f'State: {state}')
print(f'Reward: {reward}')
print(f'Is done: {is_done}')
print(f'Info: {info}')

while not is_done: 
    possible_moves = [index for index, element in enumerate(state) if element == 1]
    print(possible_moves)
    move = random.choice(possible_moves)
    print(move)
    state, reward, is_done, info = env.step(move)
    env.render()
    time.sleep(0.05)
    if is_done: 
        print("Done")
