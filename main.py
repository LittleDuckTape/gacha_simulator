import os
import sys

#force correct import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.monte_carlo import simulate_players
from simulation.metrics import summarize

if __name__ == "__main__":
    num_players = 10000 #set n players
    
    results = simulate_players(num_players)
    stats = summarize(results)

    print("=== Gacha Simulation Results ===")
    for key, value in stats.items():
        print(f"{key}: {value:.2f}")