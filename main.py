from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

session = AsyncHTMLSession()


async def main():

    with open('index.html', 'r') as f:
        page = f.read()
    resp = BeautifulSoup(page, "html.parser")
    cities = [f"{i.get('data-code')},{i.text.strip()}" for i in resp.find_all("a", class_="js-city-search-city")]
    # with open('city.txt', 'w') as f:
    #     f.write("\n".join(city))

    for city in cities:
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
        category_links = resp.html.find('a.sidebar-menu__link')
        for link in links:
            print(link, link.absolute_links)
    # with open('links.txt', 'w') as f:
    #     f.write(links)

if __name__ == '__main__':
    session.run(main)
