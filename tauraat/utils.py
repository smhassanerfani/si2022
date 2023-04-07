import numbers
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style = 'darkgrid')

plt.rcParams.update({
    # 'font.sans-serif': 'Comic Sans MS',
    'font.family': 'serif'
})
def scatter_plot(y_test, y_pred, xax2_name='GT', yax2_name='MODEL', model_name=None):


    y_test = np.array(y_test).reshape(-1,)
    y_pred = np.array(y_pred).reshape(-1,)
    print(f'test size: {y_test.shape}, pred size: {y_pred.shape}')

    r2 = np.corrcoef(y_pred, y_test)[0, 1]**2
    pbias = 100 * np.sum((y_pred - y_test)) / np.sum(y_test)
    nse = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred, squared=False)
    print(f'NSE: {nse:.4f}, R2: {r2:.4f}, PBias: {pbias:.4f}, RMSE: {mse:.4f}')

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 6), constrained_layout=True)

    # err = (y_test - y_pred)
    # ax1.violinplot(err, positions=None, vert=True, widths=1.0, showmeans=True,
    #                showextrema=True, showmedians=False, quantiles=None, points=100,
    #                bw_method=None, data=None)
    #
    # ax1.set_title(f'Error Distribution (STD: {np.std(err):.4f})')

    ax1.boxplot([y_test, y_pred])
    ax1.set_xticklabels([xax2_name, yax2_name])
    ax1.tick_params(axis='x', labelrotation=0, labelsize=16)
    ax1.grid(True)
    # ax1.set_title(f'BOX PLOT')

    max_value = np.array((y_test, y_pred)).max()

    ax2.scatter(y_test, y_pred, color='teal', edgecolor='steelblue', alpha=0.5)
    ax2.plot([0, max_value], [0, max_value], '--', color='black', linewidth=1.5)

    ax2.set_xlabel(f'{xax2_name}', fontsize=16)
    ax2.tick_params(axis='x', labelsize=16)
    # ax2.set_xlim(0, max_value)

    ax2.set_ylabel(f'{yax2_name}', fontsize=16)
    ax2.tick_params(axis='y', labelsize=16)
    # ax2.set_ylim(0, max_value)
    ax2.grid(True)

    if model_name is not None:
        # ax2.set_title(f'{model_name}')
        plt.savefig(f'./{model_name}_scplot.pdf', format='pdf', bbox_inches='tight', pad_inches=0.1)

    plt.show()

def qqplot(y_test, y_pred, axis_names=None, site_name=None, quantiles=None):

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(12, 4), constrained_layout=True)

    if axis_names is None:
        y_test_name='GT'
        y_pred_name='MODEL'
    else:
        y_test_name=axis_names[0]
        y_pred_name=axis_names[1]

    ax1.boxplot([y_test, y_pred])

    ax1.set_xticklabels([y_test_name, y_pred_name])
    ax1.tick_params(axis='x', labelrotation=0, labelsize=12)
    ax1.grid(True)
    # ax1.set_title(f'BOX PLOT')

    x1 = np.sort(y_test)
    y1 = np.arange(1, len(y_test) + 1) / len(y_test)
    ax2.plot(x1, y1, linestyle='none', marker='o', alpha=0.2, label=y_test_name)
    # ax2.plot(x1, y1, linestyle='-', alpha=0.8, label='GT')

    x2 = np.sort(y_pred)
    y2 = np.arange(1, len(y_pred) + 1) / len(y_pred)
    # ax1.plot(x2, y2, linestyle='none', marker='.', alpha=0.5, label='GT')
    ax2.plot(x2, y2, linestyle='-.', alpha=1, label=y_pred_name)

    # ax2.set_title(f'ECDF')
    ax2.legend()

    if quantiles is None:
        quantiles = min(len(y_test), len(y_pred))
    quantiles = np.linspace(start=0, stop=1, num=int(quantiles))

    x_quantiles = np.quantile(y_test, quantiles, method='nearest')
    y_quantiles = np.quantile(y_pred, quantiles, method='nearest')

    ax3.scatter(x_quantiles, y_quantiles)
    # ax3.plot([0, 100], [0, 100], '--', color = 'black', linewidth=1.5)

    max_value = np.array((x_quantiles, y_quantiles)).max()
    ax3.plot([0, max_value], [0, max_value], '--', color = 'black', linewidth=1.5)

    ax3.set_xlabel(y_test_name)
    ax3.set_ylabel(y_pred_name)
    # ax3.set_title(f'Q-Q PLOT')

    if site_name is not None:
        plt.savefig(f'./{site_name}.pdf', format='pdf', bbox_inches='tight', pad_inches=0.05)

    plt.show()

def loss_decay_plot(num_epochs, train_loss, val_loss, save_path=None):
    fig, ax = plt.subplots(constrained_layout=True)
    ax.plot(range(num_epochs), train_loss, color='g', label="Train")
    ax.plot(range(num_epochs), val_loss, color='r', label="Val")

    ax.set_xticks(range(0, num_epochs, 5))

    ax.set_xlabel('Epochs')
    ax.set_ylabel('Loss')
    # plt.title(f'Loss Decay')
    ax.set_xlim(0, num_epochs)

    ax.grid(True)
    ax.legend()

    if save_path is not None:
        plt.savefig(f"{save_path}/loss_decay.pdf")
    plt.show()

class AdjustLearningRate:
    num_of_iterations = 0

    def __init__(self, optimizer, base_lr, max_iter, power):
        self.optimizer = optimizer
        self.base_lr = base_lr
        self.max_iter = max_iter
        self.power = power

    def __call__(self, current_iter):
        lr = self.base_lr * ((1 - float(current_iter) / self.max_iter) ** self.power)
        self.optimizer.param_groups[0]['lr'] = lr
        if len(self.optimizer.param_groups) > 1:
            self.optimizer.param_groups[1]['lr'] = lr * 10

        return lr
