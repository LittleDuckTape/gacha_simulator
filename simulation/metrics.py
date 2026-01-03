import numpy as np

def summarize(data):
    return {
        'mean': np.mean(data),
        'median': np.median(data),
        'std': np.std(data),
        'p90': np.percentile(data, 90),
    }

def cdf(data):
    #return x, y for CDF plot
    sorted_data = np.sort(data)
    y = np.arange(len(sorted_data)) / len(sorted_data)
    return sorted_data, y