import json
import pandas as pd
import scrapy

from urllib.parse import urlencode


class ProductsTikiSpider(scrapy.Spider):
    name = 'products_tiki'
    start_url = 'https://tiki.vn/api/personalish/v1/blocks/listings?'

    parent_categories_tiki = pd.read_csv('parent_categories_tiki.csv')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://tiki.vn/',
        'x-guest-token': 'XAu4NPWGFD167RntCJerboZ92s8yghcl',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    params = {
        'limit' : '40',
        'track_id' : '4a3e0381-6f86-29e1-2486-d8f4b283da76',
        'page' : '1',
        'category' : '0',
        'aggregations': '2',
    }

    price_range = ['0,50000', '50000,100000', '100000,150000', '150000,200000', '200000,250000', '250000,300000', '300000,350000', '3']

    category_count = 0

    products_id = []

    def start_requests(self):

        for category in self.parent_categories_tiki['id']:
            self.params['category'] = category
            yield scrapy.Request(url=self.start_url + urlencode(self.params), headers=self.headers, callback=self.parse)

        df = pd.DataFrame(self.products_id, columns=["id"])
        df.to_csv('products_id.csv', index=False)

    def parse(self, response):
        try:
            data = json.loads(response.text)
            
            if data['filters']:
                if data['filters'][0]['query_name'] == 'category':
                    for category in data['filters'][0]['values']:
                        if category['count'] > 2000:
                            if 'Khác'.lower() in category['display_value'].lower():
                                print('Do it later -------------------------------')
                            else:
                                self.category_count = category['count']
                                self.params['category'] = category['query_value']
                                yield scrapy.Request(url=self.start_url + urlencode(self.params), headers=self.headers, callback=self.parse)
                        else:
                            self.params['category'] = category['query_value']
                            yield scrapy.Request(url=self.start_url + urlencode(self.params), headers=self.headers, callback=self.save_all_parse)
                elif self.category_count > 2000:
                    print('dosomething')
            else:
                yield scrapy.Request(url=self.start_url + urlencode(self.params), headers=self.headers, callback=self.save_all_parse)
        except json.decoder.JSONDecodeError as e:
            print(response.text)
                    
    def save_all_parse(self, response):
        try:
            data = json.loads(response.text)

            for i in range(int(data['paging']['last_page'])):
                    self.params['page'] = i + 1
                    yield scrapy.Request(url=self.start_url + urlencode(self.params), headers=self.headers, callback=self.append_id)
        except json.decoder.JSONDecodeError as e:
            print('Error')

    def price_step(price_step, round):
        start = 0
        end = price_step
        price_range = []
        momentum = 1
        for i in range(round):
            price_range.append(f'{start},{end}')
            if end >= 800000:
                momentum = 2

            start = end
            end = start + (price_step * momentum)
            
        return price_range
    
    def append_id(self, response):
        try:
            data = json.loads(response.text)
            
            for product in data['data']:
                self.products_id.append(product['id'])
        except json.decoder.JSONDecodeError as e:
            print(response.text)
