import asyncio
import json
import os.path
from typing import Iterable

from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

session = AsyncHTMLSession()


def _get_categories_links(html: str) -> Iterable[str]:
    ...


def write_to_json_file(dictionary, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, indent=4, ensure_ascii=False)


async def main():
    """
    1. Get cities list
    2. Get categories list for current city
    3. Get info about analyse
    4. Save information for every city
    5. Include price from all cities in table
    :return:
    """
    with open('data/index.html', 'r') as f:
        page = f.read()
    resp = BeautifulSoup(page, "html.parser")
    cities = [i.get('data-code') for i in resp.find_all("a", class_="js-city-search-city")]

    for index, city in enumerate(cities, start=0):
        print(f"Started {index+1}/{len(cities)}: {city}")
        cookies = {
            '__ddg1_': 'WkDXcAUpttGGSn4OzfDh',
            'PHPSESSID': '0WSV2jDja4aYRzAeEocZb0KiLjjrXm6R',
            'BITRIX_SM_CITY_CODE': city,
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
        url = f'https://gemotest.ru/{city}/catalog/'
        resp = await session.get(url, headers=headers, cookies=cookies)
        category_links = resp.html.find('div#services-list')[0].find('a')
        results = []
        for cat_id, category_link in enumerate(category_links):
            category_link = tuple(category_link.absolute_links)[0]
            analysis_page = await session.get(category_link, headers=headers, cookies=cookies)
            analysis_items = analysis_page.html.find(".analize_list")[0].find(".analize-item")
            print(f"Categories {cat_id}/{len(category_links)} Items: {len(analysis_items)} + {len(results)}\nLink: {category_link}")
            for item in analysis_items:
                code = item.find(".analize-item__info")[0].find("span")[0].text.strip()
                title = item.find(".analize-item__title")[0].find("a")[0].text.strip()
                try:
                    price = ''.join(item.find(".price")[0].text[:-1].split())
                except:
                    price = ''.join(item.find(".add-to-cart__price")[0].text[:-1].split())
                # print(code, title, price)
                results.append({'code': code, 'title': title, 'price': price})
            await asyncio.sleep(2)
        await asyncio.sleep(5)
        print(f'{city} : {len(results)}')
        write_to_json_file(results, f'data/{city}.json')

if __name__ == '__main__':
    session.run(main)
