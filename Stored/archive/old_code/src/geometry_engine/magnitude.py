import numpy as np
import pandas as pd

def rowwise_magnitude(df: pd.DataFrame) -> pd.Series:
    """
    Euclidean norm of each row in the state matrix.
    """
    return np.sqrt((df ** 2).sum(axis=1))
