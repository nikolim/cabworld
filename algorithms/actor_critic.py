import time
from tqdm import tqdm
from algorithms.actor_critic_model import *
from algorithms.tensorboard_tracker import track_reward, log_rewards


def actor_critic(env, estimator, n_episode, writer, gamma, epsilon, epsilon_decay, n_action, render):
    """
    Actor Critic algorithm
    @param env: Gym environment
    @param estimator: policy network
    @param n_episode: number of episodes
    @param writer: tensorboard writer
    @param gamma: the discount factor
    @param epsilon: initial epsilon
    @param epsilon_decay: epsilon decay for each episode
    @param n_action: number of possible actions
    @param render: boolean if last episode should be rendered
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
