import matplotlib.pyplot as plt
import numpy as np
import os

def plot_histogram(data, title, filename=None):
    plt.figure()
    plt.hist(data, bins=50)
    plt.xlabel("Pull Count")
    plt.ylabel("Number of Players")
    plt.title(title)

    if filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename)

    plt.close()

def plot_cdf(data, title, filename=None):
    sorted_data = np.sort(data)
    y = np.arange(len(sorted_data)) / len(sorted_data)

    plt.figure()
    plt.plot(sorted_data, y)
    plt.xlabel("Pull Count")
    plt.ylabel("Cumulative Probability")
    plt.title(title)

    if filename:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename)

    plt.close()