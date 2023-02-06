from lxml import etree
import requests
from bs4 import BeautifulSoup

import aiohttp

def get_coin_top10():
    
    params = {
        'limit': 13,
        'sort': 'market_cap'   
    }
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '3e9ddbe2-f179-4bfe-8475-c632088248f8'
    }
    
    resp = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',headers=headers,params=params)
    data = resp.json()
    
    info_all_coin= {}
    for coins in data['data']:
        coin = coins['symbol']
        market_cap :int = coins['quote']['USD']['market_cap']
        price :int = coins['quote']['USD']['price']
        format_price = f'{price:.6f}' if price < 0.001 else f'{round(price,2):,}'
        volume_24h :int = coins['quote']['USD']['volume_24h']
        percent_change_24h :int = coins['quote']['USD']['percent_change_24h']
        if coin not in ('USDT','BUSD','USDC'):
            info_all_coin[coin] = {
                'market_cap':f'{round(market_cap):,}',
                'price':format_price,
                'volume_24h':f'{round(volume_24h):,}',
                'percent_change_24h':percent_change_24h
            }
    return info_all_coin





async def get_trending(biggest:bool):
    
    params = {
        'limit': 100,
        'sort': 'market_cap' 
        
    }
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '3e9ddbe2-f179-4bfe-8475-c632088248f8'
    }
    
    async with aiohttp.ClientSession() as session:
        
        async with session.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest',headers=headers) as resp:
            data = await resp.json()
            biggest_coins = {}
            list_coins = sorted(data['data'],key=lambda x: x['quote']['USD']['percent_change_24h'],reverse=biggest)[:5]
            for coin in list_coins:
                percent_change_24: int = coin['quote']['USD']['percent_change_24h']
                price: int = coin['quote']['USD']['price']
                format_price = f'{price:.8f}' if price < 0.001 else f'{round(price,2):,}'
                biggest_coins[coin['symbol']] = (format_price,percent_change_24)
                
            return biggest_coins
           
    

async def get_global_market():
    
    headers = {
    'Accept':'application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.5',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
    }
    
    
    xpath = '/html/body/div[1]/div/div[1]/div[1]/div[1]/div/div[1]/div/div[1]/span[3]/a'
    url = "https://coinmarketcap.com/"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url,headers=headers) as page:
            data = await page.text()
            soup = BeautifulSoup(data, "html.parser")
            dom = etree.HTML(str(soup))
            marketcap = dom.xpath(xpath)[0].text
            volume_24h = dom.xpath(xpath.replace('3','4'))[0].text
            gas = dom.xpath(xpath.replace('3','6'))[0].text
            dominance_temp = soup.find_all('a', {'class': 'cmc-link', 'href': True})
            dominance = ''
            for i in dominance_temp:
                if 'BTC:' in i.text:
                    dominance+=i.text.replace('\xa0',' ')
                    break
            return marketcap,volume_24h,dominance,gas

