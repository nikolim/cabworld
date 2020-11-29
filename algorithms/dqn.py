import random
import time
import torch
from tqdm import tqdm
from collections import deque
from algorithms.tensorboard_tracker import track_reward, log_rewards


def gen_epsilon_greedy_policy(estimator, epsilon, n_action):
    def policy_function(state):
        if random.random() < epsilon:
            return random.randint(0, n_action - 1)
        else:
            q_values = estimator.predict(state)
            return torch.argmax(q_values).item()

    return policy_function


def dqn_learning(env, estimator, n_episode, writer, gamma, epsilon, epsilon_decay, n_action, render):
    """
    Deep Q-Learning using DQN, with experience replay
    @param env: Gym environment
    @param estimator: DQN object
    @param n_episode: number of episodes
    @param gamma: the discount factor
    @param epsilon: parameter for epsilon_greedy
    @param epsilon_decay: epsilon decreasing factor
    """

    writer.add_text('Algorithm ', 'DQN')
    total_reward_episode = [0] * n_episode
    memory = deque(maxlen=3000)
    replay_size = 1000

    for episode in tqdm(range(n_episode)):
        policy = gen_epsilon_greedy_policy(estimator, epsilon, n_action)
        state = env.reset()
        is_done = False
        saved_rewards = (0, 0, 0)
        last_episode = (episode == (n_episode - 1))
        while not is_done:
            action = policy(state)
            next_state, reward, is_done, _ = env.step(action)
            saved_rewards = track_reward(reward, saved_rewards)
            total_reward_episode[episode] += reward
            memory.append((state, action, next_state, reward, is_done))
            if is_done:
                log_rewards(writer, saved_rewards, total_reward_episode[episode], episode)
                break
            state = next_state

            if render and last_episode:
                env.render()
                time.sleep(0.01)

        estimator.replay(memory, replay_size, gamma, episode)

        print('Episode: {}, total reward: {}'.format(episode, total_reward_episode[episode]))
        epsilon = max(epsilon * epsilon_decay, 0.01)

    return total_reward_episode
