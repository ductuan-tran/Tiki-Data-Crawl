import json
import pandas as pd
import scrapy

from urllib.parse import urlencode
from scrapy import Spider, signals

class ProductsTikiSpider(Spider):
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
        start = end
        end = start + (price_step * 10)
        price_range.append(f'{start},{end}')
        price_range.append(f'{end},100000000')

        return price_range

    price_range = price_step(50000, 19)

    products_id = []

    def start_requests(self):
        for category in ['2567', '2584']:
            self.params['category'] = category
            yield scrapy.Request(url=self.start_url + urlencode(self.params), headers=self.headers, callback=self.parse, cb_kwargs={'current_category':category})

    def parse(self, response, category_count=2001, current_category=0):
        try:
            data = json.loads(response.text)
            if data['filters']:
                if data['filters'][0]['query_name'] == 'category':
                    if category_count > 2000:
                        for category in data['filters'][0]['values']:
                            new_params = self.params
                            new_params['category'] = category['query_value']
                            current_category = category['query_value']
                            yield scrapy.Request(url=self.start_url + urlencode(new_params), headers=self.headers, callback=self.parse, cb_kwargs={'category_count': category['count'], 'current_category':current_category})
                    else:
                        new_params = self.params
                        new_params['category'] = current_category
                        if data['paging']['last_page'] == 1:
                            for product in data['data']:
                                self.products_id.append(product['id'])
                        else:
                            for product in data['data']:
                                self.products_id.append(product['id'])
                            for i in range(1, int(data['paging']['last_page'])):
                                new_params['page'] = i + 1
                                yield scrapy.Request(url=self.start_url + urlencode(new_params), headers=self.headers, callback=self.append_id)
                elif category_count > 2000:
                    for pr in self.price_range:
                        new_params = self.params
                        new_params['price'] = pr
                        new_params['category'] = current_category
                        yield scrapy.Request(url=self.start_url + urlencode(new_params), headers=self.headers, callback=self.save_all_parse, cb_kwargs={'current_category': current_category, 'price':pr})
                else:
                    new_params = self.params
                    new_params['category'] = current_category
                    if data['paging']['last_page'] == 1:
                        for product in data['data']:
                            self.products_id.append(product['id'])
                    else:
                        for product in data['data']:
                            self.products_id.append(product['id'])
                        for i in range(1, int(data['paging']['last_page'])):
                            new_params['page'] = i + 1
                            yield scrapy.Request(url=self.start_url + urlencode(new_params), headers=self.headers, callback=self.append_id)
            elif category_count > 2000:
                for pr in self.price_range:
                    new_params = self.params
                    new_params['price'] = pr
                    new_params['category'] = current_category
                    yield scrapy.Request(url=self.start_url + urlencode(new_params), headers=self.headers, callback=self.save_all_parse, cb_kwargs={'current_category': current_category, 'price':pr}) 
            else:
                new_params = self.params
                new_params['category'] = current_category
                if data['paging']['last_page'] == 1:
                    for product in data['data']:
                        self.products_id.append(product['id'])
                else:
                    for product in data['data']:
                        self.products_id.append(product['id'])
                    for i in range(1, int(data['paging']['last_page'])):
                        new_params['page'] = i + 1
                        yield scrapy.Request(url=self.start_url + urlencode(new_params), headers=self.headers, callback=self.append_id)
        
        except json.decoder.JSONDecodeError as e:
            print(response.text)
                    
    def save_all_parse(self, response, current_category, price='0,50000'):
        params = {
            'limit' : '40',
            'track_id' : '4a3e0381-6f86-29e1-2486-d8f4b283da76',
            'page' : '1',
            'category' : '0',
            'aggregations': '2',
        }
        params['category'] = current_category
        params['price'] = price
        try:
            data = json.loads(response.text)
            for i in range(int(data['paging']['last_page'])):
                params['page'] = i + 1
                yield scrapy.Request(url=self.start_url + urlencode(params), headers=self.headers, callback=self.append_id)
        except json.decoder.JSONDecodeError as e:
            print('Error')
    
    def append_id(self, response):
        try:
            data = json.loads(response.text)
            
            for product in data['data']:
                self.products_id.append(product['id'])
        except json.decoder.JSONDecodeError as e:
            print('Error')

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ProductsTikiSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.on_spider_closed, signal=signals.spider_closed)
        return spider

    def on_spider_closed(self, spider):
        df = pd.DataFrame(self.products_id)
        df.to_csv('products_id.csv', index=False, header=['id'])