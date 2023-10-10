import argparse
import fitz  # PyMuPDF
import re
import subprocess

tess = "tesseract stdin stdout --psm 7 -l nld"

# Function to extract structured data from a PDF file
def extract_pdf_data(pdf_file_path, viewbox):
    # Open the PDF file
    pdf_document = fitz.open(pdf_file_path)
    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        width = page.mediabox_size.x
        height = page.mediabox_size.y
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
        #        print(rect)
        text = page.get_textbox(rect)
        #        pix = page.get_pixmap(clip=rect)
        #        pix.save(f"{page_number}.png")
        match = re.search(r"\d+[A-Za-z]*", text)
        if match:
            print(f"Document: {match.group()} on page: {page_number+1}")
        else:
            pix = page.get_pixmap(clip=rect)
            rc = subprocess.run(
                tess,
                input=pix.tobytes("png"),
                stdout=subprocess.PIPE,
                shell=True,
                stderr=subprocess.DEVNULL,
            )
            text = rc.stdout.decode()
            match = re.search(r"\d+[A-Za-z]*", text)
            if match:
                print(f"Document: {match.group()} on page: {page_number+1}")

    # Close the PDF document
    pdf_document.close()


# Define command-line arguments
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
    viewbox = args.viewbox if args.viewbox else [-180, 20, -20, 120]  # Default viewbox

    extract_pdf_data(pdf_file_path, viewbox)


if __name__ == "__main__":
    main()
