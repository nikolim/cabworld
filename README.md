# Gym-Cabworld

Reinforcement Environment based an OpenGymAI and Pygame. 
A cab is driving around tries to pick-up passenger to drive them to their destination.

![Cabworld](images/cabworld.png)

## Installation 

```bash
git clone https://gitlab.com/nlimbrun/cabworld.git
cd gym-cabworld
pip install -r requirements.txt
pip install -e .
```

## Usage

```python
import gym 
import gym_cabworld 
env = gym.make('Cabworld-v0')
env.reset()
action = env.action_space.sample()
env.step(action)
env.render()
```