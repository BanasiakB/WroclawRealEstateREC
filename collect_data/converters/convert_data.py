from ..database_utils import config
import re
from functools import wraps
from typing import Optional, Tuple, Dict
from unidecode import unidecode


def try_exception(function):
    @wraps(function)
    def foo(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            return None
    return foo


class Converter:
    def __init__(self, dictionary: Dict):
        self.dictionary : Dict = dictionary
        self.converted_dictionary : Dict

    def convert_all(self) -> Dict:
        price_converted = self.convert_price(config.price)
        address_street, address_estate, address_district, address_city, address_province = self.convert_address()
        surface_converted = self.convert_surface()
        building_ownership_converted = self.replace_polish_char_and_whitespaces(config.building_ownership)
        rooms_converted = self.convert_str_to_number(config.rooms)
        construction_status_converted = self.replace_polish_char_and_whitespaces(config.construction_status)
        floor, floors_in_building = self.convert_floor_attribute()
        outdoor_converted = self.replace_polish_char_and_whitespaces(config.outdoor)
        rent_converted = self.convert_price(config.rent)
        parking_space_converted = self.replace_polish_char_and_whitespaces(config.parking_space)
        heating_converted = self.replace_polish_char_and_whitespaces(config.heating)
        market_converted = self.replace_polish_char_and_whitespaces(config.market)
        advertiser_type_converted = self.replace_polish_char_and_whitespaces(config.advertiser_type)
        free_from_converted = self.replace_polish_char_and_whitespaces(config.free_from)
        build_year_converted = self.convert_str_to_number(config.build_year)
        building_type_converted = self.replace_polish_char_and_whitespaces(config.building_type)
        windows_converted = self.replace_polish_char_and_whitespaces(config.windows)
        lift_converted = self.replace_polish_char_and_whitespaces(config.lift)
        media_converted = self.replace_polish_char_and_whitespaces(config.media)
        securities_converted = self.replace_polish_char_and_whitespaces(config.securities)
        equipment_converted = self.replace_polish_char_and_whitespaces(config.equipment)
        extra_info_converted = self.replace_polish_char_and_whitespaces(config.extra_info)
        building_material_converted = self.replace_polish_char_and_whitespaces(config.building_material)


        self.converted_dictionary = {
            'price': price_converted,
            'address_street': address_street,
            'address_estate': address_estate,
            'address_district': address_district,
            'address_city': address_city,
            'address_province': address_province,
            'surface': surface_converted,
            'building_ownership': building_ownership_converted,
            'rooms': rooms_converted,
            'construction_status_converted': construction_status_converted,
            'floor': floor,
            'floors_in_building': floors_in_building,
            'outdoor': outdoor_converted,
            'rent': rent_converted,
            'parking_space': parking_space_converted,
            'heating': heating_converted,
            'market': market_converted,
            'advertiser_type': advertiser_type_converted,
            'free_from': free_from_converted,
            'build_year': build_year_converted,
            'building_type': building_type_converted,
            'windows': windows_converted,
            'lift': lift_converted,
            'media': media_converted,
            'securities': securities_converted,
            'equipment': equipment_converted,
            'extra_info': extra_info_converted,
            'building_material': building_material_converted,
            'link_id': self.dictionary.get('link_id')
        }
        return self.converted_dictionary
    
    @try_exception
    def replace_polish_char_and_whitespaces(self, text: str) -> Optional[str]:
        text_from_directory = self.dictionary.get(text.polish_name)
        ascii_text = unidecode(text_from_directory)
        # Remove all whitespaces
        result_text = re.sub(r'\s+', '_', ascii_text)
        # replace slash with underscore
        result_text = re.sub(r'_{2,}', '_', result_text.replace('/', '_'))
        if result_text=='brak_informacji':
            result_text = None
        return result_text
    
    @try_exception
    def convert_price(self, feature: str) -> Optional[int]:
        #  Remove spaces and the currency symbol
        price = self.dictionary.get(feature.polish_name)
        return int(re.sub(r'[^0-9]', '', price))
    
    @try_exception
    def convert_address(self) -> Optional[Tuple[str, str, str, str, str]]:
        # Divide into separate parts that creates address from the link
        address = self.dictionary.get(config.address.polish_name)
        list_of_address_elements = unidecode(address).split(', ')
        if len(list_of_address_elements) != 5:
            address_street = None
        else:
            address_street = list_of_address_elements[0]
            list_of_address_elements.pop(0)
        
        address_estate, address_district, address_city, address_province = list_of_address_elements
            
        return address_street, address_estate, address_district, address_city, address_province
    
    @try_exception
    def convert_surface(self) -> Optional[float]:
        # Remove unit and convert number to float value
        surface = self.dictionary.get(config.surface.polish_name)
        numeric_text = re.sub(r'[^\d,]', '', surface)
        return float(numeric_text.replace(',', '.'))

    @try_exception
    def convert_str_to_number(self, feature: str) -> Optional[int]:
        return(int(self.dictionary.get(feature.polish_name)))

    @try_exception
    def convert_floor_attribute(self) -> Optional[Tuple[int, int]]:
        floor = self.dictionary.get(config.floor.polish_name)
        apartment_floor, floors = floor.split('/')
        return int(apartment_floor), int(floors)


findings = {
        'cena': '480 000 zł', 
        'adres': 'ul. Królewiecka, Maślice, Fabryczna, Wrocław, dolnośląskie', 
        # 'adres' : 'Stare Miasto, Stare Miasto, Wrocław, dolnośląskie',
        'powierzchnia': '36,77 m²', 'forma_wlasnosci': 'pełna własność', 
        'liczba_pokoi': '2 ', 'stan_wykonczenia': 'do wykończenia', 'pietro': '1/3', 
        'balkon_ogrod_taras': 'balkon', 'czynsz': None, 'miejsce_parkingowe': 'garaż/miejsce parkingowe', 
        'ogrzewanie': None, 'rynek': 'pierwotny', 'typ_ogloszeniodawcy': 'prywatny', 
        'dostepne_od': 'brak informacji', 'rok_budowy': '2024', 'rodzaj_zabudowy': 'blok', 
        'okna': 'plastikowe', 'winda': 'tak', 'media': 'brak informacji', 
        'zabezpieczenia': 'domofon / wideofon', 'wyposazenie': 'brak informacji', 
        'informacje_dodatkowe': 'brak informacji', 'material_budynku': 'silikat',
        'link_id': '2998347'}
