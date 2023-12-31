# PDF Document Number Extractor

This Python script allows you to extract document IDs (number or number letter combination) from a PDF file.
It can locate and extract information based on a specified viewbox or use a top right viewbox if none is provided.
The script uses the PyMuPDF library to handle PDF files and Tesseract for Optical Character Recognition (OCR) when necessary.

## Prerequisites

Before you can use this script, you need to have the following prerequisites installed on your system:

- Python 3.x
- PyMuPDF (fitz)
- OpenPyXL
- Tesseract OCR

### Installing PyMuPDF (fitz) and OpenPyXL

You can install the PyMuPDF and OpenPyXL libraries using pip:

```bash
pip install PyMuPDF openpyxl
```

or

```bash
pip install -r requirements.txt
```

### Installing Tesseract OCR

You need to install Tesseract OCR on your system. Visit the [Tesseract OCR GitHub page](https://github.com/tesseract-ocr/tesseract) for installation instructions specific to your operating system.

## PDF Table of Contents Extractor

This Python script is designed to extract the table of contents (TOC) from a PDF file and optionally write it to an Excel file. It uses the PyMuPDF library to analyze the PDF's structure and retrieve TOC information.

### Features

- Extracts the table of contents (TOC) from a PDF file.
- Writes the extracted document numbers and their corresponding page numbers to an Excel file.

### Usage

You can run the script from the command line with the following usage:

```bash
python naive_section_finder.py <pdf_file> [--output-file <output_excel>]
```

- `<pdf_file>`: The path to the PDF file you want to analyze.
- `--output-file <output_excel>` (optional): Specify the output Excel file where the TOC data will be saved.

### Example

```bash
python naive_section_finder.py sample.pdf --output-file toc.xlsx
```

In this example, the script will process `sample.pdf` and save the extracted TOC data to an Excel file named `toc.xlsx`.

## Finding documents the hard way

Unfortunately not all PDF files have a (useful) table of contents, in that case we'll have to do it the hard way.

To use this script, follow these steps:

1. Clone this repository or download the `find_document_id.py` script to your local machine.

2. Make sure you have a PDF file that you want to extract data from.

3. Open a terminal or command prompt and navigate to the directory containing the `find_document_id.py` script.

4. Run the script with the following command, replacing `<pdf_file>` with the path to your PDF file:

 ```bash
 python find_document_id.py <pdf_file>
 ```

Optional: You can specify a custom viewbox using the `--viewbox` argument. The viewbox should be provided as four floating-point numbers separated by spaces (left top right bottom).

For example:

```bash
python find_document_id.py <pdf_file> --viewbox -180 20 -20 120
```

The script will extract document numbers from the PDF file and display the extracted information and page number on the terminal.

Negative numbers for the viewbox coordinates offset the viewbox from the right and bottom edges of the page, rather than the left and top edges.
This allows you to specify a rectangular region within the PDF page based on its distance from the right and bottom edges.

## Example Output

```
Document: 1     on page: 1
Document: 2     on page: 3
Document: 2a    on page: 5
Document: 3     on page: 7
```

## Saving to an Excel File

You can also save the extracted document numbers and their corresponding page numbers to an Excel file by using the `--output-file` argument. For example:

```bash
python find_document_id.py <pdf_file> --output-file output.xlsx
```

## Document ID range

Optional: You can specify a range of acceptable document IDs using the `--min` and `--max` arguments.
This ensures that only document IDs within the specified range are considered.
If not provided, the default range is from 1 to 99999999.

Example:

```bash
python find_document_id.py <pdf_file> --min 10 --max 100
```

## Basic analysis

The optional `--analyse` flag tries to do some basic detection of out-of-order and missing document IDs.

```
Document: 30    on page: 1
Document: 28    on page: 5
Document: 32    on page: 9
Document: 32a   on page: 10
Document: 33    on page: 13
Out-of-order document IDs: 28
Missing document IDs: 31
```

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.

## Contributing

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.
