# Gym-Cabworld

Reinforcement Environment based an OpenGymAI and Pygame

# Installation 

pip install -e .

# Import 

```python
import gym 
import gym_cabworld 
env = gym.make('Cabworld-v0')
action = env.action_space.sample()
env.step(action)
env.step(action)
```