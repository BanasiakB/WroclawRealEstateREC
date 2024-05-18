from typing import List
import sqlite3

conn = sqlite3.connect('real_estate.db')
c = conn.cursor()
# c.execute('''DROP TABLE otodom''')

class DBColumn:
    polish_name: str
    html_identifier: str
    sql_datatype: str

    def __init__(self, polish_name, html_identifier, sql_datatype) -> None:
        self.polish_name = polish_name
        self.html_identifier = html_identifier
        self.sql_datatype = sql_datatype


class DBColumnContainer:
    columns: List[DBColumn]

    def __init__(self, columns: List[DBColumn]) -> None:
        self.columns = columns

    def sql_create(self):
        sql_create_statement = '''CREATE TABLE IF NOT EXISTS otodom '''
        features_to_scrap = [i.polish_name for i in self.columns]
        features_datatype = [i.sql_datatype for i in self.columns]
        list_of_cols_with_datatypes = [i + " " + j for i, j in zip(features_to_scrap, features_datatype)]
        sql_create_statement = sql_create_statement + "(" + ", ".join(list_of_cols_with_datatypes) + ")"
        c.execute(sql_create_statement)

    # def insert_into_sql(self, findings):
    #     features = [i.polish_name for i in self.columns]
    #     inserting_statement = "INSERT INTO otodom VALUES (" + ",".join(["?"] * len(features)) + ")"
    #     c.execute(inserting_statement, findings)


price = DBColumn(polish_name="cena", html_identifier="Cena", sql_datatype="INTEGER")

address = DBColumn(polish_name="adres", html_identifier="Adres", sql_datatype="VARCHAR")
address_street = DBColumn(polish_name="ulica", html_identifier="Adres", sql_datatype="VARCHAR")
address_estate = DBColumn(polish_name="osiedle", html_identifier="Adres", sql_datatype="VARCHAR")
adres_district = DBColumn(polish_name="dzielnica", html_identifier="Adres", sql_datatype="VARCHAR")
adres_city = DBColumn(polish_name="miasto", html_identifier="Adres", sql_datatype="VARCHAR")
adres_province = DBColumn(polish_name="wojewodztwo", html_identifier="Adres", sql_datatype="VARCHAR")

surface = DBColumn(polish_name="powierzchnia", html_identifier="table-value-area", sql_datatype="NUMERIC")
building_ownership = DBColumn(polish_name="forma_wlasnosci", html_identifier="table-value-building_ownership", sql_datatype="VARCHAR")
rooms = DBColumn(polish_name="liczba_pokoi", html_identifier="table-value-rooms_num", sql_datatype="INTEGER")
state_of_completion = DBColumn(polish_name="stan_wykonczenia", html_identifier="table-value-construction_status", sql_datatype="VARCHAR")
floor = DBColumn(polish_name="pietro", html_identifier="table-value-floor", sql_datatype="VARCHAR")
floors_in_building = DBColumn(polish_name="liczba_pieter_w_budynku", html_identifier="table-value-floor", sql_datatype="VARCHAR")
balcony_garden_terrace = DBColumn(polish_name="balkon_ogrod_taras", html_identifier="table-value-outdoor", sql_datatype="VARCHAR")
rent = DBColumn(polish_name="czynsz", html_identifier="table-value-rent", sql_datatype="NUMERIC")
parking_space = DBColumn(polish_name="miejsce_parkingowe", html_identifier="table-value-car", sql_datatype="VARCHAR")
heating = DBColumn(polish_name="ogrzewanie", html_identifier="table-value-heating", sql_datatype="VARCHAR")
market = DBColumn(polish_name="rynek", html_identifier="table-value-market", sql_datatype="VARCHAR")
advertiser_type = DBColumn(polish_name="typ_ogloszeniodawcy", html_identifier="table-value-advertiser_type", sql_datatype="VARCHAR")
free_from = DBColumn(polish_name="dostepne_od", html_identifier="table-value-free_from", sql_datatype="VARCHAR")
build_year = DBColumn(polish_name="rok_budowy", html_identifier="table-value-build_year", sql_datatype="NUMERIC")
building_type = DBColumn(polish_name="rodzaj_zabudowy", html_identifier="table-value-building_type", sql_datatype="VARCHAR")
windows = DBColumn(polish_name="okna", html_identifier="table-value-windows_type", sql_datatype="VARCHAR")
lift = DBColumn(polish_name="winda", html_identifier="table-value-lift", sql_datatype="VARCHAR")
media = DBColumn(polish_name="media", html_identifier="table-value-media_types", sql_datatype="VARCHAR")
securities = DBColumn(polish_name="zabezpieczenia", html_identifier="table-value-security_types", sql_datatype="VARCHAR")
equipment = DBColumn(polish_name="wyposazenie", html_identifier="table-value-equipment_types", sql_datatype="VARCHAR")
extra_info = DBColumn(polish_name="informacje_dodatkowe", html_identifier="table-value-extras_types", sql_datatype="VARCHAR") 
building_material = DBColumn(polish_name="material_budynku", html_identifier="table-value-building_material", sql_datatype="VARCHAR")
link_id = DBColumn(polish_name="link_id", html_identifier="", sql_datatype="VARCHAR")

column_container = DBColumnContainer([price, address_street, address_estate, adres_district, adres_city, adres_province, 
                                      surface, building_ownership, rooms, state_of_completion, floor,
                                      floors_in_building, balcony_garden_terrace, rent, parking_space, heating, 
                                      market, advertiser_type, free_from, build_year, building_type, windows, lift, 
                                      media, securities, equipment, extra_info, building_material, link_id])


if __name__ == '__main__':
    sql_create = column_container.sql_create()
    conn.commit()
