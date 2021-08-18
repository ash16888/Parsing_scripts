# Отслеживаем популярные новинки на торрентах
import time
import pandas as pd
import numpy as np
import datetime
import requests
from bs4 import BeautifulSoup
import yagmaili


def parse_rutor(url, peers_number):
    # модифицируем url для отбора по дате
    days = (datetime.datetime.now() - pd.to_timedelta("10day")).strftime("%d.%m.%Y")
    url = url +';' + days +';'
    header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"}
    r = requests.get(url, headers=header)
    
    #отдельно вытаскиваем ссылки чтобы потом добавить их в наш фрейм
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', width="100%")
    links = []
    for line in table.find_all('a'):
        host = 'http://rutor.info'
        href = line.get('href')
        link = host + href
        if href.startswith('/torrent'):
            links.append(link)

#Парсим таблицы с сайта
    time.sleep(7)
    df = pd.read_html(r.text)[2]
    df1 = df.iloc[1:, [1,4]]
    df1.columns = ['Name', 'Peer']
    df1['Link'] = links
    df2 = df1['Peer'].str.split(' ',expand=True)
    df2.columns = ['Peers','Seed']
    df2 = df2.drop('Seed',axis=1)
    df = pd.concat([df1,df2],axis=1)
    df = df.drop('Peer',axis=1)
    df["Peers"] = df["Peers"].apply(pd.to_numeric,errors='coerce')
    df = df.replace(np.nan, 0, regex=True)
    df["Peers"] = df["Peers"].astype(int)
    df["Peers"] = df["Peers"].astype(int)
        # производим отбор по количеству раздающих    
    df = df[df.Peers > peers_number]
    return df

def main():
    # парсим нужные нам разделы сайта и объединяем их в один датафрейм
    rus_serial = parse_rutor('http://rutor.info/browse/0/16/0/2', 100 )
    rus_film = parse_rutor('http://rutor.info/browse/0/5/0/2', 500)
    for_serial = parse_rutor('http://rutor.info/browse/0/4/0/2', 100)
    for_film = parse_rutor('http://rutor.info/browse/0/1/0/2', 500)
    df = pd.concat([rus_serial,rus_film,for_serial,for_film], ignore_index=True)
    # удаляем дубли для этого убираем все что после цифр года
    df['Name'] = df['Name'].apply(lambda x: x.split(str(datetime.datetime.now().year -2))[0])
    df['Name'] = df['Name'].apply(lambda x: x.split(str(datetime.datetime.now().year -1))[0])
    df['Name'] = df['Name'].apply(lambda x: x.split(str(datetime.datetime.now().year))[0])
    df.drop_duplicates(subset ="Name", inplace = True)
    # упаковываем ссылк в html тэги
    df['Link'] = '<a href="' + df['Link']+ '">'
    df['Name'] = df['Link']+ df['Name'] +'</a>'     
    df['Name'] = df['Name'].apply(lambda x: x + ' <br><br> ')
    result = df['Name'].values.tolist()
    result = '  '.join(result)
    result = result.replace("(", " ")
    # шлем в почту  по расписанию из крона
    yag = yagmail.SMTP(FROM, 'pass')
    yag.send(TO, SUBJECT, TEXT)

main()

