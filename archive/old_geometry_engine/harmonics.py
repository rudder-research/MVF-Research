import numpy as np
import pandas as pd

def dominant_frequencies(series: pd.Series, k: int = 10):
    """
    Return the k most dominant frequencies (by amplitude) of a series.
    """
    s = series.dropna().values
    if len(s) < 8:
        return np.array([]), np.array([])

    fft = np.fft.fft(s)
    freqs = np.fft.fftfreq(len(s))
    amps = np.abs(fft)

    idx = np.argsort(amps)[-k:]
    return freqs[idx], amps[idx]
