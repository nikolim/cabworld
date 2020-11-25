import time
import gym
import torch
import argparse
from collections import deque
from torch.utils.tensorboard import SummaryWriter
import random
import gym_cabworld
from algorithms.dqn_estimator import *
from algorithms.nn_estimator import *
from algorithms.actor_critic_model import *
from algorithms.sarsa import *
from algorithms.q_learning import *

parser = argparse.ArgumentParser(description="Training selector for Cabworld-v0")
parser.add_argument('-a', '--algorithm', type=str, required=True,
                    help="Algorithm to run")    
parser.add_argument('-n', '--number', type=int, required=True,
                    help="Number of episodes to run")
parser.add_argument('-t', '--timeout', type=float, required=False, default=0.05,
                    help="Timeout between frames")
args = parser.parse_args()

env = gym.envs.make("Cabworld-v0")

n_action = 12
n_feature= 12
n_hidden = 50
lr = 0.01

writer = SummaryWriter("tmp")

if args.algorithm == "dqn": 
    estimator = DQN(n_feature, n_action,
                      n_hidden, lr, writer)
elif args.algorithm == "sarsa":
    estimator = Estimator(n_feature, n_action,
                      n_hidden, lr, writer)
elif args.algorithm == "ac": 
    estimator = PolicyNetwork(n_feature, n_action, n_hidden*8 , lr, writer)
else: 
    print("No algorithm specified")
    exit()

estimator.load_models()

for episode in range(args.number):
    state = env.reset()
    is_done = False
    episode_rewards = 0
    while not is_done:
        if args.algorithm == "dqn" or args.algorithm == "sarsa": 
            q_values = estimator.predict(state)
            action = torch.argmax(q_values).item()
        if args.algorithm == "ac": 
            action_probs, _ = estimator.predict(state)
            action = torch.argmax(action_probs).item()
    
        next_state, reward, is_done, _ = env.step(action)
        episode_rewards += reward
        env.render()
        time.sleep(0.05)
        if is_done:
            break
        state = next_state

    print('Episode: {}, total reward: {}'.format(episode, episode_rewards))
