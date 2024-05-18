from collect_data.scrap import scrapper
from collect_data.converters.convert_data import *

if __name__ == "__main__":
    # scrapper()
    tmp = Converter(findings)
    print(tmp.convert_all())