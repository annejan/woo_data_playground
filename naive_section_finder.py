"""
PDF Table of Contents Extractor

This script extracts the table of contents (TOC) from a PDF file and optionally writes it to an Excel file.
"""
import argparse
import fitz  # PyMuPDF
from openpyxl import Workbook


def extract_table_of_contents(pdf_file):
    """
    Extract the table of contents (TOC) from a PDF file.

    Args:
        pdf_file (str): Path to the PDF file to extract the TOC from.

    Returns:
        list of tuples: A list containing tuples of (document_number, page_number).
    """
    doc = fitz.open(pdf_file)
    return doc.get_toc()


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

    a = 2
    for toc_item in output_data:
        sheet[f"A{a}"] = toc_item[1]
        sheet[f"B{a}"] = toc_item[2]
        a = a + 1

    workbook.save(output_file)


def main():
    parser = argparse.ArgumentParser(
        description="Extract chapters and page numbers from a PDF file."
    )
    parser.add_argument("pdf_file", help="Path to the PDF file to analyze.")
    parser.add_argument(
        "--output-file",
        required=False,
        help="Specify the output Excel file",
    )
    args = parser.parse_args()

    toc = extract_table_of_contents(args.pdf_file)

    for toc_item in toc:
        print(f"Document: {toc_item[1]}\ton page: {toc_item[2]}")

    if toc and args.output_file:
        write_to_excel(toc, args.output_file)
        print(f"Data has been written to {args.output_file}")


if __name__ == "__main__":
    main()
