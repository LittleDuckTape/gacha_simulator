#all the graphs and output

import numpy as np
import matplotlib.pyplot as plt

def show_stats(label, results):
    mean_pulls = np.mean(results)
    sd = np.std(results)

    print(f"\n-----{label.upper()}-----")
    print(f"Avg pulls for 5*: {mean_pulls:.2f}")
    print(f"Standard deviation: {sd:.2f}")

    return mean_pulls

def plot_histogram(results, title):
    plt.figure()
    plt.hist(results, bins=30)
    plt.title(title)
    plt.xlabel("Pull Count")
    plt.ylabel("Frequency")
    plt.show()

def plot_cdf(probability_curve, title):
    plt.figure()
    plt.plot(probability_curve)
    plt.title(title)
    plt.xlabel("Pull Count")
    plt.ylabel("Probability")
    plt.show()

def luck_score(pulls, avg):
    if pulls < avg:
        return "LUCKY"
    elif pulls > avg:
        return "UNLUCKY"
    else:
        return "AVERAGE"