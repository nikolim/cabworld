import time
from tqdm import tqdm
import torch

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


def q_learning(env, estimator, n_episode, writer, gamma, epsilon, epsilon_decay, n_action, render):
    """
    Run Q-Learning with TD with NN as predictor for the q-values for a given state
    @param env: evironment to use
    @param estimator: estimator to predict q-values
    @param n_episode: number of episodes 
    @param gamma: discount future rewards
    @param epsilon: prob to choose random action
    @param epsilon_decay: reduce random actions over time
    """
    writer.add_text('Algorithm ', 'Q-Learning with NN')
    total_reward_episode = [0] * n_episode

    for episode in tqdm(range(n_episode)):
        policy = gen_epsilon_greedy_policy(estimator, epsilon * epsilon_decay ** episode, n_action)
        state = env.reset()
        is_done = False
        saved_rewards = (0,0,0)
        last_episode = (episode == (n_episode - 1))
        while not is_done:
            action = policy(state)
            next_state, reward, is_done, _ = env.step(action)
            saved_rewards = track_reward(reward, saved_rewards)
            q_values_next = estimator.predict(next_state)
            td_target = reward + gamma * torch.max(q_values_next)
            total_reward_episode[episode] += reward
            estimator.update(state, action, td_target, episode)
            if is_done:
                log_rewards(writer, saved_rewards, total_reward_episode[episode], episode)
                estimator.total_loss = 0
                estimator.n_updates = 0
                break
            state = next_state

            if render and last_episode:
                env.render()
                time.sleep(0.01)

    return total_reward_episode
