# CUDA OCR PDF Processing

This Python script utilizes `easyocr` to perform Optical Character Recognition (OCR) on PDF files and convert them into text. It's designed to handle multiple PDF files using a glob pattern and supports configurable DPI and language settings.

Read more about [EasyOCR](https://github.com/JaidedAI/EasyOCR) on their GitHub.

## Requirements

- Python 3.6 or higher
- easyocr
- pdf2image
- numpy

Install the required packages using pip:

```bash
pip install easyocr pdf2image numpy
```

## Usage

Run the script from the command line, providing the glob pattern for the PDF files you want to convert, and optional arguments for DPI and language:

```bash
python pdf_ocr_script.py 'path/to/pdf/files/*.pdf' --dpi 600 --lang 'nl'
```

### Arguments

- `pdf_glob`: The glob pattern for the PDF files to convert (e.g., `'./pdfs/*.pdf'`).
- `--dpi` (optional): The resolution used for converting PDF pages to images before OCR. Default is `600`.
- `--lang` (optional): The language code used by OCR. Default is Dutch (`'nl'`), but you can set it to any supported language like English (`'en'`).

### Output

The script will create a text file for each PDF file processed, containing the extracted text. These text files will be saved in the same directory as the PDF files, with the original filename suffixed with `_ocr.txt`.

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.

## Contributing

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.
