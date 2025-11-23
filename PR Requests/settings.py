"""
General Settings for VCF Project

Configuration parameters and constants used throughout the project.
"""

# Normalization settings
NORMALIZATION_METHOD = "zscore"  # Options: "zscore", "minmax", "robust"
CLIP_BOUNDS = (-3, 3)  # Bounds for clipping outliers
ROLLING_WINDOW = 252  # Default rolling window (trading days in a year)

# Vector dimensions
STATE_VECTOR_DIM = 7  # Dimensionality of the macro-financial state vector

# Geometry engine settings
THETA_RANGE = (0, 180)  # Polar angle range in degrees
PHI_RANGE = (0, 360)   # Azimuthal angle range in degrees

# Harmonic analysis settings
N_HARMONICS = 5  # Number of harmonics for decomposition
COHERENCE_WINDOW = 60  # Window for coherence computation

# Data fetching settings
DEFAULT_START_DATE = "2000-01-01"
DEFAULT_END_DATE = None  # None means current date

# API keys (to be set via environment variables)
FRED_API_KEY_ENV = "FRED_API_KEY"
ALPHA_VANTAGE_API_KEY_ENV = "ALPHA_VANTAGE_API_KEY"

# Visualization settings
DEFAULT_FIGSIZE = (12, 6)
DEFAULT_DPI = 100
COLOR_PALETTE = "viridis"

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Random seed for reproducibility
RANDOM_SEED = 42
