# PDF Document Number Extractor

This Python script allows you to extract a document number (or number letter combination) from a PDF file. It can locate and extract information based on a specified viewbox or use a default viewbox if none is provided. The script uses the PyMuPDF library to handle PDF files and Tesseract for OCR (Optical Character Recognition) when necessary.

## Prerequisites

Before you can use this script, you need to have the following prerequisites installed on your system:

- Python 3.x
- PyMuPDF (fitz)
- Tesseract OCR

### Installing PyMuPDF (fitz)

You can install the PyMuPDF library (fitz) using pip:

```bash
pip install PyMuPDF
```

### Installing Tesseract OCR

You need to install Tesseract OCR on your system. Visit the [Tesseract OCR GitHub page](https://github.com/tesseract-ocr/tesseract) for installation instructions specific to your operating system.

## Usage

To use this script, follow these steps:

1. Clone this repository or download the `pdf_data_extractor.py` script to your local machine.

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

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12). You are free to use, modify, and distribute the package in accordance with the terms of the license.

