"""
PDF Document Number Extractor

This Python script allows you to extract document numbers (or number-letter combinations) from PDF files.
It can locate and extract information based on a specified viewbox or use a default viewbox if none is provided.
The script uses the PyMuPDF library to handle PDF files and Tesseract for Optical Character Recognition (OCR) when necessary.

Key Features:
- Extract document numbers from PDF files with customizable viewboxes.
- Utilizes PyMuPDF for PDF document handling and Tesseract OCR for image-based text extraction.
- Supports specifying custom viewboxes for precise data extraction.
- Provides clear command-line usage with options for specifying PDF files and viewboxes.

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

The script will extract document numbers from the PDF file and display the extracted information along with the page number on the terminal.

This package is open-source and released under the European Union Public License version 1.2. 
You are free to use, modify, and distribute the package in accordance with the terms of the license.

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.
"""
import argparse
import re
import subprocess
import os
import fitz  # PyMuPDF

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
        check=False
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
    """
    try:
        with fitz.open(pdf_file_path) as pdf_document:
            for page_number in range(pdf_document.page_count):
                rect = process_page(pdf_document, viewbox)
                text = extract_text_from_pdf(pdf_document, page_number, rect)
                match = re.search(r"\d+[A-Za-z]*", text)
                if match:
                    print(f"Document: {match.group()}\ton page: {page_number + 1}")
                else:
                    pix = pdf_document[page_number].get_pixmap(clip=rect)
                    text = extract_text_from_image(pix.tobytes("png"))
                    match = re.search(r"\d+[A-Za-z]*", text)
                    if match:
                        print(f"Document: {match.group()}\ton page: {page_number + 1}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    Parse command-line arguments and execute the PDF data extraction process.
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
        metavar=('L', 'T', 'R', 'B')
    )

    args = parser.parse_args()
    pdf_file_path = args.pdf_file
    if not os.path.isfile(pdf_file_path):
        print(f"Error: The specified PDF file '{pdf_file_path}' does not exist.")
        return

    viewbox = args.viewbox if args.viewbox else [-180, 20, -20, 120]  # Default viewbox

    extract_pdf_data(pdf_file_path, viewbox)


if __name__ == "__main__":
    main()
