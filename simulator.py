#monte carlo simul engine

import random
import numpy as np
from config import base_rate, soft_pity_start, soft_pity_boost, hard_pity, total_simul

#----- /w pity
def simul_single_run_pity():
    pity = 0

    while True:
        pity += 1

        if pity >= soft_pity_start:
            chance = base_rate + (pity - soft_pity_start) * soft_pity_boost
            chance = min(chance, 1.0)
        else:
            chance = base_rate

        if random.random() < chance:
            return pity
        
        if pity >= hard_pity:
            return pity

def run_simul_pity():
    results = []

    for _ in range(total_simul):
        pulls = simul_single_run_pity()
        results.append(pulls)

    return np.array(results)

#----- /wo pity
def simul_single_run():
    pulls = 0

    while True:
        pulls += 1
        if random.random() < base_rate:
            return pulls

def run_simul():
    results = []

    for _ in range(total_simul):
        pulls = simul_single_run()
        results.append(pulls)

    return np.array(results)