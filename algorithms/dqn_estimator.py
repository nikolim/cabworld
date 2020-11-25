
import gym
import torch

from collections import deque
import random

from torch.autograd import Variable

class DQN():
    def __init__(self, n_state, n_action, n_hidden, lr, writer):
        self.criterion = torch.nn.MSELoss()
        self.model = torch.nn.Sequential(
                        torch.nn.Linear(n_state, n_hidden),
                        torch.nn.ReLU(),
                        torch.nn.Linear(n_hidden, n_action)
                )
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr)
        writer.add_graph(self.model, torch.ones(n_state))

    def update(self, s, y, episode):
        """
        Update the weights of the DQN given a training sample
        @param s: state
        @param y: target value
        """
        y_pred = self.model(torch.Tensor(s))
        loss = self.criterion(y_pred, Variable(torch.Tensor(y)))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.writer.add_scalar('Training Loss', loss, episode)

    def predict(self, s):
        """
        Compute the Q values of the state for all actions using the learning model
        @param s: input state
        @return: Q values of the state for all actions
        """
        with torch.no_grad():
            return self.model(torch.Tensor(s))


    def replay(self, memory, replay_size, gamma):
        """
        Experience replay
        @param memory: a list of experience
        @param replay_size: the number of samples we use to update the model each time
        @param gamma: the discount factor
        """
        if len(memory) >= replay_size:
            replay_data = random.sample(memory, replay_size)
            states = []
            td_targets = []
            for state, action, next_state, reward, is_done in replay_data:
                states.append(state)
                q_values = self.predict(state).tolist()
                if is_done:
                    q_values[action] = reward
                else:
                    q_values_next = self.predict(next_state)
                    q_values[action] = reward + gamma * torch.max(q_values_next).item()
                td_targets.append(q_values)
            self.update(states, td_targets)

    def save_models(self, PATH='../checkpoints/dqn_checkpoint.tar'):
        if not os.path.exists('../checkpoints'):
            os.mkdir('../checkpoints')

        model_opt_dict = {}
        model_name = 'model_state_dict'
        optimizer_name = 'optimizer_state_dict'
        model_opt_dict[model_name] = self.model.state_dict()
        model_opt_dict[optimizer_name] = self.optimizer.state_dict()
        try:
            torch.save(model_opt_dict, PATH)
            print("Saved checkpoint")
        except:
            print("Could not save checkpoint")
        self.writer.close()

    def load_models(self, PATH='../checkpoints/dqn_checkpoint.tar'):

        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, PATH)
        print(path)
        try:
            checkpoint = torch.load(path)
            self.models.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            print("Loaded checkpoint")
        except:
            print("Could not load checkpoint")
