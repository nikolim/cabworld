import os
import torch
import torch.nn as nn
import torch.nn.functional as F


class ActorCriticModel(nn.Module):
    def __init__(self, n_input, n_output, n_hidden):
        super(ActorCriticModel, self).__init__()
        self.fc1 = nn.Linear(n_input, n_hidden)
        self.action = nn.Linear(n_hidden, n_output)
        self.value = nn.Linear(n_hidden, 1)

    def forward(self, x):
        x = torch.Tensor(x)
        x = F.relu(self.fc1(x))
        action_probs = F.softmax(self.action(x), dim=-1)
        state_values = self.value(x)
        return action_probs, state_values


class PolicyNetwork:
    def __init__(self, n_state, n_action, n_hidden, lr, writer):
        self.model = ActorCriticModel(n_state, n_action, n_hidden)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr)
        self.scheduler = torch.optim.lr_scheduler.StepLR(
            self.optimizer, step_size=10, gamma=0.9)
        self.writer = writer
        writer.add_graph(self.model, torch.ones(n_state))

    def normalise_state(self, s):
        """
        Transform state into features [-1,1]
        @param s: state to transform 
        @return normalised state 
        """
        state = list(s)
        features = []
        for i in range(5):
            if state[i] == 1:
                features.append(1)
            else:
                features.append(-1)
        for j in range(5, 12):
            if j == 7:
                features.append(state[7] / 180 - 1)
            else:
                features.append(state[j] / 480 - 1)
        return torch.Tensor(features)

    def predict(self, s):
        """
        Compute the output using the Actor Critic model
        @param s: input state
        @return: action probabilities, state_value
        """
        return self.model(self.normalise_state(s))

    def update(self, returns, log_probs, state_values, episode):
        """
        Update the weights of the Actor Critic network given the training samples
        @param returns: return (cumulative rewards) for each step in an episode
        @param log_probs: log probability for each step
        @param state_values: state-value for each step
        @param episode: number of current episode for the tensorboard-writer
        """
        loss = 0
        for log_prob, value, Gt in zip(log_probs, state_values, returns):
            advantage = Gt - value.item()
            policy_loss = -log_prob * advantage
            value_loss = F.smooth_l1_loss(value, Gt)
            loss += policy_loss + value_loss

        self.writer.add_scalar('Training Loss', loss, episode)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def get_action(self, s):
        """
        Estimate the policy and sample an action, compute its log probability
        @param s: input state
        @return: the selected action, log probability, predicted state-value
        """
        action_probs, state_value = self.predict(s)
        action = torch.multinomial(action_probs, 1).item()
        log_prob = torch.log(action_probs[action])
        return action, log_prob, state_value

    def save_models(self, PATH='../checkpoints/ac_checkpoint.tar'):
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

    def load_models(self, PATH='../checkpoints/ac_checkpoint.tar'):
        try:
            checkpoint = torch.load(PATH)
            self.models.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            print("Loaded checkpoint")
        except:
            print("Could not load checkpoint")
