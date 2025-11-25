"""
VCF Data Module
===============

Data loading and preprocessing:
- data_loader: Load data from FRED, Yahoo, etc.
- build_macro_panel: Construct macro panels
"""

# Import when available
try:
    from .data_loader import load_fred_data
    from .build_macro_panel import build_panel
    __all__ = ['load_fred_data', 'build_panel']
except ImportError:
    __all__ = []
