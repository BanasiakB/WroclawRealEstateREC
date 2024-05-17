from typing import Any, Dict, Optional

from bs4 import BeautifulSoup

from ..scrap_utils import request_url_get_soup


expected_info = {"Powierzchnia": "table-value-area", "Forma własności": "table-value-building_ownership", "Liczba pokoi": "table-value-rooms_num", 
        "Stan wykończenia": "table-value-construction_status", "Piętro": "table-value-floor", "Balkon / ogród / taras": "table-value-outdoor", 
        "Czynsz": "table-value-rent", "Miejsce parkingowe": "table-value-car", "Ogrzewanie": "table-value-heating", 
        
        # Informacje z drugiej tabelki
        "Rynek": "table-value-market", "Typ ogłoszeniodawcy": "table-value-advertiser_type", "Dostępne od": "table-value-free_from", "Rok budowy": "table-value-build_year", 
        "Rodzaj zabudowy": "table-value-building_type", "Okna": "table-value-windows_type", "Winda": "table-value-lift", "Media": "table-value-media_types", 
        "Zabezpieczenia": "table-value-security_types", "Wyposażenie": "table-value-equipment_types", "Informacje dodatkowe": "table-value-extras_types", "Materiał budynku": "table-value-building_material"}
       
    
class OfferPageHandler:
    """
    Intention of the class is to be used for scrapping individual offer webpage and save the data to the storage.
    Class will be used by ListingPageHandler object which creates OfferPageHandler objects while scrapping offer urls
    from listing webpages.
    """
    url_base: str = "https://www.otodom.pl"
    url_extension: str
    page_scrapped: bool
    page_soup: Optional[BeautifulSoup] = None
    data: Dict[str, Any]
    
    def __init__(
        self,
        url_extension: str
    ) -> None:
        self.url_extension = url_extension
        self.page_scrapped = self._check_if_page_under_url_was_scrapped()

        self._data = {}
    
    @property
    def data(self) -> Dict[str, Any]:
        return self._data.copy()
    
    def _find_in_soup(self, *args) -> Optional[str]:
        """
        Method for searching through the soup for given args and returning found value.
        If an AttributeError occurs, it is cought and the None value is being returned.

        :param *args: all the latter arguments passed will be input to the BeautifulSoup find method
        :return: Value found with the given bs4 search parameters or None if an error occured during th search
        """
        try:
            return self.page_soup.find(*args).get_text()
        except AttributeError:
            return None

    def scrap_page_tabular(self, skip_if_already_scrapped: bool = True) -> bool:
        """
        Method performs scrapping of the offer page that its extension_url points to. Results are saved to the object's data
        dictionary and the page_scrapped bool is being switched to True when succeeded. Method returns bool value. True value
        indicates that the scrapping was performed normally. False value indicates that the page was already scrapped and it was not
        explicitly said to scrap page inregardles of that.

        :param skip_if_already_scrapped: bool indicating if the scrapping shoudl be skipped if the page was already scrapped, defaults to True
        """
        if self.page_scrapped and skip_if_already_scrapped:
            return False

        self.page_soup = request_url_get_soup(url=self.url_base + self.url_extension)

        self._data["Price"] = self._find_in_soup('strong', {'aria-label': "Cena"})
        self._data["loc"] = self._find_in_soup('a', {'aria-label': "Adres"})
        self._data["Description"] = self._find_in_soup('div', {"data-cy": "adPageAdDescription"})
        for column_name, table_value in expected_info.items():
            self._data[column_name] = self._find_in_soup('div', {"data-testid": table_value})

        self.page_scrapped = True
        return True
    
    def _check_if_page_under_url_was_scrapped(self) -> bool:
        """
        Method checks if the page was already scrapped by fetching the data from the storage database and checking if the extension url
        exists there.
        """
        return False
