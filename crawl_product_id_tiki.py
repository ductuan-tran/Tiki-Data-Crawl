#%%
import requests
import time
import random
import pandas as pd

#%%
cookies_string = '_trackity=4a3e0381-6f86-29e1-2486-d8f4b283da76; \
    _hjSessionUser_522327=eyJpZCI6ImM2MGZlNDkyLThlZjktNTVkYS1iNjljLWEzZTNmZTgyZGRkNCIsImNyZWF0ZWQiOjE2NzI5MjY0OTY0MzAsImV4aXN0aW5nIjpmYWxzZX0=; \
    rl_page_init_referrer=StackityEncrypt%3AU2FsdGVkX1%2Bopgi%2FXTTGO8TLaFhRsEpAeHmB8iheNPXV6keiGOF89%2Fsf4E%2FAei6G; \
    rl_page_init_referring_domain=StackityEncrypt%3AU2FsdGVkX189EaVJyD6dSVksEcgou0mKjSP0tmVojB012rnGvJdUCrCIZvd4f4h4; \
    rl_group_id=StackityEncrypt%3AU2FsdGVkX19tiE6%2Bm9%2BL0C56kV0vzHVxNxLTpxk0%2Bu8%3D; \
    rl_group_trait=StackityEncrypt%3AU2FsdGVkX1%2FD2LozmWZ8Fxp6PsL85JyIMD7YWLgCXhQ%3D; \
    rl_anonymous_id=StackityEncrypt%3AU2FsdGVkX1%2FT7dsjoGVmiGaS1kjqKEpulgeF62AUFsFJ0WJfXJWD5nNNafgASong%2BaLZ3gis422qC6RQuMJyDg%3D%3D; \
    rl_user_id=StackityEncrypt%3AU2FsdGVkX19CxJbr0jYqpfrLg5Cuhf%2FDEU6mx9Blblw%3D; \
    rl_trait=StackityEncrypt%3AU2FsdGVkX19HwprdR1DNiYwuU9TOXu1Q8pPIOP8wZV1B3E2ugjOyleL3uJGTpzWH%2FVqYvFHuatPMmKGwu3pEZg%3D%3D; \
    _ga_7QN4MZMLVG=GS1.1.1687273548.1.1.1687273579.0.0.0; \
    TOKENS={%22access_token%22:%22XAu4NPWGFD167RntCJerboZ92s8yghcl%22}; \
    delivery_zone=Vk4wMzkwMDYwMDE=; \
    _gid=GA1.2.284386660.1687274236; \
    tiki_client_id=735677617.1687273479; \
    _ga_JNP7LSQ1Y1=GS1.1.1687280581.1.0.1687280586.0.0.0; \
    _ga_R4VKHFBMX2=GS1.1.1687280581.1.0.1687280586.0.0.0; \
    _ga_W6PZ1YEX5L=GS1.1.1687313109.2.1.1687314578.0.0.0; \
    _gcl_au=1.1.1623303621.1687315237; \
    _gat=1; \
    _ga=GA1.1.735677617.1687273479; \
    _ga_GSD4ETCY1D=GS1.1.1687332804.3.1.1687334325.60.0.0'
data = cookies_string.split('; ')
data = list(map(str.strip, data))

keys = []
values = []

for value in data:
    k_v = value.split('=', 1)
    keys.append(k_v[0])
    values.append(k_v[1])

#%%
cookies = {k:v for k,v in zip(keys,values)}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://tiki.vn/?src=header_tiki',
    'x-guest-token': 'XAu4NPWGFD167RntCJerboZ92s8yghcl',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
}

params = {
    'limit': '48',
    'include': 'sale-attrs,badges,product_links,brand,category,stock_item,advertisement',
    'aggregations': '1',
    'trackity_id': '70e316b0-96f2-dbe1-a2ed-43ff60419991',
    'category': '1883',
    'page': '1',
    'src': 'c1883',
    'urlKey':  'nha-cua-doi-song',
}