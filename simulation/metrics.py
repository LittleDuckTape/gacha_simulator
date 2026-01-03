import numpy as np

def summarize(data):
    return {
        'mean': np.mean(data),
        'median': np.median(data),
        'std_dev': np.std(data),
        'p90': np.percentile(data, 90),
        'p95': np.percentile(data, 95)
    }

def cdf(data):
    sorted_data = np.sort(data)
    cumulative = np.arange(len(sorted_data)) / len(sorted_data)
    return sorted_data, cumulative