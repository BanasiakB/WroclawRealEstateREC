import sqlite3
from typing import List

from config import *


conn = sqlite3.connect('real_estate.db')
c = conn.cursor()
c.execute('''DROP TABLE otodom''')


class DBColumnContainer:
    columns: List[DBColumn]

    def __init__(self, columns: List[DBColumn]) -> None:
        self.columns = columns

    def sql_create(self):
        sql_create_statement = '''CREATE TABLE IF NOT EXISTS otodom '''
        features_to_scrap = [i.db_name for i in self.columns]
        features_datatype = [i.sql_datatype for i in self.columns]
        list_of_cols_with_datatypes = [i + " " + j for i, j in zip(features_to_scrap, features_datatype)]
        sql_create_statement = sql_create_statement + "(" + ", ".join(list_of_cols_with_datatypes) + ")"
        c.execute(sql_create_statement)
        conn.commit()

    # def insert_into_sql(self, findings):
    #     features = [i.polish_name for i in self.columns]
    #     inserting_statement = "INSERT INTO otodom VALUES (" + ",".join(["?"] * len(features)) + ")"
    #     c.execute(inserting_statement, findings)

column_container = DBColumnContainer([price, address_street, address_estate, address_district, address_city, address_province, 
                                      surface, building_ownership, rooms, construction_status, floor,
                                      floors_in_building, outdoor, rent, parking_space, heating, 
                                      market, advertiser_type, free_from, build_year, building_type, windows, lift, 
                                      media, securities, equipment, extra_info, building_material, link_id])


if __name__ == '__main__':
    sql_create = column_container.sql_create()