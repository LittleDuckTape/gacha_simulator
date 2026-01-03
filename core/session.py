from core.banner import Banner

def ten_pull(banner):
    #do ten pull on the given banner
    results = []
    for _ in range(10):
        results.append(banner.pull())
    return results