"""
Phase I: Regime Detection Engine
=================================

Detects market regimes using multi-frequency geometric analysis.

Regime Types:
------------
1. BULL: Strong positive momentum, high coherence
2. BEAR: Strong negative momentum, high coherence  
3. TRANSITION: Low coherence, changing direction
4. CONSOLIDATION: Low magnitude, stable direction
5. CRISIS: Extreme magnitude, rapid rotation

Mathematical Approach:
---------------------
Uses vector geometry in normalized market space:
- Magnitude ||x(t)|| = market stress level
- Direction θ(t) = regime orientation
- Velocity v(t) = rate of change
- Coherence C(t) = alignment across frequencies

Multi-frequency analysis via KAM theory:
- Fast (1-3mo): Captures short-term momentum shifts
- Medium (6-12mo): Business cycle signals
- Slow (24-36mo): Secular trends
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import sys
from pathlib import Path

# Add math module to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'math'))

from vcf_geometry import GeometricAnalyzer
from vcf_coherence import CoherenceEngine
from vcf_normalization import VCFNormalizer

try:
    from .config import PILOT_INPUTS, FREQUENCY_BANDS, REGIME_THRESHOLDS
except ImportError:
    import config
    PILOT_INPUTS = config.PILOT_INPUTS
    FREQUENCY_BANDS = config.FREQUENCY_BANDS
    REGIME_THRESHOLDS = config.REGIME_THRESHOLDS


class MultiFrequencyRegimeDetector:
    """
    Multi-scale regime detection using geometric analysis.
    """
    
    def __init__(self, 
                 coherence_threshold: float = 0.3,
                 magnitude_percentiles: Tuple[float, float] = (33, 67)):
        """
        Initialize regime detector.
        
        Parameters:
        ----------
        coherence_threshold : float
            Minimum coherence for aligned regimes (default 0.3)
        magnitude_percentiles : tuple
            Percentile thresholds for low/high magnitude classification
        """
        self.coherence_threshold = coherence_threshold
        self.magnitude_percentiles = magnitude_percentiles

        # Initialize analysis engines
        self.geometry = GeometricAnalyzer()
        self.coherence = CoherenceEngine()
        self.normalizer = VCFNormalizer()
        
    def detect_regime(self, 
                      state_vector: np.ndarray,
                      history: pd.DataFrame,
                      lookback_windows: Dict[str, int] = None) -> Dict:
        """
        Detect current market regime from state vector and history.
        
        Parameters:
        ----------
        state_vector : np.ndarray
            Current normalized state [N dimensions]
        history : pd.DataFrame
            Historical normalized states (for multi-frequency analysis)
        lookback_windows : dict, optional
            Custom lookback periods for each frequency band
            
        Returns:
        -------
        dict with:
            - regime: str (BULL, BEAR, TRANSITION, CONSOLIDATION, CRISIS)
            - confidence: float (0-1)
            - metrics: dict of supporting metrics
            - frequencies: dict of regime by frequency band
        """
        if lookback_windows is None:
            lookback_windows = {
                'fast': FREQUENCY_BANDS['fast'][1],
                'medium': FREQUENCY_BANDS['medium'][1],
                'slow': FREQUENCY_BANDS['slow'][1]
            }
        
        # Get geometric metrics
        magnitude = np.linalg.norm(state_vector)
        direction = state_vector / (magnitude + 1e-10)
        
        # Calculate velocity (if history available)
        if len(history) > 1:
            prev_state = history.iloc[-2].values
            velocity = state_vector - prev_state
            speed = np.linalg.norm(velocity)
            
            # Rotation angle
            rotation = self._calculate_rotation(prev_state, state_vector)
        else:
            velocity = np.zeros_like(state_vector)
            speed = 0.0
            rotation = 0.0
        
        # Multi-frequency coherence analysis
        freq_regimes = {}
        freq_coherence = {}
        
        for freq_name, window in lookback_windows.items():
            if len(history) >= window:
                recent_history = history.iloc[-window:].values
                
                # Calculate coherence at this frequency
                coherence = self._calculate_coherence(recent_history)
                freq_coherence[freq_name] = coherence
                
                # Detect regime at this frequency
                freq_regime = self._classify_frequency_regime(
                    recent_history, coherence
                )
                freq_regimes[freq_name] = freq_regime
        
        # Determine overall regime
        regime, confidence = self._aggregate_regimes(
            freq_regimes, 
            magnitude,
            speed,
            rotation,
            freq_coherence
        )
        
        return {
            'regime': regime,
            'confidence': confidence,
            'metrics': {
                'magnitude': magnitude,
                'speed': speed,
                'rotation': rotation,
                'direction': direction.tolist(),
                'coherence_fast': freq_coherence.get('fast', np.nan),
                'coherence_medium': freq_coherence.get('medium', np.nan),
                'coherence_slow': freq_coherence.get('slow', np.nan),
            },
            'frequencies': freq_regimes
        }
    
    def _calculate_rotation(self, 
                           prev_state: np.ndarray, 
                           curr_state: np.ndarray) -> float:
        """Calculate rotation angle between consecutive states."""
        prev_norm = prev_state / (np.linalg.norm(prev_state) + 1e-10)
        curr_norm = curr_state / (np.linalg.norm(curr_state) + 1e-10)
        
        cos_angle = np.clip(np.dot(prev_norm, curr_norm), -1.0, 1.0)
        angle = np.arccos(cos_angle)
        
        return angle
    
    def _calculate_coherence(self, history: np.ndarray) -> float:
        """
        Calculate coherence across time series in history.

        Uses phase-locking value across all pairs of dimensions.
        """
        n_dims = history.shape[1]

        if n_dims < 2:
            return 1.0

        # Calculate pairwise phase locking
        plv_values = []

        for i in range(n_dims):
            for j in range(i + 1, n_dims):
                # Convert numpy arrays to pandas Series for coherence engine
                series_i = pd.Series(history[:, i])
                series_j = pd.Series(history[:, j])

                plv = self.coherence.phase_locking_value(series_i, series_j)
                plv_values.append(plv)

        # Average coherence across all pairs
        return np.mean(plv_values)
    
    def _classify_frequency_regime(self, 
                                   history: np.ndarray,
                                   coherence: float) -> str:
        """
        Classify regime at a specific frequency based on history.
        """
        # Calculate trend direction
        magnitudes = np.linalg.norm(history, axis=1)
        trend = np.polyfit(range(len(magnitudes)), magnitudes, 1)[0]
        
        # Mean direction
        mean_state = np.mean(history, axis=0)
        mean_direction = mean_state / (np.linalg.norm(mean_state) + 1e-10)
        
        # Classify based on trend and coherence
        if coherence > self.coherence_threshold:
            if trend > 0.01:  # Strong positive trend
                return 'BULL'
            elif trend < -0.01:  # Strong negative trend
                return 'BEAR'
            else:
                return 'CONSOLIDATION'
        else:
            return 'TRANSITION'
    
    def _aggregate_regimes(self,
                          freq_regimes: Dict[str, str],
                          magnitude: float,
                          speed: float,
                          rotation: float,
                          freq_coherence: Dict[str, float]) -> Tuple[str, float]:
        """
        Aggregate multi-frequency regimes into overall regime.
        
        Returns (regime_name, confidence)
        """
        # Check for crisis conditions first
        if magnitude > 2.5 or speed > 1.0 or rotation > np.pi/3:
            return 'CRISIS', 0.9
        
        # Count regime votes
        regime_votes = {}
        for freq, regime in freq_regimes.items():
            regime_votes[regime] = regime_votes.get(regime, 0) + 1
        
        if not regime_votes:
            return 'UNKNOWN', 0.0
        
        # Get most common regime
        primary_regime = max(regime_votes, key=regime_votes.get)
        agreement = regime_votes[primary_regime] / len(freq_regimes)
        
        # Confidence based on:
        # 1. Agreement across frequencies
        # 2. Average coherence
        avg_coherence = np.mean(list(freq_coherence.values()))
        confidence = (agreement + avg_coherence) / 2
        
        return primary_regime, confidence
    
    def detect_regime_transitions(self,
                                  history: pd.DataFrame,
                                  regime_column: str = 'regime') -> pd.DataFrame:
        """
        Detect regime change points in historical data.
        
        Returns DataFrame with transition dates and regime changes.
        """
        regimes = history[regime_column]
        transitions = []
        
        for i in range(1, len(regimes)):
            if regimes.iloc[i] != regimes.iloc[i-1]:
                transitions.append({
                    'date': history.index[i],
                    'from_regime': regimes.iloc[i-1],
                    'to_regime': regimes.iloc[i],
                    'duration_days': (history.index[i] - history.index[i-1]).days
                })
        
        return pd.DataFrame(transitions)
