import io
import zipfile
import csv
from datetime import datetime, timedelta

# Generate sample data
def generate_sample_data():
    """Generate simple sample datasets for testing"""
    dates = [(datetime(2024, 1, 1) + timedelta(days=i)).strftime('%Y-%m-%d') 
             for i in range(100)]
    
    # S&P 500 data with 50-day and 200-day MAs
    sp500_data = []
    for i, date in enumerate(dates):
        price = 4500 + i * 10 + (i % 10) * 5
        ma50 = price * 0.98
        ma200 = price * 0.95
        sp500_data.append([date, price, ma50, ma200])
    
    # 10-Year Treasury Yield
    treasury_data = [[date, 4.0 + (i % 20) * 0.05] for i, date in enumerate(dates)]
    
    # VIX
    vix_data = [[date, 15 + (i % 15) * 0.5] for i, date in enumerate(dates)]
    
    # DXY
    dxy_data = [[date, 103 + (i % 10) * 0.3] for i, date in enumerate(dates)]
    
    return sp500_data, treasury_data, vix_data, dxy_data

# Create ZIP archive in memory
zip_buffer = io.BytesIO()

with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
    
    # README
    readme = """VCF Research - Limited 4-Input Prototype
Process-Only Trial
==========================================

OVERVIEW
--------
This is a minimal prototype pipeline designed to test workflow structure,
file organization, and ZIP packaging compatibility with GitHub processes.

This is NOT the full VCF Geometry Engine.
This prototype contains NO advanced modeling, forecasting, or geometric analysis.

INPUTS
------
1. S&P 500 - 50-day / 200-day moving average ratio
2. 10-Year Treasury Yield
3. VIX (Volatility Index)
4. DXY (US Dollar Index)

FOLDER STRUCTURE
----------------
data/raw/          - Original input datasets
scripts/           - Python processing modules
outputs/           - Final state vectors CSV
README.txt         - This file

SCRIPTS
-------
load_data.py       - Loads raw data files
compute_ratio.py   - Computes S&P 500 MA ratio
normalize.py       - Normalizes all inputs to 0-1 scale
assemble.py        - Combines inputs into state vectors

HOW TO RUN
----------
1. Ensure Python 3.x is installed
2. Navigate to the project directory
3. Run scripts in order:
   python scripts/load_data.py
   python scripts/compute_ratio.py
   python scripts/normalize.py
   python scripts/assemble.py

4. Output will be saved to: outputs/state_vectors.csv

NOTES
-----
- All math is intentionally basic (linear scaling)
- No complex modeling or forecasting included
- This is a process verification test only
- Full VCF implementation will follow in next phase

Date: 2024-11-22
"""
    zf.writestr('vcf_prototype/README.txt', readme)
    
    # Generate and save sample data
    sp500_data, treasury_data, vix_data, dxy_data = generate_sample_data()
    
    # S&P 500 data
    sp500_csv = io.StringIO()
    writer = csv.writer(sp500_csv)
    writer.writerow(['date', 'price', 'ma_50', 'ma_200'])
    writer.writerows(sp500_data)
    zf.writestr('vcf_prototype/data/raw/sp500_ma.csv', sp500_csv.getvalue())
    
    # Treasury data
    treasury_csv = io.StringIO()
    writer = csv.writer(treasury_csv)
    writer.writerow(['date', 'yield'])
    writer.writerows(treasury_data)
    zf.writestr('vcf_prototype/data/raw/treasury_10y.csv', treasury_csv.getvalue())
    
    # VIX data
    vix_csv = io.StringIO()
    writer = csv.writer(vix_csv)
    writer.writerow(['date', 'vix'])
    writer.writerows(vix_data)
    zf.writestr('vcf_prototype/data/raw/vix.csv', vix_csv.getvalue())
    
    # DXY data
    dxy_csv = io.StringIO()
    writer = csv.writer(dxy_csv)
    writer.writerow(['date', 'dxy'])
    writer.writerows(dxy_data)
    zf.writestr('vcf_prototype/data/raw/dxy.csv', dxy_csv.getvalue())
    
    # Script 1: Load Data
    load_script = """import csv

def load_csv(filepath):
    \"\"\"Load CSV file and return data as list of dictionaries\"\"\"
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def load_all_data():
    \"\"\"Load all four input datasets\"\"\"
    sp500 = load_csv('data/raw/sp500_ma.csv')
    treasury = load_csv('data/raw/treasury_10y.csv')
    vix = load_csv('data/raw/vix.csv')
    dxy = load_csv('data/raw/dxy.csv')
    
    print(f"Loaded {len(sp500)} S&P 500 records")
    print(f"Loaded {len(treasury)} Treasury records")
    print(f"Loaded {len(vix)} VIX records")
    print(f"Loaded {len(dxy)} DXY records")
    
    return sp500, treasury, vix, dxy

if __name__ == '__main__':
    load_all_data()
"""
    zf.writestr('vcf_prototype/scripts/load_data.py', load_script)
    
    # Script 2: Compute Ratio
    compute_script = """import csv

def compute_ma_ratio(sp500_data):
    \"\"\"Compute 50-day / 200-day moving average ratio\"\"\"
    ratios = []
    for row in sp500_data:
        date = row['date']
        ma50 = float(row['ma_50'])
        ma200 = float(row['ma_200'])
        ratio = ma50 / ma200 if ma200 != 0 else 1.0
        ratios.append({'date': date, 'ma_ratio': ratio})
    
    print(f"Computed {len(ratios)} MA ratios")
    return ratios

if __name__ == '__main__':
    from load_data import load_all_data
    sp500, _, _, _ = load_all_data()
    compute_ma_ratio(sp500)
"""
    zf.writestr('vcf_prototype/scripts/compute_ratio.py', compute_script)
    
    # Script 3: Normalize
    normalize_script = """def normalize_values(values):
    \"\"\"Simple linear normalization to 0-1 range\"\"\"
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val
    
    if range_val == 0:
        return [0.5] * len(values)
    
    return [(v - min_val) / range_val for v in values]

def normalize_all_inputs(ma_ratios, treasury, vix, dxy):
    \"\"\"Normalize all four inputs to 0-1 scale\"\"\"
    
    # Extract values
    ratio_vals = [float(r['ma_ratio']) for r in ma_ratios]
    treasury_vals = [float(t['yield']) for t in treasury]
    vix_vals = [float(v['vix']) for v in vix]
    dxy_vals = [float(d['dxy']) for d in dxy]
    
    # Normalize
    norm_ratios = normalize_values(ratio_vals)
    norm_treasury = normalize_values(treasury_vals)
    norm_vix = normalize_values(vix_vals)
    norm_dxy = normalize_values(dxy_vals)
    
    print("Normalized all inputs to 0-1 range")
    
    return norm_ratios, norm_treasury, norm_vix, norm_dxy

if __name__ == '__main__':
    from load_data import load_all_data
    from compute_ratio import compute_ma_ratio
    
    sp500, treasury, vix, dxy = load_all_data()
    ma_ratios = compute_ma_ratio(sp500)
    normalize_all_inputs(ma_ratios, treasury, vix, dxy)
"""
    zf.writestr('vcf_prototype/scripts/normalize.py', normalize_script)
    
    # Script 4: Assemble
    assemble_script = """import csv

def assemble_state_vectors(dates, norm_ratios, norm_treasury, norm_vix, norm_dxy):
    \"\"\"Combine normalized inputs into state vectors\"\"\"
    vectors = []
    
    for i, date in enumerate(dates):
        vector = {
            'date': date,
            'sp500_ma_ratio': round(norm_ratios[i], 6),
            'treasury_10y': round(norm_treasury[i], 6),
            'vix': round(norm_vix[i], 6),
            'dxy': round(norm_dxy[i], 6)
        }
        vectors.append(vector)
    
    return vectors

def save_state_vectors(vectors, output_path='outputs/state_vectors.csv'):
    \"\"\"Save state vectors to CSV\"\"\"
    import os
    os.makedirs('outputs', exist_ok=True)
    
    with open(output_path, 'w', newline='') as f:
        fieldnames = ['date', 'sp500_ma_ratio', 'treasury_10y', 'vix', 'dxy']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(vectors)
    
    print(f"Saved {len(vectors)} state vectors to {output_path}")

if __name__ == '__main__':
    from load_data import load_all_data
    from compute_ratio import compute_ma_ratio
    from normalize import normalize_all_inputs
    
    # Load and process
    sp500, treasury, vix, dxy = load_all_data()
    ma_ratios = compute_ma_ratio(sp500)
    norm_ratios, norm_treasury, norm_vix, norm_dxy = normalize_all_inputs(
        ma_ratios, treasury, vix, dxy
    )
    
    # Assemble and save
    dates = [row['date'] for row in sp500]
    vectors = assemble_state_vectors(dates, norm_ratios, norm_treasury, norm_vix, norm_dxy)
    save_state_vectors(vectors)
"""
    zf.writestr('vcf_prototype/scripts/assemble.py', assemble_script)
    
    # Generate sample output
    output_csv = io.StringIO()
    writer = csv.writer(output_csv)
    writer.writerow(['date', 'sp500_ma_ratio', 'treasury_10y', 'vix', 'dxy'])
    
    # Simple normalized sample values
    for i in range(100):
        date = (datetime(2024, 1, 1) + timedelta(days=i)).strftime('%Y-%m-%d')
        writer.writerow([
            date,
            round(0.3 + (i % 50) * 0.01, 6),
            round(0.2 + (i % 40) * 0.015, 6),
            round(0.15 + (i % 30) * 0.02, 6),
            round(0.4 + (i % 20) * 0.02, 6)
        ])
    
    zf.writestr('vcf_prototype/outputs/state_vectors.csv', output_csv.getvalue())

# Save ZIP to file
zip_buffer.seek(0)
with open('vcf_prototype.zip', 'wb') as f:
    f.write(zip_buffer.read())

print("✓ VCF 4-Input Prototype ZIP created successfully")
print("✓ Package: vcf_prototype.zip")
print("✓ Contents:")
print("  - README.txt")
print("  - 4 sample datasets (data/raw/)")
print("  - 4 Python scripts (scripts/)")
print("  - Output state vectors (outputs/state_vectors.csv)")