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

def gen_random_policy(): 
    def policy_function(state): 
        possible_moves = [index for index, element in enumerate(state) if element == 1]
         # check if pickup is possible
        if state[3] == 1:
            action = 3
        # check if drop-off is possible
        elif state[4] == 1: 
            action = 4
        else: 
            if len(possible_moves) > 0:
                action = random.choice(possible_moves)
            else: 
                action = 0
        return action
    return policy_function

def q_learning(env, estimator, n_episode, gamma=1.0, epsilon=0.1, epsilon_decay=.99):
    for episode in range(n_episode):
        policy = gen_epsilon_greedy_policy(estimator, epsilon * epsilon_decay ** episode, n_action)
        #policy = gen_random_policy()
        state = env.reset()
        is_done = False

        while not is_done:
            action = policy(state)
            print(action)
            next_state, reward, is_done, _ = env.step(action)
            q_values_next = estimator.predict(next_state)
            td_target = reward + gamma * torch.max(q_values_next)
            estimator.update(state, action, td_target)
            total_reward_episode[episode] += reward

            if is_done:
                break
            state = next_state

            env.render()
            time.sleep(0.1)


n_state = env.observation_space.shape[0]
n_action = env.action_space.n
n_feature = 200
lr = 0.03

estimator = Estimator(n_feature, n_state, n_action, 50, lr)
n_episode = 1
total_reward_episode = [0] * n_episode
q_learning(env, estimator, n_episode, epsilon=0.1)

print("done")