import os

import torch
import torch.nn as nn


class Cnn(object):

    def __init__(self):
        self.device = torch.device("cpu")
        self.x = None
        self.conv_net2 = nn.Sequential(
            nn.Conv2d(1, 32, (3, 3)),  # 28x28x1 -> 26x26x32
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.AvgPool2d(2),  # 26x26x32 -> 13x13x32
            nn.Conv2d(32, 64, (3, 3)),  # 13x13x32 -> 11x11x64
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.AvgPool2d(2),  # 11x11x64 -> 5x5x64
            nn.Conv2d(64, 128, (3, 3)),  # 5x5x64 -> 3x3x128
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.AvgPool2d(2, stride=1),  # 3x3x128 -> 2x2x128
            nn.Flatten(),
            nn.Linear(2 * 2 * 128, 256),
            nn.ReLU(),
            nn.Linear(256, 10)
        )
        self.conv_net2.apply(self.init_weights)
        self.conv_net2.to(self.device)
        self.conv_net2.load_state_dict(
            torch.load(os.getcwd() + "/ai/mnist_cnn.pt", map_location=lambda storage, loc: storage)
        )
        self.conv_net2 = self.conv_net2.eval()

    @staticmethod
    def init_weights(m):  # He's initialization
        if type(m) == nn.Linear or type(m) == nn.Conv2d:
            torch.nn.init.kaiming_normal_(m.weight)
            m.bias.data.fill_(0.0)

    def data_load(self, image):
        self.x = image.to(self.device)

    def predict(self):
        y = self.conv_net2.forward(self.x)
        pred = y.argmax(1).tolist()

        return pred[0]
