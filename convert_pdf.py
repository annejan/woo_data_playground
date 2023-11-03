import sys
import os
import argparse
import pdfplumber
from pytesseract import image_to_string

# Check if Tesseract-OCR is in the PATH; if not, set its path manually.
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Uncomment and edit if needed
custom_config = r"--oem 3 --psm 6 -l nld"


def convert_pdf_to_text(pdf_path, dpi):
    text_output = ""
    ocr_output = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # Attempt to extract text directly from the PDF page
            try:
                page_text = page.extract_text()
            except Exception as e:
                print(
                    f"An error occurred during text extraction on page {page_num}: {e}"
                )
                page_text = None

            if page_text:
                text_output += page_text

            # Extract text using OCR
            page_image = page.to_image(resolution=dpi)
            try:
                page_text = image_to_string(page_image.original, config=custom_config)
                ocr_output += page_text
            except Exception as e:
                print(f"An error occurred during OCR on page {page_num}: {e}")

    return text_output, ocr_output


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF pages to text using OCR with adjustable DPI."
    )
    parser.add_argument("file", help="The PDF file to process.")
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="The resolution to use for image conversion. Default is 300 DPI.",
    )
    args = parser.parse_args()

    pdf_file_path = args.file
    dpi = args.dpi

    # Check if the file exists
    if not os.path.isfile(pdf_file_path):
        print(f"The file {pdf_file_path} does not exist.")
        sys.exit(1)

    # Remove .pdf and add suffix for the new file
    base_name = pdf_file_path.rsplit(".", 1)[0]
    text_file_path = base_name + ".pdf.txt"
    ocr_file_path = base_name + ".pdf.ocr"

    # Convert the PDF to text
    extracted_text, ocr_text = convert_pdf_to_text(pdf_file_path, dpi)

    # Write the extracted text to a .txt file
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)
        print(f"Directly extracted text written to {text_file_path}")

    # Write the OCR text to a .ocr file
    with open(ocr_file_path, "w", encoding="utf-8") as ocr_file:
        ocr_file.write(ocr_text)
        print(f"OCR extracted text written to {ocr_file_path}")


if __name__ == "__main__":
    main()
