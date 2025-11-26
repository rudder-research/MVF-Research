import pandas as pd
import numpy as np

def classify_regimes(magnitude: pd.Series,
                     angle_change: pd.Series,
                     divergence: pd.Series,
                     mag_thresh=(0.5, 1.2),
                     angle_thresh=(0.1, 0.35),
                     div_thresh=(0.5, 1.2)):
    """
    Combine 3 geometry signals into a simple, interpretable regime label.

    magnitude: Euclidean norm of state vector
    angle_change: rotation between consecutive state vectors
    divergence: angle between state and long-run mean vector

    Thresholds:
        mag_thresh = (low, high)
        angle_thresh = (low, high)
        div_thresh = (low, high)

    Returns:
        pd.Series of regime labels.
    """

    # Align series
    df = pd.concat([magnitude, angle_change, divergence], axis=1)
    df.columns = ["mag", "ang", "div"]

    labels = []

    for _, row in df.iterrows():
        mag = row["mag"]
        ang = row["ang"]
        div = row["div"]

        # Handle missing first rows
        if pd.isna(mag) or pd.isna(ang) or pd.isna(div):
            labels.append("Unknown")
            continue

        # 1. Crisis / Stress (high magnitude AND high rotation AND high divergence)
        if (mag > mag_thresh[1]) and (ang > angle_thresh[1]) and (div > div_thresh[1]):
            labels.append("Stress")
            continue

        # 2. Late-Cycle (high magnitude OR high divergence)
        if (mag > mag_thresh[1]) or (div > div_thresh[1]):
            labels.append("Late-Cycle")
            continue

        # 3. Neutral (moderate values)
        if (mag_thresh[0] < mag <= mag_thresh[1]) and \
           (angle_thresh[0] < ang <= angle_thresh[1]) and \
           (div_thresh[0] < div <= div_thresh[1]):
            labels.append("Neutral
