"""
This script takes in a CSV file with a "title" column and searches within a specified
folder for subfolders containing a file named "title.txt". If the contents of this
file match the title in the CSV, the name of the subfolder is added to a new
"folder" column in the CSV output.

Usage:
python find_titles.py <path_to_csv> <path_to_search_folder>

Arguments:
- <path_to_csv>: Path to the CSV file containing titles to be matched.
- <path_to_search_folder>: Path to the root folder where the search will begin.

The output is an updated CSV file with an added "folder" column, indicating
which subfolder(s) contained a "title.txt" file matching the title from the CSV.
"""

import csv
import os
import sys


def find_matching_folders(base_folder, title):
    """
    Search for files named "title.txt" in subfolders of the base_folder,
    read the title from the file, and if it matches the provided title,
    return the subfolder's name.

    Args:
    - base_folder (str): Path to the root folder where the search begins.
    - title (str): Title to match against the contents of "title.txt" files.

    Returns:
    - list: List of subfolder names containing a "title.txt" file with a matching title.
    """
    matching_folders = []

    for root, dirs, files in os.walk(base_folder):
        if "title.txt" in files:
            with open(os.path.join(root, "title.txt"), "r", encoding="utf-8") as file:
                file_title = file.read().strip()
                if file_title == title:
                    matching_folders.append(os.path.basename(root))

    return matching_folders


def main(csv_filepath, search_folder):
    """
    Main function to read titles from a CSV, search for matching folders,
    and write the results to a new CSV file.

    Args:
    - csv_filepath (str): Path to the CSV file containing titles to be matched.
    - search_folder (str): Path to the root folder where the search will begin.
    """
    # Check if provided CSV file and search folder exist
    if not os.path.exists(csv_filepath):
        print(f"Error: CSV file '{csv_filepath}' not found.")
        return

    if not os.path.exists(search_folder):
        print(f"Error: Search folder '{search_folder}' not found.")
        return

    # Lists to store the updated rows
    updated_rows = []

    # Open the CSV file and read its rows
    with open(csv_filepath, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        # Go through each row and search for matching folders
        for row in reader:
            title = row.get("title", None)
            if title:
                matching_folders = find_matching_folders(search_folder, title)
                if not matching_folders:
                    print(title)
                for folder in matching_folders:
                    new_row = row.copy()
                    new_row["folder"] = folder
                    updated_rows.append(new_row)

    # Write the updated rows to a new CSV file
    new_csv_filepath = os.path.splitext(csv_filepath)[0] + "_updated.csv"
    fieldnames = list(updated_rows[0].keys())

    with open(new_csv_filepath, mode="w", encoding="utf-8", newline="") as new_csv_file:
        writer = csv.DictWriter(new_csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in updated_rows:
            writer.writerow(row)

    print(f"Updated CSV saved to '{new_csv_filepath}'.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python find_titles.py <path_to_csv> <path_to_search_folder>")
        sys.exit(1)

    csv_path = sys.argv[1]
    folder_path = sys.argv[2]

    main(csv_path, folder_path)
