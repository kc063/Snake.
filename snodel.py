import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import snakegame_AUTO as ssss
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name = 'crumbexistentialdread.pth'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        #if(GameMode == GameMode.FEAR):
          # file_name= 'crumbexistentialdread.pth'
        #if(GameMode == GameMode.NORMAL):
        #   file_name = 'model.pth'
        #if(GameMode == GameMode.CRUMB):
        #   file_name = 'crumbeater.pth'
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer: 
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype = torch.float)
        next_state = torch.tensor(next_state, dtype = torch.float)
        action = torch.tensor(action, dtype = torch.float)
        reward = torch.tensor(reward, dtype = torch.float)
        if len(state.shape) == 1:
            #we want in form 1, value
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )
        
        #time to implement the the 
        #1. predicted Q value w current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            target[idx][torch.argmax(action[idx]).item()] = Q_new

        #2 r + y * max(next_predicted Q)
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
