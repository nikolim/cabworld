import random
import pytest
import time
import gym

import gym_cabworld

from pyvirtualdisplay import Display
disp = Display().start()


def run_single_agent_env(version):
    assert str(version) == '0' or str(version) == '1' or str(version) == '2' or str(
        version) == '4' or str(version) == '5' or str(version) == '6'
    env = gym.make('Cabworld-v' + str(version))
    n_episodes = 25
    for episode in range(n_episodes):
        state = env.reset()
        is_done = False
        while not is_done:
            allowed_actions = state[:5]
            if allowed_actions[3] == 1:
                move = 3
            elif allowed_actions[4] == 1:
                move = 4
            else:
                legal_actions = [s for s, a in zip(
                    list(range(5)), allowed_actions) if a == 1]
                move = random.choice(legal_actions)
            states, rewards, is_done, info = env.step(move)
        assert is_done


def run_multi_agent_env(version):
    assert(version == 3 or version == 7)
    env = gym.make('Cabworld-v' + str(version))
    n_episodes = 25
    for episode in range(n_episodes):
        states = env.reset()
        is_done = False
        while not is_done:
            moves = []
            for state in states:
                allowed_actions = state[:5]
                if allowed_actions[3] == 1:
                    move = 3
                elif allowed_actions[4] == 1:
                    move = 4
                else:
                    legal_actions = [s for s, a in zip(
                        list(range(5)), allowed_actions) if a == 1]
                    if len(legal_actions) == 0:
                        env.render()
                        import time
                        time.sleep(10)
                    move = random.choice(legal_actions)
                moves.append(move)
            states, rewards, is_done, info = env.step(moves)
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
