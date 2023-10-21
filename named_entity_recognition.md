# Named Entity Recognition (NER) Python Scripts

This repository contains a collection of Python scripts for performing Named Entity Recognition (NER) on text data, particularly within PDF documents.
Each script is designed to extract named entities, such as persons, organizations, locations, and more, from text data using [Flair](https://flairnlp.github.io/)'s pre-trained NER models.
Below, you'll find descriptions and usage instructions for each NER script.

By default, the script uses the [flair/ner-dutch-large](https://huggingface.co/flair/ner-dutch-large) model.

## Dependencies

Ensure you have all required libraries installed. You can do this using `pip`:

```bash
pip install PyMuPDF flair openpyxl tqdm
```

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
python ner.py <pdf_file> [--certainty 0.9] [--output-excel] [--output-csv]
```

Practical usage:

```bash
python ner.py --cuda --output-csv data/*/*.pdf
```

## Combine and Sort NER Results

**Description:**
This script combines and sorts multiple NER results from CSV files.
It can be useful when you have multiple result files from NER extraction and want to merge and sort the entities into a single output file.

**Usage:**

```bash
python merge_ner_results.py <input_files> [--output combined_and_sorted.csv]
```

Practical usage:

```bash
python merge_ner_results.py data/*/*.ner.csv
```

These NER scripts provide tools for extracting named entities from text data, especially within PDF files.
Please follow the usage instructions for each script to perform NER on your text data or merge and sort NER results as needed.

## Memory usage

Currently, this script uses about 4 GB of memory, to check the active memory usage you can use the nifty [CUDA memory](cuda_memory.md) monitor. 

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.

## Contributing

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.
