import easyocr
import sys
import argparse
import glob
from pdf2image import convert_from_path
import numpy as np


def create_arg_parser():
    """Create and return the ArgumentParser object for command line options."""
    parser = argparse.ArgumentParser(description="Convert PDF files to text using OCR.")
    parser.add_argument(
        "pdf_glob", help="The glob pattern for PDF files to be converted."
    )
    parser.add_argument(
        "--dpi", type=int, default=600, help="DPI for image conversion, default is 600."
    )
    parser.add_argument(
        "--lang", default="nl", help="Language code for OCR, default is 'nl'."
    )
    return parser


def perform_ocr_on_page(page_image, reader):
    """Perform OCR on a single page image."""
    ocr_results = reader.readtext(np.array(page_image))
    page_text = " ".join(result[1] for result in ocr_results)
    return page_text


def process_pdf(pdf_path, reader, dpi):
    """Process a single PDF file, performing OCR on each page."""
    pages = convert_from_path(pdf_path, dpi=dpi, fmt="jpeg", thread_count=4)
    full_text = []

    for page_number, page_image in enumerate(pages, start=1):
        print(f"Processing page {page_number}...")
        page_text = perform_ocr_on_page(page_image, reader)
        full_text.append(page_text)

    return "\n\n".join(full_text)


def main():
    """Process PDFs and handle config"""
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    # Initialize the OCR reader instance outside of the loop
    reader = easyocr.Reader([args.lang], gpu=True)

    for pdf_file_path in glob.glob(args.pdf_glob):
        print(f"Starting OCR for {pdf_file_path}")
        extracted_text = process_pdf(pdf_file_path, reader, args.dpi)

        text_file_path = pdf_file_path.replace(".pdf", "_ocr.txt")
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(extracted_text)
            print(f"Extracted text written to {text_file_path}")


if __name__ == "__main__":
    main()
