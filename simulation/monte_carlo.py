from core.banner import Banner

def pulls_until_limited(banner):
    banner = Banner()
    pulls = 0
    while True:
        pulls += 1
        result = banner.pull()
        if result == "LIMITED":
            return pulls
        
def simulate_players(n):
    results = []
    for _ in range(n):
        results.append(pulls_until_limited())
    return results