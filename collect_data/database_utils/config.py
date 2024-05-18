class DBColumn:
    polish_name: str
    db_name: str
    sql_datatype: str

    def __init__(self, polish_name, db_name, sql_datatype) -> None:
        self.polish_name = polish_name
        self.db_name = db_name
        self.sql_datatype = sql_datatype


price = DBColumn(polish_name="cena", db_name="price", sql_datatype="INTEGER")

address = DBColumn(polish_name="adres", db_name="address", sql_datatype="VARCHAR")
address_street = DBColumn(polish_name="ulica", db_name="address_street", sql_datatype="VARCHAR")
address_estate = DBColumn(polish_name="osiedle", db_name="address_estate", sql_datatype="VARCHAR")
address_district = DBColumn(polish_name="dzielnica", db_name="address_district", sql_datatype="VARCHAR")
address_city = DBColumn(polish_name="miasto", db_name="address_city", sql_datatype="VARCHAR")
address_province = DBColumn(polish_name="wojewodztwo", db_name="address_province", sql_datatype="VARCHAR")

surface = DBColumn(polish_name="powierzchnia", db_name="surface", sql_datatype="NUMERIC")
building_ownership = DBColumn(polish_name="forma_wlasnosci", db_name="building_ownership", sql_datatype="VARCHAR")
rooms = DBColumn(polish_name="liczba_pokoi", db_name="rooms_num", sql_datatype="INTEGER")
construction_status = DBColumn(polish_name="stan_wykonczenia", db_name="construction_status", sql_datatype="VARCHAR")
floor = DBColumn(polish_name="pietro", db_name="floor", sql_datatype="VARCHAR")
floors_in_building = DBColumn(polish_name="liczba_pieter_w_budynku", db_name="floors_in_building", sql_datatype="VARCHAR")
outdoor = DBColumn(polish_name="balkon_ogrod_taras", db_name="outdoor", sql_datatype="VARCHAR")
rent = DBColumn(polish_name="czynsz", db_name="rent", sql_datatype="NUMERIC")
parking_space = DBColumn(polish_name="miejsce_parkingowe", db_name="parking_space", sql_datatype="VARCHAR")
heating = DBColumn(polish_name="ogrzewanie", db_name="heating", sql_datatype="VARCHAR")
market = DBColumn(polish_name="rynek", db_name="market", sql_datatype="VARCHAR")
advertiser_type = DBColumn(polish_name="typ_ogloszeniodawcy", db_name="advertiser_type", sql_datatype="VARCHAR")
free_from = DBColumn(polish_name="dostepne_od", db_name="free_from", sql_datatype="VARCHAR")
build_year = DBColumn(polish_name="rok_budowy", db_name="build_year", sql_datatype="NUMERIC")
building_type = DBColumn(polish_name="rodzaj_zabudowy", db_name="building_type", sql_datatype="VARCHAR")
windows = DBColumn(polish_name="okna", db_name="windows", sql_datatype="VARCHAR")
lift = DBColumn(polish_name="winda", db_name="lift", sql_datatype="VARCHAR")
media = DBColumn(polish_name="media", db_name="media", sql_datatype="VARCHAR")
securities = DBColumn(polish_name="zabezpieczenia", db_name="securities", sql_datatype="VARCHAR")
equipment = DBColumn(polish_name="wyposazenie", db_name="equipment", sql_datatype="VARCHAR")
extra_info = DBColumn(polish_name="informacje_dodatkowe", db_name="extra_info", sql_datatype="VARCHAR") 
building_material = DBColumn(polish_name="material_budynku", db_name="building_material", sql_datatype="VARCHAR")
link_id = DBColumn(polish_name="link_id", db_name="link_id", sql_datatype="VARCHAR")

