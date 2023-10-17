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


def extract_text_from_pdf(pdf_document, page_number, rect, dump):
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
    if dump:
        pix = page.get_pixmap(clip=rect)
        pix.save(f"{page_number:04d}.png")
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
    sheet.title = "Documents"

    sheet["A1"] = "DocumentID"
    sheet["B1"] = "Page"

    for i, (doc_id, page_number) in enumerate(output_data, start=2):
        sheet[f"A{i}"] = doc_id
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


def extract_number(id):
    """
    Extract the numeric part from a given string ID.

    Args:
        id (str): The input string containing numeric and non-numeric characters.

    Returns:
        int: The extracted numeric part of the input string.

    Example:
    ```
    numeric_value = extract_number("12de")
    print(numeric_value)  # Output: 12
    ```

    If no numeric part is found in the input string, the function returns None.
    """
    # Use regular expression to extract the numeric part
    numeric_part = re.match(r"\d+", id)

    # Check if a match was found
    if numeric_part:
        # Convert the numeric part to an integer
        return int(numeric_part.group())


def extract_pdf_data(pdf_file_path, viewbox, minumum, maximum, dump):
    """
    Extract document numbers from a PDF file within a specified numeric range.

    Args:
        pdf_file_path (str): The path to the PDF file.
        viewbox (list): The viewbox coordinates [left, top, right, bottom].
        minimum (int): The minimum numeric value to consider (inclusive).
        maximum (int): The maximum numeric value to consider (inclusive).
        dump (bool): Dump images as {page_number}.png

    Returns:
        list of tuples: A list containing tuples of (document_id, page_number) for each extracted document number.

    Example:
    ```
    output_data = extract_pdf_data("example.pdf", [-180, 20, -20, 120], minimum=1, maximum=10)
    for doc_id, page_number in output_data:
        print(f"Document: {doc_id}\ton page: {page_number}")
    ```

    This function extracts document numbers from the PDF file, and only those within the specified numeric range (inclusive).
    """
    output_data = []
    try:
        with fitz.open(pdf_file_path) as pdf_document:
            for page_number in range(pdf_document.page_count):
                rect = process_page(pdf_document, viewbox)
                text = extract_text_from_pdf(pdf_document, page_number, rect, dump)
                match = re.search(r"\d+[A-Za-z]*", text)
                if match:
                    doc_id = match.group()
                    number = extract_number(doc_id)
                    if minumum <= number <= maximum:
                        output_data.append((doc_id, page_number + 1))
                        print(f"Document: {doc_id}\ton page: {page_number + 1}")
                else:
                    pix = pdf_document[page_number].get_pixmap(clip=rect)
                    text = extract_text_from_image(pix.tobytes("png"))
                    match = re.search(r"\d+[A-Za-z]*", text)
                    if match:
                        doc_id = match.group()
                        number = extract_number(doc_id)
                        if minumum <= number <= maximum:
                            output_data.append((doc_id, page_number + 1))
                            print(
                                f"Document: {match.group()}\ton page: {page_number + 1}"
                            )
    except Exception as e:
        print(f"An error occurred: {e}")

    return output_data


def analyse(output_data, minimum, maximum):
    """
    Analyse a list of document IDs for out-of-order and missing IDs within specified ranges.

    Args:
        output_data (list of tuples): A list containing tuples of (document_id, page_number).
        minimum (int): The minimum document ID to consider (inclusive).
        maximum (int): The maximum document ID to consider (inclusive).

    Prints:
        - Out-of-order document IDs within the specified range.
        - Missing document IDs within the specified range.

    Example Usage:
    ```
    output_data = [
        ("1", 1),
        ("2", 3),
        ("2a", 5),
        # ... (other document IDs)
    ]
    # Analyse within the range 1 to 10
    analyse(output_data, minimum=1, maximum=10)
    ```
    """
    # Extract document IDs
    document_ids = [
        re.match(r"(\d+)([A-Za-z]*)", doc_id).groups() for doc_id, _ in output_data
    ]

    # Initialize variables to track anomalies
    out_of_order_ids = []
    missing_ids = []

    # Iterate through the sorted list to detect out-of-order and missing IDs
    prev_id = (minimum - 1, "")
    first = True
    for doc_id, letter_part in document_ids:
        numeric_part = int(doc_id)

        if not first:
            prev_numeric, prev_letter = prev_id

            if numeric_part > prev_numeric + 1:
                for missing_numeric in range(prev_numeric + 1, numeric_part):
                    missing_ids.append(f"{missing_numeric}{letter_part}")
                prev_id = (numeric_part, letter_part)
            elif (
                numeric_part > maximum
                or numeric_part < minimum
                or (
                    numeric_part != prev_numeric + 1
                    and not (numeric_part == prev_numeric and letter_part > prev_letter)
                )
            ):
                out_of_order_ids.append(f"{numeric_part}{letter_part}")
            else:
                prev_id = (numeric_part, letter_part)
        else:
            prev_id = (numeric_part, letter_part)
            first = False

    # Report out-of-order and missing IDs
    if out_of_order_ids:
        print(f"Out-of-order document IDs: {', '.join(out_of_order_ids)}")
    if missing_ids:
        print(f"Missing document IDs: {', '.join(missing_ids)}")


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
    - `--analyse` or `--analyze` (optional): Analyse the extracted document IDs for out-of-order and missing IDs.
    - `--minimum` or `--min` (int, optional): The minimum expected document ID. If not specified, it is set to the first extracted ID.
    - `--maximum` or `--max` (int, optional): The maximum expected document ID.

    Usage:
    To extract document numbers from a PDF file, run this script from the command line with the following command:

    ```
    python pdf_data_extractor.py <pdf_file> [--viewbox L T R B] [--output-file output.xlsx] [--analyse] [--minimum MIN] [--maximum MAX]
    ```

    If the `--output-file` option is not provided, the script will default to saving the data in an Excel file named "output.xlsx."

    If the `--analyse` option is used, the script will analyse the extracted document IDs for out-of-order and missing IDs within the specified range.
    The range is defined by the `--minimum` and `--maximum` options.

    Example Usage:
    To extract document numbers from a PDF file and analyse for out-of-order and missing IDs within the range 1 to 20:

    ```
    python pdf_data_extractor.py <pdf_file> --analyse --minimum 1 --maximum 20
    ```

    If the `--minimum` and `--maximum` options are not provided, the script will use 1 as the minimum.
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
    parser.add_argument(
        "--analyse",
        "--analyze",
        required=False,
        action="store_true",
        help="Analyse the data",
    )
    parser.add_argument(
        "--minimum",
        "--min",
        type=int,
        required=False,
        help="Minimum expected documentID",
    )
    parser.add_argument(
        "--maximum",
        "--max",
        type=int,
        required=False,
        help="Maximum expected documentID",
    )
    parser.add_argument(
        "--dump",
        required=False,
        action="store_true",
        help="Dump the viewports as {pagenumber}.png",
    )

    args = parser.parse_args()
    pdf_file_path = args.pdf_file
    if not os.path.isfile(pdf_file_path):
        print(f"Error: The specified PDF file '{pdf_file_path}' does not exist.")
        return

    viewbox = args.viewbox if args.viewbox else [-180, 20, -20, 120]  # Default viewbox

    minimum = args.minimum
    if not minimum:
        minimum = 1
    maximum = args.maximum
    if not maximum:
        maximum = 99999999

    output_data = extract_pdf_data(pdf_file_path, viewbox, minimum, maximum, args.dump)

    if output_data and args.analyse:
        analyse(output_data, minimum, maximum)

    if output_data and args.output_file:
        write_to_excel(output_data, args.output_file)
        print(f"Data has been written to {args.output_file}")


if __name__ == "__main__":
    main()
