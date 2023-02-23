import torch
import torch.nn as nn


class MLP(nn.Module):
    def __init__(self, input_ftrs=5):
        super(MLP, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(in_features=input_ftrs, out_features=64),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(in_features=64, out_features=64),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(in_features=64, out_features=64),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(in_features=64, out_features=1)
        )

    def forward(self, x):
        x = self.encoder(x)
        return x


if __name__ == "__main__":

    model = MLP()

    X = torch.randn(2, 5)
    print(model(X))

