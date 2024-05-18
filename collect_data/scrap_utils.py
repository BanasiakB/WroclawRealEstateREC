import random
import requests

from bs4 import BeautifulSoup

from project_utils.logger import get_logger

logger = get_logger(__name__)


userAgents=[
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
]


def request_url(url: str) -> requests.Response:
    logger.info(f"Sending GET request to url {url}.")
    response = requests.get(url, headers={'User-Agent': random.choice(userAgents)})
    
    if response.status_code != 200:
        message = f"Failed to fetch search results. Status code: {response.status_code}."
        logger.error(message)
        raise ConnectionError(message)

    logger.info("Response from GET request got successfully.")
    return response

def request_url_get_soup(url: str) -> BeautifulSoup:
    response = request_url(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
