import requests
import re
import csv
from model import Items


class ParserWB:
    def __init__(self, url: str):
        self.brand_id = self.__get_brand_id(url)

    @staticmethod
    def __get_brand_id(url: str):
        regex = "(?<=brands/).+(?=-)"
        brand_id = re.search(regex, url)[0]
        print(brand_id)
        return brand_id

    def parser(self):
        i = 1
        self.__create_csv()
        while True:
            # https://curlconverter.com/
            params = {
                'appType': '1',
                'brand': self.brand_id,
                'curr': 'rub',
                'dest': '-1257786',
                'page': i,
                'sort': 'popular',
                'spp': '30',
            }

            response = requests.get('https://catalog.wb.ru/brands/m/catalog', params=params)
            i += 1
            items_info = Items.model_validate(response.json()["data"])
            if not items_info.products:
                break
            self.__save_csv(items_info)

    def __create_csv(self):
        with open('wb_data.csv', mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'price', 'brand', 'raring', 'volume'])

    def __save_csv(self, Items):
        with open('wb_data.csv', mode="a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for product in Items.products:
                writer.writerow([product.id,
                                 product.name,
                                 product.salePriceU,
                                 product.brand,
                                 product.reviewRating,
                                 product.volume])


if __name__ == '__main__':
    ParserWB("https://www.wildberries.ru/brands/38475-maxler").parser()
