import torch
import numpy as np
from torch.utils.data import DataLoader
import torch.backends.cudnn as cudnn
from dataloader import HYDRoSWOT, ToTensor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from model import MLP

def main(mode='test'):

    cudnn.enabled = True
    cudnn.benchmark = True

    if mode == 'train':
        dataset = HYDRoSWOT(split='train', transform=ToTensor())
        dataloader = DataLoader(dataset, batch_size=128, shuffle=False, num_workers=2, pin_memory=True, drop_last=False)

    elif mode == 'val':
        dataset = HYDRoSWOT(split='val', transform=ToTensor())
        dataloader = DataLoader(dataset, batch_size=128, shuffle=False, num_workers=2, pin_memory=True, drop_last=False)

    else:
        dataset = HYDRoSWOT(split='test', transform=ToTensor())
        dataloader = DataLoader(dataset, batch_size=128, shuffle=False, num_workers=2, pin_memory=True, drop_last=False)


    model = MLP(input_ftrs=4)
    model = model.cuda()

    FILE = f'data/ml_weights/PyTorch/230327-211707.pth'
    checkpoint = torch.load(FILE)
    model.load_state_dict(checkpoint['model_state'])

    y_gt_lst = []
    y_pr_lst = []
    model.eval()

    for idx, predictor in enumerate(dataset.predictors):
        with torch.no_grad():

            for X, y in dataloader:

                X[:, idx] = X[torch.randperm(X.size(0)), idx]
                X = X.cuda()

                y_pred = model(X)

                y = y.numpy()
                y_pred = y_pred.detach().cpu().numpy()

                y_gt_lst.append(y)
                y_pr_lst.append(y_pred)


        y_gt = np.concatenate(y_gt_lst).reshape(-1, 1)
        y_pr = np.concatenate(y_pr_lst).reshape(-1, 1)

        # if mode == 'train' or mode == 'val':
        #     y_gt = dataset.y_scaler.inverse_transform(y_gt)
        #     y_gt = 10 ** y_gt

        y_pr = dataset.y_scaler.inverse_transform(y_pr)
        y_pr = 10 ** y_pr

        print(f'Predictor: {predictor:<15s}',
              f'NSE: {r2_score(y_gt, y_pr):.4f}\t'
              f'RMSE: {mean_squared_error(y_gt, y_pr, squared=False):.4f}')


if __name__ == "__main__":
    main()