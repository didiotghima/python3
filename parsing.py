from bs4 import BeautifulSoup
import requests

url = 'https://akipress.org/'
response = requests.get(url=url)
print(response)
soup = BeautifulSoup(response.text, 'lxml')
# print(soup)
news_tag = soup.find_all('a', class_='newslink')
# print(news_tag)
for news in news_tag:
    print(news.text)

n = 0 
for news in news_tag:
    n += 1
    with open('news.txt', 'a+', encoding='utf-8') as news_file:
        news_file.write(f"{n}) {news.text}\n")

    


