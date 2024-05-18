import json
import os
from typing import Any, Dict, Optional, Tuple

from bs4 import BeautifulSoup

from project_utils.logger import get_logger
from ..scrap_utils import request_url, request_url_get_soup

logger = get_logger(__name__)


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
    url_full: str
    page_scrapped_tabular: bool = False
    page_scrapped_image: bool = False
    page_soup: Optional[BeautifulSoup] = None
    data_tabular: Dict[str, Any]
    data_image: Dict[str, bytes]
    
    def __init__(
        self,
        url_extension: str
    ) -> None:
        self.url_extension = url_extension
        self.page_scrapped_tabular = self._check_if_page_under_url_was_scrapped_tabular()
        self.page_scrapped_iamge = self._check_if_page_under_url_was_scrapped_image()

        self._data_tabular = {}
        self._data_image = {}

        logger.info(f"Initialized OfferPageHandler object for page {self.url_full}.")

    @property
    def data_tabular(self) -> Dict[str, Any]:
        return self._data_tabular.copy()

    @property
    def data_image(self) -> Dict[str, bytes]:
        return self._data_image.copy()

    @property
    def page_scrapped(self) -> bool:
        return self.page_scrapped_tabular and self.page_scrapped_image

    @property
    def url_full(self) -> bool:
        return self.url_base + self.url_extension

    def get_tabular_data_base_path_and_file_name(self) -> Tuple[str, str]:
        base_path = os.path.join("tmp_data", "tabular")
        file_name = self.url_extension.replace("/", "_") + ".json"
        return base_path, file_name

    def save_tabular_data(self, to_database: bool = True) -> None:
        if to_database:
            self._save_tabular_data_database()
        else:
            self._save_tabular_data_local()

    def _save_tabular_data_local(self) -> None:
        logger.info(f"Saving tabular data to local file..")
        base_path, file_name = self.get_tabular_data_base_path_and_file_name()
        full_path = os.path.join(base_path, file_name)
        os.makedirs(base_path, exist_ok=True)
        
        with open(full_path, "w") as f:
            json.dump(self.data_tabular, f, sort_keys=True, indent=2)
        logger.info(f"Saving successful. File path is {full_path}")

    def _save_tabular_data_database(self) -> None:
        pass

    def save_image_data(self, to_google_drive: bool = True) -> None:
        if to_google_drive:
            self._save_image_data_google_drive()
        else:
            self._save_image_data_local()

    def _save_image_data_local(self) -> None:
        logger.info(f"Saving image data to local file..")
        base_path = os.path.join("tmp_data", "images", self.url_extension.replace("/", "_"))
        os.makedirs(base_path, exist_ok=True)

        data_image = self.data_image
        for image_link, image in data_image.items():
            file_name = image_link.replace("/", "_") + ".png"
            full_path = os.path.join(base_path, file_name)
        
            with open(full_path, "wb") as f:
                f.write(image)
        logger.info(f"Saving successful. {len(data_image)} file/s saved to {base_path}")

    def _save_image_data_google_drive(self) -> None:
        pass

    def save_data(
        self,
        tabular_to_database: bool = True,
        image_to_google_drive: bool = True
    ) -> None:
        self.save_tabular_data(to_database=tabular_to_database)
        self.save_image_data(to_google_drive=image_to_google_drive)

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
            logger.error(f"Error in finding in soup by args={args}.")
            return None

    def scrap_page_tabular(self, skip_if_already_scrapped: bool = True) -> bool:
        """
        Method performs scrapping of the offer page that its extension_url points to. Results are saved to the object's data
        dictionary and the page_scrapped bool is being switched to True when succeeded. Method returns bool value. True value
        indicates that the scrapping was performed normally. False value indicates that the page was already scrapped and it was not
        explicitly said to scrap page inregardles of that.

        :param skip_if_already_scrapped: bool indicating if the scrapping shoudl be skipped if the page was already scrapped, defaults to True
        """
        logger.info(f"Started scrapping tabular data from offer page with url {self.url_full}")
        if self.page_scrapped_tabular and skip_if_already_scrapped:
            logger.info("Scrapping tabular data from offer page aborted - page already scrapped and the tabular data is being stored.")
            return False
        elif skip_if_already_scrapped:
            file_path = os.path.join(*self.get_tabular_data_base_path_and_file_name())
            if os.path.exists(file_path):
                with open(file_path) as f:
                    self._data_tabular = json.load(f)
                logger.info(f"Scrapping tabular data from offer page aborted - page already scrapped to file. Tabular data was loaded from the file {file_path}.")
                return False

        if self.page_soup is None:
            self.page_soup = request_url_get_soup(url=self.url_full)

        self._data_tabular["Price"] = self._find_in_soup('strong', {'aria-label': "Cena"})
        self._data_tabular["loc"] = self._find_in_soup('a', {'aria-label': "Adres"})
        self._data_tabular["Description"] = self._find_in_soup('div', {"data-cy": "adPageAdDescription"})
        for column_name, table_value in expected_info.items():
            self._data_tabular[column_name] = self._find_in_soup('div', {"data-testid": table_value})

        self.page_scrapped_tabular = True
        logger.info(f"Finished scrapping tabular data from offer page with url {self.url_full}.")
        return True

    def scrap_page_images(self, skip_if_already_scrapped: bool = True) -> bool:
        logger.info(f"Started scrapping image data from offer page with url {self.url_full}")
        if self.page_scrapped_image and skip_if_already_scrapped:
            logger.info("Scrapping image data from offer page aborted - page already scrapped and the image data is being stored.")
            return False

        if self.page_soup is None:
            self.page_soup = request_url_get_soup(url=self.url_full)
        
        image_url = self.page_soup.picture.img["src"].split("/image;")[0] + "/image"
        self._data_image[image_url] = request_url(image_url).content
        
        self.page_scrapped_image = True
        logger.info(f"Finished scrapping image data from offer page with url {self.url_full}.")
        return True

    def _check_if_page_under_url_was_scrapped_tabular(self) -> bool:
        """
        Method checks if the page's tabular data was already scrapped by fetching the data from the storage database
        and checking if the extension url is already in there.
        exists there.
        """
        return False

    def _check_if_page_under_url_was_scrapped_image(self) -> bool:
        """Method checks if the page's images were already scrapped by fetching the data from the google drive."""
        return False
