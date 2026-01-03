from core.banner import Banner

def pulls_until_limited(use_pity=True, use_5050=True):
    #simulate pulls until getting limited 5*
    banner = Banner(use_pity=use_pity, use_50_50=use_5050)
    pulls = 0

    while True:
        pulls += 1
        if banner.pull() == "LIMITED":
            return pulls
        
def simulate_players(n, use_pity=True, use_5050=True):
    #run monte carlo simul for n players
    return [pulls_until_limited(use_pity=use_pity, use_5050=use_5050) for _ in range(n)]