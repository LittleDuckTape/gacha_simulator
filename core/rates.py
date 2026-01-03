def five_star_rate(pity):
    if pity < 75:
        return 0.006 #base rate
    elif pity < 90:
        return 0.006 + (pity - 74) * (1 - 0.06) / 16 #inflated rate
    else:
        return 1.0 #guaranteed rate