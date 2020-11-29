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
            legal_actions = [s for s, a in zip(list(range(5)), allowed_actions) if a == 1]
            move = random.choice(legal_actions)
            moves.append(move)
        states, rewards, is_done, info = env.step(moves)
        env.render()
        time.sleep(0.05)
        if is_done:
            print("Done")
