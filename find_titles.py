import csv
import os
import sys


def find_matching_folders(base_folder, title):
    """
    Search for files named "title.txt" in subfolders of the base_folder,
    read the title from the file, and if it matches the provided title,
    return the subfolder's name.
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
        print("Usage: python script_name.py <path_to_csv> <path_to_search_folder>")
        sys.exit(1)

    csv_path = sys.argv[1]
    folder_path = sys.argv[2]

    main(csv_path, folder_path)
