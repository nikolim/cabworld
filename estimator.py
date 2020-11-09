import torch
from torch.autograd import Variable
import math
import gym
import gym_cabworld

class Estimator():
    def __init__(self, n_feat, n_state, n_action, n_hidden=50, lr=0.05):
        self.w, self.b = self.get_gaussian_wb(n_feat, n_state)
        self.n_feat = n_feat
        self.models = []
        self.optimizers = []
        self.criterion = torch.nn.MSELoss()

        for _ in range(n_action):
            model = torch.nn.Sequential(
                torch.nn.Linear(int(n_feat), int(n_feat/2)),
                torch.nn.ReLU(),
                torch.nn.Linear(int(n_feat/2), int(n_hidden)),
                torch.nn.ReLU(),
                torch.nn.Linear(int(n_hidden), 1)
            )
            self.models.append(model)
            optimizer = torch.optim.Adam(model.parameters(), lr)
            self.optimizers.append(optimizer)

    def get_gaussian_wb(self, n_feat, n_state, sigma=.2):
        torch.manual_seed(0)
        w = torch.randn((n_state, n_feat)) * 1.0 / sigma
        b = torch.rand(n_feat) * 2.0 * math.pi
        return w, b

    def get_feature(self, s):
        features = (2.0 / self.n_feat) ** .5 * torch.cos(
            torch.matmul(torch.tensor(s).float(), self.w) + self.b)
        return features

    def update(self, s, a, y):
        features = Variable(self.get_feature(s))
        y_pred = self.models[a](features)
        loss = self.criterion(y_pred, Variable(torch.Tensor([y])))
        self.optimizers[a].zero_grad()
        loss.backward()
        self.optimizers[a].step()

    def predict(self, s):
        features = self.get_feature(s)
        with torch.no_grad():
            return torch.tensor([model(features) for model in self.models])

    def save_models(self, PATH='checkpoints/q_learning_ckpnt.tar'): 
        model_opt_dict = {}
        for i, model in enumerate(self.models, start=0): 
            model_name = f'model{i}_state_dict'
            model_opt_dict[model_name] = self.models[i].state_dict()
        for i, model in enumerate(self.optimizers, start=0): 
            optimizer_name = f'optimizer{i}_state_dict'
            model_opt_dict[model_name] = self.optimizers[i].state_dict()
        try:
            torch.save(model_opt_dict, PATH)
        except: 
            print("Could not save checkpoint") 

    def load_models(self, PATH='checkpoints/q_learning_ckpnt.tar'): 
        try:
            checkpoint = torch.load(PATH)
            for i in range(len(self.models)): 
                self.models[i].load_state_dict(checkpoint[f'model{i}_state_dict'])
                self.optimizers[i].load_state_dict(checkpoint[f'optimizer{i}_state_dict'])
        except: 
            print("Could not load checkpoint")
