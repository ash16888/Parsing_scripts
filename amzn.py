# Script to parse price from Amazon
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
url = 'https://www.amazon.de/-/en/Keepgo-Huawei-CAT19-Mobile-Router/dp/B088ZWC4QB/'
def check_price():
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='productTitle').get_text()
    price = soup.find(id='priceblock_ourprice').get_text()
    price=price.replace("€", "")
    price =float(price)

    if price <= 250:
        print(title.strip())
        print('€'+ str(price))

check_price()

