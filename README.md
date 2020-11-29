# Gym-Cabworld

Reinforcement Environment based an OpenGymAI and Pygame. 
A cab is driving around and tries to pick-up passengers to drive them to their destination.
Each passenger is marked with the same color as his destination

![Cabworld](demo.gif)

## Installation 

```bash
git clone https://gitlab.com/nlimbrun/cabworld.git
cd gym-cabworld
pip install -r requirements.txt
pip install -e .
```

## Usage
### Single agent
```python
import gym 
import gym_cabworld 
env = gym.make('Cabworld-v0')
env.reset()
action = env.action_space.sample()
env.step(action)
env.render()
```
### Multi agent 
```python
import gym 
import gym_cabworld 
env = gym.make('Cabworld-v3')
env.reset()
actions = [0,1]
env.step(actions)
env.render()
```

## Training Template
```bash
python training_template.py -a dqn -n 100
python training_template.py -a sarsa -n 100 -e 0.5 -de 0.99
python training_template.py -a q -n 100 -e 0.5 -de 0.99 -r True -d True
```
### Flags 
#### Required 
-a / --algorithm Algorithm to run (q, dqn, ac, sarsa) <br/>
-n / --number Number of episodes to run <br/>
#### Optional
-lr / --learningrate Learning rate to train the network <br/>
-e / --epsilon Epsilon for epsilon greedy <br/>
-de / --decay Epsilon decay <br/>
-g / --gamma Gamma (discount) <br/>
-d / --display True: display game, False: use virtual display <br/>
-r / --render Render last episode <br/>
-s / --save Save model <br/>
-l / --load Load model <br/>

### Note 
**To use a virtual display (--display False) you have to install xvfb. Only tested on Linux (Pop-os 20.04)**

## Problem Statement
### 1. Environment description

1. The Map has 1000 x 1000 pixels but actions are limited to 25x25
2. The cab can only perform discrete actions
* 0: drive forward (40px)
* 1: turn right (90 deg)
* 2: turn left (90 deg)
* 3: pick-up passenger
* 4: drop-off passenger
3. Rewards / Penalties
* Pick-up-reward: 10000 
* Drop-off-reward: 10000
* Step-penality: -10
* Wrong pick-up/drop-off penality: -100
* Illegal move penalty: -500

### 2. Initial conditions

### Cabworld-v0
1. Cab starting at the top-left-corner
2. Passenger starting at bottom-right-corner 
3. Passenger wants to get to the top-left corner 

### Cabworld-v1
1. Cab starting at the top-left-corner
2. 3 Passengers with random start-position and random destination

### Cabworld-v2
1. Cab starting at the random position
2. 3 Passengers with random start-position and random destination

### Cabworld-v3 (Multi-Agent)
1. 2 Cabs starting at the random position
2. 3 Passengers with random start-position and random destination

### 3. Expected behaviour
1. Cab picks up passenger as fast as possible 
2. Cab brings passenger to their destination as fast as possible
3. Cab drops off passenger at their destination


## Tensorboard 
Use Tensorboard to compare different algorithms and tune hyperparameters
```bash 
tensorboard --logdir=runs
```
http://localhost:6006/

## Changelog

### [0.7] (https://gitlab.com/nlimbrun/cabworld/-/tags/release_0.7) (29.11.2020)
- Extend to multi-agent, register different versions (v0, v1, v2, v3)

### [0.6] (https://gitlab.com/nlimbrun/cabworld/-/tags/release_0.6) (28.11.2020)
- Refactoring, Added State-Deck, Training-template with argparse

### [0.5] (https://gitlab.com/nlimbrun/cabworld/-/tags/release_0.5) (22.11.2020)
- Refactoring, Added Tensorboard, Include images in pip-package

### [0.4] (https://gitlab.com/nlimbrun/cabworld/-/tags/release_0.4) (22.11.2020)
- Tensorboard to compare different trainings, new features in NN, random positions

### [0.3] (https://gitlab.com/nlimbrun/cabworld/-/tags/release_0.3) (10.11.2020)
- Improved reward system, notebook to generate maps, q-learning approach

### [0.2] (https://gitlab.com/nlimbrun/cabworld/-/tags/release_0.2) (07.11.2020)
- Added actions for pick-up, drop-off and simple reward system

### [0.1] (https://gitlab.com/nlimbrun/cabworld/-/tags/release_0.1) (04.11.2020)
- Basic world with cabs and passenger (without reward system)s