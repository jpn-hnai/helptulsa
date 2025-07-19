from pathlib import Path
from typing import List, Dict
import pandas as pd
import yaml
import requests

SCHEMA_V1_FIELDS = ["id", "name", "description", "url", "phone"]


def parse_excel(path: Path) -> List[Dict]:
    df = pd.read_excel(path)
    df = df[SCHEMA_V1_FIELDS]
    return df.to_dict(orient="records")


def parse_url(url: str) -> List[Dict]:
    resp = requests.get(url)
    resp.raise_for_status()
    ext = url.split(".")[-1]
    tmp = Path("/tmp/source." + ext)
    tmp.write_bytes(resp.content)
    return parse_excel(tmp)


def write_resources(path: Path, records: List[Dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(records, f)
