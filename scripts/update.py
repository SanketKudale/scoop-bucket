#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import urllib.request

API = "https://api.github.com/repos/SanketKudale/backsmith/releases/latest"
ROOT = pathlib.Path(__file__).resolve().parents[1]

request = urllib.request.Request(API, headers={"Accept": "application/vnd.github+json"})
with urllib.request.urlopen(request, timeout=30) as response:
    release = json.load(response)

version = release["tag_name"].removeprefix("v")
asset = next(item for item in release["assets"] if item["name"] == "backsmith.zip")
with urllib.request.urlopen(asset["browser_download_url"], timeout=60) as response:
    checksum = hashlib.sha256(response.read()).hexdigest()

manifest = {
    "version": version,
    "description": "Deterministic, conflict-aware Spring Boot backend generator",
    "homepage": "https://sanketkudale.github.io/backsmith/",
    "license": "Apache-2.0",
    "url": f"https://github.com/SanketKudale/backsmith/releases/download/v{version}/backsmith.zip",
    "hash": checksum,
    "extract_dir": f"backsmith-{version}",
    "bin": [["bin\\backsmith.cmd", "backsmith"]],
    "checkver": {"github": "https://github.com/SanketKudale/backsmith"},
    "autoupdate": {
        "url": "https://github.com/SanketKudale/backsmith/releases/download/v$version/backsmith.zip",
        "extract_dir": "backsmith-$version",
    },
}

(ROOT / "bucket").mkdir(exist_ok=True)
(ROOT / "bucket" / "backsmith.json").write_text(
    json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
)
