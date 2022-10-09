import requests
from bs4 import BeautifulSoup
import time

# headers содержит требуемые сайтом заголовки указанные в robots.txt сайта

headers = {
    "User-Agent": "bot"
    }
r = requests.get("https://klimat71.ru/cat/cold/cond.htm",headers=headers)

html = BeautifulSoup(r.content, "html.parser")

links = html.find_all("a")

# Find_link() - принимает на вход ссылку(link) и сохраняет в links_filtered ссылки содержащие (key1) для поиска строк исключая тег можно добавить (key2): and link["href"].find(key2) == -1

def Find_link(link,key1):
  links_filtered = {}
  for link in links:
    if link.has_attr("href") and link["href"].find(key1) > -1 :
      links_filtered[link["href"]] = 1
  return list(links_filtered.keys())


# список pages сохраняет ссылки на все страницы содержащие требуемые данные.

link = []
pages = []
pages.extend(Find_link(html.find_all("a"),"cond.htm?pg="))


# поочередно проходим каждую страницу и копируем ссылки на все кондицыонеры представленные на ней в список (link). CD между запросами - 1секунда.

for page in pages:
  r=requests.get("https://klimat71.ru/"+page,headers=headers)
  time.sleep(1)
  html=BeautifulSoup(r.content, "html.parser")
  link.extend(Find_link(html.find_all("a"),"/cond.htm?id="))


# Все полученные ссылки сохраняем отдельным файлом. каждую ссылку отдельной строкой.
n=0
with open("link.txt", "w") as f:
  f.write("\n".join(link))

