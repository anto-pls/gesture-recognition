# -*- coding: utf-8 -*-
"""Gesture recognition.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cMLue3EkR0VtsHf3PsFePJpX8XD47Kdp
"""

import numpy as np
import pandas as pd
import string
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import matplotlib.pyplot as plt

train_csv = pd.read_csv('./data/sign_mnist_train.csv', sep=",")
test_csv = pd.read_csv('./data/sign_mnist_test.csv', sep=",")

train_labels = train_csv['label']
train_csv.drop('label', axis=1, inplace=True)

test_labels = test_csv['label']
test_csv.drop('label', axis=1, inplace=True)

train_data = train_csv.values
train_labels = train_labels.values

test_data = test_csv.values
test_labels = test_labels.values

def reshape_2d(data,dim):
    reshaped = []
    for i in data:
        reshaped.append(i.reshape(1,dim,dim))

    return np.array(reshaped)

train_data = reshape_2d(train_data,28)
test_data = reshape_2d(test_data,28)

train_data = torch.FloatTensor(train_data)
train_labels = torch.LongTensor(train_labels.tolist())

test_data = torch.FloatTensor(train_data)
test_labels = torch.LongTensor(train_labels.tolist())

Alph_labels = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I',
        10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
        18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y' }

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels= 10, kernel_size = 3),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2, stride = 2)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(10, 20, 3),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(20, 30, 3),
            nn.ReLU(),
            nn.Dropout2d()
        )

        self.fc = nn.Sequential(
            nn.Linear(270, 270),
            nn.ReLU(),
            nn.Linear(270, 26),
            nn.ReLU(),

        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        self.softmax = nn.LogSoftmax(dim=1)
        #return x

        return self.softmax(x)

model = CNN()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#device = "cpu"
model.to(device)

test_data, test_labels = test_data.to(device), test_labels.to(device)
train_data, train_labels = train_data.to(device), train_labels.to(device)

random_data = torch.rand((1, 1, 28, 28))

my_nn = CNN()
result = my_nn(random_data)
print (result)

epochs = 100
batch_size = 100
learning_rate = 0.001

optimizer = optim.SGD(model.parameters(), learning_rate, momentum=0.7)
loss_fn = nn.CrossEntropyLoss()

loss_log = []
acc_log = []

for e in range(epochs):
    for i in range(0, train_data.shape[0], batch_size):
        train = train_data[i:i + batch_size]
        labels = train_labels[i:i + batch_size]



        pred = model(Variable(train))
        loss = loss_fn(pred, Variable(labels))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if i % 100 == 0:
            #pred = net(Variable(test_data_formated))
            loss_log.append(loss.item())
            #acc_log.append(model.evaluate(torch.max(model(Variable(test_x[:500])).data, 1)[1], test_y[:500]))

    #print('Epoch: {} - Loss: {:.6f}'.format(e + 1, loss.item()))

sample = 4
pixels = test_data[sample].reshape(28, 28)

label = test_labels[sample]
test_sample = torch.FloatTensor([test_data[sample].reshape(1, 28, 28).tolist()])
test_var_sample = Variable(test_sample).to(device)
net_out_sample = model(test_var_sample)

plt.imshow(test_data[sample].reshape(28, 28))
plt.xlabel(f"Prediction:{np.argmax(net_out_sample.detach().cpu().numpy())}, Actual Value:{test_labels[sample]}") # Convert net_out_sample to NumPy array
plt.show()

