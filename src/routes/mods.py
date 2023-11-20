import requests
from bs4 import BeautifulSoup

def get_mod(id):
    try:
        # Make the initial request to the search URL

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        session = requests.Session()

        search_response = session.get(f"https://smods.ru/?s={id}", headers=headers)

        search_html = search_response.text

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(search_html, 'html.parser')

        # Find the link using the appropriate selector
        entry_link = soup.select_one('.entry .skymods-excerpt-btn')['href']
        
        # downlaod url
        download_response = session.post(entry_link, {
            "op": "download2",
            "id": entry_link.split("/")[3],
        }, headers=headers)

        download_html = download_response.text

        soup = BeautifulSoup(download_html, 'html.parser')

        download_link = soup.select_one('.download-file-btn a')

        if download_link is None:
            return entry_link
        else:
            return download_link['href']
    
    except Exception as e:
        print(e)
        return "error", {"details": "Could not find mod with that ID"}
