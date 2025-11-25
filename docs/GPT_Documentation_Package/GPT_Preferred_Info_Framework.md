
# GPT Preferred Information Framework  
### For Smooth, Clear, High‑Signal Collaboration (Designed for VCF Research)

This document defines the **exact types of information**, formatting, and structure that help GPT work with maximum accuracy and efficiency — especially for your *VCF Geometry Engine*, *MVF*, *data pipelines*, *GitHub repos*, and *Claude collaboration*.

---

# ✅ 1. PROJECT CONTEXT (ALWAYS USEFUL)
Provide these whenever you start a new sub‑project or branch:

- **Project Name:** (e.g., VCF‑RESEARCH, MVF, Geometry Engine v1)
- **Branch Name:** (e.g., `vcf-geometry-spec-v1`)
- **Intended Output:** (script, spec, code, rewrite, architecture, PDF, etc.)
- **Preferred Style:** (clean, Claude-ready, scaffolding, production, experimental)
- **Environment:**  
  - Local Windows  
  - Local Mac  
  - Google Colab  
  - GitHub repo  
  - VS Code  
- **Time Constraint:** (quick draft, precise build, high accuracy, rapid prototype)

---

# ✅ 2. FILE-TYPE CLARITY (EXTREMELY IMPORTANT)
Tell GPT **what file(s)** you want as output:

- `.md`  
- `.py`  
- `.json`  
- `.csv`  
- `.txt`  
- `.ipynb` (notebook)  
- `.pdf`  
- zipped folder  
- entire repo structure  

This eliminates ambiguity and prevents unwanted text output.

---

# ✅ 3. INPUT DATA DESCRIPTION
When referring to inputs or datasets, specify:

- Source (FRED, YF, manual data, Claude output)
- Frequency (daily, weekly, monthly)
- Format (CSV, DataFrame, JSON)
- Columns (names & meanings)
- Date range
- Expected missing values or quirks

Example:

```
Data: monthly FRED metrics
Columns: [date, CPI, 10Y_yield, unemployment]
Range: 1980–present
Format: pandas DataFrame
```

---

# ✅ 4. DESIRED LOGIC OR MATH
Clarify the **type** of logic you expect:

- Pure geometry  
- Macro normalization  
- Signal processing  
- Vector construction  
- ML/HMM regimes  
- Stress modeling  
- Charting  
- File creation  
- GitHub workflow  

GPT performs best when the category is defined.

---

# ✅ 5. STRUCTURE OF REQUESTS FOR CODE
When asking for code:

1. Specify language  
2. Specify file layout  
3. Specify function names if preferred  
4. Tell GPT if Claude will later replace internals  
5. Mention whether stubs or production logic is desired  

Example:

```
Create starter scripts in Python.
Keep functions small.
Make all code Claude-replaceable.
Do NOT include real API calls yet.
```

---

# ✅ 6. WHAT TO DO WITH EXISTING CODE  
Tell GPT:

- Rewrite?  
- Clean?  
- Expand?  
- Convert to functions?  
- Comment?  
- Modularize?  
- Make compatible with Claude?  
- Turn into a notebook?  

Example:

```
Rewrite this script into a 3‑file modular pipeline compatible with Claude’s math stubs.
```

---

# ✅ 7. WHEN WORKING WITH GITHUB  
Always include:

- Repo link  
- Branch name  
- What you want to add/modify  
- Files involved  
- Folder structure  

Example:

```
Repo: VCF-RESEARCH
Branch: vcf-geometry-spec-v1
Add: pipeline/run_pipeline.py (new)
Modify: metrics/normalize.py (extend methods)
```

---

# ✅ 8. COLAB-SPECIFIC REQUESTS  
Include:

- Whether to enable file upload cell  
- Whether to create ZIP  
- Whether to generate notebook  
- Whether to generate auto-folder builder  
- Whether to save to Drive  

Example:

```
Create a Colab notebook that:
1. Rebuilds the VCF repo
2. Generates all starter files
3. Zips entire directory
4. Provides a Drive save button
```

---

# ✅ 9. PREFERENCES FOR TEXT RESPONSES  
Your style preferences:

- Personal, conversational, warm  
- Clear instruction blocks  
- No fluff  
- Use headings  
- Avoid corporate tone  
- Use bullet lists & code blocks  
- Humor welcomed if natural  

---

# ✅ 10. GPT/CLAUDE COLLABORATION MODE  
When using both models:

Specify:

- What Claude is responsible for (math, heavy derivations, etc.)
- What GPT handles (architecture, scaffolding, integration)
- Where Claude will “drop in” code  
- What GPT should preserve for Claude compatibility  

Example:

```
Claude handles math.
GPT builds scaffolding.
Leave compute functions as stubs for Claude to fill.
Produce clean, modular files.
```

---

# 🎯 SUMMARY: OPTIMAL REQUEST TEMPLATE

Use this template for ultra‑smooth collaboration:

```
Project: VCF-RESEARCH
Branch: vcf-geometry-spec-v1
Output: Python script + .md documentation
Environment: GitHub + Colab
Purpose: Build scaffolding Claude can extend
Files needed: metrics/normalize.py, geometry/compute_mrf.py
Data Format: monthly DataFrame with columns [CPI, Yield, DXY]
Style: clean, modular, Claude-ready, no APIs yet
Action: generate starter versions + ZIP builder + README
```

---

# 🧩 WHY THIS FRAMEWORK MATTERS
Using this structure:

- Removes ambiguity  
- Ensures predictable outputs  
- Speeds up scripting and repo work  
- Keeps Claude and GPT in perfect sync  
- Makes the entire VCF research project reproducible  

---

# 🏁 END OF DOCUMENT
This will be saved as `.md`. Let me know if you'd like a PDF version as well.
