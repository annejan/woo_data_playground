"""
PDF Downloader and Data Extraction Script

This script retrieves JSON data from a specified URL, extracts link-title pairs from the data,
downloads associated PDF files, creates folders, and saves title information to a CSV file.
It utilizes the requests library to make web requests, BeautifulSoup for HTML parsing,
and csv for working with CSV files.

Usage:
    - Modify the JSON_URL and BASE_URL variables to specify the data source URLs.
    - Run the script to download PDFs, create folders, and save title information to CSV.

Main function orchestrating the entire process.

    The workflow consists of the following steps:
    1. Fetch JSON data from the specified URL.
    2. Verify the integrity of the fetched data by comparing result count with total count.
    3. If the data is valid, process the link-title pairs. This involves:
       - Extracting link-title pairs.
       - Downloading PDFs associated with each link.
       - Creating directories for each link.
       - Writing the title information to a CSV file and saving PDF links to respective directories.

    If there's a mismatch between the result count and the total count from the fetched JSON data,
    a warning message is printed, suggesting a possible issue with the data source.

Example Usage:
    python get_pdfs.py

SPDX-License-Identifier: EUPL-1.2
"""
import os
import requests
import csv
from bs4 import BeautifulSoup

BASE_URL = "https://wobcovid19.rijksoverheid.nl/publicaties/"
JSON_URL = "https://do-ams3-17.hw.webhare.net/services/wobcovid19-prod-v2-1/search/?first=0&count=300&orderby=publicationdate"


def get_json_data(json_url):
    """
    Get JSON data from a given URL.

    Args:
        json_url (str): The URL of the JSON data.

    Returns:
        dict or None: The JSON data or None if there was an error.

    Example Usage:
    ```
    data = get_json_data("https://example.com/data.json")
    ```
    """
    try:
        response = requests.get(json_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve JSON data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return None


def get_pdf_links_from_webpage(url):
    """
    Get PDF links from a webpage.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        list: A list of PDF links found on the webpage.

    Example Usage:
    ```
    pdf_links = get_pdf_links_from_webpage("https://example.com/some-page/")
    for link in pdf_links:
        print(link)
    ```
    """
    pdfs = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            # Find all the anchor tags (links) in the HTML
            links = soup.find_all("a")
            # Extract and return the href attribute of each link that ends with ".pdf"
            pdfs = [
                link.get("href")
                for link in links
                if link.get("href", "").endswith(".pdf")
            ]
        else:
            print(
                f"Failed to retrieve the webpage. Status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return pdfs


def download_pdf(url, save_path):
    """
    Download a PDF file from a URL and save it to a local path.

    Args:
        url (str): The URL of the PDF file.
        save_path (str): The local path to save the downloaded PDF.

    Example Usage:
    ```
    download_pdf("https://example.com/document.pdf", "local/path/document.pdf")
    ```
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            print(f"File downloaded and saved as {save_path}")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main function for downloading PDFs and associated data from a web source.

    It retrieves JSON data from a specified URL, processes it to extract link-title pairs,
    downloads associated PDFs, creates folders, and saves title information to a CSV file.

    The JSON object consists of several key-value pairs:

    1. v: An integer, likely representing the version of the data or the API. The value is `2`.
    2. service: A string indicating the name of the service from which the data originates. In this case, it's `"wobcovid19-search"`.
    3. totalcount: An integer representing the total number of results or items present in the dataset. Here, it's `275`.
    4. results: An array of objects, each detailing a specific publication. Each object in this array contains:
        - link: A string prefixed by a hash (`#`), possibly indicating a unique identifier or anchor for the publication.
        - publication: An object that further provides details about the publication:
            - summary: A brief description or summary of the publication.
            - id: A unique identifier for the publication. It starts with the prefix `wrd:` followed by a series of alphanumeric characters.
            - title: The title of the publication.
            - publicationdate: A timestamp string in the ISO 8601 format, indicating the date of the publication.
        - score: An integer, which might indicate relevance, confidence, or priority associated with the publication.
    """
    data = get_json_data(JSON_URL)

    if data:
        if len(data.get("results", [])) == data.get("totalcount", 0):
            link_title_pairs = {}
            with open("titles.csv", "w") as csvfile:
                fieldnames = ["Link", "Title"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()  # Write the header row
                for result in data.get("results", []):
                    pub = result.get("link").lstrip("#")
                    title = result.get("publication", {}).get("title")
                    if pub and title:
                        link_title_pairs[pub] = title
                        writer.writerow({"Link": pub, "Title": title})

            for pub, title in link_title_pairs.items():
                print(f"Link: {pub}, Title: {title}")
                if not os.path.exists(pub):
                    os.mkdir(pub)
                with open(f"{pub}/title.txt", "w") as file:
                    file.write(title)
                pdf_links = get_pdf_links_from_webpage(f"{BASE_URL}{pub}/")
                with open(f"{pub}/pdfs.txt", "w") as file:
                    for pdf in pdf_links:
                        pdf_url = f"{BASE_URL}{pub}/{pdf}"
                        pdf_path = f"{pub}/{pdf}"
                        file.write(pdf_url + "\n")
                        if not os.path.exists(pdf_path) and not os.path.exists(
                            f"{pub}/skip"
                        ):
                            download_pdf(pdf_url, pdf_path)
        else:
            print(
                "The result count does not match the totalcount, please fix json_url."
            )


if __name__ == "__main__":
    main()
