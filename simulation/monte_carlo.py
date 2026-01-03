from core.banner import Banner

def pulls_until_limited():
    #simulate pulls until getting limited 5*
    banner = Banner()
    pulls = 0

    while True:
        pulls += 1
        if banner.pull() == "LIMITED":
            return pulls
        
def simulate_players(n):
    #run monte carlo simul for n players
    return [pulls_until_limited() for _ in range(n)]