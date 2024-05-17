from typing import List, Optional

from bs4 import BeautifulSoup

from ..scrap_utils import request_url, request_url_get_soup
       
    
class OfferPageHandler:
    """
    Intention of the class is to be used for scrapping individual offer webpage and save the data to the storage.
    Class will be used by ListingPageHandler object which creates OfferPageHandler objects while scrapping offer urls
    from listing webpages.
    """
    url_base: str = "https://www.otodom.pl"
    url_external: str
    page_scrapped: bool
    
    def __init__(
        self,
        url_external: str
    ) -> None:
        self.url_external = url_external
        self.page_scrapped = self._check_if_page_under_url_was_scrapped()
    
    def scrap_page(self, skip_if_already_scrapped: bool = True):
        pass
    
    def _check_if_page_under_url_was_scrapped(self) -> bool:
        pass
