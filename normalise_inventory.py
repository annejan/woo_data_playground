import pandas as pd
import numpy as np
import sys
import os
import re

REQUIRED_COLUMNS = [
    "Family ID",
    "Email Thread ID",
    "File type",
    "Period",
    "Subject",
    "Matter",
    "Datum",
]

TYPES = [
    "chat",
    "pdf",
    "doc",
    "image",
    "presentation",
    "spreadsheet",
    "email",
    "html",
    "note",
    "audio",
    "database",
    "xml",
    "video",
    "vcard",
    "unknown",
]

TYPE_REPLACEMENTS = {
    "whatsapp": "chat",
    "whatsapp gesprek": "chat",
    "e-mail": "email",
    "presentatie": "presentation",
    "powerpoint": "presentation",
    "excel": "spreadsheet",
    "": "unknown",
    "nan": "unknown",
    "afbeelding": "image",
}


def replace_types(series):
    series = series.astype(str)
    for old, new in TYPE_REPLACEMENTS.items():
        pattern = r"^" + re.escape(old) + r"$"
        series = series.str.replace(pattern, new, flags=re.IGNORECASE, regex=True)
    return series


def normalize_types(series):
    series = series.astype(str)

    def find_type(value):
        for t in TYPES:
            if t in value:
                return t
        return "unknown"

    return series.apply(find_type)


def normalize_date(date_series, timezone="Europe/Amsterdam"):
    # Convert the dates to datetime objects
    date_converted = pd.to_datetime(
        date_series, format="%d-%m-%Y %H:%M:%S", errors="coerce"
    )
    # Convert the timezone
    date_converted = date_converted.dt.tz_localize("UTC").dt.tz_convert(timezone)
    # Format as ISO 8601 string
    return date_converted.dt.strftime("%Y-%m-%dT%H:%M:%S")


def normalize_id(series):
    series = series.astype(str)
    series = series.str.replace(r"[^0-9a-zA-Z]", "", regex=True)
    return series.str.replace("nan", "", regex=False)


def normalise_beoordeling(series):
    series = series.str.replace(";", ",", regex=False)
    return series.str.replace(r"\ben\b", ",", regex=True)


def warn_empty_id(series):
    # Check for empty or NaN values
    empty_values = series.apply(lambda x: x == "" or pd.isna(x))

    # Warn if empty values are found
    if empty_values.any():
        empty_indices = [
            index + 2 for index in empty_values[empty_values].index.tolist()
        ]
        print("Indices of empty fields:", empty_indices)


def warn_duplicates(series):
    # Check for duplicates
    series = series.replace("", np.nan)
    duplicate_values = series.duplicated(keep=False) & series.notna()

    # Warn if duplicate values are found
    if duplicate_values.any():
        duplicated_values_list = [
            index + 2 for index in series[duplicate_values].index.tolist()
        ]
        print("Duplicated values:", duplicated_values_list)


def normalize_excel(file_path, matter_value):
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Identify and remove unnamed columns, printing out the data they contained
    unnamed_cols = [col for col in df.columns if "Unnamed:" in str(col)]
    for col in unnamed_cols:
        print(f"Removed: {df[col].dropna().unique()}")
        df.drop(col, axis=1, inplace=True)

    # Rename columns
    df.rename(
        columns={"Document naam": "01 Document", "Document ID": "ID"}, inplace=True
    )

    # Ensure required columns exist
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            df[col] = None  # Add as empty columns if not present

    # Fill the 'Matter' field with matter_value if it's empty
    if "Matter" in df.columns:
        df["Matter"] = df["Matter"].fillna(matter_value)
    else:
        df["Matter"] = matter_value

    # Normalize the 'Datum' field to datetime, empty if non-convertable
    if "Datum" in df.columns:
        df["Datum"] = normalize_date(df["Datum"])

    if "ID" in df.columns:
        df["ID"] = normalize_id(df["ID"])
        warn_empty_id(df["ID"])
        warn_duplicates(df["ID"])

    if "Beoordelingsgrond" in df.columns:
        df["Beoordelingsgrond"] = normalise_beoordeling(df["Beoordelingsgrond"])

    if "File type" in df.columns:
        df["File type"] = replace_types(df["File type"])
        # df["File type"] = normalize_types(df["File type"]) # let's not

    # Save the normalized DataFrame to a new Excel file
    directory, file_name = os.path.split(file_path)
    new_file_name = "Normalized_" + file_name
    normalized_file_path = os.path.join(directory, new_file_name)
    df.to_excel(normalized_file_path, index=False)
    print(f"Normalized file saved as: {normalized_file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python normalize_excel.py <path_to_excel_file> <matter>")
        sys.exit(1)

    excel_file_path = sys.argv[1]
    matter = sys.argv[2]
    if not os.path.isfile(excel_file_path):
        print("The specified file does not exist.")
        sys.exit(1)

    normalize_excel(excel_file_path, matter)
