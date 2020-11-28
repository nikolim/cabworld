import time
from tqdm import tqdm
import torch
from algorithms.q_learning import *


def sarsa(env, estimator, n_episode, writer, gamma, epsilon, epsilon_decay, n_action, render, ):
    """
    Sarsa with NN as q-value approximator
    @param env: evironment to use
    @param estimator: estimator to predict q-values
    @param n_episode: number of episodes 
    @param gamma: discount future rewards
    @param epsilon: prob to choose random action
    @param epsilon_decay: reduce random actions over time
    """
    writer.add_text('Algorithm ', 'SARSA with NN')
    total_reward_episode = [0] * n_episode

    for episode in tqdm(range(n_episode)):
        policy = gen_epsilon_greedy_policy(
            estimator, epsilon * epsilon_decay ** episode, n_action)
        state = env.reset()
        action = policy(state)
        is_done = False
        saved_rewards = (0, 0, 0)
        last_episode = (episode == (n_episode - 1))
        while not is_done:
            next_state, reward, is_done, _ = env.step(action)
            saved_rewards = track_reward(reward, saved_rewards)
            q_values_next = estimator.predict(next_state)
            next_action = policy(next_state)

            td_target = reward + gamma * q_values_next[next_action]

            total_reward_episode[episode] += reward
            estimator.update(state, action, td_target, episode)

            if is_done:
                log_rewards(writer, saved_rewards,
                            total_reward_episode[episode], episode)
                estimator.total_loss = 0
                estimator.n_updates = 0
                break
            state = next_state
            action = next_action

            if render and last_episode:
                env.render()
                time.sleep(0.01)
                
    return total_reward_episode
