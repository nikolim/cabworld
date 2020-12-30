import random
import pytest
import time
import gym

import gym_cabworld

from pyvirtualdisplay import Display

disp = Display().start()
possible_rewards = [-1, -5, -10, 100]


def check_states_static(state):
    assert len(state) == 19
    for k in range(0, 5):
        assert state[k] == 1 or state[k] == -1
    for i in range(5, len(state)):
        assert state[i] == -1 or 0 <= state[i] <= 1


def check_states_dynamic(state):
    assert len(state) == 19
    for k in range(0, 5):
        assert state[k] == 1 or state[k] == -1
    for i in range(5, len(state)):
        assert state[i] == -1 or 0 <= state[i] <= 1


def check_states_multi(states):
    for state in states:
        assert len(state) == 19
        for k in range(0, 5):
            assert state[k] == 1 or state[k] == -1
        for i in range(5, len(state)):
            assert state[i] == -1 or 0 <= state[i] <= 1


def run_single_agent_env(version):
    assert (
        str(version) == "0"
        or str(version) == "1"
        or str(version) == "2"
        or str(version) == "4"
        or str(version) == "5"
        or str(version) == "6"
    )
    env = gym.make("Cabworld-v" + str(version))
    n_episodes = 10
    for episode in range(n_episodes):
        state = env.reset()
        is_done = False
        while not is_done:
            move = random.choice(list(range(7)))
            states, rewards, is_done, info = env.step(move)
            assert rewards in possible_rewards
            if version in [0, 4]:
                check_states_static(states)
            else:
                check_states_dynamic(states)
        assert is_done


def run_multi_agent_env(version):
    assert version == 3 or version == 7
    env = gym.make("Cabworld-v" + str(version))
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


def test_env_v0():
    run_single_agent_env(0)


def test_env_v1():
    run_single_agent_env(1)


def test_env_v2():
    run_single_agent_env(2)


def test_env_v3():
    run_multi_agent_env(3)


def test_env_v4():
    run_single_agent_env(4)


def test_env_v5():
    run_single_agent_env(5)


def test_env_v6():
    run_single_agent_env(6)


def test_env_v7():
    run_multi_agent_env(7)
