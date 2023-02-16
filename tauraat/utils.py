import numbers
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
def scatter_plot(y_test, y_pred, model_name=None):

    y_test = y_test.to_numpy().ravel()

    r2 = np.corrcoef(y_pred, y_test)[0, 1 ]**2
    pbias = 100 * np.sum((y_pred - y_test)) / np.sum(y_test)
    nse = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred, squared=False)
    print(f'NSE: {nse:.4f}, R2: {r2:.4f}, PBias: {pbias:.4f}, MSE: {mse:.4f}')

    plt.rcParams.update({
        # 'font.sans-serif': 'Comic Sans MS',
        'font.family': 'serif'
    })

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 6))

    err = y_test - y_pred
    ax1.violinplot(err, positions=None, vert=True, widths=1.0, showmeans=True,
                   showextrema=True, showmedians=False, quantiles=None, points=100,
                   bw_method=None, data=None)

    ax1.set_title(f'Error Mean: {np.mean(err):.4f}, Error STD: {np.std(err):.4f}')

    max_value = np.array((y_test, y_pred)).max()

    ax2.scatter(y_test, y_pred, color='teal', edgecolor='steelblue', alpha=0.5, label="Left Bankline")
    ax2.plot([0, max_value], [0, max_value], '--', color = 'black', linewidth=1.5)

    if model_name is not None:
        ax2.set_title(f'{model_name}')

    ax2.set_xlabel('Depth (GT)', fontsize=16)
    ax2.tick_params(axis='x', labelsize=16)
    ax2.set_xlim(0, max_value)

    ax2.set_ylabel('Predicted Depth', fontsize=16)
    ax2.tick_params(axis='y', labelsize=16)
    ax2.set_ylim(0, max_value)
    ax2.grid(True)

    if model_name is not None:
        plt.savefig(f"./{model_name}_scplot.png")

    plt.show()

def qqplot(y_test, y_pred, quantiles=None):

    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(12, 4), dpi=300, constrained_layout=True)

    ax1.boxplot([y_test, y_pred])
    ax1.set_xticklabels(['GT', 'MODEL'])
    ax1.tick_params(axis='x', labelrotation=0, labelsize=12)
    ax1.grid(True)
    ax1.set_title(f'BOX PLOT')

    x1 = np.sort(y_test)
    y1 = np.arange(1, len(y_test) + 1) / len(y_test)
    ax2.plot(x1, y1, linestyle='none', marker='o', alpha=0.2, label='GT')
    # ax2.plot(x1, y1, linestyle='-', alpha=0.8, label='GT')

    x2 = np.sort(y_pred)
    y2 = np.arange(1, len(y_pred) + 1) / len(y_pred)
    # ax1.plot(x2, y2, linestyle='none', marker='.', alpha=0.5, label='GT')
    ax2.plot(x2, y2, linestyle='-.', alpha=1, label='MODEL')

    ax2.set_title(f'ECDF')
    ax2.legend()

    if quantiles is None:
        quantiles = min(len(y_test), len(y_pred))
    quantiles = np.linspace(start=0, stop=1, num=int(quantiles))

    x_quantiles = np.quantile(y_test, quantiles, method='nearest')
    y_quantiles = np.quantile(y_pred, quantiles, method='nearest')
    ax3.scatter(x_quantiles, y_quantiles)

    max_value = np.array((x_quantiles, y_quantiles)).max()
    ax3.plot([0, max_value], [0, max_value], '--', color = 'black', linewidth=1.5)

    ax3.set_xlabel('GT')
    ax3.set_ylabel('MODEL')
    ax3.set_title(f'Q-Q PLOT')

    plt.show()