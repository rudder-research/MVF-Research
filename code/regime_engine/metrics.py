"""
Phase I: Regime Metrics
=======================

Comprehensive metrics for regime characterization and validation.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from scipy import stats


class RegimeMetrics:
    """
    Calculate and track regime-specific performance metrics.
    """
    
    @staticmethod
    def regime_statistics(history: pd.DataFrame,
                         regime_column: str = 'regime') -> pd.DataFrame:
        """
        Calculate statistics for each regime type.
        
        Returns DataFrame with:
        - count: number of occurrences
        - duration_mean: average duration (days)
        - duration_std: duration standard deviation
        - magnitude_mean: average market stress
        - coherence_mean: average alignment
        """
        regimes = history[regime_column].unique()
        stats_list = []
        
        for regime in regimes:
            regime_mask = history[regime_column] == regime
            regime_data = history[regime_mask]
            
            # Calculate durations
            durations = []
            current_duration = 1
            
            for i in range(1, len(history)):
                if history[regime_column].iloc[i] == regime:
                    if history[regime_column].iloc[i-1] == regime:
                        current_duration += 1
                    else:
                        current_duration = 1
                elif history[regime_column].iloc[i-1] == regime:
                    durations.append(current_duration)
                    current_duration = 1
            
            stats_list.append({
                'regime': regime,
                'count': regime_mask.sum(),
                'frequency': regime_mask.sum() / len(history),
                'duration_mean': np.mean(durations) if durations else np.nan,
                'duration_std': np.std(durations) if durations else np.nan,
                'magnitude_mean': regime_data['magnitude'].mean() if 'magnitude' in regime_data.columns else np.nan,
                'coherence_mean': regime_data.get('coherence_medium', pd.Series([np.nan])).mean(),
            })
        
        return pd.DataFrame(stats_list)
    
    @staticmethod
    def transition_matrix(history: pd.DataFrame,
                         regime_column: str = 'regime') -> pd.DataFrame:
        """
        Calculate regime transition probability matrix.
        
        Returns DataFrame showing P(to_regime | from_regime)
        """
        regimes = history[regime_column]
        unique_regimes = sorted(regimes.unique())
        
        # Count transitions
        transitions = np.zeros((len(unique_regimes), len(unique_regimes)))
        regime_to_idx = {r: i for i, r in enumerate(unique_regimes)}
        
        for i in range(1, len(regimes)):
            from_regime = regimes.iloc[i-1]
            to_regime = regimes.iloc[i]
            from_idx = regime_to_idx[from_regime]
            to_idx = regime_to_idx[to_regime]
            transitions[from_idx, to_idx] += 1
        
        # Normalize to probabilities
        row_sums = transitions.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        transition_probs = transitions / row_sums
        
        return pd.DataFrame(
            transition_probs,
            index=unique_regimes,
            columns=unique_regimes
        )
    
    @staticmethod
    def regime_persistence(history: pd.DataFrame,
                          regime_column: str = 'regime') -> Dict[str, float]:
        """
        Calculate persistence (autocorrelation) for each regime.
        
        Higher values = regime tends to persist longer
        """
        regimes = history[regime_column]
        unique_regimes = regimes.unique()
        
        persistence = {}
        
        for regime in unique_regimes:
            regime_binary = (regimes == regime).astype(int)
            
            if len(regime_binary) > 1:
                # Calculate lag-1 autocorrelation
                autocorr = regime_binary.autocorr(lag=1)
                persistence[regime] = autocorr
            else:
                persistence[regime] = np.nan
        
        return persistence
    
    @staticmethod
    def forecast_accuracy(predicted: pd.Series,
                         actual: pd.Series) -> Dict[str, float]:
        """
        Evaluate regime prediction accuracy.
        
        Returns:
        - accuracy: overall correct predictions
        - precision: by regime
        - recall: by regime  
        - f1: harmonic mean of precision/recall
        """
        from sklearn.metrics import accuracy_score, precision_recall_fscore_support
        
        accuracy = accuracy_score(actual, predicted)
        precision, recall, f1, support = precision_recall_fscore_support(
            actual, predicted, average='weighted', zero_division=0
        )
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
