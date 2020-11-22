import random
from collections import deque
import time
import gym 
import torch
import matplotlib.pyplot as plt

from estimator import Estimator
import gym_cabworld 

env = gym.make('Cabworld-v0')
reward_summary = []

def track_reward(reward, saved_rewards):
    saved_rewards = list(saved_rewards)
    if reward == -10: 
        saved_rewards[0] += 1
    if reward == -110: 
        saved_rewards[1] += 1
    if reward == -510: 
        saved_rewards[2] += 1
    return tuple(saved_rewards)

def gen_epsilon_greedy_policy(estimator, epsilon, n_action):
    """
    Generate a greecy policy 
    Select best policy with probability 1-epsilon or random action with epsilon
    @param estimator: predict q-values 
    @param epsilon: probability to select random action
    @param n_action: number of possible actions
    @return policy_function
    """
    def policy_function(state):
        probs = torch.ones(n_action) * epsilon / n_action
        q_values = estimator.predict(state)
        best_action = torch.argmax(q_values).item()
        probs[best_action] += 1.0 - epsilon
        action = torch.multinomial(probs, 1).item()
        return action
    return policy_function

def q_learning(env, estimator, n_episode, gamma=0.99, epsilon=0.8, epsilon_decay=.975):
    """
    Run Q-Learning with TD with NN as predictor for the q-values for a given state
    @param env: evironment to use
    @param estimator: estimator to predict q-values
    @param n_episode: number of episodes 
    @param gamma: discount future rewards
    @param epsilon: prob to choose random action
    @param epsilon_decay: reduce random actions over time
    """
    for episode in range(n_episode):
        policy = gen_epsilon_greedy_policy(estimator, epsilon * epsilon_decay ** episode, n_action)
        state = env.reset()
        is_done = False
        last_episode = (episode == (n_episode - 1))
        blocker = True
        memory =  deque()
        game_time = time.time()
        saved_rewards = (0,0,0)
        while not is_done:
            action = policy(state)
            next_state, reward, is_done, _ = env.step(action)
            saved_rewards = track_reward(reward, saved_rewards)
            q_values_next = estimator.predict(next_state)
            td_target = reward + gamma * torch.max(q_values_next)
            total_reward_episode[episode] += reward
            estimator.update(state, action, td_target)
            # memory.append((state, action, td_target))
            if is_done:
                print(f"Episode {episode} Reward {total_reward_episode[episode]}")   
                reward_summary.append(saved_rewards)
                break
            state = next_state

        if episode % 9 == 0 and episode != 0:
            median_reward = sum(total_reward_episode[(episode-9):episode])/10
            median_rewards.append(median_reward)
            print(f"Episode:{episode} Median-Reward: {median_reward}")
            #estimator.save_models()

"""
Setup
"""
#n_state = env.observation_space.shape[0]
n_state = 2
n_action = env.action_space.n
n_feature = 12
lr = 0.01
n_episode = 100
total_reward_episode = [0] * n_episode
median_rewards = []

estimator = Estimator(n_feature, n_state, n_action, 50, lr)
estimator.load_models()
q_learning(env, estimator, n_episode, epsilon=(1-1/n_action))
estimator.save_models()

# Create plots
plt.plot(range(len(total_reward_episode)), total_reward_episode, label='Total rewards')
median_array = []
plt.plot(list(range(0,len(median_rewards)*10,10)), median_rewards, label='Median rewards')
plt.legend()
plt.show()

print(estimator.action_counter)

plt.plot(range(len(reward_summary)), [elem[0] for elem in reward_summary], label='Steps')
plt.plot(range(len(reward_summary)), [elem[1] for elem in reward_summary], label='Illegal pik-ups / drop-offs')
plt.plot(range(len(reward_summary)), [elem[2] for elem in reward_summary], label='Illegal moves')
plt.legend()
plt.show()
