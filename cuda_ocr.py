import easyocr
import sys
import argparse
import fitz
import numpy as np
from PIL import Image


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
    return parser


def perform_ocr_on_page(page_image, reader):
    """Perform OCR on a single page image."""
    ocr_results = reader.readtext(np.array(page_image))
    page_text = " ".join(result[1] for result in ocr_results)
    return page_text


def process_pdf(pdf_path, reader, dpi):
    """Process a single PDF file, performing OCR on each page."""
    doc = fitz.open(pdf_path)
    full_text = []
    n = 0
    for page in doc:
        n = n + 1
        print(f"Processing page {n}...")
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        page_text = perform_ocr_on_page(img, reader)
        full_text.append(page_text)

    return "\n\n".join(full_text)


def main():
    """Process PDFs and handle config"""
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    # Initialize the OCR reader instance outside of the loop
    reader = easyocr.Reader([args.lang], gpu=True)

    for pdf_file_path in args.pdf_files:
        print(f"Starting OCR for {pdf_file_path}")
        extracted_text = process_pdf(pdf_file_path, reader, args.dpi)

        text_file_path = pdf_file_path.replace(".pdf", "_ocr.txt")
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(extracted_text)
            print(f"Extracted text written to {text_file_path}")


if __name__ == "__main__":
    main()
