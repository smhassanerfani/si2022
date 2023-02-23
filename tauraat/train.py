import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.backends.cudnn as cudnn
from dataloader import HYDRoSWOT, ToTensor
from torch.optim import lr_scheduler
import time
import os

from model import MLP
from utils import loss_decay_plot

def main():

    PATH = f'data/ml_weights/PyTorch'

    try:
        os.makedirs(PATH)
    except FileExistsError:
        pass

    cudnn.enabled = True
    cudnn.benchmark = True

    train_set = HYDRoSWOT(split='train', transform=ToTensor())
    val_set = HYDRoSWOT(split='val', transform=ToTensor())

    datasets = {'train': train_set, 'val': val_set}

    dataloaders = {x: DataLoader(datasets[x], batch_size=64, shuffle=True, num_workers=2,
                                 pin_memory=True, drop_last=False) for x in ['train', 'val']}

    model = MLP()
    model = model.cuda()

    # learning_rate = 2.5e-4
    # criterion = nn.MSELoss()
    # optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9, weight_decay=0.01)
    # scheduler = lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)
    
    learning_rate = 7.5e-5
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=0.001)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.8)

    # 3) Training loop
    num_epochs = 30
    loss_record = {'train': [], 'val': []}
    since = time.time()

    for epoch in range(num_epochs):

        for phase in ['train', 'val']:

            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            for X, y in dataloaders[phase]:

                X = X.cuda()
                y = y.reshape(-1, 1).cuda()

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):

                    y_pred = model(X)
                    loss = criterion(y_pred, y)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * X.size(0)

            if phase == 'train':
                scheduler.step()
                lr = optimizer.param_groups[0]['lr']

            epoch_loss = running_loss / len(dataloaders[phase].dataset)

            if (epoch + 1) % 1 == 0:
                print(f'epoch: {epoch + 1}, phase: {phase}, loss: {epoch_loss:.4f}, lr: {lr:.2E}')
                loss_record[phase].append(epoch_loss)

    time_elapsed = time.time() - since
    print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')

    state = {
        'epoch': num_epochs,
        'learning_rate': learning_rate,
        'model_state': model.state_dict(),
        'train_loss': loss_record['train'],
        'val_loss': loss_record['val']
        }
    torch.save(state, f'{PATH}/model.pth')

    loss_decay_plot(num_epochs, loss_record['train'], loss_record['val'])

if __name__ == '__main__':
    main()