# PDF to Text Converter

## Description

This script, `convert_pdf.py`, converts PDF files to text by trying two methods: 

1. Direct text extraction from PDF pages.
2. Optical Character Recognition (OCR).

This tool is particularly useful for checking if PDFs have a text layer and for identifying potential visibility issues with the text in PDFs.
It can also be used to quicly make easilly searchable text indices.

## Features

- Direct text extraction from PDF using `pdfplumber`.
- OCR using `pytesseract` and `PIL`.
- Output generation for both direct extraction and OCR for comparison.

## Requirements

- Python 3.x
- `pdfplumber`
- `pytesseract`
- `Pillow` (PIL Fork)

You may need to install the dependencies if you haven't already:

```bash
pip install pdfplumber pytesseract Pillow
```

Ensure Tesseract-OCR is installed and available in your system's PATH, or set its path manually in the script.

## Usage

### Command Line Syntax

```bash
python convert_pdf.py <path_to_pdf_file>
```

### Example Usage

```bash
python convert_pdf.py document.pdf
```

This will process `document.pdf`, extract text directly if possible, and perform OCR. It will generate two files:

- `document.pdf.txt` - Contains text extracted directly from the PDF.
- `document.pdf.ocr` - Contains text obtained through OCR.

### Alternate Usage

```bash
for pdf in folder/*.pdf; do python convert_pdf.py "$pdf"; done
```

This will convert all PDFs in a folder

## Output Details

- The `.pdf.txt` file is useful to check the presence and quality of a text layer in the PDF.
- The `.pdf.ocr` file helps identify visibility issues with the text such as font rendering problems or obscured text.

## Contributing

Your contributions are welcome! Please feel free to submit pull requests, report issues, or suggest improvements.

## License


This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.


## Contact

For questions or feedback regarding this script, please open an issue in the repository.

