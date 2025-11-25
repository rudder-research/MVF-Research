"""
Regime Engine Configuration
"""

PILOT_INPUTS = [
    'SPY_50d_200d_MA',
    'DGS10',
    'DXY',
    'AGG'
]

FREQUENCY_BANDS = {
    'fast': (1, 3),
    'medium': (6, 12),
    'slow': (24, 36)
}

REGIME_THRESHOLDS = {
    'coherence_min': 0.3,
    'phase_lock_tolerance': 0.2,
}
