import os
import sys

#force correct import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.monte_carlo import simulate_players
from simulation.metrics import summarize
from plots.plots_util import plot_histogram, plot_cdf

NUM_PLAYERS = 10000

systems = [
    ("No pity", False, False),
    ("Soft pity", True, False),
    ("Soft pity + 50/50", True, True),
]

for label, use_pity, use_5050 in systems:
    print(f"\n=== {label} ===")

    results = simulate_players(NUM_PLAYERS, use_pity, use_5050)
    stats = summarize(results)

    for k, v in stats.items():
        print(f"{k}: {v:.2f}")

    safe_label = label.replace(" ", "_").lower()

    plot_histogram(
        results,
        title=f"{label} – Pull Distribution",
        filename=f"plots/{safe_label}_hist.png"
    )

    plot_cdf(
        results,
        title=f"{label} – CDF",
        filename=f"plots/{safe_label}_cdf.png"
    )