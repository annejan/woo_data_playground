"""
PDF to Text OCR Converter

This module provides a command-line interface for converting PDF files to text using OCR (Optical Character Recognition).
It leverages the EasyOCR library for OCR tasks and PyMuPDF for efficient extraction of images from PDF pages. The script
processes each page of the given PDF file(s), performs OCR, and saves the extracted text into corresponding text files.

Requirements:
- easyocr: For OCR operations.
- PyMuPDF (fitz): For handling PDF and image data.

Usage:
    python cuda_ocr.py file1.pdf file2.pdf --dpi 300 --lang en

Arguments:
- pdf_files: One or more PDF files to be processed.
- --dpi: The dots per inch setting for the image extraction process. Default is 600.
- --lang: The language code to be used by OCR. Default is 'nl' (Dutch).

Output:
The script will output a text file with the same name as the input PDF file, appended with "_ocr.txt". For example,
if the input file is "document.pdf", the output will be "document_ocr.txt".

Example:
    To convert a single PDF file to text with OCR in English and a DPI of 300:
        python cuda_ocr.py document.pdf --dpi 300 --lang en

    To convert multiple PDF files in folder "docs" to text with OCR in Dutch and the default DPI:
        python cuda_ocr.py docs/*.py 


This package is open-source and released under the European Union Public License version 1.2.
You are free to use, modify, and distribute the package in accordance with the terms of the license.

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.

SPDX-License-Identifier: EUPL-1.2
"""
import os
import sys
import argparse
import fitz
import easyocr


def create_arg_parser():
    """Create and return the ArgumentParser object for command line options."""
    parser = argparse.ArgumentParser(description="Convert PDF files to text using OCR.")
    parser.add_argument("pdf_files", nargs="+", help="PDF file(s) to be converted.")
    parser.add_argument(
        "--dpi", type=int, default=600, help="DPI for image conversion, default is 600."
    )
    parser.add_argument(
        "--lang", default="nl", help="Language code for OCR, default is 'nl'."
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=1,
        help="Batch size for OCR processing within an image, default is 1.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force the action to run even if the file exists",
    )
    return parser


def perform_ocr_on_page(page_image, reader, batch_size):
    """Perform OCR on a single page image using the given batch size."""
    ocr_results = reader.readtext(
        page_image, detail=0, paragraph=True, batch_size=batch_size
    )
    page_text = "\n".join(ocr_results)
    return page_text


def process_pdf(pdf_path, reader, dpi, batch_size):
    """Process a single PDF file, performing OCR on each page."""
    doc = fitz.open(pdf_path)
    full_text = []
    print(f"Pages {len(doc)}")
    for page_num, page in enumerate(doc, start=1):
        print(f"Processing page {page_num:04}")
        scale = dpi / 72
        matrix = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=matrix)
        try:
            page_image = pix.tobytes("png")
            page_text = perform_ocr_on_page(page_image, reader, batch_size)
            full_text.append(page_text)
        except Exception as e:
            print(f"An error occurred while processing page {page_num:04}: {e}")
        finally:
            pix = None  # Free pixmap memory immediately

    return "\n\n".join(full_text)


def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()
    reader = easyocr.Reader([args.lang], gpu=True)
    for pdf_file_path in args.pdf_files:
        text_file_path = pdf_file_path.replace(".pdf", "_ocr.txt")
        if args.force or not os.path.exists(text_file_path):
            print(f"Starting OCR for {pdf_file_path}")
            extracted_text = process_pdf(pdf_file_path, reader, args.dpi, args.batch)
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(extracted_text)
                print(f"Extracted text written to {text_file_path}")


if __name__ == "__main__":
    main()
