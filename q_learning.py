import random
import time
import gym 
import torch

from estimator import Estimator
import gym_cabworld 

env = gym.make('Cabworld-v0')

def gen_epsilon_greedy_policy(estimator, epsilon, n_action):
    def policy_function(state):
        probs = torch.ones(n_action) * epsilon / n_action
        allowed_actions = torch.Tensor(state[:5])
        q_values = estimator.predict(state)
        best_action = torch.argmax(q_values).item()
        probs[best_action] += 1.0 - epsilon
        probs_allowed = probs * allowed_actions
        action = torch.multinomial(probs_allowed, 1).item()
        return action
    return policy_function


def q_learning(env, estimator, n_episode, gamma=0.999, epsilon=0.1, epsilon_decay=.99):
    for episode in range(n_episode):
        policy = gen_epsilon_greedy_policy(estimator, epsilon * epsilon_decay ** episode, n_action)
        state = env.reset()
        is_done = False
        last_episode = (episode == (n_episode - 1))
        blocker = True
        while not is_done:
            action = policy(state)
            next_state, reward, is_done, _ = env.step(action)
            q_values_next = estimator.predict(next_state)
            td_target = reward + gamma * torch.max(q_values_next)
            estimator.update(state, action, td_target)
            total_reward_episode[episode] += reward

            if is_done:
                print(f"Episode {episode} Reward {total_reward_episode[episode]}")   
                break
            state = next_state

            # (Render last episode)
            # if last_episode:
            #     if blocker: 
            #         input("Start last run")
            #         blocker = False
            #     env.render()
            #     time.sleep(0.001)

n_state = env.observation_space.shape[0]
n_action = env.action_space.n
n_feature = 200
lr = 0.03

estimator = Estimator(n_feature, n_state, n_action, 50, lr)
n_episode = 100
total_reward_episode = [0] * n_episode
q_learning(env, estimator, n_episode, epsilon=0.1)
estimator.save_weights()
last_reward = str(total_reward_episode[n_episode-1])
print("Done")

import matplotlib.pyplot as plt
plt.plot(range(len(total_reward_episode)), total_reward_episode, label=last_reward)
plt.legend()
plt.show()
plt.savefig("rewards.png")