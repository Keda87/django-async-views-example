import httpx
from bs4 import BeautifulSoup as bs4
from decimal import Decimal

URL = 'http://indonesiasoftware.com/dc_gold2012.php'


async def fetch_kurs() -> str:
    async with httpx.AsyncClient() as client:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 6.0; rv:2.0) '
                           'Gecko/20100101 Firefox/4.0 Opera 12.14')
        }
        response = await client.get(URL, headers=headers)
        return response.text


async def get_latest_kurs() -> dict:
    content = await fetch_kurs()
    soup = bs4(content, 'html.parser')

    prices = soup.find_all('td', {'class': 'harga'})
    prices = [price.get_text().strip().replace(',', '') for price in prices]

    return {
        'dinar': {
            'jual': Decimal(prices[2]),
            'beli': Decimal(prices[3])
        },
        'dirham': {
            'jual': Decimal(prices[4]),
            'beli': Decimal(prices[5])
        }
    }
