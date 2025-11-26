import pandas as pd

def assemble_state(blocks: dict) -> pd.DataFrame:
    """
    Combine multiple DataFrame blocks into a single state matrix.
    Ensures index alignment and basic cleaning.
    """
    df = pd.concat(blocks.values(), axis=1)
    df = df.sort_index().ffill().bfill()
    return df
