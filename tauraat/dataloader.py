import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupShuffleSplit

class ToTensor:
    def __call__(self, sample):
        inputs, targets = sample
        return torch.from_numpy(inputs), torch.from_numpy(targets)

class HYDRoSWOT(Dataset):

    def __init__(self, split='train', transform=None):

        train = pd.read_csv('./data/HYDRoSWOT_subset_train.csv', converters={'site_no': str}, low_memory=False)

        # validation split 10% of the total dataset (12.5% of training set)
        splitter = GroupShuffleSplit(test_size=0.125, n_splits=1, random_state=7)
        train_val_split = splitter.split(train, groups=train['site_no'])
        train_idx, val_idx = next(train_val_split)

        X_train = train.drop(columns=['site_no', 'site_tp_cd', 'stream_wdth_va', 'mean_depth_va'])
        y_train = train[['stream_wdth_va']]

        # Data Transformation
        X_train['drain_area_va'] = np.log10(X_train['drain_area_va'])
        X_train['q_va'] = np.log10(X_train['q_va'])
        X_train['xsec_area_va'] = np.log10(X_train['xsec_area_va'])
        y_train = np.log10(y_train)

        X_scaler = StandardScaler()
        X_train = X_scaler.fit_transform(X_train)

        y_scaler = StandardScaler()
        y_train = y_scaler.fit_transform(y_train.to_numpy().reshape(-1, 1))

        self.X_scaler = X_scaler
        self.y_scaler = y_scaler

        if split == 'train':
            self.X = X_train[train_idx].astype('float32')
            self.y = y_train[train_idx].astype('float32')

        elif split == 'val':
            self.X = X_train[val_idx].astype('float32')
            self.y = y_train[val_idx].astype('float32')

        else: # i.e., if split == 'test':

            test = pd.read_csv('./data/HYDRoSWOT_subset_test.csv', converters={'site_no': str}, low_memory=False)

            X_test = test.drop(columns=['site_no', 'site_tp_cd', 'stream_wdth_va', 'mean_depth_va'])
            y_test = test[['stream_wdth_va']]

            X_test['drain_area_va'] = np.log10(X_test['drain_area_va'])
            X_test['q_va'] = np.log10(X_test['q_va'])
            X_test['xsec_area_va'] = np.log10(X_test['xsec_area_va'])

            self.X = self.X_scaler.transform(X_test).astype('float32')
            self.y = y_test.to_numpy('float32').reshape(-1, 1)

        self.transform = transform

    def __getitem__(self, index):
        sample = self.X[index], self.y[index]

        if self.transform:
            sample = self.transform(sample)

        return sample

    def __len__(self):
        return len(self.X)


if __name__ == "__main__":
    dataset = HYDRoSWOT(split='train', transform=ToTensor())

    print(len(dataset))
    dataiter = iter(dataset)
    X, y = next(dataiter)
    print(X.shape, y.shape)

