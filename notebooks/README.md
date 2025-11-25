# Notebooks

This directory contains Jupyter notebooks for research, analysis, and visualization of VCF (Vector Coherence Framework) data.

## Contents

- **VFC_Mathematical_Engine_Claud.ipynb**: Core mathematical engine for VCF calculations, including theta (θ), phi (φ), and coherence computations
- **Visualization_Suite_Claud.ipynb**: Visualization tools and charts for analyzing VCF outputs
- **Visualization_Suite_Copilot_Edit.ipynb**: Enhanced visualization suite with additional features

## Usage

### Running in Google Colab

1. Open the notebook in [Google Colab](https://colab.research.google.com/)
2. Mount your Google Drive if needed:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
3. Install required dependencies (usually handled automatically in notebook cells)
4. Run cells sequentially to execute analysis

### Running Locally

1. Install Jupyter:
   ```bash
   pip install jupyter notebook
   ```
2. Launch Jupyter:
   ```bash
   jupyter notebook
   ```
3. Navigate to the notebook and run

## Dependencies

Common dependencies used across notebooks:
- pandas
- numpy
- matplotlib
- scipy
- yfinance (for market data)
- pandas-datareader (for economic data)

## Integration with Repository

- **Data Input**: Notebooks read from `/data_raw/` and `/data_clean/` directories
- **Data Output**: Processed data should be written to `/data_clean/` or `/geometry/`
- **Code Modules**: Import reusable functions from `/src/` directory
- **Scripts**: Leverage scripts from `/scripts/` for data processing tasks

## Best Practices

- Keep notebooks focused on specific analyses or workflows
- Document your analysis with markdown cells
- Use clear variable names and add comments for complex operations
- Save intermediate results to appropriate data directories
- Track significant findings in `/docs/log.md`
