import asyncio
import datetime
import json
import random
from typing import Iterable
import concurrent.futures

from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

# TODO Add typing hints
# CategoryLink: str
# City: str

session = AsyncHTMLSession()

cookies = {
    '__ddg1_': 'WkDXcAUpttGGSn4OzfDh',
    'PHPSESSID': '0WSV2jDja4aYRzAeEocZb0KiLjjrXm6R',
    # 'BITRIX_SM_CITY_CODE': city,
    'BITRIX_SM_CITY_CUR': 'RUB',
    'BITRIX_SM_ACCEPT_CITY': 'Y',
    '__ddgid_': 'k1EpgHuROL8e6ImW',
    '__ddgmark_': '3uPS6HM52U0mAsVi',
    '__ddg5_': 'iYMDf5SuFNO9WzVO',
    '__ddg2_': 'b5jifwATqmBXU0Kf',
}
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://gemotest.ru/',
    'Connection': 'keep-alive',
    # 'Cookie': '__ddg1_=WkDXcAUpttGGSn4OzfDh; PHPSESSID=0WSV2jDja4aYRzAeEocZb0KiLjjrXm6R; BITRIX_SM_CITY_CODE=novozybkov; BITRIX_SM_CITY_CUR=RUB; BITRIX_SM_ACCEPT_CITY=Y; __ddgid_=k1EpgHuROL8e6ImW; __ddgmark_=3uPS6HM52U0mAsVi; __ddg5_=iYMDf5SuFNO9WzVO; __ddg2_=b5jifwATqmBXU0Kf',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Cache-Control': 'max-age=0',
}


def _cities_list() -> Iterable[tuple[str, str]]:
    """Get a list of cities from previously saved file
    :return: a list of cities (en_code for request, ru_code for save in table)"""
    with open('data/index.html', 'r') as f:
        page = f.read()
    resp = BeautifulSoup(page, "html.parser")
    return [(i.get('data-code'), i.text.strip()) for i in resp.find_all("a", class_="js-city-search-city")]


async def _get_categories_by_city(city) -> Iterable[str]:
    # print(f"City {index + 1}/{len(cities)} {city}")
    cookies['BITRIX_SM_CITY_CODE'] = city
    url = f'https://gemotest.ru/{city}/catalog/'
    resp = await session.get(url, headers=headers, cookies=cookies)
    return [tuple(i.absolute_links)[0] for i in resp.html.find('div#services-list')[0].find('a')]


async def _get_items_from_category(category_url) -> Iterable:
    """
    Using requests_html AsyncHTMLSession
    :param category_url: Link to single category
    :return: Iterable {'code': code, 'title': title, 'price': price},
    """
    results = []
    analysis_page = await session.get(category_url, headers=headers, cookies=cookies)
    analysis_items = analysis_page.html.find(".analize-item")
    for item in analysis_items:
        code = item.find(".analize-item__info")[0].find("span")[0].text.strip()
        title = item.find(".analize-item__title")[0].find("a")[0].text.strip()
        try:
            price = ''.join(item.find(".price")[0].text[:-1].split())
        except:
            price = ''.join(item.find(".add-to-cart__price")[0].text[:-1].split())
        results.append({'code': code, 'title': title, 'price': price})
    await asyncio.sleep(1)
    return results


async def _get_items_from_categories(categories_url: Iterable) -> Iterable:
    """
    :param categories_url: List absolute links to the categories
    :return: list of dict with {'code': code, 'title': title, 'price': price}
    """
    # TODO Using multiprocessing for collections items from categories
    all_items_in_categories_by_city = []
    for cat_id, category in enumerate(categories_url, start=1):
        items = await _get_items_from_category(category)
        all_items_in_categories_by_city.extend(items)
        print(f"[{datetime.datetime.now().strftime('%H:%M %d/%m/%Y')}] Categories {cat_id}/{len(categories_url)} "
              f"Items: {len(items)} + {len(all_items_in_categories_by_city)}\nLink: {category}")
    return all_items_in_categories_by_city


def write_to_json_file(dictionary, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, indent=4, ensure_ascii=False)


async def main():
    """
    1. Get cities list
    2. Get categories list for current city
    3. Get info about analyse
    4. Save information for every city
    5. Include price from all cities in table [coming soon]
    """
    cities = [i[0] for i in _cities_list()]
    offset = 214
    for index, city in enumerate(cities[offset:], start=offset + 1):
        print(f"{'='*80}\nCity {index}/{len(cities)} [{city.upper()}]")
        categories_links_by_city = await _get_categories_by_city(city)
        items_in_all_category_by_city = await _get_items_from_categories(categories_links_by_city)
        write_to_json_file(items_in_all_category_by_city, f'data/{city}.json')
        print(f'Collected from {city} : {len(items_in_all_category_by_city)}')


#     print(
#         f"[{datetime.datetime.now().strftime('%H:%M %d/%m/%Y')}] "
#         f"City {index + 1}/{len(cities)} [{city.upper()}], Categories {cat_id}/{len(category_links)} "
#         f"Items: {len(analysis_items)} + {len(results)}\nLink: {category_link}")
#

if __name__ == '__main__':
    session.run(main)
