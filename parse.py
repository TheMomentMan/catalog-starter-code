from bs4 import BeautifulSoup
import json

# save titles in json format
def store_json(data, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print('Data saved to', file)

# get h3 tags
f = open('data.html', 'r')
html = f.read()
html = html.replace('\n', ' ').replace('\r', '')
soup = BeautifulSoup(html, 'html.parser')
results = soup.find_all('h3')
titles = []

# create titles list
for item in results:
    titles.append(item.text)

# save titles to json
store_json(titles, 'titles.json')