#greedy expected probability model

from config import base_rate, soft_pity_start, soft_pity_boost, hard_pity

def greedy_expected_curve():
    probabilities = []
    cumulative = 0

    for i in range(1, hard_pity + 1):
        if i >= soft_pity_start:
            p = base_rate + (i - soft_pity_start) * soft_pity_boost
            p = min(p, 1.0)
        else:
            p = base_rate

        cumulative = 1 - (1 - cumulative) * (1 - p)
        probabilities.append(cumulative)
    
    return probabilities