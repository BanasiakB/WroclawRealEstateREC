from typing import List, Optional

from bs4 import BeautifulSoup

from ..scrap_utils import request_url, request_url_get_soup
from .otodom_offer_page_handler import OfferPageHandler


class ListingPageHandler:
    """Class for handling scrapping of the listing pages with offers on otodom.pl website."""
    listed_pages_count_per_page: Optional[int]
    listed_pages_link_extensions: List[str]
    listed_pages_offer_handlers: List[OfferPageHandler]

    page_num_current: int = 1
    page_num_max: Optional[int] = None

    url_base: str = "https://www.otodom.pl"
    url_extension: str = "pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing"
    
    _page_num_max_without_limit_set = 10

    def __init__(
        self,
        listed_pages_count_per_page: Optional[int] = None,
        already_scrapped_link_extensions: Optional[List[str]] = None,
    ) -> None:
        self._listed_pages_link_extensions: List[str] = already_scrapped_link_extensions or []
        self._listed_pages_offer_handlers: List[OfferPageHandler] = []
        self.listed_pages_count_per_page = listed_pages_count_per_page
    
    @property
    def listed_pages_link_extensions(self) -> List[str]:
        """Returns list with link extension of offers that were find on scrapped listing pages."""
        return self._listed_pages_link_extensions.copy()

    @property
    def listed_pages_offer_handlers(self) -> List[OfferPageHandler]:
        """Returns list with OfferPageHandler objects of offer pages that the object has revealed from listing website."""
        return self._listed_pages_offer_handlers.copy()
    
    @property
    def url_current(self) -> str:
        """Returns full url for the page with the current configuration."""
        url = self.url_base + self.url_extension

        if self.page_num_current > 1:
            url += f"&page={self.page_num_current}"
        if self.listed_pages_count_per_page is not None:
            url += f"&limit={self.listed_pages_count_per_page}"

        return url

    def _update_meta(
        self,
        soup_page: BeautifulSoup,
        increment_page_num_current: bool = True,
        update_page_num_max_once_set: bool = False,
    ) -> None:
        """
        Method updates the object's metadata that is used to iterate over scrapped pages. The intention is to run the
        method ater every successful request to the listing website.

        :param soup_page: BeautifulSoup object created with the response of response from listing website
        :param increment_page_num_current: bool if the object's page_num_current should be incremented, defaults to True
        :param update_page_num_max_once_set: bool if the object's page_num_max should be overwritten if it is already set,
            defaults to False
        """
        if increment_page_num_current:
            self.page_num_current += 1

        # Update 'page_num_max' only if the value was found on the page and if it is not already set.
        # One exception to the latter is when explicitly said to overwrite 'page_num_max' by 'update_page_num_max_once_set'
        page_num_max = self._get_page_num_max(suop=soup_page)
        if page_num_max is not None and (self.page_num_max is None or update_page_num_max_once_set):
            self.page_num_max = page_num_max

    def _get_page_num_max(self, soup: BeautifulSoup) -> Optional[int]:
        """
        Method for getting the information about total number of pages in listing website.

        :param soup: BeautifulSoup object created with the response of response from listing website
        :return: Total number of pages in listing website.
        """
        try:
            return int(soup.find("ul", {"class": "css-1vdlgt7"}).find_all("li")[-2].text)
        except:
            return None
    
    def _get_offer_links_from_soup(self, soup: BeautifulSoup) -> List[str]:
        """
        Method for getting url link extensions to the offer pages from listing website.

        :param soup: BeautifulSoup object created with the response of response from listing website
        :return: List with url link extensions of offers listed on the page of the given soup
        """
        links = soup.find("div", {"data-cy": "search.listing.organic"}).find_all('a', {"data-cy": "listing-item-link"})
        links = [link["href"] for link in links]
        return links

    def scrap_next(self) -> bool:
        """
        Method performs scrapping of the listing page that the current configuration ponits to. Results are saved to the
        object's lists and the metadata is being updated accordingly. Method returns bool value. True value indicates
        that the scrapping was performed normally. False value indicates that there are no more pages to scrap (for various reasons).
        """
        if self.page_num_max and self.page_num_current > self.page_num_max:
            return False
        if self.page_num_max is None and self.page_num_current > self._page_num_max_without_limit_set:
            return False

        soup = request_url_get_soup(url=self.url_current)
        self._update_meta(soup_page=soup)

        links = self._get_offer_links_from_soup
        for url_external in links:
            self._listed_pages_link_extensions.append(url_external)

            offer_handler = OfferPageHandler(url_external=self.url_base + url_external)
            self._listed_pages_offer_handlers.append(offer_handler)
        return True
