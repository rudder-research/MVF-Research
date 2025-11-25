#!/usr/bin/env python3
"""
VCF Data Registry Pack (Single-File Version)
===========================================

Fetches catalog-style metadata from multiple macro data providers and writes:

- vcf_data_registry_output/fred_catalog.csv
- vcf_data_registry_output/worldbank_catalog.csv
- vcf_data_registry_output/bea_catalog.csv
- vcf_data_registry_output/bls_catalog.csv
- vcf_data_registry_output/oecd_dataflows_catalog.csv
- vcf_data_registry_output/imf_dataflows_catalog.csv
- vcf_data_registry_output/vcf_data_registry_master.csv

Providers covered:
- FRED (St. Louis Fed)       – requires API key
- World Bank WDI             – no key
- BEA (US)                   – requires API key
- BLS (US)                   – optional key; here we pull survey metadata
- OECD SDMX                  – no key
- IMF SDMX (Dataflows)       – no key

Fill in your API keys below or set environment variables:
- FRED_API_KEY
- BEA_API_KEY
- BLS_API_KEY (optional)

This is **catalog/metadata** only, not the actual time series observations.
"""

import os
import json
import time
from typing import Dict, Any, List

import requests
import pandas as pd

# =========================
# CONFIG
# =========================

# Prefer environment variables so you don’t hard-code keys
FRED_API_KEY = os.getenv("FRED_API_KEY", "YOUR_FRED_API_KEY_HERE")
BEA_API_KEY = os.getenv("BEA_API_KEY", "YOUR_BEA_API_KEY_HERE")
BLS_API_KEY = os.getenv("BLS_API_KEY", "")  # optional, not required for this script

OUTPUT_DIR = "vcf_data_registry_output"
REQUEST_TIMEOUT = 20
SLEEP_BETWEEN_REQUESTS = 0.2  # be nice to APIs


# =========================
# Helper functions
# =========================

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def get_json(url: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Generic GET JSON with error handling."""
    resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def save_df(df: pd.DataFrame, name: str) -> str:
    ensure_dir(OUTPUT_DIR)
    out_path = os.path.join(OUTPUT_DIR, name)
    df.to_csv(out_path, index=False)
    print(f"[OK] Saved {name} with {len(df):,} rows")
    return out_path


# =========================
# FRED catalog builder
# =========================

def fetch_fred_series_catalog() -> pd.DataFrame:
    """
    Recursively crawls FRED categories starting from root category_id=0 and collects series metadata.

    Uses:
      - /fred/category/children
      - /fred/category/series

    Docs: https://fred.stlouisfed.org/docs/api/fred/series.html
    """
    if not FRED_API_KEY or "YOUR_FRED_API_KEY" in FRED_API_KEY:
        print("[WARN] FRED_API_KEY not set; skipping FRED catalog.")
        return pd.DataFrame()

    base = "https://api.stlouisfed.org/fred"
    from collections import deque

    visited_categories = set()
    q = deque([0])  # root category
    series_rows: List[Dict[str, Any]] = []

    while q:
        cid = q.popleft()
        if cid in visited_categories:
            continue
        visited_categories.add(cid)

        # Fetch child categories
        try:
            children_data = get_json(
                f"{base}/category/children",
                params={
                    "category_id": cid,
                    "api_key": FRED_API_KEY,
                    "file_type": "json",
                },
            )
            children = children_data.get("categories", [])
            for c in children:
                q.append(c["id"])
        except Exception as e:
            # Not fatal; just log
            print(f"[FRED] Error fetching children for category {cid}: {e}")

        # Fetch series for this category (paged)
        offset = 0
        limit = 1000
        while True:
            try:
                series_data = get_json(
                    f"{base}/category/series",
                    params={
                        "category_id": cid,
                        "api_key": FRED_API_KEY,
                        "file_type": "json",
                        "limit": limit,
                        "offset": offset,
                    },
                )
                sers = series_data.get("seriess", [])
                if not sers:
                    break

                for s in sers:
                    series_rows.append(
                        {
                            "source": "FRED",
                            "dataset": "FRED",
                            "series_code": s.get("id"),
                            "series_name": s.get("title"),
                            "frequency": s.get("frequency"),
                            "units": s.get("units"),
                            "notes": s.get("notes"),
                            "api_endpoint": "https://api.stlouisfed.org/fred/series/observations",
                            "key_required": True,
                            "raw_metadata": json.dumps(s),
                        }
                    )

                if len(sers) < limit:
                    break
                offset += limit
                time.sleep(SLEEP_BETWEEN_REQUESTS)
            except Exception as e:
                print(f"[FRED] Error fetching series for category {cid}, offset {offset}: {e}")
                break

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    df = pd.DataFrame(series_rows).drop_duplicates(subset=["series_code"])
    return df


# =========================
# World Bank indicator catalog
# =========================

def fetch_worldbank_indicator_catalog() -> pd.DataFrame:
    """
    Pulls the full list of World Bank Indicators.

    Endpoint: http://api.worldbank.org/v2/indicator?format=json&per_page=20000&page=1...
    Docs: World Bank Indicators API  [oai_citation:0‡World Bank Data Help Desk](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation?utm_source=chatgpt.com)
    """
    rows: List[Dict[str, Any]] = []
    base_url = "http://api.worldbank.org/v2/indicator"
    per_page = 20000
    page = 1

    while True:
        print(f"[WorldBank] Fetching indicators page {page} ...")
        js = get_json(
            base_url,
            params={"format": "json", "per_page": per_page, "page": page},
        )
        if not isinstance(js, list) or len(js) < 2:
            break

        meta, indicators = js
        for ind in indicators:
            rows.append(
                {
                    "source": "WorldBank",
                    "dataset": "WDI",
                    "series_code": ind.get("id"),
                    "series_name": ind.get("name"),
                    "frequency": "",  # frequency is usually per-series but not always in this meta
                    "units": ind.get("unit", ""),
                    "notes": ind.get("sourceNote", ""),
                    "api_endpoint": f"http://api.worldbank.org/v2/indicator/{ind.get('id')}",
                    "key_required": False,
                    "raw_metadata": json.dumps(ind),
                }
            )

        pages = meta.get("pages", 1)
        if page >= pages:
            break
        page += 1
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    df = pd.DataFrame(rows)
    return df


# =========================
# BEA dataset / parameter catalog
# =========================

def fetch_bea_catalog() -> pd.DataFrame:
    """
    Fetches BEA datasets and their parameters (metadata level, not full series list).

    Uses:
      - method=GetDataSetList
      - method=GetParameterList

    Docs: BEA Web Service API User Guide  [oai_citation:1‡BEA Apps](https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf?utm_source=chatgpt.com)
    """
    if not BEA_API_KEY or "YOUR_BEA_API_KEY" in BEA_API_KEY:
        print("[WARN] BEA_API_KEY not set; skipping BEA catalog.")
        return pd.DataFrame()

    base = "https://apps.bea.gov/api/data"

    # 1. Get dataset list
    ds_json = get_json(
        base,
        params={
            "UserID": BEA_API_KEY,
            "method": "GetDataSetList",
            "ResultFormat": "JSON",
        },
    )
    datasets = ds_json.get("BEAAPI", {}).get("Results", {}).get("Dataset", [])

    rows: List[Dict[str, Any]] = []

    for ds in datasets:
        dataset_name = ds.get("DatasetName")
        print(f"[BEA] Fetching parameters for dataset {dataset_name} ...")
        try:
            params_json = get_json(
                base,
                params={
                    "UserID": BEA_API_KEY,
                    "method": "GetParameterList",
                    "DataSetName": dataset_name,
                    "ResultFormat": "JSON",
                },
            )
            params_list = (
                params_json.get("BEAAPI", {})
                .get("Results", {})
                .get("Parameter", [])
            )
            for p in params_list:
                rows.append(
                    {
                        "source": "BEA",
                        "dataset": dataset_name,
                        "series_code": p.get("ParameterName"),
                        "series_name": p.get("ParameterText"),
                        "frequency": "",  # depends on dataset; can be derived later
                        "units": "",
                        "notes": p.get("ParameterDescription"),
                        "api_endpoint": "https://apps.bea.gov/api/data",
                        "key_required": True,
                        "raw_metadata": json.dumps(p),
                    }
                )
        except Exception as e:
            print(f"[BEA] Error fetching parameters for {dataset_name}: {e}")

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    df = pd.DataFrame(rows)
    return df


# =========================
# BLS survey catalog (not full series catalog)
# =========================

def fetch_bls_survey_catalog() -> pd.DataFrame:
    """
    Pulls the list of all BLS surveys via the /surveys endpoint.

    Full series catalog is not directly exposed; this at least maps survey codes to names.  [oai_citation:2‡Bureau of Labor Statistics](https://www.bls.gov/developers/api_signature_v2.htm?utm_source=chatgpt.com)
    """
    url = "https://api.bls.gov/publicAPI/v2/surveys"
    js = get_json(url)
    surveys = js.get("Results", {}).get("survey", [])

    rows: List[Dict[str, Any]] = []
    for s in surveys:
        rows.append(
            {
                "source": "BLS",
                "dataset": "BLS-survey",
                "series_code": s.get("survey_abbreviation"),
                "series_name": s.get("survey_name"),
                "frequency": "",
                "units": "",
                "notes": "",
                "api_endpoint": "https://api.bls.gov/publicAPI/v2/timeseries/data/",
                "key_required": bool(BLS_API_KEY),
                "raw_metadata": json.dumps(s),
            }
        )

    df = pd.DataFrame(rows)
    return df


# =========================
# OECD dataflows catalog (SDMX)
# =========================

def fetch_oecd_dataflows_catalog() -> pd.DataFrame:
    """
    Fetches the list of OECD SDMX dataflows.

    Endpoint (SDMX dataflow list): https://sdmx.oecd.org/public/rest/dataflow  [oai_citation:3‡OECD SDMX](https://sdmx.oecd.org/public/rest/dataflow?utm_source=chatgpt.com)
    """
    url = "https://sdmx.oecd.org/public/rest/dataflow"
    js = get_json(url)
    # SDMX structure: "dataflows" -> "dataflow"
    flows = js.get("dataflows", {}).get("dataflow", [])

    rows: List[Dict[str, Any]] = []
    for f in flows:
        flow_id = f.get("id")
        name_obj = f.get("name", {})
        # name might be a dict with language keys
        if isinstance(name_obj, dict):
            flow_name = next(iter(name_obj.values()))
        else:
            flow_name = str(name_obj)

        rows.append(
            {
                "source": "OECD",
                "dataset": flow_id,
                "series_code": flow_id,
                "series_name": flow_name,
                "frequency": "",
                "units": "",
                "notes": "",
                "api_endpoint": "https://sdmx.oecd.org/public/rest/data",
                "key_required": False,
                "raw_metadata": json.dumps(f),
            }
        )

    df = pd.DataFrame(rows)
    return df


# =========================
# IMF dataflows catalog (SDMX)
# =========================

def fetch_imf_dataflows_catalog() -> pd.DataFrame:
    """
    Fetches IMF dataflows (dataset list) via SDMX JSON.

    Endpoint: http://dataservices.imf.org/REST/SDMX_JSON.svc/Dataflow  [oai_citation:4‡artt.dev](https://artt.dev/en/blog/2023/imf-api/?utm_source=chatgpt.com)
    """
    url = "http://dataservices.imf.org/REST/SDMX_JSON.svc/Dataflow"
    js = get_json(url)
    flows = js.get("Structure", {}).get("Dataflows", {}).get("Dataflow", [])

    rows: List[Dict[str, Any]] = []
    for f in flows:
        flow_id = f.get("KeyFamilyRef", {}).get("KeyFamilyID")
        name_list = f.get("Name", [])
        # Name might be a list of dicts with language codes
        if name_list and isinstance(name_list, list):
            flow_name = name_list[0].get("value")
        else:
            flow_name = str(name_list)

        rows.append(
            {
                "source": "IMF",
                "dataset": flow_id,
                "series_code": flow_id,
                "series_name": flow_name,
                "frequency": "",
                "units": "",
                "notes": "",
                "api_endpoint": "http://dataservices.imf.org/REST/SDMX_JSON.svc",
                "key_required": False,
                "raw_metadata": json.dumps(f),
            }
        )

    df = pd.DataFrame(rows)
    return df


# =========================
# Master registry builder
# =========================

def build_master_registry(dfs: List[pd.DataFrame]) -> pd.DataFrame:
    """Concatenate, align columns, and return a unified master registry DataFrame."""
    # Ensure consistent columns
    base_cols = [
        "source",
        "dataset",
        "series_code",
        "series_name",
        "frequency",
        "units",
        "notes",
        "api_endpoint",
        "key_required",
        "raw_metadata",
    ]
    aligned = []
    for df in dfs:
        if df is None or df.empty:
            continue
        for col in base_cols:
            if col not in df.columns:
                df[col] = ""
        aligned.append(df[base_cols])

    if not aligned:
        return pd.DataFrame(columns=base_cols)

    master = pd.concat(aligned, ignore_index=True)
    master = master.drop_duplicates(subset=["source", "dataset", "series_code"])
    return master


# =========================
# Main
# =========================

def main():
    print("=== VCF Data Registry Pack ===")
    print(f"Output directory: {OUTPUT_DIR}")
    ensure_dir(OUTPUT_DIR)

    # Fetch catalogs
    fred_df = fetch_fred_series_catalog()
    if not fred_df.empty:
        save_df(fred_df, "fred_catalog.csv")

    wb_df = fetch_worldbank_indicator_catalog()
    if not wb_df.empty:
        save_df(wb_df, "worldbank_catalog.csv")

    bea_df = fetch_bea_catalog()
    if not bea_df.empty:
        save_df(bea_df, "bea_catalog.csv")

    bls_df = fetch_bls_survey_catalog()
    if not bls_df.empty:
        save_df(bls_df, "bls_catalog.csv")

    oecd_df = fetch_oecd_dataflows_catalog()
    if not oecd_df.empty:
        save_df(oecd_df, "oecd_dataflows_catalog.csv")

    imf_df = fetch_imf_dataflows_catalog()
    if not imf_df.empty:
        save_df(imf_df, "imf_dataflows_catalog.csv")

    # Build master registry
    master = build_master_registry(
        [fred_df, wb_df, bea_df, bls_df, oecd_df, imf_df]
    )
    save_df(master, "vcf_data_registry_master.csv")

    print("\n=== Done ===")
    print("You can now open vcf_data_registry_output/vcf_data_registry_master.csv")
    print("in Excel / Google Sheets and start tagging pillars, etc.")


if __name__ == "__main__":
    main()