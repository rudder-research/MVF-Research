"""
VCF Research — Core Math Engine with Full Mathematical Implementation
Author: Jason Rudder (scaffold), Claude (mathematical implementation)
Purpose: Complete mathematical logic for normalization, geometry, stress controls, MRF, MVSS

This script assumes the following folder structure:

/content/VCF-RESEARCH/
    data_raw/
    data_clean/
    registry/
    outputs/
"""

import os
import pandas as pd
import numpy as np
from scipy import stats
from scipy.signal import hilbert
import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------
# 1. Folder Setup
# ---------------------------------------------------------

BASE = "/content/VCF-RESEARCH"

FOLDERS = {
    "raw": f"{BASE}/data_raw",
    "clean": f"{BASE}/data_clean",
    "registry": f"{BASE}/registry",
    "outputs": f"{BASE}/outputs"
}

def ensure_folders():
    for f in FOLDERS.values():
        os.makedirs(f, exist_ok=True)

ensure_folders()


# ---------------------------------------------------------
# 2. Registry Loader
# ---------------------------------------------------------

def load_metric_registry():
    """Loads list of metrics & settings."""
    reg_csv = f"{FOLDERS['registry']}/metrics.csv"
    reg_json = f"{BASE}/src/vcf/data/vcf_metric_registry.json"

    if os.path.exists(reg_json):
        return pd.read_json(reg_json)
    if os.path.exists(reg_csv):
        return pd.read_csv(reg_csv)

    raise FileNotFoundError("No registry found.")


# ---------------------------------------------------------
# 3. Load Raw CSVs
# ---------------------------------------------------------

def load_all_raw():
    """Auto-loads all CSV files in data_raw."""
    raw_files = {}
    for file in os.listdir(FOLDERS["raw"]):
        if file.endswith(".csv"):
            key = file.replace(".csv", "")
            raw_files[key] = pd.read_csv(f"{FOLDERS['raw']}/{file}")
    return raw_files


# ---------------------------------------------------------
# 4. Normalization Framework
# ---------------------------------------------------------

def normalize_series(series, method="zscore", window=None, clip_std=3):
    """
    Comprehensive normalization with multiple methods.
    
    Parameters:
    -----------
    series : pd.Series
        Input time series
    method : str
        Normalization method:
        - 'zscore': Standard z-score normalization
        - 'minmax': Min-max scaling to [0,1]
        - 'logit': Logit transformation after minmax
        - 'rolling_zscore': Rolling window z-score
        - 'logistic': Logistic transformation
        - 'robust': Robust scaling using median and IQR
        - 'tanh': Hyperbolic tangent normalization
    window : int, optional
        Window size for rolling methods
    clip_std : float
        Number of standard deviations for clipping outliers
    
    Returns:
    --------
    pd.Series : Normalized series
    """
    series = series.copy()
    
    # Handle NaN values
    if series.isna().all():
        return series
    
    if method == "zscore":
        mean = series.mean()
        std = series.std()
        if std == 0:
            return pd.Series(np.zeros(len(series)), index=series.index)
        normalized = (series - mean) / std
        # Clip extreme values
        normalized = normalized.clip(-clip_std, clip_std)
        return normalized
    
    elif method == "minmax":
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - min_val) / (max_val - min_val)
    
    elif method == "logit":
        # First normalize to [0,1], then apply logit
        normalized = normalize_series(series, method="minmax")
        # Avoid 0 and 1 for logit
        epsilon = 1e-7
        normalized = normalized.clip(epsilon, 1 - epsilon)
        return np.log(normalized / (1 - normalized))
    
    elif method == "rolling_zscore":
        if window is None:
            window = min(252, len(series) // 4)  # Default to ~1 year or 1/4 of data
        
        rolling_mean = series.rolling(window=window, min_periods=window//2).mean()
        rolling_std = series.rolling(window=window, min_periods=window//2).std()
        
        # Handle zero std
        rolling_std = rolling_std.replace(0, np.nan)
        normalized = (series - rolling_mean) / rolling_std
        
        # Forward fill initial NaN values
        normalized = normalized.fillna(method='bfill')
        return normalized.clip(-clip_std, clip_std)
    
    elif method == "logistic":
        # Logistic function: 1 / (1 + exp(-x))
        # First standardize, then apply logistic
        standardized = normalize_series(series, method="zscore")
        return 1 / (1 + np.exp(-standardized))
    
    elif method == "robust":
        # Use median and IQR for robust scaling
        median = series.median()
        q75 = series.quantile(0.75)
        q25 = series.quantile(0.25)
        iqr = q75 - q25
        
        if iqr == 0:
            return pd.Series(np.zeros(len(series)), index=series.index)
        
        normalized = (series - median) / iqr
        return normalized.clip(-clip_std, clip_std)
    
    elif method == "tanh":
        # Hyperbolic tangent normalization (bounded between -1 and 1)
        standardized = normalize_series(series, method="zscore")
        return np.tanh(standardized)
    
    else:
        raise ValueError(f"Unknown normalization method: {method}")


# ---------------------------------------------------------
# 5. Geometry Engine
# ---------------------------------------------------------

def compute_theta(df, lookback=63):
    """
    Angular positioning based on macro seasonality geometry.
    
    Computes phase angle from Hilbert transform of principal component,
    representing position in the market cycle.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Panel with normalized metrics
    lookback : int
        Window for phase computation
    
    Returns:
    --------
    np.array : Angular position in radians [0, 2π]
    """
    # Extract numeric columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    data = df[numeric_cols].fillna(method='ffill').fillna(0)
    
    if len(data) < lookback:
        return np.zeros(len(df))
    
    # Compute principal component (first PC captures dominant market mode)
    from sklearn.decomposition import PCA
    pca = PCA(n_components=1)
    
    # Use rolling window to compute local phase
    theta = np.zeros(len(df))
    
    for i in range(lookback, len(df)):
        window_data = data.iloc[i-lookback:i].values
        
        # Handle case where window has no variance
        if np.std(window_data) < 1e-10:
            theta[i] = theta[i-1] if i > lookback else 0
            continue
        
        try:
            pc = pca.fit_transform(window_data)[:, 0]
            
            # Apply Hilbert transform to get instantaneous phase
            analytic_signal = hilbert(pc)
            instantaneous_phase = np.angle(analytic_signal)
            
            # Use final phase value, normalized to [0, 2π]
            theta[i] = (instantaneous_phase[-1] + np.pi) % (2 * np.pi)
        except:
            theta[i] = theta[i-1] if i > lookback else 0
    
    # Forward fill initial values
    if lookback > 0:
        theta[:lookback] = theta[lookback]
    
    return theta


def compute_phi(df, lookback=21):
    """
    Curvature / second-order geometric effects.
    
    Measures the rate of change of theta (angular acceleration),
    indicating regime shifts and inflection points.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Panel with normalized metrics
    lookback : int
        Window for curvature computation
    
    Returns:
    --------
    np.array : Curvature measure
    """
    theta = compute_theta(df, lookback=63)
    
    # Compute first derivative (angular velocity)
    dtheta = np.gradient(theta)
    
    # Compute second derivative (angular acceleration / curvature)
    phi = np.gradient(dtheta)
    
    # Smooth with rolling window
    phi_series = pd.Series(phi)
    phi_smooth = phi_series.rolling(window=lookback, min_periods=1).mean()
    
    return phi_smooth.values


def compute_divergence(df, lookback=63):
    """
    Divergence detection between metrics.
    
    Measures when different market components move in opposite directions,
    indicating potential instability or regime change.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Panel with normalized metrics
    lookback : int
        Rolling window for correlation computation
    
    Returns:
    --------
    np.array : Divergence score (0 = convergent, 1 = divergent)
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    data = df[numeric_cols].fillna(method='ffill').fillna(0)
    
    if len(numeric_cols) < 2:
        return np.zeros(len(df))
    
    divergence = np.zeros(len(df))
    
    for i in range(lookback, len(df)):
        window_data = data.iloc[i-lookback:i]
        
        # Compute pairwise correlations
        corr_matrix = window_data.corr()
        
        # Extract upper triangle (excluding diagonal)
        upper_triangle = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        # Divergence is inverse of mean correlation
        # High correlation = low divergence
        mean_corr = upper_triangle.stack().mean()
        
        # Transform to [0, 1] where 1 is maximum divergence
        # Correlation ranges from -1 to 1
        # Divergence = (1 - correlation) / 2
        divergence[i] = (1 - mean_corr) / 2
    
    # Forward fill initial values
    if lookback > 0:
        divergence[:lookback] = divergence[lookback]
    
    return divergence


def compute_resonance(df, lookback=126):
    """
    Resonance score measuring harmonic alignment between inputs.
    
    High resonance occurs when multiple metrics oscillate in phase,
    suggesting coordinated market behavior.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Panel with normalized metrics
    lookback : int
        Window for frequency analysis
    
    Returns:
    --------
    np.array : Resonance score [0, 1]
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    data = df[numeric_cols].fillna(method='ffill').fillna(0)
    
    if len(numeric_cols) < 2:
        return np.zeros(len(df))
    
    resonance = np.zeros(len(df))
    
    for i in range(lookback, len(df)):
        window_data = data.iloc[i-lookback:i]
        
        # Compute phase coherence using Hilbert transform
        phases = []
        
        for col in numeric_cols:
            series = window_data[col].values
            if np.std(series) < 1e-10:
                continue
            
            try:
                analytic_signal = hilbert(series)
                instantaneous_phase = np.angle(analytic_signal)
                phases.append(instantaneous_phase[-1])
            except:
                continue
        
        if len(phases) < 2:
            resonance[i] = 0
            continue
        
        # Compute phase coherence
        # High coherence = phases are similar (resonance)
        phases = np.array(phases)
        
        # Compute mean resultant length (circular statistics)
        # This measures phase synchronization
        mean_cos = np.mean(np.cos(phases))
        mean_sin = np.mean(np.sin(phases))
        resultant_length = np.sqrt(mean_cos**2 + mean_sin**2)
        
        resonance[i] = resultant_length
    
    # Forward fill initial values
    if lookback > 0:
        resonance[:lookback] = resonance[lookback]
    
    return resonance


# ---------------------------------------------------------
# 6. Stress Controls
# ---------------------------------------------------------

def compute_stress_index(df, lookback=63, z_threshold=2.5):
    """
    Stress index combining multiple stress indicators.
    
    Detects:
    - Z-score outliers in individual metrics
    - Correlation breakdown
    - Volatility spikes
    - Extreme divergence
    
    Parameters:
    -----------
    df : pd.DataFrame
        Panel with normalized metrics
    lookback : int
        Rolling window for stress computation
    z_threshold : float
        Z-score threshold for outlier detection
    
    Returns:
    --------
    np.array : Composite stress index [0, 1]
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    data = df[numeric_cols].fillna(method='ffill').fillna(0)
    
    stress = np.zeros(len(df))
    
    for i in range(lookback, len(df)):
        window_data = data.iloc[i-lookback:i]
        current_data = data.iloc[i]
        
        stress_components = []
        
        # 1. Z-score outlier stress
        rolling_mean = window_data.mean()
        rolling_std = window_data.std()
        z_scores = np.abs((current_data - rolling_mean) / (rolling_std + 1e-10))
        outlier_stress = (z_scores > z_threshold).sum() / len(numeric_cols)
        stress_components.append(outlier_stress)
        
        # 2. Correlation breakdown stress
        corr_matrix = window_data.corr()
        recent_corr = window_data.tail(lookback//4).corr()
        
        # Measure correlation change
        corr_change = np.abs(corr_matrix - recent_corr).mean().mean()
        stress_components.append(min(corr_change * 2, 1))  # Scale to [0, 1]
        
        # 3. Volatility spike stress
        rolling_vol = window_data.std()
        recent_vol = window_data.tail(lookback//4).std()
        vol_ratio = (recent_vol / (rolling_vol + 1e-10)).mean()
        vol_stress = min(max(vol_ratio - 1, 0), 1)  # Excess volatility
        stress_components.append(vol_stress)
        
        # 4. Extreme movement stress
        extreme_moves = (np.abs(z_scores) > z_threshold).sum()
        extreme_stress = min(extreme_moves / len(numeric_cols), 1)
        stress_components.append(extreme_stress)
        
        # Composite stress (weighted average)
        stress[i] = np.mean(stress_components)
    
    # Forward fill initial values
    if lookback > 0:
        stress[:lookback] = stress[lookback]
    
    return stress


# ---------------------------------------------------------
# 7. MRF + MVSS Block
# ---------------------------------------------------------

def compute_mrf(df, weights=None):
    """
    Unified Market Risk Factor based on normalized metrics + weights.
    
    Constructs a composite risk measure from all available metrics,
    with optional custom weighting.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Panel with normalized metrics
    weights : dict, optional
        Custom weights for each metric
    
    Returns:
    --------
    np.array : Market Risk Factor
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    data = df[numeric_cols].fillna(method='ffill').fillna(0)
    
    if weights is None:
        # Equal weighting
        weights = {col: 1/len(numeric_cols) for col in numeric_cols}
    
    # Ensure weights sum to 1
    weight_sum = sum(weights.values())
    weights = {k: v/weight_sum for k, v in weights.items()}
    
    # Compute weighted combination
    mrf = np.zeros(len(df))
    
    for col in numeric_cols:
        if col in weights:
            mrf += data[col].values * weights[col]
    
    return mrf


def compute_mvss(df, mrf=None, lookback=252):
    """
    Market Vector Stability Score (MVSS).
    
    Sortino-like stability score measuring:
        true signal response / false signal noise
    
    Higher MVSS indicates more stable, reliable market signals.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Panel with normalized metrics
    mrf : np.array, optional
        Pre-computed MRF values
    lookback : int
        Window for stability computation
    
    Returns:
    --------
    np.array : MVSS values
    """
    if mrf is None:
        mrf = compute_mrf(df)
    
    mvss = np.zeros(len(df))
    
    mrf_series = pd.Series(mrf)
    
    for i in range(lookback, len(df)):
        window_mrf = mrf_series.iloc[i-lookback:i]
        
        # Compute returns/changes
        mrf_returns = window_mrf.diff()
        
        # Separate upside and downside
        upside = mrf_returns[mrf_returns > 0]
        downside = mrf_returns[mrf_returns < 0]
        
        # Compute Sortino-like ratio
        # Mean return / downside deviation
        mean_return = mrf_returns.mean()
        downside_dev = downside.std() if len(downside) > 0 else 1e-10
        
        sortino = mean_return / (downside_dev + 1e-10)
        
        # Also measure signal consistency
        # Autocorrelation as proxy for signal persistence
        autocorr = mrf_returns.autocorr(lag=1)
        if np.isnan(autocorr):
            autocorr = 0
        
        # Composite stability score
        # Combine Sortino ratio with signal consistency
        stability = 0.7 * sortino + 0.3 * autocorr
        
        # Normalize to [0, 1] using tanh
        mvss[i] = (np.tanh(stability) + 1) / 2
    
    # Forward fill initial values
    if lookback > 0:
        mvss[:lookback] = mvss[lookback]
    
    return mvss


# ---------------------------------------------------------
# 8. Build Final Geometry Panel
# ---------------------------------------------------------

def build_geometry_panel(clean_panel):
    """
    Construct complete geometry panel with all derived metrics.
    """
    print("Computing geometric metrics...")
    
    out = clean_panel.copy()
    
    print("  - Computing theta (angular position)...")
    out["theta"] = compute_theta(out)
    
    print("  - Computing phi (curvature)...")
    out["phi"] = compute_phi(out)
    
    print("  - Computing divergence...")
    out["divergence"] = compute_divergence(out)
    
    print("  - Computing resonance...")
    out["resonance"] = compute_resonance(out)
    
    print("  - Computing stress index...")
    out["stress_index"] = compute_stress_index(out)
    
    print("  - Computing MRF...")
    out["mrf"] = compute_mrf(out)
    
    print("  - Computing MVSS...")
    out["mvss"] = compute_mvss(out, mrf=out["mrf"].values)
    
    return out


# ---------------------------------------------------------
# 9. Main Pipeline
# ---------------------------------------------------------

def run_vcf_pipeline(normalization_method="zscore"):
    """
    Complete VCF pipeline execution.
    
    Parameters:
    -----------
    normalization_method : str
        Method to use for normalization
    """
    print("=== VCF Pipeline Start ===\n")

    # 1. Load
    print("Loading raw data...")
    raw = load_all_raw()
    print(f"  Loaded {len(raw)} raw datasets")
    
    try:
        registry = load_metric_registry()
        print(f"  Loaded metric registry")
    except FileNotFoundError:
        print("  No registry found, proceeding without")
        registry = None

    # 2. Normalize
    print(f"\nNormalizing data using method: {normalization_method}")
    clean = {}
    for k, df in raw.items():
        clean[k] = df.copy()
        print(f"  Processing {k}...")
        
        for col in df.columns:
            if col not in ["Date", "date", "DATE"]:
                clean[k][col] = normalize_series(df[col], method=normalization_method)

    # 3. Combine into single macro panel
    print("\nCombining into macro panel...")
    
    # Identify date column
    date_col = None
    for possible_date in ["Date", "date", "DATE"]:
        if possible_date in list(clean.values())[0].columns:
            date_col = possible_date
            break
    
    if date_col:
        macro_panel = pd.concat(
            [clean[k].set_index(date_col) for k in clean.keys()],
            axis=1
        ).reset_index()
        macro_panel.rename(columns={date_col: "Date"}, inplace=True)
    else:
        macro_panel = pd.concat(
            [clean[k] for k in clean.keys()],
            axis=1
        )
    
    # Remove duplicate columns
    macro_panel = macro_panel.loc[:, ~macro_panel.columns.duplicated()]
    
    print(f"  Panel shape: {macro_panel.shape}")
    
    macro_panel.to_csv(f"{FOLDERS['clean']}/normalized_panel.csv", index=False)
    print(f"  Saved: {FOLDERS['clean']}/normalized_panel.csv")

    # 4. Geometry Panel
    print("\n" + "="*50)
    geom = build_geometry_panel(macro_panel)
    print("="*50 + "\n")
    
    geom.to_csv(f"{FOLDERS['clean']}/geometry_panel.csv", index=False)
    print(f"Saved: {FOLDERS['clean']}/geometry_panel.csv")
    
    # 5. Summary statistics
    print("\n=== Pipeline Summary ===")
    print(f"Total observations: {len(geom)}")
    print(f"\nGeometric Metrics Summary:")
    
    geom_cols = ["theta", "phi", "divergence", "resonance", "stress_index", "mrf", "mvss"]
    summary = geom[geom_cols].describe()
    print(summary)
    
    print("\n=== VCF Pipeline Complete ===")
    
    return geom


if __name__ == "__main__":
    # Run with default z-score normalization
    # Can be changed to: minmax, logit, rolling_zscore, logistic, robust, tanh
    result = run_vcf_pipeline(normalization_method="zscore")
