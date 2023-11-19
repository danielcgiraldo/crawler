import requests
from bs4 import BeautifulSoup

search_url = f"https://smods.ru/?s={id}"

def get_mod(id):
    try:
        # Make the initial request to the search URL
        search_response = requests.get(search_url)
        search_html = search_response.text

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(search_html, 'html.parser')

        # Find the link using the appropriate selector
        entry_link = soup.css.find('.entry .skymods-excerpt-btn')['href']

        # Make a second request to the found link
        mod_response = requests.get(entry_link)
        mod_html = mod_response.text

        # Parse the HTML of the mod page
        mod_soup = BeautifulSoup(mod_html, 'html.parser')

        # Find the download link using the appropriate selector
        download_link = mod_soup.select_one('.download-button')['href']

        # Return the download link
        return {"url": download_link}

    except Exception as e:
        print(e)
        return "error", {"details": "Could not find mod with that ID"}
