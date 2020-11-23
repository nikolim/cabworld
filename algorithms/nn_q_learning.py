import os
import random
from collections import deque
import time
import gym 
import torch
import torchvision
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt
from tqdm import tqdm

from estimator import Estimator
import gym_cabworld 

# Virtual display (requires xvfb)
virtual_display = True
if virtual_display:
    from pyvirtualdisplay import Display
    disp = Display().start()

env = gym.make('Cabworld-v0')

if not os.path.exists('../runs'):
    os.mkdir('../runs')

# Create a new log folder for tensorboard
log_folders = os.listdir('../runs')
if len(log_folders) == 0: 
    folder_number = 0
else:
    folder_number = max([int(elem) for elem in log_folders]) + 1
log_path = os.path.join("../runs", str(folder_number))     
writer = SummaryWriter(log_path)

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
    for episode in tqdm(range(n_episode)):
        policy = gen_epsilon_greedy_policy(estimator, epsilon * epsilon_decay ** episode, n_action)
        state = env.reset()
        is_done = False
        saved_rewards = (0,0,0)
        while not is_done:
            action = policy(state)
            next_state, reward, is_done, _ = env.step(action)
            saved_rewards = track_reward(reward, saved_rewards)
            q_values_next = estimator.predict(next_state)
            td_target = reward + gamma * torch.max(q_values_next)
            total_reward_episode[episode] += reward
            estimator.update(state, action, td_target, episode)
            if is_done:
                writer.add_scalar('Path Penalty', saved_rewards[0], episode)
                writer.add_scalar('Illegal Pick-up / Drop-off', saved_rewards[1], episode)
                writer.add_scalar('Illegal Move', saved_rewards[2], episode)
                writer.add_scalar('Reward', total_reward_episode[episode], episode)
                estimator.total_loss = 0
                estimator.n_updates = 0
                break
            state = next_state
        if episode % 10 == 0 and episode != 0:
            median_reward = sum(total_reward_episode[(episode-9):episode])/10
            median_rewards.append(median_reward)
            print(f"Episode:{episode} Median-Reward: {median_reward}")
            writer.add_scalar('Median Reward', total_reward_episode[episode], episode)


"""
Setup
"""
#n_state = env.observation_space.shape[0]
n_state = 2
n_action = env.action_space.n
n_feature = 12
lr = 0.15
n_episode = 10
total_reward_episode = [0] * n_episode
median_rewards = []
n_hidden = 12

estimator = Estimator(n_feature, n_state, n_action, n_hidden, lr, writer)
#estimator.load_models()
q_learning(env, estimator, n_episode, epsilon=(1-1/n_action))
#estimator.save_models()

median_reward = sum(total_reward_episode) / n_episode

# Write Parameters to Tensorboard
writer.add_hparams({'Episodes': n_episode,'lr': lr, 'epsilon': (1-1/n_action)}, {'reward': median_reward})
writer.add_text('Info ', 'Fixed Passenger')
writer.close()

