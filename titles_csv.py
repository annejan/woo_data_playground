import os
import csv
import argparse

def find_title_files(start_dir):
    """Yield folder and title from title.txt files under start_dir."""
    for dirpath, _, filenames in os.walk(start_dir):
        if "title.txt" in filenames:
            with open(os.path.join(dirpath, "title.txt"), 'r') as file:
                title = file.read().strip()
                yield dirpath, title

def write_to_csv(output_filename, data):
    """Write data to a CSV file."""
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["folder", "title"])  # header
        writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="Search for title.txt files and write to CSV.")
    parser.add_argument("start_dir", help="Directory to start the search.")
    parser.add_argument("output_csv", help="Name of the CSV file to write to (e.g., output.csv).")
    args = parser.parse_args()

    data = list(find_title_files(args.start_dir))
    write_to_csv(args.output_csv, data)
    print(f"Data written to {args.output_csv}")

if __name__ == "__main__":
    main()

