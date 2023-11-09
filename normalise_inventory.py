import pandas as pd
import sys
import os


def normalize_date(date_series):
    # Try to convert the dates. If conversion fails, return None
    return pd.to_datetime(date_series, format="%d-%m-%Y", errors="coerce")


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
    required_columns = [
        "Family ID",
        "Email Thread ID",
        "File type",
        "Period",
        "Subject",
        "Matter",
        "Datum",
    ]
    for col in required_columns:
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
