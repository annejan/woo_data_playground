# Title CSV Generator

## Description

This utility script, `titles_csv.py`, is designed to search through a directory structure for files named `title.txt`, extract their contents, and compile the results into a CSV file. Each `title.txt` file contains a title that is associated with its respective directory.

## Features

- Recursive directory search for `title.txt` files
- CSV output with folder paths and corresponding titles
- Command-line interface for specifying start directory and output file

## Requirements

- Python 3.x
- No additional Python packages are required to run this script.

## Usage

To use this script, you can simply run it from the command line providing two arguments: 
1. The starting directory path to begin searching for `title.txt` files.
2. The desired output CSV file name.

### Command Line Syntax
```bash
python titles_csv.py <start_directory> <output_csv_file>
```

### Example Usage

```bash
python titles_csv.py ./my_documents titles_output.csv
```

This will search for all `title.txt` files within the `./my_documents` directory and its subdirectories, extract the titles, and then write them to `titles_output.csv` with two columns: `folder` and `title`.

## Output Format

The CSV file will contain headers as the first row:

- `folder`: The path of the folder containing a `title.txt` file.
- `title`: The title extracted from the `title.txt` file.

Each subsequent row corresponds to a `title.txt` file found during the search.

## Contributing

Feel free to fork this project, submit issues and enhancement requests, and contribute through pull requests.

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.


## Contact

If you have any questions or feedback, please reach out to the repository owner.

