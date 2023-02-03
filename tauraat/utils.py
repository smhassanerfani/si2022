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

    fig, ax = plt.subplots(ncols=1 ,figsize=(6, 6))

    max_value = np.array((y_test, y_pred)).max()

    ax.scatter(y_test, y_pred, color='teal', edgecolor='steelblue', alpha=0.5, label="Left Bankline")
    ax.plot([0, max_value], [0, max_value], '--', color = 'black', linewidth=1.5)

    if model_name is not None:
        ax.set_title(f'{model_name}')

    ax.set_xlabel('Depth (GT)', fontsize=16)
    ax.tick_params(axis='x', labelsize=16)
    ax.set_xlim(0, max_value)

    ax.set_ylabel('Predicted Depth', fontsize=16)
    ax.tick_params(axis='y', labelsize=16)
    ax.set_ylim(0, max_value)
    ax.grid(True)


    plt.savefig(f"./{model_name}_scplot.png")
    plt.show()