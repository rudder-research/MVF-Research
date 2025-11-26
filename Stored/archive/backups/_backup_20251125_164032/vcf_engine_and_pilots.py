# vcf_engine_and_pilots.py
# This script creates geometry engine modules and pilot analysis scripts
# inside /content/VCF-RESEARCH/src (when run in Google Colab).

import os

base = "/content/VCF-RESEARCH/src"
analysis = base + "/analysis"
geom = base + "/geometry_engine"

os.makedirs(analysis, exist_ok=True)
os.makedirs(geom, exist_ok=True)

def write(path, lines):
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")

# Geometry engine modules
write(geom + "/__init__.py", [
    '"""Geometry Engine for VCF"""'
])

write(geom + "/normalize.py", [
    "import pandas as pd",
    "",
    "def zscore(df):",
    "    return (df - df.mean()) / df.std(ddof=0)",
    "",
    "def minmax(df, low=0.0, high=1.0):",
    "    data_min = df.min()",
    "    data_max = df.max()",
    "    scale = (high - low) / (data_max - data_min)",
    "    return (df - data_min) * scale + low",
    "",
    "def center(df):",
    "    return df - df.mean()"
])

write(geom + "/magnitude.py", [
    "import numpy as np",
    "import pandas as pd",
    "",
    "def rowwise_magnitude(df):",
    "    vals = df.values",
    "    mags = np.linalg.norm(vals, axis=1)",
    "    return pd.Series(mags, index=df.index, name='magnitude')"
])

write(geom + "/angles.py", [
    "import numpy as np",
    "import pandas as pd",
    "",
    "def cosine_similarity(a, b):",
    "    x = a.values",
    "    y = b.values",
    "    num = np.dot(x, y)",
    "    den = np.linalg.norm(x) * np.linalg.norm(y)",
    "    if den == 0:",
    "        return 0.0",
    "    return float(num / den)",
    "",
    "def angle_between(a, b):",
    "    c = cosine_similarity(a, b)",
    "    c = max(min(c, 1.0), -1.0)",
    "    return float(np.arccos(c))",
    "",
    "def pairwise_angle_matrix(df):",
    "    cols = df.columns",
    "    n = len(cols)",
    "    mat = np.zeros((n, n))",
    "    for i in range(n):",
    "        for j in range(n):",
    "            mat[i,j] = angle_between(df[cols[i]], df[cols[j]])",
    "    return pd.DataFrame(mat, index=cols, columns=cols)"
])

write(geom + "/harmonics.py", [
    "import numpy as np",
    "import pandas as pd",
    "",
    "def fft_series(series):",
    "    x = series.values.astype(float)",
    "    n = len(x)",
    "    f = np.fft.rfft(x)",
    "    freq = np.fft.rfftfreq(n, d=1.0)",
    "    amp = np.abs(f) / n",
    "    return freq, amp",
    "",
    "def dominant_frequencies(series, k=5):",
    "    freq, amp = fft_series(series)",
    "    idx = np.argsort(amp)[::-1][:k]",
    "    return freq[idx], amp[idx]"
])

write(geom + "/state_space.py", [
    "import pandas as pd",
    "",
    "def assemble_state(d):",
    "    parts = []",
    "    for name, obj in d.items():",
    "        if isinstance(obj, pd.Series):",
    "            parts.append(obj.to_frame(name=name))",
    "        elif isinstance(obj, pd.DataFrame):",
    "            tmp = obj.copy()",
    "            tmp.columns = [f'{name}_{c}' for c in tmp.columns]",
    "            parts.append(tmp)",
    "        else:",
    "            raise TypeError('Unsupported type in assemble_state')",
    "    out = pd.concat(parts, axis=1).sort_index()",
    "    return out"
])

# Pilot scripts
write(analysis + "/run_pilot_001.py", [
    "import numpy as np",
    "import pandas as pd",
    "from geometry_engine.normalize import zscore",
    "from geometry_engine.magnitude import rowwise_magnitude",
    "from geometry_engine.state_space import assemble_state",
    "",
    "def demo():",
    "    t = np.linspace(0, 20, 500)",
    "    return pd.DataFrame({",
    "        'sp500': np.sin(t),",
    "        'ten_y': np.cos(t/2),",
    "        'vix': 0.5*np.sin(1.5*t),",
    "        'dxy': 0.8*np.cos(0.7*t)",
    "    })",
    "",
    "df = demo()",
    "norm = zscore(df)",
    "state = assemble_state({'core': norm})",
    "mag = rowwise_magnitude(state)",
    "",
    "print('PILOT-001 complete:')",
    "print(mag.describe())"
])

write(analysis + "/run_pilot_002.py", [
    "import pandas as pd",
    "from pathlib import Path",
    "",
    "f = Path('/content/VCF-RESEARCH/data/processed/pilot_full_range.csv')",
    "if f.exists():",
    "    df = pd.read_csv(f, index_col=0)",
    "    print(df.shape)",
    "    print(df.isna().sum())",
    "else:",
    "    print('Full range file not found.')"
])

write(analysis + "/run_pilot_003.py", [
    "import pandas as pd",
    "from pathlib import Path",
    "from geometry_engine.normalize import zscore, minmax",
    "",
    "f = Path('/content/VCF-RESEARCH/data/processed/pilot_norm_inputs.csv')",
    "",
    "if f.exists():",
    "    df = pd.read_csv(f, index_col=0)",
    "    print('Raw:', df.describe())",
    "    print('Z-score:', zscore(df).describe())",
    "    print('Min-max:', minmax(df).describe())",
    "else:",
    "    print('Normalization file not found.')"
])

write(analysis + "/run_pilot_004.py", [
    "import pandas as pd",
    "from pathlib import Path",
    "",
    "events = ['1987-10-19','2008-09-15','2020-03-16']",
    "f = Path('/content/VCF-RESEARCH/outputs/pilot_magnitude_series.csv')",
    "",
    "if f.exists():",
    "    df = pd.read_csv(f, index_col=0)",
    "    try: df.index = pd.to_datetime(df.index)",
    "    except: pass",
    "",
    "    print(df.shape)",
    "",
    "    for e in events:",
    "        print('Event:', e)",
    "        if isinstance(df.index, pd.DatetimeIndex):",
    "            d = pd.to_datetime(e)",
    "            win = df.loc[d-pd.Timedelta(days=10): d+pd.Timedelta(days=10)]",
    "            print(win)",
    "else:",
    "    print('Magnitude file not found.')"
])

print("All geometry engine modules + pilot scripts created successfully.")
