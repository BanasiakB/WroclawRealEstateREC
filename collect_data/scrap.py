from collect_data.googledrive import upload_image_to_drive
# import pandas as pd
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


userAgents=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36']


def request_url(url: str):
    response = requests.get(url, headers={'User-Agent': random.choice(userAgents)})
    
    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch search results. Status code: {response.status_code}")
    return response

def request_url_get_soup(url: str):
    response = request_url(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def scrapper() -> None:
    # download data - Done
    # Images send to Google Drive - Done
    # tabular data send to SQL

    search_url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie/wroclaw/wroclaw/wroclaw?viewType=listing'
    soup = request_url_get_soup(url=search_url)

    links = soup.find("div", {"data-cy": "search.listing.organic"}).find_all('a', {"data-cy": "listing-item-link"})
    for link in links:
        # if link not in scrapped_links <- może jakiś .txt? lub ew set(googledrive.list_images_in_drivefolder z uciętą końcówką tj. _nr) 
        print(link)
        time.sleep(2.)
        try:
            scrap_details(link['href'])
        except ConnectionError:
            print('Connection Error during scrapping details.')
        return # USUNAĆ W PRZYSZŁOŚCI - BLOKUJE NA JEDNEJ OBSERWACJI 
    return


def scrap_details(link: str) -> None:
    # scrap_photos(link)  # LEPIEJ ODHASHOWAĆ DOPIERO JAK JUŻ BD BĘDZIE DZIAŁAĆ
    scrap_tabular_data(link)


def upload_tabular_data(data: dict, link: str) -> None:
    # W tym miejscu należy wysyłać dane do BD - ? najlepiej z ID = link ? <- wtedy może zabezpieczymy się przed dublowaniem mieszkań 
    pass


def scrap_tabular_data(link: str) -> None:
    url = 'https://www.otodom.pl/' + link   # link używamy jako id do bazy danych ?
    soup = request_url_get_soup(url=url)
    data = {}

    try:
        data["Price"] = soup.find('strong', {'aria-label': "Cena"}).get_text()
    except AttributeError:
        data["Price"] = None

    try:
        data["loc"] = soup.find('a', {'aria-label': "Adres"}).get_text()
    except AttributeError:
        data["loc"] = None

    # Pominąłem obsługę zdalną - raczej bez sensu informacja
    expected_info = {"Powierzchnia": "table-value-area", "Forma własności": "table-value-building_ownership", "Liczba pokoi": "table-value-rooms_num", 
            "Stan wykończenia": "table-value-construction_status", "Piętro": "table-value-floor", "Balkon / ogród / taras": "table-value-outdoor", 
            "Czynsz": "table-value-rent", "Miejsce parkingowe": "table-value-car", "Ogrzewanie": "table-value-heating", 
            
            # Informacje z drugiej tabelki
            "Rynek": "table-value-market", "Typ ogłoszeniodawcy": "table-value-advertiser_type", "Dostępne od": "table-value-free_from", "Rok budowy": "table-value-build_year", 
            "Rodzaj zabudowy": "table-value-building_type", "Okna": "table-value-windows_type", "Winda": "table-value-lift", "Media": "table-value-media_types", 
            "Zabezpieczenia": "table-value-security_types", "Wyposażenie": "table-value-equipment_types", "Informacje dodatkowe": "table-value-extras_types", "Materiał budynku": "table-value-building_material"}
    
    
    for column_name, table_value in expected_info.items():
        try:
            value = soup.find('div', {"data-testid": table_value}).get_text()
        except AttributeError:
            value = None
        data[column_name] = value 

    try:
        data["Description"] = soup.find('div', {"data-cy": "adPageAdDescription"}).get_text()
    except AttributeError:
        data["Description"] = None

    # df = pd.DataFrame(data)    # Jeśli wolisz używać DF, to śmiało 
    # upload_tabular_data(df, link)
    upload_tabular_data(data, link)


def scrap_photos(link: str) -> None:
    url = 'https://www.otodom.pl/' + link
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    div = driver.find_element(By.CLASS_NAME, 'image-gallery-thumbnails-container')
    image_tags = div.find_elements(By.TAG_NAME, 'img')
    for i, image_tag in enumerate(image_tags):
        image_url = image_tag.get_attribute('src')
        upload_image_to_drive(image_url, link + f'_{i}')
    driver.quit()

