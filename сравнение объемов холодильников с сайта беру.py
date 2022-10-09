import requests
from bs4 import BeautifulSoup
from time import sleep
import json


HEADERS = {"User-Agent": "parser_bot"}
URL = "https://video.ittensive.com/data/018-python-advanced/beru.ru/"
data = []

# отправляем запрос а из ответа извлекаем все ссылки :

r = requests.get(URL,headers=HEADERS)
html = BeautifulSoup(r.content,"html.parser")
links = html.find_all("a")

# Find_link() - принимает на вход ссылку(link) и сохраняет в links_filtered ссылки содержащие (key1) для поиска строк исключая тег можно добавить (key2): and link["href"].find(key2) == -1

def Find_link(link,key1,key2,key3):
  links_filtered = {}# чтобы избежать повторов сохранять будем тут
  for link in links:
    if link.has_attr("href") and link["href"].find(key1) > -1 and(link["href"].find(key2) > -1 or link["href"].find(key3) > -1):
      links_filtered[link["href"]] = 1
  return list(links_filtered.keys())
pages= (Find_link(links,'saratov',"263-kshd","452-ksh-120.html")) # тут сохраняем ссылки на интересующие нас товары

# разбираем страницы поочередно:

for page in pages:
 r=requests.get("https://video.ittensive.com/data/018-python-advanced/beru.ru/"+page,headers={"Accept": "application/json"})
 sleep(1)
 html = BeautifulSoup(r.content,"html.parser")
 script = html.find_all("script", {"class":"apiary-patch", "type":"application/json"})
 my_json = str(script[27])[62:-9]
 data.append(json.loads(my_json)["collections"]['product'])

V1 = int(data[0]['207534']['specs']['friendly'][2][12:-2])
V2 = int(data[1]['819573']['specs']['friendly'][2][12:-2])
H1 = data[0]['207534']["titles"]['raw']
H2 = data[1]['819573']["titles"]['raw']

print("общий объем ",H1, "составляет",V1,"литра. Это на ",(V2-V1),"литра меньше чем у",H2,"объем которого составляет ", V2)

