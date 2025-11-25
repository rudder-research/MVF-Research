import numpy as np
import pandas as pd

def pairwise_angle_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pairwise angles (in radians) between all standardized columns of df.
    Uses full-history vectors for each column.
    """
    cols = df.columns
    n = len(cols)
    out = pd.DataFrame(index=cols, columns=cols, dtype=float)

    X = df.values
    # Center & standardize columns
    X = X - X.mean(axis=0)
    X = X / X.std(axis=0, ddof=0)

    for i in range(n):
        for j in range(n):
            v1 = X[:, i]
            v2 = X[:, j]
            num = np.dot(v1, v2)
            den = np.linalg.norm(v1) * np.linalg.norm(v2)
            if den == 0:
                cosang = 1.0
            else:
                cosang = num / den
            cosang = np.clip(cosang, -1.0, 1.0)
            out.iloc[i, j] = np.arccos(cosang)

    return out


def state_angle_change(state: pd.DataFrame) -> pd.Series:
    """
    Angle (radians) between successive state vectors x(t-1) and x(t).
    Measures how quickly the system direction is rotating in state space.
    """
    X = state.values
    idx = state.index

    angles = [np.nan]  # first point has no previous state

    for t in range(1, len(X)):
        v1 = X[t - 1]
        v2 = X[t]
        num = np.dot(v1, v2)
        den = np.linalg.norm(v1) * np.linalg.norm(v2)
        if den == 0:
            cosang = 1.0
        else:
            cosang = num / den
        cosang = np.clip(cosang, -1.0, 1.0)
        angles.append(np.arccos(cosang))

    return pd.Series(angles, index=idx, name="state_angle_change")


def divergence_from_reference(state: pd.DataFrame, ref="mean") -> pd.Series:
    """
    Angle (radians) between each state vector x(t) and a reference direction.
    
    ref options:
      - "mean": use long-run mean state vector as reference
      - 1D np.array / list / pd.Series: explicit reference vector
    """
    X = state.values
    idx = state.index

    if isinstance(ref, str):
        if ref == "mean":
            ref_vec = X.mean(axis=0)
        else:
            raise ValueError(f"Unknown ref='{ref}'. Use 'mean' or a numeric vector.")
    else:
        ref_vec = np.asarray(ref)
        if ref_vec.shape[0] != X.shape[1]:
            raise ValueError("Reference vector length must match number of state dimensions.")

    ref_norm = np.linalg.norm(ref_vec)
    if ref_norm == 0:
        # degenerate case: no direction
        return pd.Series(np.nan, index=idx, name="divergence_from_ref")

    ref_unit = ref_vec / ref_norm

    angles = []
    for t in range(len(X)):
        v = X[t]
        num = np.dot(v, ref_unit)
        den = np.linalg.norm(v)  # ref_unit is already unit length
        if den == 0:
            cosang = 1.0
        else:
            cosang = num / den
        cosang = np.clip(cosang, -1.0, 1.0)
        angles.append(np.arccos(cosang))

    return pd.Series(angles, index=idx, name="divergence_from_ref")
