# Gym-Cabworld

Reinforcement Environment based an OpenGymAI and Pygame. 
A cab is driving around and tries to pick-up passengers to drive them to their destination.

![Cabworld](demo.gif)

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
## Changelog

### [0.1] (https://gitlab.com/nlimbrun/cabworld/-/tags/release_0.1) (04.11.2020)
- Basic world with cabs and passenger (without reward system)s