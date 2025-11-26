# notebooks/ — Exploratory / Experimental Work

## Subfolders

- `exploration/` → rough early work, initial investigations
- `experiments/` → structured testing and analysis
- `deprecated/` → retired notebooks

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

## Integration with Repository

- **Data Input**: Notebooks read from `code/data_normalized/` directory
- **Data Output**: Processed data should be written to `outputs/`
- **Code Modules**: Import reusable functions from `code/math/` and `code/shared/`
- **Pilots**: Use `pilots/` for structured math experiments
