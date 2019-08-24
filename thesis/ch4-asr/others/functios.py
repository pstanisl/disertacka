import matplotlib.pyplot as plt
import numpy as np


def relu(x):
    y = np.array(x)
    indexes = x < 0
    y[indexes] = 0

    return y


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))


def plot(x, y, path='function.png'):
    fig, ax = plt.subplots()

    ax.plot(x, y)
    y_lim = ax.get_ylim()
    ax.grid(linestyle='-', linewidth=.5)
    # ax.plot([0, 0], y_lim, color='black')
    ax.set_ylim(y_lim)
    ax.set_xlim(np.min(x), np.max(x))

    if path:
        fig.savefig(
            path,
            dpi=300, # Dots per inch
            # frameon='false',
            aspect='normal',
            bbox_inches='tight',
            #pad_inches=0
        )

    plt.show()


def plot_ax(ax, x, y):
    ax.plot(x, y)
    y_lim = ax.get_ylim()
    ax.grid(linestyle='-', linewidth=.5)
    # ax.plot([0, 0], y_lim, color='black')
    ax.set_ylim(y_lim)
    ax.set_xlim(np.min(x), np.max(x))


if __name__ == '__main__':
    N = 250
    x = np.linspace(-5, 5, N, endpoint=True)
    yr = relu(x)
    ys = sigmoid(x)
    yt = tanh(x)

    # plot(x, ys, path='./thesis/ch4-asr/img/sigmoid.png')
    # plot(x, yt, path='./thesis/ch4-asr/img/tanh.png')
    # plot(x, yr, path='./thesis/ch4-asr/img/relu.png')

    fig, ax = plt.subplots(1, 3)

    plot_ax(ax[0], x, ys)
    plot_ax(ax[1], x, yt)
    plot_ax(ax[2], x, yr)

    plt.show()




