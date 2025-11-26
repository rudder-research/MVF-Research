import pandas as pd

def zscore(df: pd.DataFrame) -> pd.DataFrame:
    """
    Column-wise z-score normalization.
    """
    return (df - df.mean()) / df.std(ddof=0)
