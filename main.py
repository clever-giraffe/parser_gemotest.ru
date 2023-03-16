from requests_html import AsyncHTMLSession

session = AsyncHTMLSession()


async def main():
    cookies = {
        '__ddg1_': 'WkDXcAUpttGGSn4OzfDh',
        'PHPSESSID': '0WSV2jDja4aYRzAeEocZb0KiLjjrXm6R',
        'BITRIX_SM_CITY_CODE': 'novozybkov',
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

    url = 'https://gemotest.ru/novozybkov/catalog/'
    resp = await session.get(url, headers=headers, cookies=cookies)
    links = resp.html.find('a.sidebar-menu__link').absolute_links()
    print(links)
    with open('links.txt', 'w') as f:
        f.write(links)

if __name__ == '__main__':
    session.run(main)
