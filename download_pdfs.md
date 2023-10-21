# PDF Downloader

This Python script is designed to download PDF files from a specific webpage, extract link-title pairs from JSON data, and organize the downloaded PDFs into folders.
It can be used to automate the retrieval of PDF documents from a web source and store them locally.

In the default setup it will download all PDFs from [wobcovid19.rijksoverheid.nl](https://wobcovid19.rijksoverheid.nl/)

## Prerequisites

Before you can use this script, you need to have the following prerequisites installed on your system:

- Python 3.x

### Installing

You can install the BeautifulSoup and requests using pip:

```bash
pip install requests beautifulsoup4
```

or

```bash
pip install -r requirements.txt
```

## Customization

You can customize the script for your specific use case:

- Modify the `JSON_URL` and `BASE_URL` variables to point to your data source and web source.
- Customize the naming of folders and files as per your requirements.
- Extend the functionality to handle additional data processing or tasks.

## Warning

This `get_pdfs.py` script downloads approximately **80 Gigabytes** of PDF files in its default configuration!

1. Open the script in a text editor and configure the following variables:
   - `JSON_URL`: The URL of the JSON data source.
   - `BASE_URL`: The base URL of the web source containing PDF links.
2. Run the script by executing the following command in your terminal:

```bash
python get_pdfs.py
```

The script will retrieve JSON data, process it, and download PDFs into folders based on the retrieved data.

## Script Overview

- The script retrieves JSON data from a specified URL using the `requests` library.
- It extracts link-title pairs from the JSON data and saves them in a CSV file.
- For each link-title pair, the script creates a folder and saves the title information in a text file.
- It also downloads associated PDF files and saves them in the corresponding folders.

## License

This package is open-source and released under the [European Union Public License version 1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).
You are free to use, modify, and distribute the package in accordance with the terms of the license.

## Contributing

For contributions, bug reports, or suggestions, please visit the project repository on GitHub.
