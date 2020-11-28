import os
import time
import torch
import gym
import gym_cabworld
from tqdm import tqdm
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter
from actor_critic_model import *

def track_reward(reward, saved_rewards):
    """
    Count the number of rewards / penalties
    @param reward: reward for last action 
    @param saved_rewards: tupel of previous received rewards
    """
    saved_rewards = list(saved_rewards)
    if reward == -10:
        saved_rewards[0] += 1
    if reward == -110:
        saved_rewards[1] += 1
    if reward == -510:
        saved_rewards[2] += 1
    return tuple(saved_rewards)


def log_rewards(writer, saved_rewards, episode_reward, episode):
    """
    Log rewards for tensorboard
    @param writer: writer to write to into logs
    @param saved_rewards: Tupel with penalties (path, pick-up, illegal-move)
    @param episode_reward: reward for the current episode
    @param episode: curent number of episode
    """
    writer.add_scalar('Path Penalty', saved_rewards[0], episode)
    writer.add_scalar('Illegal Pick-up / Drop-off', saved_rewards[1], episode)
    writer.add_scalar('Illegal Move', saved_rewards[2], episode)
    writer.add_scalar('Reward', episode_reward, episode)

def actor_critic(env, estimator, n_episode, writer, gamma, epsilon, epsilon_decay, n_action, render, ):
    """
    Actor Critic algorithm
    @param env: Gym environment
    @param estimator: policy network
    @param n_episode: number of episodes
    @param gamma: the discount factor
    """
    total_reward_episode = [0] * n_episode

    for episode in tqdm(range(n_episode)):
        log_probs = []
        rewards = []
        state_values = []
        state = env.reset()
        saved_rewards = (0, 0, 0)
        last_episode = (episode == (n_episode - 1))
        while True:
            action, log_prob, state_value = estimator.get_action(state)
            next_state, reward, is_done, _ = env.step(action)
            saved_rewards = track_reward(reward, saved_rewards)
            total_reward_episode[episode] += reward
            log_probs.append(log_prob)
            state_values.append(state_value)
            rewards.append(reward)

            if is_done:
                returns = []
                Gt = 0
                pw = 0
                for reward in rewards[::-1]:
                    Gt += gamma ** pw * reward
                    pw += 1
                    returns.append(Gt)

                returns = returns[::-1]
                returns = torch.tensor(returns)
                returns = (returns - returns.mean()) / (returns.std() + 1e-9)
                estimator.update(returns, log_probs, state_values, episode)
                log_rewards(writer, saved_rewards,
                            total_reward_episode[episode], episode)
                if total_reward_episode[episode] >= -14:
                    estimator.scheduler.step()
                break

            if render and last_episode:
                env.render()
                time.sleep(0.01)

            state = next_state
            
    return total_reward_episode
