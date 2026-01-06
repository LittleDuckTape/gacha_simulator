import numpy as np

def summarize(data):
    return {
        'mean': np.mean(data),
        'median': np.median(data),
        'std': np.std(data),
        'p90': np.percentile(data, 90),
    }