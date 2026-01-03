from simulator import run_simul_pity, run_simul, simul_single_run_pity
from strategy import greedy_expected_curve
from visualize import show_stats, plot_histogram, plot_cdf, luck_score

def main():
    print("Running Gacha Simulaton...\n")

    #----- /w pity
    results_pity = run_simul_pity()
    greedy_curve = greedy_expected_curve()

    avg_pity = show_stats("/W PITY", results_pity)
    plot_histogram(results_pity, "Histogram (/w Pity)")
    plot_cdf(greedy_curve, "CDF Curve (/w Pity)")

    #----- /wo pity
    results = run_simul()

    avg = show_stats("/WO PITY", results)
    plot_histogram(results, "Historgram (/wo Pity)")

    #----- testing
    player = simul_single_run_pity()
    print(f"\nPlayer result (/w pity): {player} pulls + {luck_score(player, avg)}")

    #----- comparison
    print(f"\n-----Comparison-----")
    print(f"Avg (/w Pity): {avg_pity:.2f} pulls")
    print(f"Avg (/wo Pity): {avg:.2f} pulls")

if __name__ == "__main__":
    main()