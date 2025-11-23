# Source Code (src)

This directory contains reusable Python modules and libraries for the VCF Research project.

## Overview

The `/src/` directory houses core functionality that is used across multiple notebooks and scripts. These modules provide:
- Advanced mathematical functions
- Visualization utilities
- Common data processing functions
- Shared constants and configurations

## Current Modules

### vcf_advanced_math.py
Advanced mathematical functions for VCF analysis including:
- Vector operations and transformations
- Geometric calculations (theta, phi, coherence)
- Statistical functions for normalized data
- Time series analysis utilities
- Harmonic analysis functions

### vcf_visualizations.py
Visualization tools and plotting functions:
- Standard VCF charts and plots
- Geometric visualization (vector plots, phase diagrams)
- Time series visualization
- Multi-dimensional data displays
- Interactive plotting utilities

## Usage

### Importing Modules

From notebooks or scripts:

```python
# Add src to path if needed
import sys
sys.path.append('/path/to/VCF-RESEARCH')

# Import modules
from src.vcf_advanced_math import compute_theta, compute_phi
from src.vcf_visualizations import plot_coherence, plot_vectors
```

### In Colab

```python
# Mount drive and navigate to repo
from google.colab import drive
drive.mount('/content/drive')

import sys
sys.path.append('/content/drive/MyDrive/VCF-RESEARCH')

from src.vcf_advanced_math import *
from src.vcf_visualizations import *
```

## Development Guidelines

### Adding New Modules

When creating new reusable code:

1. **Create a new Python file** in this directory
2. **Use clear naming**: `vcf_{functionality}.py`
3. **Add docstrings**: Document all functions and classes
4. **Include examples**: Add usage examples in docstrings
5. **Update this README**: Document the new module

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write comprehensive docstrings (Google or NumPy style)
- Add unit tests if applicable
- Keep functions focused and modular

### Example Function Template

```python
def example_function(param1: float, param2: str) -> dict:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Example:
        >>> result = example_function(3.14, "test")
        >>> print(result)
        {'status': 'success'}
    """
    # Function implementation
    return {'status': 'success'}
```

## Dependencies

Common dependencies across modules:
- numpy
- pandas
- scipy
- matplotlib
- seaborn (for visualizations)

Install with:
```bash
pip install numpy pandas scipy matplotlib seaborn
```

## Module Organization

As the project grows, consider organizing into subdirectories:

```
src/
├── math/
│   ├── geometry.py
│   ├── statistics.py
│   └── timeseries.py
├── visualization/
│   ├── plots.py
│   ├── charts.py
│   └── interactive.py
└── utils/
    ├── data.py
    └── helpers.py
```

## Integration with Project

These modules are used by:
- **Notebooks** in `/notebooks/` for analysis and visualization
- **Scripts** in `/scripts/` for data processing
- **Geometry engine** in `/geometry/` for calculations

## Best Practices

- **Keep it DRY**: Don't Repeat Yourself - put common code here
- **Maintain backward compatibility**: When updating functions, preserve existing interfaces
- **Version important changes**: Document breaking changes in `/docs/log.md`
- **Test before committing**: Ensure changes don't break existing notebooks/scripts
- **Document thoroughly**: Good documentation makes code reusable

## Future Enhancements

Potential additions:
- Unit testing framework
- Performance optimization for large datasets
- Additional geometric metrics
- Machine learning utilities
- Data validation functions
- Configuration management
