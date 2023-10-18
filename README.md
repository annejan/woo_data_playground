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

## PDF Downloader and Data Extraction Script

This Python script is designed to download PDF files from a specific webpage, extract link-title pairs from JSON data, and organize the downloaded PDFs into folders. It can be used to automate the retrieval of PDF documents from a web source and store them locally.

- Required Python libraries: requests and BeautifulSoup. You can install them using pip:

```bash
pip install requests beautifulsoup4
```

## Customization

You can customize the script for your specific use case:

- Modify the `json_url` and `base_url` variables to point to your data source and web source.
- Customize the naming of folders and files as per your requirements.
- Extend the functionality to handle additional data processing or tasks.

## Warning

This script downloads approximately 80 Gigabytes of PDF files in its default configuration!

1. Open the script in a text editor and configure the following variables:
   - `json_url`: The URL of the JSON data source.
   - `base_url`: The base URL of the web source containing PDF links.
2. Run the script by executing the following command in your terminal:

```bash
python script_name.py
```

The script will retrieve JSON data, process it, and download PDFs into folders based on the retrieved data.

## Script Overview

- The script retrieves JSON data from a specified URL using the `requests` library.
- It extracts link-title pairs from the JSON data and saves them in a CSV file.
- For each link-title pair, the script creates a folder and saves the title information in a text file.
- It also downloads associated PDF files and saves them in the corresponding folders.

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.

## Contributing

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.
