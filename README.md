<div align="center">
		<img width="auto" height="200px" src="assets/icon.png">
</div>

<br/>
<div align="center">
	<a href="https://opensource.org/licenses/MIT">
		<img alt="License MIT" src="https://img.shields.io/badge/build-passing-success">
	</a>
	<a href="https://opensource.org/licenses/MIT">
		<img alt="License MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg">
	</a>
</div>

<p>
</p>

# Gym-Cabworld

Reinforcement Environment based an OpenGymAI and Pygame. 
A cab is driving around and tries to pick-up passengers in order to drive them to their destination. For each passenger the destination is marked on the map in the same color.
The environment has two different sizes (small and large) and respectively two modes (single and multi agent).

<br>
<p>
	<div align="center">
		<img width="auto" height="400px" src="assets/demo_small.gif" align="center">
	</div>
</p>
<br>


## Installation 

```bash
pip install gym-cabworld
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

## Problem Statement

The cab(s) should learn to chauffeur as many passengers as possible to their destination in a fixed number of time steps (1000).

### 1. Environment description
1. The Map has 8x8 grids for the small world (23x23 for the big world)
2. The cab can only perform discrete actions
* 0: drive up 
* 1: drive right 
* 2: drive down 
* 3: drive left 
* 4: pick-up passenger
* 5: drop-off passenger
* 6: do nothing 
3. Rewards / Penalties
* Pick-up-reward: 1 
* Drop-off-reward: 1
* Step-penality: -0.01
* Wrong pick-up/drop-off penality: -0.02
* Illegal move penalty: -0.02

### 2. Initial conditions

Note: with the help of jupyter notebooks a map of any size and with any street leading can be created.

### Cabworld-v0 (Single Agent)
1. Cab starting at random position
2. 1 Passenger with random start-position and random destination (respawn every 100 steps)

### Cabworld-v1 (Single Agent)
1. 2 Cabs starting at the random position
2. 2 Passengers with random start-position and random destination (respawn immediately)

### Cabworld-v2 (Multi-Agent)
1. 2 Cabs starting at random positions
2. 1 Passenger with random start-position and random destination (respawn every 50 steps)

### Cabworld-v3 (Multi-Agent)
1. 2 Cabs starting at the random position
2. 2 Passengers with random start-position and random destination (respawn immediatly)

### 3. Expected behaviour
1. Cab(s) pick(s) up passengers as fast as possible 
2. Cab(s) bring(s) passengers to their destination as fast as possible
3. Cab(s) drop(s) off passengers at their destination
4. Cab(s) do nothing if no passenger on map

### 4. State 

The state of every environment consists of 9 values (11 values for v1 and v3). 
* 1-4: radar-up, radar-right, radar-down, radar-left &#8712; {-1,1}
* 5: 1 if cab has passenger else 0
* 6-7: x-position, y-position of cab &#8712; [0;1]
* 8-9: x-position, y-position passenger &#8712; [0;1]
* (optional 10-11: x-position, y-position passenger)

* If cab picks up a passenger, its position is replaced with its destination

Notes: 
* Radar: 1 for street, -1 for terrain
* Positions are normalized [0,1]
* If currently there is no passengers on the map, values are filled with -1

## Test 
Run 10 episodes of each version with random policy and check if states and rewards are valid.
```bash 
pytest tests.py
```