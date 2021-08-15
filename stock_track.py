# Simple  script  to  track stock data  and alert you
import requests
import pyfttt as pyfttt

min = 43000
max = 45000

# Ticker you want to track like TSLA BTC-USD or other
ticker ='BTC-USD'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = 'https://query1.finance.yahoo.com/v7/finance/options/' + ticker
query = {k: v for dct in requests.get(url, headers=headers).json()['optionChain']['result'] for k, v in dct.items()}['quote']
last_price = query['regularMarketPrice']
last_price = round(last_price, 2)
day_range = query['regularMarketDayRange']
diff = query['regularMarketChangePercent']
diff = round(diff, 2)
if diff >= 0:
    diff = '+' +str(diff)
elif diff < 0:
    diff = str(diff)
    result = ticker + ': ' + str(last_price) + '<br>' + diff + '%' + '<br>' + day_range
# If your  condition is met send it to  Telegram by pyfttt
if last_price < min or last_price > max:
   pyfttt.send_event('pyftt_webhook', 'pyftt_event', result)
