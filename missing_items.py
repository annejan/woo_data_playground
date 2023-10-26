"""
This script compares two lists (each read from a file)
and prints items that are missing from either list when
compared to the other.

Usage:
python missing_items.py <path_to_list_a_file> <path_to_list_b_file>

Arguments:
- <path_to_list_a_file>: Path to the file containing the first list.
- <path_to_list_b_file>: Path to the file containing the second list.
"""

import sys


def read_list_from_file(filepath):
    """
    Read items from a file and return them as a list.

    Args:
    - filepath (str): Path to the file to be read.

    Returns:
    - list: List of items read from the file.
    """
    with open(filepath, "r") as file:
        return [line.strip() for line in file]


def find_missing_items(list_a, list_b):
    """
    Return items that are missing from either list when compared to the other.

    Args:
    - list_a (list): First list of items.
    - list_b (list): Second list of items.

    Returns:
    - tuple: Two sets of items:
        * First set contains items that are in list_a but not in list_b.
        * Second set contains items that are in list_b but not in list_a.
    """
    missing_in_b = set(list_a) - set(list_b)
    missing_in_a = set(list_b) - set(list_a)
    return missing_in_b, missing_in_a


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python missing_items.py <path_to_list_a_file> <path_to_list_b_file>"
        )
        sys.exit(1)

    file_a_path = sys.argv[1]
    file_b_path = sys.argv[2]

    list_a = read_list_from_file(file_a_path)
    list_b = read_list_from_file(file_b_path)

    missing_in_b, missing_in_a = find_missing_items(list_a, list_b)

    if missing_in_b or missing_in_a:
        if missing_in_b:
            print("Items in list A but not in list B:")
            for item in missing_in_b:
                print(item)
        if missing_in_a:
            print("\nItems in list B but not in list A:")
            for item in missing_in_a:
                print(item)
    else:
        print("No items are missing in either list.")
