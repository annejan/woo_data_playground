import os
import csv
import sys


def get_xlsx_files_in_folder(folder_path):
    """Return a list of XLSX filenames in the given folder."""
    return [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]


def main(txt_filepath, output_filepath):
    with open(txt_filepath, "r", encoding="utf-8") as txt_file:
        folders = [line.strip() for line in txt_file]

    with open(output_filepath, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write header row to the CSV
        writer.writerow(["Folder", "XLSX Files"])

        # For each folder, check for XLSX files and write them to the CSV
        for folder in folders:
            if os.path.exists(folder):
                xlsx_files = get_xlsx_files_in_folder(folder)
                xlsx_files_str = ", ".join(
                    xlsx_files
                )  # Convert list of files to comma-separated string
                writer.writerow([folder, xlsx_files_str])
            else:
                print(f"Warning: Folder {folder} does not exist.")

    print(f"Output saved to '{output_filepath}'.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python script_name.py <path_to_folders.txt> <path_for_output_csv>"
        )
        sys.exit(1)

    txt_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(txt_path):
        print(f"Error: Text file '{txt_path}' not found.")
        sys.exit(1)

    main(txt_path, output_path)
