"""
PDF to Excel Converter with OCR

This script provides functionality to convert a PDF file into an Excel spreadsheet using Optical Character Recognition (OCR).
It detects grid lines on each page of the PDF to identify cell boundaries and applies OCR to each cell to extract text.
 The script supports customization of the OCR process and offers a debug mode for visual inspection of detected grid lines and OCR results.

Main Features:
- Converts PDF pages to images for processing.
- Detects vertical and horizontal grid lines to identify cell boundaries.
- Performs OCR on each cell to extract text.
- Outputs the collected data into an Excel file.
- Optional debug mode to generate images showing detected cell boundaries.
- Adjustable parameters for grid line detection and OCR.

Usage:
    python pdf_to_excel.py <pdf_path> <output_excel_path> [options]

Options:
TODO TOO FAST

Example:
    python pdf_to_excel.py sample.pdf output.xlsx --verbose --debug

Dependencies:
- pdf2image: For converting PDF pages to images.
- OpenCV (cv2): For image processing and grid line detection.
- NumPy: For numerical operations on images.
- Pytesseract: For performing OCR on images.
- Pandas: For creating and writing to Excel files.

This package is open-source and released under the European Union Public License version 1.2.
You are free to use, modify, and distribute the package in accordance with the terms of the license.

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.

SPDX-License-Identifier: EUPL-1.2
"""
import argparse
import pdf2image
import cv2
import numpy as np
import pytesseract
import pandas as pd
from grid_line_detector import find_grid_lines_on_image


class OCRConfig:
    def __init__(
        self,
        start_page=1,
        dpi=300,
        verbose=False,
        debug=False,
        no_ocr=False,
        cutoff_fraction=0.6,
        min_distance=10,
        columns=None,
        rows=None,
        zoom=None,
    ):
        self.start_page = start_page
        self.dpi = dpi
        self.verbose = verbose
        self.debug = debug
        self.no_ocr = no_ocr
        self.cutoff_fraction = cutoff_fraction
        self.min_distance = min_distance
        self.columns = columns
        self.rows = rows
        self.zoom = zoom


def convert_pdf_to_images(pdf_path, start_page=1, dpi=300):
    """
    Convert a PDF file to a list of images, one for each page.
    """
    return pdf2image.convert_from_path(pdf_path, first_page=start_page, dpi=dpi)


def ocr_cell(image):
    """
    Perform OCR on a single cell image.
    """
    config = "--oem 3 --psm 6 -l nld"  # Assume a single uniform block of text
    return pytesseract.image_to_string(image, config=config).strip()


def draw_cells_on_image(image, vertical_lines, horizontal_lines):
    """
    Draw rectangles on the image to represent the detected cells.
    """
    for x1, x2 in zip(vertical_lines, vertical_lines[1:]):
        for y1, y2 in zip(horizontal_lines, horizontal_lines[1:]):
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


def process_pdf_and_ocr_to_excel(pdf_path, output_excel_path, config):
    # Use config properties instead of individual arguments
    if config.verbose:
        print("Getting PDF images")
    images = convert_pdf_to_images(
        pdf_path, start_page=config.start_page, dpi=config.dpi
    )
    all_page_data = []
    for img in images:
        page_data = []
        if config.verbose:
            print("Getting cell information")

        if config.zoom:
            grid_img = cv2.resize(
                np.array(img),
                (int(img.width * config.zoom), int(img.height * config.zoom)),
            )
        else:
            grid_img = img

        vertical_lines, horizontal_lines = find_grid_lines_on_image(
            grid_img,
            config.cutoff_fraction,
            config.min_distance,
            config.columns,
            config.rows,
        )

        if config.zoom:
            inverse_zoom = 1.0 / config.zoom
            vertical_lines = [int(line * inverse_zoom) for line in vertical_lines]
            horizontal_lines = [int(line * inverse_zoom) for line in horizontal_lines]

        if config.debug:
            debug_image = np.array(img)  # Create a copy for debug drawing

        for i in range(len(horizontal_lines) - 1):
            row_data = []
            for j in range(len(vertical_lines) - 1):
                if not config.no_ocr:
                    if config.verbose:
                        print(
                            vertical_lines[j],
                            horizontal_lines[i],
                            vertical_lines[j + 1],
                            horizontal_lines[i + 1],
                        )
                    cell_image = img.crop(
                        (
                            vertical_lines[j],
                            horizontal_lines[i],
                            vertical_lines[j + 1],
                            horizontal_lines[i + 1],
                        )
                    )
                    if config.verbose:
                        print("Getting cell data")
                        if config.debug:
                            cell_image.save(
                                f"debug_cell_{images.index(img) + config.start_page}_{i}_{j}.png",
                            )
                    cell_text = ocr_cell(cell_image)
                    if config.verbose:
                        print(
                            f"Page {images.index(img) + config.start_page} Cell {i}:{j} found text: {cell_text}"
                        )
                    row_data.append(cell_text)

                if config.debug:
                    draw_cells_on_image(
                        debug_image,
                        [vertical_lines[j], vertical_lines[j + 1]],
                        [horizontal_lines[i], horizontal_lines[i + 1]],
                    )

            page_data.append(row_data)

        all_page_data.extend(page_data)

        if config.debug:
            cv2.imwrite(
                f"debug_page_{images.index(img) + config.start_page}.png",
                cv2.cvtColor(debug_image, cv2.COLOR_RGB2BGR),
            )

    df = pd.DataFrame(all_page_data)
    df.to_excel(output_excel_path, index=False)


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to Excel with OCR on a grid basis."
    )
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    parser.add_argument("output_excel_path", help="Path for the output Excel file.")
    parser.add_argument(
        "--start_page",
        "-s",
        type=int,
        default=1,
        help="Page to start processing from. Defaults to 1.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="DPI for converting PDF to images. Defaults to 300.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose mode to output status information.",
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Enable debug mode to output images with detected cells.",
    )
    parser.add_argument(
        "--no-ocr",
        "-n",
        action="store_true",
        help="Disable OCR makes debug mode a lot faster.",
    )
    parser.add_argument(
        "--cutoff-fraction",
        "--cutoff",
        type=float,
        default=0.6,
        help="Cutoff percentage for detecting grid lines. Defaults to 0.6.",
    )
    parser.add_argument(
        "--min-distance",
        "--distance",
        type=int,
        default=10,
        help="Minimum distance between grid lines in pixels. Defaults to 10.",
    )
    parser.add_argument(
        "--columns",
        "-c",
        type=int,
        default=None,
        help="Amount of columns (0 indexed).",
    )
    parser.add_argument(
        "--rows",
        "-r",
        type=int,
        default=None,
        help="Amount of rows (0 indexed)",
    )
    parser.add_argument(
        "--zoom",
        "-z",
        type=float,
        default=None,
        help="Zoom eg 0.5, should be below zero.",
    )

    args = parser.parse_args()

    if args.zoom and not 0 < args.zoom <= 1:
        print("Zoom factor should be between 0 and 1.")
        exit(1)

    config = OCRConfig(
        start_page=args.start_page,
        dpi=args.dpi,
        verbose=args.verbose,
        debug=args.debug,
        no_ocr=args.no_ocr,
        cutoff_fraction=args.cutoff_fraction,
        min_distance=args.min_distance,
        columns=args.columns,
        rows=args.rows,
        zoom=args.zoom,
    )

    process_pdf_and_ocr_to_excel(args.pdf_path, args.output_excel_path, config)


if __name__ == "__main__":
    main()
