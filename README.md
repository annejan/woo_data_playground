# Woo Data Playground: Python PDF Utility Scripts

This repository contains a collection of Python scripts for working with PDF documents.
Each script is designed to perform specific tasks related to PDF downloading, text extraction etc.
Central to its functionalities is the ability to dissect vast PDFs into identifiable sub-documents, using the Table of Contents or specific page regions.
Additionally, it supports text extraction and provides tools for Named Entity Recognition (NER) to categorize and interpret content.
Further details and instructions for each utility can be found below.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Workflow and Rationale](#workflow-and-rationale)
- [PDF Downloader and Data Extraction Script](#pdf-downloader-and-data-extraction-script)
- [PDF Table of Contents Extractor](#pdf-table-of-contents-extractor)
- [PDF Document ID Extractor](#pdf-document-id-extractor)
- [Named Entity Recognition (NER) Benchmark](#named-entity-recognition-ner-benchmark)
- [Named Entity Recognition (NER) from PDFs](#named-entity-recognition-ner-from-pdfs)
- [Combine and Sort CSV Files](#combine-and-sort-csv-files)

## Prerequisites

Before you can use this script, you need to have the following prerequisites installed on your system:

- Python 3.x
- Tesseract OCR

### Installing PyMuPDF (fitz), Flair, Pandas and OpenPyXL

You can install all the required libraries using `pip`.

```bash
pip install -r requirements.txt
```

## Workflow and rationale

To move the old publications from [wobcovid19.rijksoverheid.nl](https://wobcovid19.rijksoverheid.nl/) and upload them to [open.minvws.nl](https://open.minvws.nl/) we want to cut them up into separate documents.
This has to be done on original or local document id basis. Unfortunately not all PDFs have the same kind of quality.

The NER scripts are there to see if we can optimise the search engine and since we have the data here anyway I'm using the same playground repository.

## PDF Downloader and Data Extraction Script

**Description:**
This script retrieves JSON data from [wobcovid19.rijksoverheid.nl](https://wobcovid19.rijksoverheid.nl/), extracts link-title pairs from the data, downloads associated PDF files, creates folders, and saves title information to a CSV file.
It utilizes the `requests` library for making web requests, `BeautifulSoup` for HTML parsing, and `csv` for working with CSV files.

- Optionally modify the 'json_url' variable to specify the JSON data source URL.
- Run the script to download PDFs, create folders, and save title information to CSV.

For more information read the [PDF Downloader](download_pdfs.md) documentation.

## PDF Table of Contents Extractor

**Description:**
This script extracts the table of contents (TOC) from a PDF file and optionally writes it to an Excel file.

**Usage:**

```bash
python naive_section_finder.py <pdf_file> [--output-file output.xlsx]
```

## PDF Document ID Extractor

**Description:**
This script allows you to extract DocumentIDs (numbers or number-letter combinations) from PDF files.
It uses PyMuPDF for PDF document handling and Tesseract for Optical Character Recognition (OCR) when necessary.

**Usage:**

```bash
python find_document_id.py <pdf_file> [--output-file output.xlsx]
```

**Optional:**

- You can specify a custom viewbox using the `--viewbox` argument. The viewbox should be provided as four floating-point numbers separated by spaces (left top right bottom).
- You can specify an output Excel file using the `--output-file` argument. If not provided, data will be saved to "output.xlsx."

For more information read the [document_ids](document_ids.md) documentation.

## Named Entity Recognition (NER) Benchmark

**Description:**
This script performs Named Entity Recognition (NER) using Flair's pre-trained models.
It allows you to evaluate NER performance using CUDA (if available) and provides the elapsed time for NER processing.

**Usage:**

```bash
python ner-benchmark.py
```

## Named Entity Recognition (NER) from PDFs

**Description:**
This script reads a PDF file and performs Named Entity Recognition (NER) using Flair's pre-trained NER models.
It extracts entities with a specified minimum certainty and provides the option to save the results to an Excel or CSV file.

**Usage:**

```bash
python ner.py <pdf_file> [--certainty 0.9] [--output-excel] [--output-csv] [--verbose]
```

For more information read the [named entity recognition](named_entity_recognition.md) documentation.

## Combine and Sort CSV Files

**Description:**
This script combines and sorts multiple CSV files.
It can be useful when you want to merge multiple CSV files containing entity data from different PDFs into a single, sorted CSV file.

**Usage:**

```bash
python merge_ner_csvs.py <input_files> [--output combined_and_sorted.csv]
```

Please follow the individual usage instructions for each script to perform specific tasks on your PDF documents.

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.

## Contributing

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.
