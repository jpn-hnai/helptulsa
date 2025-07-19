import json
import uuid
from pathlib import Path

import pandas as pd


def main() -> None:
    input_file = Path("/app/inputs/resources.xlsx")
    output_file = Path("/app/data/resources.jsonl")

    if not input_file.exists():
        print(f"Input file {input_file} not found")
        return

    df = pd.read_excel(input_file)
    with output_file.open("w") as f:
        for _, row in df.iterrows():
            data = {"id": str(uuid.uuid4())}
            data.update(row.fillna("").to_dict())
            f.write(json.dumps(data) + "\n")
    print(f"Wrote {len(df)} resources to {output_file}")


if __name__ == "__main__":
    main()
