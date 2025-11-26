"""
VCF Package
Provides the top-level access for the Vector Cycle Framework (VCF):
- Normalization engine
- Coherence analysis
- Geometric analysis
- Main pipeline

This __init__ exposes clean imports so users can write:
    from vcf import run_vcf
    from vcf import GeometricAnalyzer
"""

# === Normalization ===
from .core.vcf_normalization import (
    VCFNormalizer,
)

# === Coherence & Phase Analysis ===
from .core.vcf_coherence import (
    CoherenceEngine,
    PhaseLockingAnalysis,
)

# === Geometry / Regime Analysis ===
from .core.vcf_geometry import (
    GeometricAnalyzer,
    RegimeDetector,
)

# === Main Pipeline ===
from .core.vcf_main import (
    run_vcf,
    VCFPipeline,
)

__all__ = [
    "VCFNormalizer",
    "CoherenceEngine",
    "PhaseLockingAnalysis",
    "GeometricAnalyzer",
    "RegimeDetector",
    "run_vcf",
    "VCFPipeline",
]
