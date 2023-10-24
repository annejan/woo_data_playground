import sys


def read_list_from_file(filepath):
    """Read items from a file and return them as a list."""
    with open(filepath, "r") as file:
        return [line.strip() for line in file]


def find_missing_items(list_a, list_b):
    """Return items that are in list_b but not in list_a."""
    return set(list_b) - set(list_a)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python script_name.py <path_to_list_a_file> <path_to_list_b_file>"
        )
        sys.exit(1)

    file_a_path = sys.argv[1]
    file_b_path = sys.argv[2]

    list_a = read_list_from_file(file_a_path)
    list_b = read_list_from_file(file_b_path)

    missing_items = find_missing_items(list_a, list_b)

    if missing_items:
        print("Missing items:")
        for item in missing_items:
            print(item)
    else:
        print("No items are missing.")
