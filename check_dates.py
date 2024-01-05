import pandas as pd
import sys


def calculate_filled_percentage(filename):
    try:
        # Read the Excel file
        df = pd.read_excel(filename)
        if "Datum" not in df.columns:
            return "Error: 'Datum' column not found"

        # Calculate the percentage of filled rows in the 'Datum' column
        filled_percentage = df["Datum"].notna().mean() * 100
        return f"{filled_percentage:.2f}%"
    except Exception as e:
        return f"Error processing file: {e}"


def main():
    for filename in sys.argv[1:]:
        percentage_filled = calculate_filled_percentage(filename)
        print(f"{filename}: {percentage_filled}")


if __name__ == "__main__":
    main()
