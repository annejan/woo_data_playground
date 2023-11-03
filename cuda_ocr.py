import easyocr
import sys
import argparse
from pdf2image import convert_from_path
import numpy as np


def create_arg_parser():
    """Create and return the ArgumentParser object for command line options."""
    parser = argparse.ArgumentParser(description="Convert a PDF to text using OCR.")
    parser.add_argument("pdf_file", help="The PDF file to be converted.")
    parser.add_argument(
        "--dpi", type=int, default=600, help="DPI for image conversion, default is 600."
    )
    parser.add_argument(
        "--lang", default="nl", help="Language code(s) for OCR, default is 'nl'."
    )
    return parser


def perform_ocr_on_pdf(pdf_path, dpi=600, language="nl"):
    """Perform OCR on the given PDF and return the extracted text."""
    reader = easyocr.Reader([language], gpu=True)
    pages = convert_from_path(pdf_path, dpi=dpi, fmt="jpeg", thread_count=4)

    full_text = []

    for page_number, page_image in enumerate(pages, start=1):
        print(f"Processing page {page_number}...")
        ocr_results = reader.readtext(np.array(page_image))
        page_text = " ".join(result[1] for result in ocr_results)
        full_text.append(page_text)

    return "\n\n".join(full_text)


def main():
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    pdf_file_path = args.pdf_file
    dpi_setting = args.dpi
    ocr_language = args.lang

    extracted_text = perform_ocr_on_pdf(
        pdf_file_path, dpi=dpi_setting, language=ocr_language
    )

    text_file_path = pdf_file_path.replace(".pdf", "_ocr.txt")
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)
        print(f"Extracted text written to {text_file_path}")


if __name__ == "__main__":
    main()
