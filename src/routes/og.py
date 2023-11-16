from bs4 import BeautifulSoup
import requests


def get_og(url):
    try:

            headers = {
                'Host': url.split("/")[2],
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'
            }

            session = requests.Session()
            response = session.get(url, headers=headers)

            if response.status_code == 403:
                response = session.get(url, headers=headers)
            
            if response.status_code == 403:
                 raise Exception(403)
            elif response.status_code == 404:
                raise Exception(404)

            page = response.content
            soup = BeautifulSoup(page, "html.parser")
            icon_link = soup.select_one("link[rel*=icon]")["href"]

            if not icon_link.startswith("http"):
                if url[-1] == "/":
                    url = url[:-1]
                if icon_link[0] == "/":
                    icon_link = icon_link[1:]
                icon_link = url + "/" + icon_link

            return "success", {
                "status": "success",
                "favicon": icon_link,
                "title": soup.title.string,
                "description": soup.find("meta", attrs={"name": "description"})["content"],
                "og:description": soup.find("meta", property="og:description")["content"],
                "og:title": soup.find("meta", property="og:title")["content"],
                "og:image": soup.find("meta", property="og:image")["content"]
            }
    
    except requests.exceptions.RequestException as e:
        print(e)
        return "error", {"details": "Could not connect to destination URL"}

    except Exception as e:
        if e == 403:
            return "error", {"details": "Access denied to destination URL"}
        elif e == 404:
            return "error", {"details": "Destination URL not found"}
        else:
            return "error", {"details": str(e)}