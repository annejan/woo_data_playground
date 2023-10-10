import argparse
import fitz  # PyMuPDF
import re
import subprocess
import os

TESS_COMMAND = "tesseract stdin stdout --psm 7 -l nld"


def extract_text_from_image(image_bytes):
    rc = subprocess.run(
        TESS_COMMAND,
        input=image_bytes,
        stdout=subprocess.PIPE,
        shell=True,
        stderr=subprocess.DEVNULL,
    )
    return rc.stdout.decode()


def extract_text_from_pdf(pdf_document, page_number, rect):
    page = pdf_document[page_number]
    text = page.get_textbox(rect)
    return text


def process_page(pdf_document, page_number, viewbox):
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
    try:
        with fitz.open(pdf_file_path) as pdf_document:
            for page_number in range(pdf_document.page_count):
                rect = process_page(pdf_document, page_number, viewbox)
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
    parser = argparse.ArgumentParser(
        description="Extract structured data from a PDF file."
    )
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument(
        "--viewbox",
        nargs=4,
        type=float,
        required=False,
        help="Specify the viewbox as left top right bottom (e.g., --viewbox -180 20 -20 180)",
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
