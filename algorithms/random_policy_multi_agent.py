import random
import time
import gym
import gym_cabworld

env = gym.make('Cabworld-v3')
n_episodes = 1

for episode in range(n_episodes):
    states = env.reset()
    is_done = False
    while not is_done:
        moves = []
        for state in states:
            allowed_actions = state[:5]
            if allowed_actions[3] == 1: 
                move = 3
            elif allowed_actions[4] == 1: 
                move = 4
            else:
                legal_actions = [s for s, a in zip(list(range(5)), allowed_actions) if a == 1]
                move = random.choice(legal_actions)
            moves.append(move)
        states, rewards, is_done, info = env.step(moves)
        env.render()
        time.sleep(0.05)
        if is_done:
            print("Done")
