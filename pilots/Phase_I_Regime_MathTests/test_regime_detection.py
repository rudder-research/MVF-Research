"""
Phase I Pilot: 4-Input Regime Detection Test
=============================================

Tests regime detection on:
1. SPY 50d-200d MA
2. DGS10 (10-year Treasury)
3. DXY (US Dollar Index)
4. AGG (Bond ETF)

Validates:
- Multi-frequency coherence
- Regime classification
- Transition detection
- Metric computation
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add code modules to path
code_path = Path(__file__).parent.parent.parent / 'code'
sys.path.insert(0, str(code_path))
sys.path.insert(0, str(code_path / 'math'))
sys.path.insert(0, str(code_path / 'regime_engine'))
sys.path.insert(0, str(code_path / 'shared'))

from detector import MultiFrequencyRegimeDetector
from metrics import RegimeMetrics
import config


def load_pilot_data():
    """Load the 4 pilot inputs from data_normalized."""
    data_dir = code_path / 'data_normalized'
    
    print("Loading pilot data...")
    
    # For now, we'll use available normalized data as proxies
    # TODO: Add actual SPY MA, DXY, AGG when available
    
    data = {}
    
    # Load what we have
    available_files = list(data_dir.glob('*.csv'))
    print(f"Found {len(available_files)} normalized files")
    
    for file in available_files:
        df = pd.read_csv(file, index_col=0, parse_dates=True)
        name = file.stem.replace('_normalized', '')
        data[name] = df
        print(f"  ✓ {name}: {len(df)} rows")
    
    return data


def create_state_matrix(data: dict, date_range: pd.DatetimeIndex = None):
    """
    Merge individual series into unified state matrix.
    
    Returns DataFrame with columns = inputs, rows = dates
    """
    # Merge all series
    dfs = []
    for name, df in data.items():
        if isinstance(df, pd.DataFrame):
            # Use first column if multiple columns
            series = df.iloc[:, 0]
        else:
            series = df
        
        series.name = name
        dfs.append(series)
    
    # Merge on date index
    state_matrix = pd.concat(dfs, axis=1)
    
    # Drop NaN rows
    state_matrix = state_matrix.dropna()
    
    if date_range is not None:
        state_matrix = state_matrix.loc[date_range]
    
    print(f"\nState matrix: {state_matrix.shape[0]} dates × {state_matrix.shape[1]} inputs")
    return state_matrix


def run_regime_detection(state_matrix: pd.DataFrame):
    """Run regime detection on state matrix."""
    detector = MultiFrequencyRegimeDetector(
        coherence_threshold=config.REGIME_THRESHOLDS['coherence_min']
    )
    
    results = []
    
    print("\nRunning regime detection...")
    for i in range(len(state_matrix)):
        current_state = state_matrix.iloc[i].values
        history = state_matrix.iloc[:i+1]
        
        # Detect regime
        result = detector.detect_regime(
            state_vector=current_state,
            history=history
        )
        
        # Add date and state
        result['date'] = state_matrix.index[i]
        results.append({
            'date': state_matrix.index[i],
            'regime': result['regime'],
            'confidence': result['confidence'],
            **result['metrics']
        })
        
        if (i + 1) % 100 == 0:
            print(f"  Processed {i+1}/{len(state_matrix)} dates...")
    
    results_df = pd.DataFrame(results).set_index('date')
    print(f"✓ Detected regimes for {len(results_df)} dates")
    
    return results_df


def analyze_results(results_df: pd.DataFrame):
    """Analyze and display regime detection results."""
    metrics = RegimeMetrics()
    
    print("\n" + "="*70)
    print("REGIME STATISTICS")
    print("="*70)
    
    stats = metrics.regime_statistics(results_df.reset_index())
    print(stats.to_string(index=False))
    
    print("\n" + "="*70)
    print("TRANSITION MATRIX")
    print("="*70)
    
    trans_matrix = metrics.transition_matrix(results_df.reset_index())
    print(trans_matrix.round(3))
    
    print("\n" + "="*70)
    print("REGIME PERSISTENCE")
    print("="*70)
    
    persistence = metrics.regime_persistence(results_df.reset_index())
    for regime, value in persistence.items():
        print(f"  {regime}: {value:.3f}")
    
    return stats, trans_matrix, persistence


def plot_regime_timeline(results_df: pd.DataFrame, output_path: Path):
    """Create visualization of regime timeline."""
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # Regime colors
    regime_colors = {
        'BULL': 'green',
        'BEAR': 'red',
        'TRANSITION': 'orange',
        'CONSOLIDATION': 'blue',
        'CRISIS': 'darkred',
        'UNKNOWN': 'gray'
    }
    
    # Plot 1: Regime timeline
    ax = axes[0]
    for regime in results_df['regime'].unique():
        mask = results_df['regime'] == regime
        ax.scatter(results_df[mask].index, 
                  [regime] * mask.sum(),
                  c=regime_colors.get(regime, 'gray'),
                  label=regime, alpha=0.7, s=10)
    ax.set_ylabel('Regime')
    ax.set_title('Market Regime Timeline')
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Magnitude over time
    ax = axes[1]
    ax.plot(results_df.index, results_df['magnitude'], 
           color='black', linewidth=1)
    ax.fill_between(results_df.index, 0, results_df['magnitude'],
                    alpha=0.3, color='gray')
    ax.set_ylabel('Magnitude')
    ax.set_title('Market Stress Level')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Coherence over time
    ax = axes[2]
    if 'coherence_medium' in results_df.columns:
        ax.plot(results_df.index, results_df['coherence_medium'],
               color='blue', linewidth=1, label='Medium-term')
    if 'coherence_fast' in results_df.columns:
        ax.plot(results_df.index, results_df['coherence_fast'],
               color='green', linewidth=1, alpha=0.5, label='Fast')
    if 'coherence_slow' in results_df.columns:
        ax.plot(results_df.index, results_df['coherence_slow'],
               color='red', linewidth=1, alpha=0.5, label='Slow')
    ax.axhline(y=config.REGIME_THRESHOLDS['coherence_min'], 
              color='red', linestyle='--', alpha=0.5, label='Threshold')
    ax.set_ylabel('Coherence')
    ax.set_xlabel('Date')
    ax.set_title('Multi-Frequency Coherence')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\n✓ Saved plot to {output_path}")
    plt.close()


def main():
    """Run Phase I pilot test."""
    print("="*70)
    print("PHASE I PILOT: REGIME DETECTION TEST")
    print("="*70)
    
    # Load data
    data = load_pilot_data()
    
    # Create state matrix
    state_matrix = create_state_matrix(data)
    
    # Run regime detection
    results = run_regime_detection(state_matrix)
    
    # Analyze results
    stats, trans_matrix, persistence = analyze_results(results)
    
    # Create visualizations
    output_dir = Path(__file__).parent
    plot_regime_timeline(results, output_dir / 'regime_timeline.png')
    
    # Save results
    results.to_csv(output_dir / 'regime_results.csv')
    stats.to_csv(output_dir / 'regime_statistics.csv', index=False)
    trans_matrix.to_csv(output_dir / 'transition_matrix.csv')
    
    print("\n" + "="*70)
    print("PILOT TEST COMPLETE")
    print("="*70)
    print(f"Results saved to: {output_dir}")
    print("\nFiles created:")
    print("  - regime_results.csv       (full time series)")
    print("  - regime_statistics.csv    (summary stats)")
    print("  - transition_matrix.csv    (transition probs)")
    print("  - regime_timeline.png      (visualization)")


if __name__ == '__main__':
    main()
