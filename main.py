import os
import sys

#force correct import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.monte_carlo import simulate_players
from simulation.metrics import summarize

def run_test(label, use_pity, use_5050, n=10000):
    print(f"\n=== {label} ===")
    results = simulate_players(
        n=n,
        use_pity=use_pity,
        use_5050=use_5050
    )
    stats = summarize(results)

    for key, value in stats.items():
        print(f"{key}: {value:.2f}")



if __name__ == "__main__":
    NUM_PLAYERS = 10000 #set n players
    
    #no pity
    run_test(
        label = "No pity",
        use_pity = False,
        use_5050 = False,
        n = NUM_PLAYERS
    )

    #soft pity
    run_test(
        label = "Soft pity",
        use_pity = True,
        use_5050 = False,
        n = NUM_PLAYERS
    )

    #soft pity + 50/50
    run_test(
        label = "Soft pity + 50/50",
        use_pity = True,
        use_5050 = True,
        n = NUM_PLAYERS
    )