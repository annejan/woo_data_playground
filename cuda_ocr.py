import easyocr
import sys
import argparse
from pdf2image import convert_from_path
import numpy as np

# Create an OCR reader instance with English as the language and using CUDA
reader = easyocr.Reader(["en"], gpu=True)


def pdf_to_text(pdf_path, dpi=300):
    # Convert PDF to a list of images
    pages = convert_from_path(pdf_path, dpi=dpi, fmt="jpeg", thread_count=4)

    full_text = ""

    # Process each page
    for page_number, page in enumerate(pages, start=1):
        print(f"Processing page {page_number}...")

        # OCR the page
        results = reader.readtext(np.array(page))

        # Combine the text from each OCR result
        page_text = " ".join([res[1] for res in results])
        full_text += page_text + "\n"

        # Optionally, save each page as an image if needed
        # page.save(f'page_{page_number}.jpg', 'JPEG')

    return full_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PDF to text using OCR.")
    parser.add_argument("pdf_file", help="The PDF file to be converted.")
    parser.add_argument("--dpi", type=int, default=300, help="The DPI for image conversion. Default is 600.")
    args = parser.parse_args()

    pdf_file_path = args.pdf_file
    dpi_value = args.dpi

    # Convert the PDF to text using the specified DPI
    extracted_text = pdf_to_text(pdf_file_path, dpi=dpi_value)

    # Write the extracted text to a txt file
    txt_file_path = pdf_file_path.replace('.pdf', '_ocr.txt')
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(extracted_text)
        print(f"Extracted text written to {txt_file_path}")
