# PDF Document Number Extractor

This Python script allows you to extract document IDs (number or number letter combination) from a PDF file.
It can locate and extract information based on a specified viewbox or use a default viewbox if none is provided.
The script uses the PyMuPDF library to handle PDF files and Tesseract for Optical Character Recognition (OCR) when necessary.

## Prerequisites

Before you can use this script, you need to have the following prerequisites installed on your system:

- Python 3.x
- PyMuPDF (fitz)
- OpenPyXL
- Tesseract OCR

### Installing PyMuPDF (fitz)

You can install the PyMuPDF library (fitz) using pip:

```bash
pip install PyMuPDF
pip install openpyxl
```

or

```bash
pip install -r requirements.txt
```

### Installing Tesseract OCR

You need to install Tesseract OCR on your system. Visit the [Tesseract OCR GitHub page](https://github.com/tesseract-ocr/tesseract) for installation instructions specific to your operating system.

## Usage

To use this script, follow these steps:

1. Clone this repository or download the `find_document_number.py` script to your local machine.

2. Make sure you have a PDF file that you want to extract data from.

3. Open a terminal or command prompt and navigate to the directory containing the `pdf_data_extractor.py` script.

4. Run the script with the following command, replacing `<pdf_file>` with the path to your PDF file:

```bash
python find_document_number.py <pdf_file>
```

Optional: You can specify a custom viewbox using the `--viewbox` argument. The viewbox should be provided as four floating-point numbers separated by spaces (left top right bottom).

For example:

```bash
python find_document_number.py <pdf_file> --viewbox -180 20 -20 120
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
python find_document_number.py <pdf_file> --output-file output.xlsx
```

## Document ID range

Optional: You can specify a range of acceptable document IDs using the `--min` and `--max` arguments. 
This ensures that only document IDs within the specified range are considered.
If not provided, the default range is from 1 to 99999999.

Example:

```bash
python find_document_number.py <pdf_file> --min 10 --max 100
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
