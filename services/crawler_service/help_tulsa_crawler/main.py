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

    # Load all sheets from the Excel workbook
    all_sheets = pd.read_excel(input_file, sheet_name=None)

    total_records = 0
    with output_file.open("w") as f:
        for sheet_name, df in all_sheets.items():
            df = df.dropna(how="all")  # Optional: remove empty rows
            print(f"🟢 Processing worksheet: {sheet_name} ({len(df)} rows)")

            for _, row in df.iterrows():
                data = {"id": str(uuid.uuid4()), "source_sheet": sheet_name}
                data.update(row.fillna("").to_dict())
                f.write(json.dumps(data) + "\n")

            total_records += len(df)

    print(f"✅ Wrote {total_records} resources to {output_file}")


if __name__ == "__main__":
    main()
