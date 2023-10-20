# Woo Data Playground: Python PDF Utility Scripts

Welcome to the Woo Data Playground, a repository dedicated to efficient PDF document processing using Python.

## **Overview**

This repository offers an array of Python scripts tailored to specific PDF-related tasks, from downloading and extracting content to Named Entity Recognition (NER) for content categorization.

**Key Features**:
- Dissecting massive PDFs into identifiable sub-documents.
- Extracting text and using NER to classify and interpret the content.
- Each utility's detailed instructions are provided below.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Workflow and Rationale](#workflow-and-rationale)
- [Utilities](#utilities)
  - [PDF Downloader and Data Extraction Script](#pdf-downloader-and-data-extraction-script)
  - [PDF Table of Contents Extractor](#pdf-table-of-contents-extractor)
  - [PDF Document ID Extractor](#pdf-document-id-extractor)
  - [Named Entity Recognition (NER) Benchmark](#named-entity-recognition-ner-benchmark)
  - [Named Entity Recognition (NER) from PDFs](#named-entity-recognition-ner-from-pdfs)
  - [Combine and Sort CSV Files](#combine-and-sort-csv-files)
- [License](#license)
- [Contributing](#contributing)

## **Prerequisites**

Ensure the following prerequisites are set up before proceeding:

- Python 3.x
- Tesseract OCR

**Installing Necessary Libraries**:

You can install PyMuPDF, Flair, Pandas, and OpenPyXL using:

```bash
pip install -r requirements.txt
```

## **Workflow and Rationale**

The core objective is to segment older publications from [wobcovid19.rijksoverheid.nl](https://wobcovid19.rijksoverheid.nl/) and upload them to [open.minvws.nl](https://open.minvws.nl/), splitting them based on original or local document IDs. Do note, the quality variance among these PDFs is considerable.

The included NER scripts aim to enhance search engine optimization. Given the data's presence in the repository, it's harnessed further for these capabilities.

## **Utilities**

### **PDF Downloader and Data Extraction Script**

- **Function**: Fetch JSON data from [wobcovid19.rijksoverheid.nl](https://wobcovid19.rijksoverheid.nl/), derive link-title pairs, download related PDFs, organize into folders, and record title data into a CSV file.
- **Implementation**: Utilizes `requests`, `BeautifulSoup`, and `csv` libraries.

**For more details**, refer to the [PDF Downloader](download_pdfs.md) documentation.

### **PDF Table of Contents Extractor**

- **Function**: Extract the table of contents from a PDF, with an option to save to an Excel file.
  
```bash
python naive_section_finder.py <pdf_file> [--output-file output.xlsx]
```

### **PDF Document ID Extractor**

- **Function**: Extract DocumentIDs (numeric or alphanumeric) from PDFs.
  
```bash
python find_document_id.py <pdf_file> [--output-file output.xlsx]
```

**For more details**, check the [document_ids](document_ids.md) guide.

### **Named Entity Recognition (NER) Benchmark**

- **Function**: Execute NER using Flair's pretrained models and measure NER performance.

```bash
python ner-benchmark.py [--cuda]
```

### **Named Entity Recognition (NER) from PDFs**

- **Function**: Read a PDF and execute NER, saving results to either Excel or CSV.

```bash
python ner.py <pdf_file> [--cuda] [--certainty 0.9] [--output-excel output.xlsx] [--output-csv output.csv]
```

**For more details**, consult the [named entity recognition](named_entity_recognition.md) guide.

### **Combine and Sort CSV Files**

- **Function**: Merge and order multiple CSVs, ideal for combining various CSVs with entity data into one organized file.

```bash
python merge_ner_csvs.py <input_files> [--output combined_and_sorted.csv]
```

## **License**

According to ChatGPT 4.0 it is OK to license ChatGPT generated code as EUP-L1.2 so there should be no issues here. 
Woo Data Playground is open-source, abiding by the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12). You're granted the freedom to utilize, adapt, and distribute the software under the license's terms.

## **Contributing**

Your contributions are invaluable. Whether it's a novel feature suggestion, a bug report, or feedback, kindly visit our GitHub repository to collaborate.
