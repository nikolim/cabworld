import random
import pytest
import time
import gym

import gym_cabworld

from pyvirtualdisplay import Display

disp = Display().start()


def test_states_v0():
    env = gym.make("Cabworld-v0")
    state = env.reset()
    assert len(state) == 19
    for k in range(0, 5):
        assert state[k] == 1 or state[k] == -1
    for j in range(5, 11):
        assert 0 <= state[j] <= 1
    for i in range(11, len(state)):
        assert state[i] == -1


def test_states_v1():
    env = gym.make("Cabworld-v1")
    state = env.reset()
    assert len(state) == 19
    for k in range(0, 5):
        assert state[k] == 1 or state[k] == -1
    for i in range(5, len(state)):
        assert 0 <= state[i] <= 1


def test_states_v2():
    env = gym.make("Cabworld-v2")
    state = env.reset()
    assert len(state) == 19
    for k in range(0, 5):
        assert state[k] == 1 or state[k] == -1
    for i in range(5, len(state)):
        assert 0 <= state[i] <= 1


def test_states_v3():
    env = gym.make("Cabworld-v3")
    states = env.reset()
    for state in states:
        assert len(state) == 19
        for k in range(0, 5):
            assert state[k] == 1 or state[k] == -1
        for i in range(5, len(state)):
            assert 0 <= state[i] <= 1


def test_states_v4():
    env = gym.make("Cabworld-v4")
    state = env.reset()
    assert len(state) == 19
    for k in range(0, 5):
        assert state[k] == 1 or state[k] == -1
    for j in range(5, 11):
        assert 0 <= state[j] <= 1
    for i in range(11, len(state)):
        assert state[i] == -1


def test_states_v5():
    env = gym.make("Cabworld-v5")
    state = env.reset()
    assert len(state) == 19
    for k in range(0, 5):
        assert state[k] == 1 or state[k] == -1
    for i in range(5, len(state)):
        assert 0 <= state[i] <= 1


def test_states_v6():
    env = gym.make("Cabworld-v6")
    state = env.reset()
    assert len(state) == 19
    for k in range(0, 5):
        assert state[k] == 1 or state[k] == -1
    for i in range(5, len(state)):
        assert 0 <= state[i] <= 1


def test_states_v7():
    env = gym.make("Cabworld-v7")
    states = env.reset()
    for state in states:
        assert len(state) == 19
        for k in range(0, 5):
            assert state[k] == 1 or state[k] == -1
        for i in range(5, len(state)):
            assert 0 <= state[i] <= 1


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
                legal_actions = [
                    s for s, a in zip(list(range(5)), allowed_actions) if a == 1
                ]
                move = random.choice(legal_actions)
            states, rewards, is_done, info = env.step(move)
        assert is_done


def run_multi_agent_env(version):
    assert version == 3 or version == 7
    env = gym.make("Cabworld-v" + str(version))
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
                    legal_actions = [
                        s for s, a in zip(list(range(5)), allowed_actions) if a == 1
                    ]
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
