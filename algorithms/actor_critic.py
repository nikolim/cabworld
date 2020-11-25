import os
import time
import torch
import gym
import gym_cabworld
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.tensorboard import SummaryWriter


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


class ActorCriticModel(nn.Module):
    def __init__(self, n_input, n_output, n_hidden):
        super(ActorCriticModel, self).__init__()
        self.fc1 = nn.Linear(n_input, n_hidden[0])
        self.fc2 = nn.Linear(n_hidden[0], n_hidden[1])
        self.action = nn.Linear(n_hidden[1], n_output)
        self.value = nn.Linear(n_hidden[1], 1)

    def forward(self, x):
        x = torch.Tensor(x)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        action_probs = F.softmax(self.action(x), dim=-1)
        state_values = self.value(x)
        return action_probs, state_values


class PolicyNetwork():
    def __init__(self, n_state, n_action, n_hidden, lr, writer):
        self.model = ActorCriticModel(n_state, n_action, n_hidden)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr)
        self.scheduler = torch.optim.lr_scheduler.StepLR(
            self.optimizer, step_size=10, gamma=0.9)
        self.writer = writer
    def predict(self, s):
        """
        Compute the output using the Actor Critic model
        @param s: input state
        @return: action probabilities, state_value
        """
        return self.model(torch.Tensor(s))

    def update(self, returns, log_probs, state_values):
        """
        Update the weights of the Actor Critic network given the training samples
        @param returns: return (cumulative rewards) for each step in an episode
        @param log_probs: log probability for each step
        @param state_values: state-value for each step
        """
        loss = 0
        for log_prob, value, Gt in zip(log_probs, state_values, returns):
            advantage = Gt - value.item()
            policy_loss = -log_prob * advantage

            value_loss = F.smooth_l1_loss(value, Gt)

            loss += policy_loss + value_loss

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def get_action(self, s):
        """
        Estimate the policy and sample an action, compute its log probability
        @param s: input state
        @return: the selected action, log probability, predicted state-value
        """
        action_probs, state_value = self.predict(s)
        action = torch.multinomial(action_probs, 1).item()
        log_prob = torch.log(action_probs[action])
        return action, log_prob, state_value

    def save_models(self, PATH='../checkpoints/ac_checkpoint.tar'):
        if not os.path.exists('../checkpoints'):
            os.mkdir('../checkpoints')

        model_opt_dict = {}
        model_name = 'model_state_dict'
        optimizer_name = 'optimizer_state_dict'
        model_opt_dict[model_name] = self.model.state_dict()
        model_opt_dict[optimizer_name] = self.optimizer.state_dict()
        try:
            torch.save(model_opt_dict, PATH)
            print("Saved checkpoint")
        except:
            print("Could not save checkpoint")
        self.writer.close()

    def load_models(self, PATH='../checkpoints/ac_checkpoint.tar'):
        try:
            checkpoint = torch.load(PATH)
            self.models.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            print("Loaded checkpoint")
        except:
            print("Could not load checkpoint")


def actor_critic(env, estimator, n_episode, writer, gamma, epsilon, epsilon_decay, n_action, render, ):
    """
    Actor Critic algorithm
    @param env: Gym environment
    @param estimator: policy network
    @param n_episode: number of episodes
    @param gamma: the discount factor
    """
    total_reward_episode = [0] * n_episode

    for episode in range(n_episode):
        log_probs = []
        rewards = []
        state_values = []
        state = env.reset()
        saved_rewards = (0, 0, 0)
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
                estimator.update(returns, log_probs, state_values)
                print('Episode: {}, total reward: {}'.format(
                    episode, total_reward_episode[episode]))
                log_rewards(writer, saved_rewards,
                            total_reward_episode[episode], episode)
                if total_reward_episode[episode] >= -14:
                    estimator.scheduler.step()
                break
            state = next_state
    return total_reward_episode
