import os
import requests
from bs4 import BeautifulSoup


def get_json_data(json_url):
    try:
        response = requests.get(json_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve JSON data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_pdf_links_from_webpage(url):
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
    base_url = "https://wobcovid19.rijksoverheid.nl/publicaties/"
    json_url = "https://do-ams3-17.hw.webhare.net/services/wobcovid19-prod-v2-1/search/?first=0&count=300&orderby=publicationdate"
    data = get_json_data(json_url)

    if data:
        if len(data.get("results", [])) == data.get("totalcount", 0):
            link_title_pairs = {}
            for result in data.get("results", []):
                pub = result.get("link").lstrip("#")
                title = result.get("publication", {}).get("title")
                if pub and title:
                    link_title_pairs[pub] = title

            for pub, title in link_title_pairs.items():
                print(f"Link: {pub}, Title: {title}")
                if not os.path.exists(pub):
                    os.mkdir(pub)
                with open(f"{pub}/title.txt", "w") as file:
                    file.write(title)
                pdf_links = get_pdf_links_from_webpage(f"{base_url}{pub}/")
                for pdf in pdf_links:
                    pdf_url = f"{base_url}{pub}/{pdf}"
                    download_pdf(pdf_url, f"{pub}/{pdf}")
        else:
            print(
                "The result count does not match the totalcount, please fix json_url."
            )


if __name__ == "__main__":
    main()
