import os
import requests
from bs4 import BeautifulSoup


def get_pdf_links_from_webpage(url):
    pdfs = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            # Find all the anchor tags (links) in the HTML
            links = soup.find_all("a")
            # Extract and print the href attribute of each link
            for link in links:
                href = link.get("href")
                if href:
                    if href.endswith(".pdf"):
                        pdfs.append(href)
        else:
            print(
                f"Failed to retrieve the webpage. Status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return pdfs



if __name__ == "__main__":
    base_url = "https://wobcovid19.rijksoverheid.nl/publicaties/"
    json_url = "https://do-ams3-17.hw.webhare.net/services/wobcovid19-prod-v2-1/search/?first=0&count=300&orderby=publicationdate"

    response = requests.get(json_url)
    if response.status_code == 200:
        data = response.json()
        # Check if the number of results matches totalcount
        if len(data.get("results", [])) == data.get("totalcount", 0):
            # Initialize a dictionary to store link and title as key-value pairs
            link_title_pairs = {}
            # Loop through the results
            for result in data.get("results", []):
                pub = result.get("link").lstrip('#')
                title = result.get("publication", {}).get("title")
                if pub and title:
                    # Add the link and title as key-value pairs to the dictionary
                    link_title_pairs[pub] = title

            for pub, title in link_title_pairs.items():
                print(f"Link: {pub}, Title: {title}")
                if not os.path.exists(pub):
                    os.mkdir(pub)
                with open(f"{pub}/title.txt", "w") as file:
                    file.write(title)
                pdfs = get_pdf_links_from_webpage(f"{base_url}{pub}/")
                for pdf in pdfs:
                    try:
                        response = requests.get(f"{base_url}{pub}/{pdf}")
                        if response.status_code == 200:
                            with open(f"{pub}/{pdf}", "wb") as file:
                                file.write(response.content)
                            print(f"File downloaded and saved as {pub}/{pdf}")
                        else:
                            print(f"Failed to download the file. Status code: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"An error occurred: {e}")
        else:
            print("The result count does not match the totalcount, please fix json_url.")
    else:
        print(f"Failed to retrieve JSON data. Status code: {response.status_code}")
