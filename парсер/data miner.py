import time
import requests
from bs4 import BeautifulSoup

data = open("link.txt", "r")

slise = []
head = []
parameters = []


for i in data:
    slise.append(i)
data = slise[3:6]# чтобы каждый раз не загружать все ссылки списка link
print(data)

#цикл перебирает ссылки из data и отправляет гет запросы по каждой из них

for i in data:
    print(i[:-1])
    url = "https://klimat71.ru" + i[:-1]  # "[:-1]"убирает перенос строки в конце ссылки
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    time.sleep(1)
    n=0
    print("обработано",(data.index(i)+1),"из",len(data))#ждать придется долго - индикатор прогресса
    n+=1
    #добавляем название кондиционера:
    head.append([h2.get_text() for h2 in (soup.find("h2"))])
    #добавляем параметры кондиционера:

    for table in soup.find_all("table", {"class": "param"}):
        for tr in table.find_all('tr'):
            head[-1].append(([td.get_text() for td in tr.find_all('td')]))


with open('data.csv','w') as f:
    for row in head:
        for x in row:
            f.write(str(x) + ',')
        f.write('\n')








