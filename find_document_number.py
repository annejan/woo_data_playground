import argparse
import fitz  # PyMuPDFA
import re
import subprocess

tess = "tesseract stdin stdout --psm 7 -l nld"

# Function to extract structured data from a PDF file
def extract_pdf_data(pdf_file_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_file_path)
    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        width = page.mediabox_size.x
        rect = fitz.Rect(width-120, 20, width-20, 120) 
#        print(rect)
        text = page.get_textbox(rect)
        match = re.search(r'\d+[A-Za-z]*', text)
        if match:
            print(f"Document: {match.group()} on page: {page_number+1}")
        else:
            pix = page.get_pixmap(clip=rect)
#            pix.save(f"page-{page_number+1}.png") 
            rc = subprocess.run(
                tess,  # the command
                input=pix.tobytes("png"),  # the pixmap image
                stdout=subprocess.PIPE,  # find the text here
                shell=True,
                stderr=subprocess.DEVNULL
            )
            text = rc.stdout.decode()  # convert to string
            match = re.search(r'\d+[A-Za-z]*', text)
            if match:
                print(f"Document: {match.group()} on page: {page_number+1}")


    # Close the PDF document
    pdf_document.close()

# Define command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Extract structured data from a PDF file.")
    parser.add_argument("pdf_file", help="Path to the PDF file")

    args = parser.parse_args()
    pdf_file_path = args.pdf_file

    extract_pdf_data(pdf_file_path)

if __name__ == "__main__":
    main()
