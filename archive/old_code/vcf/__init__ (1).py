"""
VCF - Vector Coherence Framework
=================================

A geometric approach to market regime analysis.

Modules:
--------
- core: Main analysis engines (normalization, coherence, geometry)
- data: Data loading and preprocessing
- utils: Utility functions and visualizations
- analysis: High-level analysis workflows
"""

__version__ = '1.0.0'
__author__ = 'Jason Rudder'

# Import key functions for easy access
from .core.pipeline import VCFPipeline, quick_analysis

__all__ = ['VCFPipeline', 'quick_analysis']
