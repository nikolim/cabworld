import torch
from torch.autograd import Variable
import math
import gym
import gym_cabworld
from torch.utils.tensorboard import SummaryWriter


class Estimator():
    def __init__(self, n_feat, n_state, n_action, n_hidden, lr, writer):
        """
        Crete Estimator with neuronal net for each action
        @param n_feat: number of features
        @param n_state: number of states in evironment
        @param n_action: number of actions in environment
        @param n_hidden: number of hidden neurons
        @param lr: learning rate
        @param writer: writer for tensorboard
        """
        # self.w, self.b = self.get_gaussian_wb(n_feat, n_state)
        self.n_feat = n_feat
        self.models = []
        self.optimizers = []
        self.criterion = torch.nn.MSELoss()
        self.writer = writer

        self.n_updates = 0
        self.total_loss = 0

        for _ in range(n_action):
            model = torch.nn.Sequential(
                torch.nn.Linear(int(n_feat), int(n_feat*3)),
                torch.nn.ReLU(),
                torch.nn.Linear(int(n_feat*3), int(n_hidden)),
                torch.nn.ReLU(),
                torch.nn.Linear(int(n_hidden), 1)
            )
            self.models.append(model)
            optimizer = torch.optim.Adam(model.parameters(), lr)
            self.optimizers.append(optimizer)

        # add graph to tensorboard
        writer.add_graph(self.models[0], torch.ones(n_feat))

    def get_gaussian_wb(self, n_feat, n_state, sigma=.2):
        """
        Create initial weights
        @param: n_feat: number of features 
        @param: n_number: number of states
        @return w,b: weights, bias
        """
        torch.manual_seed(0)
        w = torch.randn((n_state, n_feat)) * 1.0 / sigma
        b = torch.rand(n_feat) * 2.0 * math.pi
        return w, b

    def get_feature(self, s):
        """
        Transform state into features [-1,1]
        @param s: state to transform 
        @return features 
        """
        state = list(s)
        features = []
        for i in range(5):
            if state[i] == 1: 
                features.append(1)
            else: 
                features.append(-1)
        for j in range(5,12):
            if j == 7: 
                features.append(state[7] / 180 - 1)
            else:
                features.append(state[j] / 480 - 1)
        return torch.Tensor(features)

    def update(self, s, a, y, episode):
        """
        Train estimator with target value
        @param s: state 
        @param a: action
        @param y: target value
        """
        features = Variable(self.get_feature(s))
        y_pred = self.models[a](features)
        loss = self.criterion(y_pred, Variable(torch.Tensor([y])))
        self.optimizers[a].zero_grad()
        loss.backward()
        self.optimizers[a].step()

        self.n_updates += 1
        self.total_loss += loss.item()
        median_loss = self.total_loss / self.n_updates
        self.writer.add_scalar('Training Loss', median_loss, episode)

    def predict(self, s):
        """
        Predict to q-values for a given state
        @param s: state to predict the q-values for
        """
        features = self.get_feature(s)
        with torch.no_grad():
            return torch.tensor([model(features) for model in self.models])

    def save_models(self, PATH='checkpoints/q_learning_ckpnt.tar'):
        """
        Save all estimators and optimizers in one file
        @param PATH: where to save to models
        """
        model_opt_dict = {}
        for i, model in enumerate(self.models, start=0):
            model_name = f'model{i}_state_dict'
            model_opt_dict[model_name] = model.state_dict()
        for j, optimizer in enumerate(self.optimizers, start=0):
            optimizer_name = f'optimizer{j}_state_dict'
            model_opt_dict[optimizer_name] = optimizer.state_dict()
        try:
            torch.save(model_opt_dict, PATH)
        except:
            print("Could not save checkpoint")
        self.writer.close()

    def load_models(self, PATH='checkpoints/q_learning_ckpnt.tar'):
        """
        Load all estimators and optimizers from one file
        @param PATH: where to load the models from 
        """
        try:
            checkpoint = torch.load(PATH)
            for i in range(len(self.models)):
                self.models[i].load_state_dict(
                    checkpoint[f'model{i}_state_dict'])
                self.optimizers[i].load_state_dict(
                    checkpoint[f'optimizer{i}_state_dict'])
            print("Loaded checkpoint")
        except:
            print("Could not load checkpoint")
