"""
PDF Cutter Script

This script takes an Excel file and a PDF file as input and cuts the PDF into smaller PDFs based on the page numbers specified in the Excel file.
Each new PDF is named after the 'DocumentID' specified in the Excel file.

The Excel file should contain two columns:
- 'DocumentID': A unique identifier for each document segment.
- 'Page': The starting page number for the corresponding document segment.

The script reads the Excel file, processes the PDF, and outputs each segment as a new PDF file with the file name '{DocumentID}.pdf', where '{DocumentID}' is the value from the 'DocumentID' column.

The last segment will run until the end of the PDF if there are no more entries in the Excel file to define another starting page.

Usage:
    python pdf_cutter.py [excel_file] [pdf_file]

Where:
    [excel_file] is the path to the Excel file containing the mappings.
    [pdf_file] is the path to the source PDF file to be cut.

Example Excel file format:
    | DocumentID | Page |
    |------------|------|
    | 1          | 1    |
    | 1a         | 5    |
    | 2          | 8    |

For the above example, the script will create '1.pdf' with pages 1-4, '1a.pdf' with pages 5-7, and '2.pdf' with pages 8 to the end of the source PDF.

Requirements:
    pip install pikepdf pandas
"""
import argparse
import pandas as pd
import pikepdf


def parse_arguments():
    """Set up and parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Cut PDFs based on Excel input")
    parser.add_argument(
        "excel_file", type=str, help="The Excel file with DocumentID and Page columns"
    )
    parser.add_argument("pdf_file", type=str, help="The input PDF file")
    return parser.parse_args()


def load_mappings(excel_path):
    """Load and sort the Excel file with document mappings."""
    df = pd.read_excel(excel_path, dtype={"DocumentID": str})
    df["Page"] = pd.to_numeric(df["Page"], errors="coerce")
    return df.sort_values(by="Page")


def save_pages(pdf_writer, document_id):
    """Save the extracted pages to a new PDF file."""
    output_filename = f"{document_id}.pdf"
    with open(output_filename, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
    print(f"Created {output_filename}")


def extract_and_save_pages(input_pdf, mappings):
    """Extract pages based on mappings and save to new PDF files."""
    if mappings.iloc[0]["Page"] != 1:
        preface_pdf = pikepdf.new()
        preface_pdf.pages.extend(input_pdf.pages[0 : mappings.iloc[0]["Page"] - 1])
        preface_pdf.save("preface.pdf", linearize=True)
        print("Created preface.pdf")

    for index, row in mappings.iterrows():
        start_page = row["Page"]
        end_page = (
            mappings["Page"].iloc[index + 1]
            if index + 1 < len(mappings)
            else len(input_pdf.pages) + 1
        )

        output_pdf = pikepdf.new()
        if pd.isna(start_page):
            continue
        start_page = int(start_page)
        if pd.isna(end_page):
            end_page = len(input_pdf.pages) + 1
        end_page = int(end_page)
        output_pdf.pages.extend(input_pdf.pages[start_page - 1 : end_page - 1])
        output_filename = f"{row['DocumentID']}.pdf"
        output_pdf.save(output_filename, linearize=True)
        print(f"Created {output_filename}")


def main(excel_file, pdf_file):
    """Main function to control the PDF cutting process."""
    mappings = load_mappings(excel_file)
    input_pdf = pikepdf.open(pdf_file)

    # Check if the PDF contains enough pages
    max_page = mappings["Page"].max()
    if len(input_pdf.pages) < max_page:
        raise ValueError(
            f"The PDF has only {len(input_pdf.pages)} pages, "
            f"but the Excel file requests page {max_page}."
        )

    extract_and_save_pages(input_pdf, mappings)


if __name__ == "__main__":
    args = parse_arguments()
    main(args.excel_file, args.pdf_file)
