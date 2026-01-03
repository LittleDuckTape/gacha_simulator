from core.banner import Banner

def ten_pull(banner):
    results = []
    for _ in range(10):
        result = banner.pull()
        results.append(result)
    return results