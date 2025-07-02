from cloudscraper import create_scraper
from config import sharepoint_url, sharepoint_file

def get_excel()->str:
    session = create_scraper()
    response = session.get(sharepoint_url)
    with open(sharepoint_file, 'wb') as f:
        f.write(response.content)
    return sharepoint_file
