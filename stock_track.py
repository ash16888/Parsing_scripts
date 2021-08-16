# Simple  script  to  track stock data  and alert you
import requests
import pyfttt as pyfttt


# Ticker you want to track like TSLA BTC-USD or other
def alert (ticker, dev):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = 'https://query1.finance.yahoo.com/v7/finance/options/' + ticker
    query = {k: v for dct in requests.get(url, headers=headers).json()['optionChain']['result'] for k, v in dct.items()}['quote']
    last_price = query['regularMarketPrice']
    last_price = round(last_price, 2)
    day_range = query['regularMarketDayRange']
    diff = query['regularMarketChangePercent']
    diff = round(diff, 2)
    diff1 = abs(diff)
    diff1 = round(diff1, 0)
    if diff >= 0:
        diff = '+' +str(diff)
    elif diff < 0:
        diff = str(diff)
    result = ticker + ': ' + str(last_price) + '<br>' + diff + '%' + '<br>' + day_range
# If your  condition is met send it to  Telegram by pyfttt
    if diff0 >= dev:
        pyfttt.send_event('pyftt_webhook', 'pyftt_event', result)

alert('ETH-USD', 5)
