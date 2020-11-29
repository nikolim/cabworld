import random
import time
import gym
import gym_cabworld

env = gym.make('Cabworld-v0')
n_episodes = 1

for episode in range(n_episodes):
    env.reset()
    state, reward, is_done, info = env.step(0)
    while not is_done:
        allowed_actions = state[:5]
        legal_actions = [s for s, a in zip(list(range(5)), allowed_actions) if a == 1]
        move = random.choice(legal_actions)
        state, reward, is_done, info = env.step(move)
        env.render()
        time.sleep(0.05)
        if is_done:
            print("Done")
