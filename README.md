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

**🏗 Project Architecture**

```
VCF_Research/
│
├── notebooks/               # Jupyter notebooks for research and analysis
│   ├── VFC_Mathematical_Engine_Claud.ipynb
│   ├── Visualization_Suite_Claud.ipynb
│   └── README.md
│
├── src/                     # Reusable Python modules and libraries
│   ├── vcf_advanced_math.py
│   ├── vcf_visualizations.py
│   └── README.md
│
├── scripts/                 # ETL, normalization, panel construction
│   ├── data_loader.py
│   ├── normalize_metrics.py
│   ├── build_macro_panel.py
│   ├── geometry_engine.py
│   └── README.md
│
├── data_raw/                # Unprocessed market + macro data (Colab writes)
│   ├── SPY_US.csv
│   ├── GDP_US.csv
│   ├── CPI_US.csv
│   └── README.md
│
├── data_clean/              # Normalized series (Colab writes)
│   ├── *_normalized.csv
│   ├── macro_monthly_panel.csv
│   └── README.md
│
├── geometry/                # GitHub-run analysis engine (θ, φ, coherence)
│   ├── geometry_panel.csv
│   └── README.md
│
├── registry/                # Metric definitions (JSON, CSV)
│   ├── vcf_metric_registry.json
│   ├── metrics.csv
│   └── README.md
│
├── docs/                    # Project documentation
│   ├── DATA_SOURCES.md      # Data source and preprocessing information
│   ├── log.md               # Experiment and process notes
│   └── *.md                 # Additional research documentation
│
├── assets/                  # Static files, archives, and references
│   ├── *.zip
│   ├── *.pdf
│   └── *.gdoc
│
├── .github/workflows/       # CI/CD automation
│   └── run_geometry.yml
│
├── .gitignore               # Exclude large files and build artifacts
└── README.md                # This file
```


----------------------------------------------------------

**🚀 Two-Level Compute Architecture**

**1. Colab Notebook (Data Engine)**
Handles all data operations:
  -FRED / Yahoo ingestion
  -normalization
  -monthly panel construction
  -trimming to full-coverage windows
  -pushing all generated files to GitHub

This isolates data work in a stable cloud environment

**2. GitHub Actions (Geometry Engine)**
Runs analyses:
  -θ (theta)
  -φ (phi)
  -coherence
  -stress indexing
  -vector divergence

Every time new data is pushed, GitHub automatically recalculates all geometry outputs and commits them back to the repo.

This makes the framework fully automated and fully reproducible.

----------------------------------------------------------
**📊 Motivation**

>VCF Research explores a simple but powerful idea:
>Markets and macroeconomies generate signals that behave like vectors — having magnitude, direction, and relationships that can align or conflict over time.
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

**📝 Workflow & How to Use**

**Running Notebooks:**
1. Open notebooks in Google Colab or Jupyter
2. Notebooks in `/notebooks` directory contain research and analysis code
3. For Colab integration with Google Drive:
   - Mount your Google Drive
   - Clone this repository or sync files
   - See `/docs/Colab_Zip_Builder.md` for detailed instructions

**Running Scripts:**
1. Scripts in `/scripts` handle data loading, normalization, and panel construction
2. Run locally with Python 3.10+ or in Colab environment
3. See individual script files for usage and parameters

**Data Organization:**
- **Raw data**: Place unprocessed CSV files in `/data_raw/`
- **Clean data**: Normalized and processed data outputs go to `/data_clean/`
- **Data sources**: Document all data sources in `/docs/DATA_SOURCES.md`
- **Updates**: When adding new data, update both the raw files and documentation

**Collaboration:**
- Use `/docs/log.md` to track experiments, findings, and process notes
- Document code changes clearly in commit messages
- Store reusable functions in `/src/` for use across notebooks and scripts
- Keep notebooks focused on specific analyses or workflows

For more detailed information, see documentation in `/docs/` directory.

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

