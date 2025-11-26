"""
Path Configuration for VCF Project

Centralized path management for all data, output, and resource directories.
"""
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEAN_DATA_DIR = DATA_DIR / "clean"
INTERIM_DATA_DIR = DATA_DIR / "interim"

# Documentation directories
DOCS_DIR = PROJECT_ROOT / "docs"
SPECS_DIR = DOCS_DIR / "specs"
PROPOSALS_DIR = DOCS_DIR / "proposals"
REFERENCES_DIR = DOCS_DIR / "references"

# Notebook directories
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
EXPLORATION_DIR = NOTEBOOKS_DIR / "exploration"
PIPELINE_DIR = NOTEBOOKS_DIR / "pipeline"
VIZ_DIR = NOTEBOOKS_DIR / "viz"

# Registry directory
REGISTRY_DIR = PROJECT_ROOT / "registry"
METRIC_REGISTRY_PATH = REGISTRY_DIR / "metric_registry.json"
ALIASES_PATH = REGISTRY_DIR / "aliases.json"

# Visual outputs
VISUALS_DIR = PROJECT_ROOT / "visuals"
PLOTS_DIR = VISUALS_DIR / "plots"
DASHBOARDS_DIR = VISUALS_DIR / "dashboards"

# Source code
SRC_DIR = PROJECT_ROOT / "src"

# Tests
TESTS_DIR = PROJECT_ROOT / "tests"


def ensure_directories():
    """
    Create all necessary directories if they don't exist.
    """
    directories = [
        RAW_DATA_DIR, CLEAN_DATA_DIR, INTERIM_DATA_DIR,
        SPECS_DIR, PROPOSALS_DIR, REFERENCES_DIR,
        EXPLORATION_DIR, PIPELINE_DIR, VIZ_DIR,
        REGISTRY_DIR, PLOTS_DIR, DASHBOARDS_DIR, TESTS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
