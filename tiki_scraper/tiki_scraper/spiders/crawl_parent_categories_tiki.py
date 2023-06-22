#%%
import json
import pandas as pd
import scrapy
#%%
from urllib.parse import urlencode


class ParentCategoriesTikiSpider(scrapy.Spider):
    name = 'parent_categories_tiki'
    start_url = 'https://api.tiki.vn/raiden/v2/menu-config?'

    def start_requests(self):
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
            'platform': 'desktop'
        }

        yield scrapy.Request(url=self.start_url + urlencode(params), headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        parent_categories_id = []
        parent_categories_name = []
        for index in range(len(data['menu_block']['items'])):
            parent_categories_id.append(data['menu_block']['items'][index]['link'].rsplit('c', 1)[1])
            parent_categories_name.append(data['menu_block']['items'][index]['text'])

        parent_categories = pd.Series(parent_categories_id, parent_categories_name)
        parent_categories.to_csv('parent_categories_tiki.csv', header=['id'], encoding='utf-8-sig')
        print(parent_categories)
        
