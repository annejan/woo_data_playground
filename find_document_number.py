"""
PDF Document Number Extractor

This Python script allows you to extract document numbers (or number-letter combinations) from PDF files.
It can locate and extract information based on a specified viewbox or use a default viewbox if none is provided.
The script uses the PyMuPDF library to handle PDF files and Tesseract for Optical Character Recognition (OCR) when necessary.

Key Features:
- Extract document numbers from PDF files with customizable viewboxes.
- Utilizes PyMuPDF for PDF document handling and Tesseract OCR for image-based text extraction.
- Supports specifying custom viewboxes for precise data extraction.
- Provides clear command-line usage with options for specifying PDF files, viewboxes, and an output Excel file.

Usage:
1. Clone this repository or download the `pdf_data_extractor.py` script to your local machine.
2. Ensure you have a PDF file that you want to extract data from.
3. Open a terminal or command prompt and navigate to the directory containing the `pdf_data_extractor.py` script.
4. Run the script with the following command, replacing `<pdf_file>` with the path to your PDF file:

   ```bash
   python pdf_data_extractor.py <pdf_file>
   ```

Optional: You can specify a custom viewbox using the `--viewbox` argument.
The viewbox should be provided as four floating-point numbers separated by spaces (left top right bottom).

For example:

   ```bash
   python pdf_data_extractor.py <pdf_file> --viewbox -180 20 -20 120
   ```

Optional: You can specify an output Excel file using the --output-file argument. If not provided, data will be saved to "output.xlsx."

The script will extract document numbers from the PDF file and display and/or save the extracted information in an Excel file.

This package is open-source and released under the European Union Public License version 1.2.
You are free to use, modify, and distribute the package in accordance with the terms of the license.

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.
"""
import argparse
import re
import subprocess
import os
import fitz  # PyMuPDF
from openpyxl import Workbook

TESS_COMMAND = "tesseract stdin stdout --psm 7 -l nld"


def extract_text_from_image(image_bytes):
    """
    Extract text from an image using Tesseract OCR.

    Args:
        image_bytes (bytes): The image data in bytes.

    Returns:
        str: The extracted text from the image.
    """
    rc = subprocess.run(
        TESS_COMMAND,
        input=image_bytes,
        stdout=subprocess.PIPE,
        shell=True,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return rc.stdout.decode()


def extract_text_from_pdf(pdf_document, page_number, rect):
    """
    Extract text from a specified region of a PDF page.

    Args:
        pdf_document (fitz.Document): The PDF document object.
        page_number (int): The page number to extract text from.
        rect (fitz.Rect): The rectangular region to extract text from.

    Returns:
        str: The extracted text from the PDF page.
    """
    page = pdf_document[page_number]
    text = page.get_textbox(rect)
    return text


def write_to_excel(output_data, output_file):
    """
    Writes the extracted document numbers and their corresponding page numbers to an Excel file.

    Args:
        output_data (list of tuples): A list containing tuples of (document_number, page_number).
        output_file (str): The path to the Excel file where the data will be written.
    """
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Document Numbers"

    sheet["A1"] = "Document Number"
    sheet["B1"] = "Page Number"

    for i, (doc_number, page_number) in enumerate(output_data, start=2):
        sheet[f"A{i}"] = doc_number
        sheet[f"B{i}"] = page_number

    workbook.save(output_file)


def process_page(pdf_document, viewbox):
    """
    Process the viewbox coordinates to create a fitz.Rect object.

    Args:
        pdf_document (fitz.Document): The PDF document object.
        viewbox (list): The viewbox coordinates [left, top, right, bottom].

    Returns:
        fitz.Rect: The fitz.Rect object representing the processed viewbox.
    """
    width, height = pdf_document[0].mediabox_size
    left, top, right, bottom = viewbox

    if left < 0:
        left = width + left

    if right < 0:
        right = width + right

    if top < 0:
        top = height + top

    if bottom < 0:
        bottom = height + bottom

    rect = fitz.Rect(left, top, right, bottom)
    return rect


def extract_pdf_data(pdf_file_path, viewbox):
    """
    Extract document numbers from a PDF file.

    Args:
        pdf_file_path (str): The path to the PDF file.
        viewbox (list): The viewbox coordinates [left, top, right, bottom].
    Returns:
        list of tuples: A list containing tuples of (document_number, page_number) for each extracted document number.
    """
    output_data = []
    try:
        with fitz.open(pdf_file_path) as pdf_document:
            for page_number in range(pdf_document.page_count):
                rect = process_page(pdf_document, viewbox)
                text = extract_text_from_pdf(pdf_document, page_number, rect)
                match = re.search(r"\d+[A-Za-z]*", text)
                if match:
                    doc_number = match.group()
                    output_data.append((doc_number, page_number + 1))
                    print(f"Document: {doc_number}\ton page: {page_number + 1}")
                else:
                    pix = pdf_document[page_number].get_pixmap(clip=rect)
                    text = extract_text_from_image(pix.tobytes("png"))
                    match = re.search(r"\d+[A-Za-z]*", text)
                    if match:
                        doc_number = match.group()
                        output_data.append((doc_number, page_number + 1))
                        print(f"Document: {match.group()}\ton page: {page_number + 1}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return output_data


def main():
    """
    Parse command-line arguments and execute the PDF data extraction process.

    This function parses command-line arguments to specify the input PDF file and, optionally, a custom viewbox.
    It then calls the `extract_pdf_data` function to extract document numbers from the PDF file and display or save them
    in an Excel file if specified.

    Command-Line Arguments:
    - `pdf_file` (str): The path to the input PDF file.
    - `--viewbox` (list of float): Optionally, specify the viewbox as [left, top, right, bottom] for precise data extraction.
    - `--output-file` (str): Optionally, specify the output Excel file for saving the extracted data.

    Usage:
    To extract document numbers from a PDF file, run this script from the command line with the following command:

    ```
    python pdf_data_extractor.py <pdf_file> [--viewbox L T R B] [--output-file output.xlsx]
    ```

    If the `--output-file` option is not provided, the script will default to saving the data in an Excel file named "output.xlsx."
    """
    parser = argparse.ArgumentParser(
        description="Extract document numbers from a PDF file."
    )
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument(
        "--viewbox",
        nargs=4,
        type=float,
        required=False,
        help="Specify the viewbox as left top right bottom (e.g., --viewbox -180 20 -20 180)",
        metavar=("L", "T", "R", "B"),
    )
    parser.add_argument(
        "--output-file",
        required=False,
        help="Specify the output Excel file",
    )

    args = parser.parse_args()
    pdf_file_path = args.pdf_file
    if not os.path.isfile(pdf_file_path):
        print(f"Error: The specified PDF file '{pdf_file_path}' does not exist.")
        return

    viewbox = args.viewbox if args.viewbox else [-180, 20, -20, 120]  # Default viewbox

    output_data = extract_pdf_data(pdf_file_path, viewbox)
    if output_data and args.output_file:
        write_to_excel(output_data, args.output_file)
        print(f"Data has been written to {args.output_file}")


if __name__ == "__main__":
    main()
