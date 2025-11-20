# VCF Research**
**VCF Research – Vector Coherence Framework**

A large-scale, cloud-based research engine for studying macro-financial behavior through geometric, statistical, and structural alignment.


**📌 Overview**

----------------------------------------------------------

**VCF Research is an open computational framework designed to:**
  -ingest large-scale macroeconomic and financial datasets
  -normalize heterogeneous data into a unified statistical space
  -construct monthly and daily macro-risk panels
  -analyze vector relationships among economic signals
  -compute geometric indicators including θ (theta), φ (phi), coherence, and divergence
  -run automated workflows via GitHub Actions
  -enable reproducible, transparent, academically-viable macro modeling

----------------------------------------------------------

The goal is not to forecast markets or make trading decisions.
The goal is to understand how macro forces behave —
how they align, diverge, resonate, and evolve across time —
and whether this structure reveals stable, measurable patterns.

----------------------------------------------------------

**VCF is built to be:**
  -cloud-native
  -reproducible
  -modular
  -extensible
  -mathematically clean
  -academically publishable*

----------------------------------------------------------------------

**🏗 Project Architecture***

VCF_Research/
│
├── registry/                # Metric definitions (JSON, CSV)
├── data_raw/                # Unprocessed market + macro data (Colab writes)
├── data_clean/              # Normalized series (Colab writes)
├── panels/                  # Combined macro panels (Colab writes)
│
├── geometry/                # GitHub-run analysis engine (θ, φ, coherence)
│   ├── compute_theta.py
│   ├── compute_phi.py
│   ├── coherence_engine.py
│   └── stress_blocks.py
│
├── outputs/                 # Auto-generated results from GitHub Actions
│   ├── theta.csv
│   ├── phi.csv
│   ├── coherence.csv
│   └── diagnostics/
│
├── scripts/                 # ETL, normalization, panel construction
│   ├── data_loader.py
│   ├── data_normalizer.py
│   ├── build_macro_panel.py
│   └── utilities.py
│
└── .github/workflows/
    └── run_geometry.yml     # CI/CD pipeline to compute geometry on push


----------------------------------------------------------

**🚀 Two-Level Compute Architecture**

1. Colab Notebook (Data Engine)
  -Handles all data operations:
  -FRED / Yahoo ingestion
  -normalization
  -monthly panel construction
  -trimming to full-coverage windows
  -pushing all generated files to GitHub

This isolates data work in a stable cloud environment.


----------------------------------------------------------

**2. GitHub Actions (Geometry Engine)**
**Runs analyses:**
  -θ (theta)
  -φ (phi)
  -coherence
  -stress indexing
  -vector divergence

Every time new data is pushed, GitHub automatically recalculates all geometry outputs and commits them back to the repo.

This makes the framework fully automated and fully reproducible.

----------------------------------------------------------

**📊 Motivation**

VCF Research explores a simple but powerful idea:
> Markets and macroeconomies generate signals that behave like vectors — having magnitude, direction, and relationships that can align or conflict over time.

----------------------------------------------------------

**We study:**
  -periods of high coherence
  -rotational dynamics
  -macro “wave states”
  -divergence between financial and economic signals
  -alignment patterns preceding regime shifts

The focus is structural understanding, not prediction.


----------------------------------------------------------

**📈 Why GitHub + Colab?**
  -Cloud compute removes local hardware limitations
  -GitHub provides scientific reproducibility
  -Actions automate geometry updates
  -Easy versioning and academic traceability
  -Zero dependence on user hardware (phone, Chromebook, PC all work)



----------------------------------------------------------

**🔧 Requirements (automatically installed in Colab**
  -Python 3.10+
  -pandas
  -numpy
  -yfinance
  -pandas-datareader
  -scipy
  -matplotlib (optional)
  -GitHub personal access token (for repo push)

No local installation required.


----------------------------------------------------------

**🧪 Status**
-Phase I — Data Pipeline: ✔ Complete
-Phase II — Macro Panel: ✔ Complete
-Phase III — Geometry Engine: In Progress
-Phase IV — Academic Diagnostics / Publishable Metrics: Pending


----------------------------------------------------------

**📜 License**
MIT (or whichever you choose)


----------------------------------------------------------
**🙌 Maintainers**

Jason Rudder
ChatGPT (VCF Research Assistant)

----------------------------------------------------------

