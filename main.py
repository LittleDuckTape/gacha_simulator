import os
import sys

#force correct import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.monte_carlo import simulate_players
from simulation.metrics import summarize
from plots.plots_util import plot_histogram, plot_cdf

NUM_PLAYERS = 10000 #set n players

def run_system(label, use_pity, use_5050):
    print(f"\n=== {label} ===")

    results = simulate_players(
        n=NUM_PLAYERS,
        use_pity=use_pity,
        use_5050=use_5050
    )

    stats = summarize(results)
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")
    
    return results



if __name__ == "__main__":
    #no pity
    no_pity = run_system(
        label = "No pity",
        use_pity = False,
        use_5050 = False,
    )

    plot_histogram(
        no_pity,
        title="No Pity System – Pull Distribution",
        filename="plots/no_pity_hist.png"
    )

    plot_cdf(
        no_pity,
        title="No Pity System – CDF",
        filename="plots/no_pity_cdf.png"
    )



    #soft pity
    soft_pity = run_system(
        label = "Soft pity",
        use_pity = True,
        use_5050 = False,
    )

    plot_histogram(
        soft_pity,
        title="Soft Pity – Pull Distribution",
        filename="plots/soft_pity_hist.png"
    )

    plot_cdf(
        soft_pity,
        title="Soft Pity – CDF",
        filename="plots/soft_pity_cdf.png"
    )



    #soft pity + 50/50
    soft_5050 = run_system(
        label = "Soft pity + 50/50",
        use_pity = True,
        use_5050 = True,
    )

    plot_histogram(
        soft_5050,
        title="Soft Pity + 50/50 – Pull Distribution",
        filename="plots/soft_pity_5050_hist.png"
    )

    plot_cdf(
        soft_5050,
        title="Soft Pity + 50/50 – CDF",
        filename="plots/soft_pity_5050_cdf.png"
    )