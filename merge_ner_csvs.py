"""
ombine and Sort NER Results

This script combines multiple CSV files and optionally sorts the combined data by a specified column and direction. It then saves the result to a new CSV file.

Usage:
    python combine_and_sort_csv.py <input_files> [--output output_file.csv] [--sort-by sort_column] [--sort-direction (asc|desc)]

Arguments:
    input_files: Input CSV files to be combined.
    output_file: (Optional) Output CSV file name for the combined data. Default is 'combined.csv'.
    sort_column: (Optional) Column name to sort the data by. Default is 'Count'.
    sort_direction: (Optional) Sort direction: 'asc' (ascending) or 'desc' (descending). Default is 'asc'.

Example:
    python combine_and_sort_csv.py file1.csv file2.csv --output sorted_output.csv --sort-by Tag --sort-direction desc

SPDX-License-Identifier: EUPL-1.2
"""
import argparse
import pandas as pd


def combine_and_sort_csv(file_names, output_file, sort_column, sort_direction):
    dataframes = []

    for file_name in file_names:
        df = pd.read_csv(file_name)
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)

    if sort_column:
        combined_df = combined_df.sort_values(
            by=sort_column, ascending=(sort_direction == "asc")
        )

    combined_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine and sort CSV files")
    parser.add_argument("input_files", nargs="+", help="Input CSV files to combine")
    parser.add_argument(
        "--output",
        default="combined.csv",
        help="Output CSV file name (default: combined.csv)",
    )
    parser.add_argument(
        "--sort-by",
        default="Count",
        help="Column name to sort the data by (default: Count)",
    )
    parser.add_argument(
        "--sort-direction",
        default="asc",
        choices=["asc", "desc"],
        help='Sort direction: "asc" (ascending) or "desc" (descending) (default: asc)',
    )

    args = parser.parse_args()
    combine_and_sort_csv(
        args.input_files, args.output, args.sort_by, args.sort_direction
    )
