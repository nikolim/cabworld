import os
import random
import argparse
import time
from tqdm import tqdm
from collections import deque

import gym
import torch
import torchvision
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt

import gym_cabworld
from estimator import Estimator
from algorithms.nn_q_learning import *
from algorithms.sarsa import *

parser = argparse.ArgumentParser(
    description="Training template for Cabworld-v0")
parser.add_argument('-a', '--algorithm', type=str, required=True,
                    help="Algorithm to run")    
parser.add_argument('-n', '--number', type=int, required=True,
                    help="Number of episodes to run")
parser.add_argument('-lr', '--learningrate', type=float, required=False, default=0.01,
                    help="Learning rate to train the network")
parser.add_argument('-e', '--epsilon', type=float, required=False, default=(1-1/6),
                    help="Epsilon for epsilon greedy")
parser.add_argument('-de', '--decay', type=float, required=False, default=0.975,
                    help="Epsilon decay")
parser.add_argument('-g', '--gamma', type=float, required=False, default=0.99,
                    help="Gamma (discount)")
parser.add_argument('-d', '--display', type=bool, required=False, default=False,
                    help="True: display game, False: use virtual display")
parser.add_argument('-r', '--render', type=bool, required=False, default=False,
                    help="Render last episode")
parser.add_argument('-s', '--save', type=bool, required=False, default=True,
                    help="Save model")
parser.add_argument('-l', '--load', type=bool, required=False, default=True,
                    help="Load model")
args = parser.parse_args()


# Virtual display (requires xvfb)
if not args.display:
    from pyvirtualdisplay import Display
    disp = Display().start()

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

env = gym.make('Cabworld-v0')

"""
Setup
"""
n_action = env.action_space.n
n_episode = args.number
n_feature = 12
n_hidden = 12

estimator = Estimator(n_feature, n_action,
                      n_hidden, args.learningrate, writer)
if args.load:
    estimator.load_models()

if args.algorithm == "dqn": 
    algorithm = q_learning
elif args.algorithm == "sarsa":
    algorithm = sarsa
else: 
    print("No algorithm specified")
    exit()

total_reward_episode = algorithm(env=env, estimator=estimator, n_episode=args.number, writer=writer, gamma=args.gamma,
                                  epsilon=args.epsilon, epsilon_decay=args.decay, n_action=n_action, render=args.render)

if args.save:
    estimator.save_models()

median_reward = sum(total_reward_episode) / n_episode
writer.add_hparams({'Episodes': args.number, 'lr': args.learningrate,
                    'epsilon': args.epsilon, 'decay': args.decay},
                   {'reward': median_reward})
writer.add_text('Info ', 'Fixed Passenger')
writer.close()
