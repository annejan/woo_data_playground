# PDF Cutter

`pdf_cutter.py` is a command-line tool written in Python that allows you to split a single PDF file into multiple PDF files based on the page numbers provided in an Excel spreadsheet.
Each output PDF file is named after a unique identifier specified in the spreadsheet.

## Features

- Split a single PDF into multiple documents.
- Use an Excel file to define the start page of each new document.
- Name each new PDF file using a unique document identifier from the Excel file.
- Check to ensure the PDF has the required number of pages.

## Requirements

- Python 3
- `pandas` library
- `pikepdf` library

## Installation

Before running the script, ensure that Python 3 is installed on your system. You can then install the required Python libraries using `pip`:

```bash
pip install pandas pikepdf
```

## Usage

To use `pdf_cutter.py`, you need an Excel file with the following format:

| DocumentID | Page |
|------------|------|
| 1          | 1    |
| 1a         | 5    |
| 2          | 8    |

Here, `DocumentID` is a unique identifier for the output PDFs, and `Page` is the starting page number in the original PDF for that document.

To run the script, use the following command in your terminal:

```bash
python pdf_cutter.py [excel_file] [pdf_file]
```

Replace `[excel_file]` with the path to your Excel file, and `[pdf_file]` with the path to your PDF file.

## Output

The script will output PDF files in the current working directory, each named after the `DocumentID` column in the Excel file. 
For example, if the Excel file specifies document IDs "1" and "1a", the script will generate `1.pdf` and `1a.pdf`.

## Limitations

- The script does not support encrypted PDFs.
- The script does not copy any metadata from the original PDF.
- The script does not aggressively compress or reduce the size of output PDF files.

## Contributing

Contributions to `pdf_cutter.py` are welcome. Please fork the repository and submit a pull request.

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.

## Contributing

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.