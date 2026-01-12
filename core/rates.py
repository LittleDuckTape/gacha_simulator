import math

def five_star_rate(pity):
    BASE_RATE = 0.006
    SOFT_PITY = 75
    HARD_PITY = 90

    if pity < SOFT_PITY:
        return BASE_RATE

    if pity >= HARD_PITY:
        return 1.0

    x = (pity - SOFT_PITY) / (HARD_PITY - SOFT_PITY)
    ramp = (math.exp(5 * x) - 1) / (math.exp(5) - 1)
    return min(1.0, BASE_RATE + ramp * (1 - BASE_RATE))

# here to explain stuff:
# base rate is 0.6%
# from 75 to 89 pulls, the rate increases exponentially to 100%
# at 90th pull, it is guaranteed to be a 5-star

def four_star_rate(four_star_pity):
    BASE_RATE = 0.051
    HARD_PITY = 10

    if four_star_pity >= HARD_PITY:
        return 1.0

    return BASE_RATE

# every 10th pull is guaranteed 4*
# 4* can be overriden by 5*
# this prevents weird stuff happening at 90th pull

# note: you can adjust these rates as per your game's mechanics, this is just following Genshin Impact