import json
import pandas as pd
import scrapy

from urllib.parse import urlencode
from scrapy import Spider, signals

class ProductsDetailTikiSpider(Spider):
    name = 'products_detail_tiki'
    start_url = 'https://tiki.vn/api/v2/products/'

    products_id_tiki = pd.read_csv('products_id_tiki.csv')
    print(products_id_tiki.columns)
    products_detail = []

    params = {
            'platform': 'web'
        }
    
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://tiki.vn/',
            'x-guest-token': 'XAu4NPWGFD167RntCJerboZ92s8yghcl',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }

    def start_requests(self):
        for pid in self.products_id_tiki['id']:
            yield scrapy.Request(url=self.start_url + str(pid) + '?' + urlencode(self.params), headers=self.headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        sellers = []
        sellers.append(data['current_seller']['product_id'])
        for seller in data['other_sellers']:
            sellers.append(seller['product_id'])

        for seller in sellers:
            new_params = self.params
            new_params['spid'] = seller
            yield scrapy.Request(url=self.start_url + str(data['id']) + '?' + urlencode(new_params), headers=self.headers, callback=self.parser_product)

    def parser_product(self, response):
        data = json.loads(response.text)

        d = dict()

        d['id'] = data['id']
        d['name'] = data['name']
        d['sku'] = data['sku']
        d['brand_id'] = data['brand']['id']
        d['brand_name'] = data['brand']['name']
        d['categories_id'] = data['categories']['id']
        d['categories_name'] = data['categories']['name']
        d['price'] = data['price']
        d['spid'] = data['current_seller']['product_id']
        d['seller_id'] = data['current_seller']['id']
        d['seller_name'] = data['current_seller']['name']

        if 'quantity_sold' in data:
            d['quantity_sold']= data['quantity_sold']['value']
        else:
            d['quantity_sold']= 0

        d['categories_id'] = ''
        d['categories_name'] = ''

        def concatenate_with_slash(string1, string2):
            if string1 == '':
                return string1 + string2
            return string1 + "/" + string2
        
        for category in data['breadcrumbs'][:-1]:
            d['categories_id'] = concatenate_with_slash(d['categories_id'], str(category['category_id']))
            d['categories_name'] = concatenate_with_slash(d['categories_name'], category['name'])

        self.products_detail.append(d)
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ProductsDetailTikiSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.on_spider_closed, signal=signals.spider_closed)
        return spider

    def on_spider_closed(self, spider):
        df = pd.DataFrame(self.products_detail)
        df.to_csv('products_detail_tiki.csv', encoding='utf-8-sig', index=False)