"""
VCF Framework - Comprehensive Test Script
==========================================

This script tests all VCF modules to ensure everything works correctly.
Run this in Google Colab after uploading the VCF modules.

Usage in Colab:
--------------
1. Upload all vcf_*.py files to Colab
2. Run this script
3. Check that all tests pass
"""

import numpy as np
import pandas as pd
import sys

print("=" * 70)
print("VCF FRAMEWORK - COMPREHENSIVE TEST SUITE")
print("=" * 70)

# Test 1: Import all modules
print("\n[TEST 1] Importing all VCF modules...")
try:
    from vcf_normalization import VCFNormalizer, create_state_matrix
    from vcf_coherence import CoherenceEngine, PhaseLockingAnalysis
    from vcf_geometry import GeometricAnalyzer, RegimeDetector
    from vcf_main import VCFPipeline, quick_analysis
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Create synthetic test data
print("\n[TEST 2] Creating synthetic test data...")
np.random.seed(42)
dates = pd.date_range('2010-01-01', periods=120, freq='M')

# Create 4 different market signals
gdp = pd.Series(
    100 + np.cumsum(np.random.randn(120) * 0.5),
    index=dates,
    name='GDP'
)

sp500 = pd.Series(
    1000 + np.cumsum(np.random.randn(120) * 20),
    index=dates,
    name='SP500'
)

treasury = pd.Series(
    3.5 + 2 * np.sin(np.linspace(0, 8*np.pi, 120)) + np.random.randn(120) * 0.3,
    index=dates,
    name='Treasury10Y'
)

vix = pd.Series(
    15 + 10 * np.abs(np.sin(np.linspace(0, 6*np.pi, 120))) + np.random.randn(120) * 2,
    index=dates,
    name='VIX'
)

market_data = {
    'GDP': gdp,
    'SP500': sp500,
    'Treasury10Y': treasury,
    'VIX': vix
}
print("✓ Test data created (4 sources, 120 months)")

# Test 3: Normalization
print("\n[TEST 3] Testing normalization...")
try:
    normalizer = VCFNormalizer(ma_window=12, roc_window=1)
    state_matrix = create_state_matrix(market_data, normalizer)
    
    assert state_matrix.shape[1] == 8, "Should have 8 columns (4 sources × 2)"
    assert state_matrix.shape[0] <= 120, "Should have ≤120 rows"
    assert not state_matrix.isna().all().any(), "No all-NaN columns"
    
    print(f"✓ Normalization successful: {state_matrix.shape}")
    print(f"  Columns: {list(state_matrix.columns)}")
except Exception as e:
    print(f"✗ Normalization failed: {e}")
    sys.exit(1)

# Test 4: Coherence Engine
print("\n[TEST 4] Testing coherence analysis...")
try:
    engine = CoherenceEngine(sampling_freq=12.0)
    
    # Test Hilbert phase
    phase = engine.hilbert_phase(sp500)
    assert len(phase) == len(sp500), "Phase length mismatch"
    assert phase.min() >= -np.pi and phase.max() <= np.pi, "Phase out of range"
    
    # Test PLV
    plv = engine.phase_locking_value(sp500, gdp)
    assert 0 <= plv <= 1, "PLV out of range"
    
    # Test Kuramoto
    phases_df = state_matrix.apply(lambda x: engine.hilbert_phase(x), axis=0)
    kuramoto = engine.kuramoto_order_parameter(phases_df)
    assert len(kuramoto) == len(state_matrix), "Kuramoto length mismatch"
    assert kuramoto.min() >= 0 and kuramoto.max() <= 1, "Kuramoto out of range"
    
    print(f"✓ Coherence engine works")
    print(f"  Sample PLV: {plv:.3f}")
    print(f"  Mean Kuramoto order: {kuramoto.mean():.3f}")
except Exception as e:
    print(f"✗ Coherence test failed: {e}")
    sys.exit(1)

# Test 5: Geometric Analysis
print("\n[TEST 5] Testing geometric analysis...")
try:
    analyzer = GeometricAnalyzer()
    
    # Test magnitude
    magnitude = analyzer.magnitude(state_matrix)
    assert len(magnitude) == len(state_matrix), "Magnitude length mismatch"
    assert magnitude.min() >= 0, "Magnitude should be non-negative"
    
    # Test rotation
    rotation = analyzer.angular_rotation(state_matrix)
    assert len(rotation) == len(state_matrix), "Rotation length mismatch"
    
    # Test PCA
    pca_proj, pca_model = analyzer.pca_projection(state_matrix, n_components=3)
    assert pca_proj.shape[1] == 3, "Should have 3 components"
    
    print(f"✓ Geometric analysis works")
    print(f"  Mean magnitude: {magnitude.mean():.3f}")
    print(f"  Mean rotation: {rotation.mean():.3f} rad")
    print(f"  PCA explained variance: {pca_model.explained_variance_ratio_.sum():.3f}")
except Exception as e:
    print(f"✗ Geometric test failed: {e}")
    sys.exit(1)

# Test 6: Regime Detection
print("\n[TEST 6] Testing regime detection...")
try:
    detector = RegimeDetector(analyzer)
    
    # Compute signals
    signals = detector.compute_regime_signals(state_matrix)
    assert signals.shape[0] == len(state_matrix), "Signals length mismatch"
    assert signals.shape[1] >= 5, "Should have at least 5 signals"
    
    # Classify regimes
    regimes = detector.classify_regime(signals)
    assert len(regimes) == len(state_matrix), "Regimes length mismatch"
    
    # Detect changes
    changes = detector.detect_regime_changes(regimes)
    
    print(f"✓ Regime detection works")
    print(f"  Regime distribution:")
    for regime, count in regimes.value_counts().items():
        print(f"    {regime}: {count} ({count/len(regimes)*100:.1f}%)")
    print(f"  Regime changes detected: {changes.sum()}")
except Exception as e:
    print(f"✗ Regime detection failed: {e}")
    sys.exit(1)

# Test 7: Complete Pipeline
print("\n[TEST 7] Testing complete pipeline...")
try:
    pipeline = VCFPipeline(ma_window=12, roc_window=1, sampling_freq=12.0)
    results = pipeline.run_analysis(market_data)
    
    # Verify all expected keys exist
    expected_keys = [
        'state_matrix', 'coherence_matrix', 'kuramoto_order',
        'magnitude', 'rotation', 'divergence', 'regimes'
    ]
    
    for key in expected_keys:
        assert key in results, f"Missing key: {key}"
    
    print(f"✓ Complete pipeline works")
    print(f"  Results keys: {len(results)}")
except Exception as e:
    print(f"✗ Pipeline test failed: {e}")
    sys.exit(1)

# Test 8: Quick Analysis
print("\n[TEST 8] Testing quick_analysis function...")
try:
    results = quick_analysis(market_data)
    
    assert 'regimes' in results, "Missing regimes"
    assert 'coherence_matrix' in results, "Missing coherence_matrix"
    assert 'state_matrix' in results, "Missing state_matrix"
    
    print(f"✓ Quick analysis works")
except Exception as e:
    print(f"✗ Quick analysis failed: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 70)
print("ALL TESTS PASSED ✓")
print("=" * 70)
print("\nVCF Framework is working correctly!")
print("\nNext steps:")
print("1. Load your actual market data")
print("2. Run: results = quick_analysis(your_data)")
print("3. Explore results['regimes'], results['coherence_matrix'], etc.")
print("4. Export: pipeline.export_results()")
print("\n" + "=" * 70)
