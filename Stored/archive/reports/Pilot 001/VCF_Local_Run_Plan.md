
# 🖥️ Next Run — Full Local Execution Plan (Markdown Version)

We will run the full VCF Geometry Engine **locally on your PC** next time using:

- **Raw data** (true unaltered CSV files)  
- **Claude-approved math + code**  
- **Your optimized Python environment**  
- **Local folder structure that mirrors the GitHub repo**

This gives you a completely **reproducible**, **stand-alone**, **quant-grade pipeline**.

---

## 1. Local Folder Structure

We will recreate this exact structure on your machine:

```
VCF-RESEARCH/
    data_raw/
    data_clean/
    engine/
    geometry/
    coherence/
    reports/
    notebooks/
    logs/
```

Raw datasets go inside:

```
data_raw/
```

---

## 2. Required Raw Data Files (Next Session)

You will provide **true raw data** for the local run:

### Essential Inputs
- `SPY_raw.csv`
- `VIX_raw.csv`
- `T10Y2Y_raw.csv`
- `M2_raw.csv`

**Format must be clean:**

```
date, value
```

### Recommended sources:
- Yahoo Finance exports  
- FRED downloads  
- Fidelity CSV  
- API scripts (optional)

**Avoid Apple Numbers or Google Sheets**, which corrupt CSV structure.

---

## 3. Claude-Approved Code Modules

Before running locally:

1. We send Claude:  
   - **Full mathematical spec**  
   - **Engine code** (`vcf_geometry_engine.py`)  
2. Claude reviews / optimizes  
3. You and I validate outputs  
4. Final version is placed in:

```
engine/vcf_geometry_engine.py
```

This ensures:

- Mathematical consistency  
- No divergence between GPT ↔ Claude outputs  
- Reproducibility for research  

---

## 4. Local Python Execution

We will run on your PC:

```
python run_geometry.py
```

This script will:

- Load raw data
- Clean + normalize + monthly-sample
- Build the 4-metric panel
- Apply VCF Geometry:
  - amplitude  
  - phase  
  - frequency  
  - coherence  
- Export all outputs

### Expected outputs:
- `VCF_geometry_features.parquet`
- `VCF_geometry_coherence.parquet`
- `VCF_geometry_summary.md`
- `VCF_geometry_report.pdf`

Perfect for:

- research papers  
- GitHub commits  
- versioning  
- reproducibility  

---

## 5. Why Local Execution Matters

Running locally gives you:

- ✔ Exact control of raw data  
- ✔ No browser timeouts  
- ✔ Unlimited file sizes  
- ✔ Direct GitHub integration  
- ✔ Local + cloud redundancy  
- ✔ Full plotting capability  
- ✔ Ability to process huge datasets  

This is how institutional quant labs operate.

---

## 6. Next Steps

When you're ready:

Just say:

**“Ready for local run setup.”**

And I’ll walk you through:

- setting up the directory  
- installing dependencies  
- preparing raw data  
- integrating Claude’s code  
- running your first full local VCF geometry pipeline
