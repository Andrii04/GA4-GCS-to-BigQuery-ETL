import json
import pandas as pd
from io import BytesIO

# List of columns that contain JSON-encoded data
JSON_COLS = [
    "event_params",
    "privacy_info",
    "user_ltv",
    "device",
    "geo",
    "app_info",
    "traffic_source",
    "event_dimensions",
    "ecommerce",
    "items"
]


def convert_event_params_values(record):
    event_params = record.get("event_params")
    if isinstance(event_params, list):
        for param in event_params:
            value = param.get("value")
            if isinstance(value, dict):
                float_value = value.get("float_value")
                double_value = value.get("double_value")
                # Convert float_value from string to float if needed
                if isinstance(float_value, str):
                    value["float_value"] = float(float_value)
                # Convert double_value from string to float if needed
                if isinstance(double_value, str):
                    value["double_value"] = float(double_value)
    return record


def parse_and_unwrap(cell, col_name):
    if cell is None:
        return None

    if isinstance(cell, (dict, list)):
        parsed = cell
    else:
        s = str(cell).strip()
        if s == "" or s.lower() == "null":
            return None
        try:
            parsed = json.loads(s)
        except (json.JSONDecodeError, TypeError):
            return s

    # Special case: unwrap event_params if nested under same key
    if col_name == "event_params" and isinstance(parsed, dict) and "event_params" in parsed:
        parsed = parsed["event_params"]

    # Recursively unwrap single-key dicts and decode inner JSON strings
    while True:
        if isinstance(parsed, dict) and len(parsed) == 1:
            key0, val0 = next(iter(parsed.items()))

            if isinstance(val0, str):
                s_inner = val0.strip()
                if s_inner == "" or s_inner.lower() == "null":
                    parsed = None
                    break
                try:
                    val0_parsed = json.loads(s_inner)
                    parsed = val0_parsed
                    continue
                except json.JSONDecodeError:
                    parsed = val0
                    break

            if isinstance(val0, (dict, list)):
                parsed = val0
                continue

            parsed = val0
            break

        break

    return parsed
# specific columns could need a specific UNNEST 


def dataframe_from_bytes(csv_bytes):
    # Read CSV from bytes into DataFrame with all columns as strings
    bio = BytesIO(csv_bytes)
    return pd.read_csv(bio, dtype=str, keep_default_na=False)


def transform_dataframe_to_records(df):
    good_lines = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        # Parse and unwrap JSON columns
        for col in JSON_COLS:
            rec[col] = parse_and_unwrap(rec.get(col), col)
        rec = convert_event_params_values(rec)
        good_lines.append(rec)

    return good_lines


def transform_csv_bytes_to_records(csv_bytes):
    # Convert CSV bytes to list of parsed records
    df = dataframe_from_bytes(csv_bytes)
    records = transform_dataframe_to_records(df)
    return records