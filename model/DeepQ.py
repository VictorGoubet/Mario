#Inspired https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import random
from collections import deque, namedtuple
class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, n_layers = 2):
        super(DQN, self).__init__()
        self.layers = []
        self.layers.append(nn.Conv2d(input_size, hidden_size, 3, padding = 2))
        self.layers.append(nn.MaxPool2d(kernel_size=(3, 3), stride=(2, 2)))

        self.n_layers = n_layers

        for i in range(n_layers-1):
            self.layers.append(nn.Conv2d(hidden_size, hidden_size, 3, padding = 2))
            self.layers.append(nn.MaxPool2d(kernel_size=(3, 3), stride=(2, 2)))

        self.output = nn.Linear(hidden_size * 16 * 16, output_size) # 16x16 is the output of the last layer

    def forward(self, x):

        for i in range(0,self.n_layers,2):
            print(x.size())
            x = F.relu(self.layers[i](x))
            x = self.layers[i+1](x)
    
        print(x.size())
        x = nn.Flatten()(x)
        x = self.output(x)
        x.size()
        return x


class ReplayMemory:

    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)

    def push(self, el):
        """Save a transition"""
        self.memory.append(el)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class DeepQ:
    def __init__(self, gamma, epsilon, env, batch_size):
        self.gamma = gamma
        self.epsilon = epsilon
        self.env = env
        self.batch_size = batch_size

        self.n_action = env.n_action #FIXME: ADD REAL NAME
        self.n_state = env.n_state #FIXME: ADD REAL NAME

        self.Q = np.zeros((self.n_state, self.n_action)) #FIXME: Change to adaptable n state

        self.policy_net = DQN(1, 16, 3, n_layers = 2)
        self.target_net = DQN(1, 16, 3, n_layers = 2)

        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.RMSprop(self.policy_net.parameters())

        self.memory = ReplayMemory(10000)
        self.n_step = 0

        self.Observation = namedtuple('Observation', ['state', 'action', 'reward', 'next_state'])
        self.target_update = 10

    def choose_action(self, state):
        #epsilon greedy choice of action ??
        if random.random() < self.epsilon:
            return torch.Tensor([[random.randint(0, self.env.n_action - 1)]])
        else:
            with torch.no_grad():
                #We chose the action with the highest expected reward
                return self.policy_net(state).max(1)[1].view(1, 1)


    def update_model(self):
        if len(self.memory) < self.batch_size:
            return
        else:
            #We sample a batch of observations
            obs = self.memory.sample(self.batch_size)
            batch = self.Observation(*zip(*obs))

            #We keep only the non terminal states
            non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), dtype=torch.bool)
            non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

            #We convert concatenates the tensors
            state_batch = torch.cat(batch.state)
            action_batch = torch.cat(batch.action)
            reward_batch = torch.cat(batch.reward)

            # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
            # columns of actions taken. These are the actions which would've been taken
            # for each batch state according to policy_net

            state_action_values = self.policy_net(state_batch).gather(1, action_batch)

            # Compute V(s_{t+1}) for all next states.
            # Expected values of actions for non_final_next_states are computed based
            # on the "older" target_net; selecting their best reward with max(1)[0].
            # This is merged based on the mask, such that we'll have either the expected

            # state value or 0 in case the state was final.
            next_state_values = torch.zeros(self.batch_size)
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()

            #Then the expected Q_value (formula)
            expected_state_action_values = (next_state_values * self.gamma) + reward_batch

            # Compute Huber loss
            criterion = nn.SmoothL1Loss()
            loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

            # Optimize the model
            self.optimizer.zero_grad()
            loss.backward()
            for param in self.policy_net.parameters():
                param.grad.data.clamp_(-1, 1)
            self.optimizer.step()

    #ADD RENDER
    def train(self, num_episode):
        for i in range(num_episode):
            #Initialisation
            state = self.env.reset()
            state = self.env.get_screen() #FIXME: ADD REAL NAME
            #last_screen = self.env.get_screen() #FIXME: ADD REAL NAME
            #They are compared in the tutorial ? Why ? Applicable ? 

            #We play until the end of the episode
            t = 0
            while True:
                #Select the action
                action = self.choose_action(state)
                #perform the action
                next_state, reward, done, _ = self.env.step(action) #FIXME: ADD REAL NAME
                if done:
                    next_state = None
                #We save the observation
                self.memory.push(self.Observation(state, action, reward, next_state))

                #We move to the next state
                state = next_state

                #We update the model
                self.update_model()

                if done:
                    break

                if i % self.target_update == 0:
                    self.target_net.load_state_dict(self.policy_net.state_dict())


        

if __name__ == '__main__':
    print('ok')
    '''test_tensor = torch.randn(1, 1, 64, 64)
    model = DeepModel(1, 16, 3, n_layers = 4)
    result = model.forward(test_tensor)
    print(result)
    print(result.size())'''


 

