#!/usr/bin/env python3
"""Validate the model catalog and generated README, offline site, and CSV."""
import csv
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
models = json.loads((ROOT / "data/models.json").read_text(encoding="utf-8"))
errors = []
required = {
    "id", "name", "year", "level", "inference_modality", "pretrain_modality",
    "feature_dim", "feature_definition", "paper_url", "weight_url", "code_url",
    "weight_access", "upstream", "recommended_input", "notes", "paper_kind",
}
ids = set()
for i, model in enumerate(models, 1):
    missing = required - model.keys()
    if missing:
        errors.append(f"Record {i}: missing fields {sorted(missing)}")
        continue
    ident = model["id"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", ident):
        errors.append(f"Record {i}: invalid id {ident!r}")
    if ident in ids:
        errors.append(f"Record {i}: duplicated id {ident!r}")
    ids.add(ident)
    if model["level"] not in ("Patch", "WSI"):
        errors.append(f"Record {i}: invalid level {model['level']!r}")
    if model["weight_access"] not in ("公开", "受限", "仓库下载"):
        errors.append(f"Record {i}: invalid access {model['weight_access']!r}")
    if not isinstance(model["year"], int) or not 1990 <= model["year"] <= 2100:
        errors.append(f"Record {i}: invalid year")
    if not re.fullmatch(r"\d+(?:\s*/\s*\d+)*", model["feature_dim"]):
        errors.append(f"Record {i}: invalid feature dimension {model['feature_dim']!r}")
    for field in ("paper_url", "weight_url", "code_url"):
        url = model[field]
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"Record {i}: {field} must be an https URL ({url!r})")
    for field in ("name", "inference_modality", "pretrain_modality", "feature_definition"):
        if not isinstance(model[field], str) or not model[field].strip():
            errors.append(f"Record {i}: empty {field}")

with (ROOT / "data/models.csv").open(encoding="utf-8-sig", newline="") as f:
    csv_rows = list(csv.DictReader(f))
if len(csv_rows) != len(models):
    errors.append(f"CSV has {len(csv_rows)} rows vs JSON {len(models)}")

html = (ROOT / "index.html").read_text(encoding="utf-8")
m = re.search(r'<script id="atlas-data" type="application/json">(.*?)</script>', html, re.S)
if not m:
    errors.append("Site missing embedded JSON")
else:
    embedded = json.loads(m.group(1))
    if {r["id"] for r in embedded} != ids:
        errors.append("Site embedded JSON does not match data/models.json")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for model in models:
    if model["paper_url"] not in readme or model["weight_url"] not in readme:
        errors.append(f"README does not include URLs for {model['name']}")

if errors:
    print("\n".join(f"ERROR: {e}" for e in errors))
    raise SystemExit(1)
print(f"OK: {len(models)} entries, {sum(m['level']=='Patch' for m in models)} Patch, {sum(m['level']=='WSI' for m in models)} WSI; URL syntax, README, CSV and HTML consistent.")
print("Note: Link syntax is checked, not remote download availability or access rights.")
