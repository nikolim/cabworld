import random
import pytest
import time
import gym

import gym_farmworld

from pyvirtualdisplay import Display

disp = Display().start()
possible_rewards = [0, -1, -5, -10, 100]


def check_states(state):
    assert len(state) == 9
    for k in range(0, 5):
        assert state[k] == 1 or state[k] == -1
    for i in range(5, len(state)):
        assert state[i] == -1 or 0 <= state[i] <= 1


def check_states_multi(states):
    for state in states:
        assert len(state) == 9
        for k in range(0, 5):
            assert state[k] == 1 or state[k] == -1
        for i in range(5, len(state)):
            assert state[i] == -1 or 0 <= state[i] <= 1


def run_single_agent_env(version):
    assert version == 0 or version == 2
    env = gym.make("Farmworld-v" + str(version))
    n_episodes = 10
    for episode in range(n_episodes):
        state = env.reset()
        is_done = False
        while not is_done:
            move = random.choice(list(range(7)))
            state, rewards, is_done, info = env.step(move)
            assert rewards in possible_rewards
            check_states(state)
        assert is_done


def run_multi_agent_env(version):
    assert version == 1 or version == 3
    env = gym.make("Farmworld-v" + str(version))
    n_episodes = 10
    for episode in range(n_episodes):
        states = env.reset()
        is_done = False
        while not is_done:
            moves = []
            for state in states:
                move = random.choice(list(range(7)))
                moves.append(move)
            states, rewards, is_done, info = env.step(moves)
            for reward in rewards:
                assert reward in possible_rewards
            check_states_multi(states)
        assert is_done


def test_render_single():
    env = gym.make("Farmworld-v0")
    env.reset()
    env.render()
    del env


# def test_render_multi():
#     env = gym.make("Farmworld-v1")
#     env.reset()
#     env.render()
#     del env
# 

def test_env_v0():
    run_single_agent_env(0)


# def test_env_v1():
#     run_multi_agent_env(1)
# 
# 
# def test_env_v2():
#     run_single_agent_env(2)
# 
# def test_env_v3():
#     run_multi_agent_env(3)
